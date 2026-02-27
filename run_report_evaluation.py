#!/usr/bin/env python3
"""
make_report_score_v5.py  🟢 2025-09 with Performance Monitoring
────────────────────────────────────────────────────────────
- 각 샘플마다 여러 평가 프롬프트 호출:
  - request_fulfillment
  - analytical_soundness
  - structural_coherence
  - format_style
  - ethics_information
- 샘플×프롬프트를 전부 async로 동시에 실행 → 완료 후 샘플별 병합
- 저장 위치 : {output_dir}/{prefix}/others/
      ├─ 0001.json … 샘플별 결과(병합 + 평균 포함)
      └─ (summary.json 생성 안 함)

요구사항:
- 프롬프트/메시지 "그대로" 전송(보정 없음)
  - prompt_fn이 (SYSTEM_PROMPT, USER_PROMPT) 튜플을 반환한다고 가정
  - _llm_call은 messages를 그대로 litellm에 전달(시스템 프롬프트 덧붙이지 않음)
- _llm_call: 단순 호출(예외 상위 전파)
- _eval_task: 어떤 예외든 MAX_RETRY 재시도(+백오프), 초과 시 예외
- 강제 N/A 주입/템플릿 제거(형식 불일치 시 실패)
- ⚠ summary.json만 제거 — 개별 파일의 종합(평균) 결과는 유지
- ⏱️  각 단계별 성능 측정 추가
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Union, Tuple

# ── 프롬프트 빌더 import ─────────────────────────────────────────────
from prompts.prompt_report import (
    get_prompt_request_fulfillment,
    get_prompt_analytical_soundness,
    get_prompt_structural_coherence,
    get_prompt_format_style,
    get_prompt_information_ethics,
)

from prompts.schemas import RESPONSE_FORMAT_MAP

try:
    import litellm
except ImportError:
    sys.exit("litellm not installed. Run: pip install litellm")

MAX_RETRY = 5
BACKOFF = [1, 2, 4, 8, 16]

TOP6 = [
    "request_fulfillment",
    "analytical_soundness",
    "structural_coherence",
    "format_style",
    "information_integrity",
    "ethics_compliance",
]

# ── 프롬프트별 최소 요구 구조(부분 검증용) ────────────────────────────
REQUEST_FULFILLMENT_STRUCTURE = {"request_fulfillment": ["completeness", "scope", "helpfulness"]}
ANALYTICAL_SOUNDNESS_STRUCTURE = {"analytical_soundness": ["quantification", "reasoning"]}
STRUCTURAL_COHERENCE_STRUCTURE = {"structural_coherence": ["introduction", "body", "conclusion", "section"]}
FORMAT_STYLE_STRUCTURE = {"format_style": ["report_format", "writing_quality", "paragraph_quality", "readability"]}
ETHICS_INFORMATION_STRUCTURE = {
    "information_integrity": ["recency"],
    "ethics_compliance": ["sensitive_handling", "safety_impact", "perspective_balance"],
}

# ── 전체 필수 구조 (병합 후 최종 검증용) ──────────────────────────────
REQUIRED: Dict[str, List[str]] = {
    "request_fulfillment": ["completeness", "scope", "helpfulness"],
    "analytical_soundness": ["quantification", "reasoning"],
    "structural_coherence": ["introduction", "body", "conclusion", "section"],
    "format_style": ["report_format", "writing_quality", "paragraph_quality", "readability"],
    "information_integrity": ["recency"],
    "ethics_compliance": ["sensitive_handling", "safety_impact", "perspective_balance"],
}

# ── 어떤 프롬프트를 돌릴지 정의 ──────────────────────────────────────
PROMPT_SPECS = [
    {"kind": "request_fulfillment", "fn": get_prompt_request_fulfillment, "structure": REQUEST_FULFILLMENT_STRUCTURE, "needs_core": True},
    {"kind": "analytical_soundness", "fn": get_prompt_analytical_soundness, "structure": ANALYTICAL_SOUNDNESS_STRUCTURE, "needs_core": True},
    {"kind": "structural_coherence", "fn": get_prompt_structural_coherence, "structure": STRUCTURAL_COHERENCE_STRUCTURE, "needs_core": True},
    {"kind": "format_style", "fn": get_prompt_format_style, "structure": FORMAT_STYLE_STRUCTURE, "needs_core": False},
    {"kind": "information_ethics", "fn": get_prompt_information_ethics, "structure": ETHICS_INFORMATION_STRUCTURE, "needs_core": False},
]

Num = Union[int, float]


# ── 샘플 리스트 파서 ──────────────────────────────────────────────────
def _parse_samples(arg: str) -> List[int]:
    if arg is None:
        return []
    arg = arg.strip()
    if not arg:
        return []
    toks = re.split(r"[,\s]+", arg)
    ids: List[int] = []
    for t in toks:
        if not t:
            continue
        if "-" in t:
            a, b = t.split("-", 1)
            a_i, b_i = int(a), int(b)
            if a_i > b_i:
                raise ValueError(f"invalid range '{t}' (start>end)")
            ids.extend(range(a_i, b_i + 1))
        else:
            ids.append(int(t))
    return sorted(set(ids))


# ── 검증 ───────────────────────────────────────────────────────────────
def _element_block_is_valid(element_data: dict) -> bool:
    if not element_data:
        return True
    keys = set(element_data.keys())
    if keys == {"..."}:
        return True
    return any(k.startswith(("C", "Q")) for k in keys)


def _validate_full(scores: dict) -> bool:
    try:
        for rub, clist in REQUIRED.items():
            if rub not in scores:
                return False
            crit_map = scores[rub]
            if not isinstance(crit_map, dict):
                return False
            for c in clist:
                if c not in crit_map:
                    return False
                elements = crit_map[c]
                if not isinstance(elements, dict):
                    return False
                for _, element_data in elements.items():
                    if not isinstance(element_data, dict):
                        return False
                    if not _element_block_is_valid(element_data):
                        return False
        return True
    except Exception:
        return False


def _safe_num(item) -> Union[int, float, None]:
    """ScoreFactor 객체 또는 dict에서 숫자 추출"""
    if hasattr(item, "score"):
        score = item.score
        return score if isinstance(score, (int, float)) else None

    if isinstance(item, dict) and "score" in item:
        score = item["score"]
        return score if isinstance(score, (int, float)) else None

    # 레거시: [desc, score] 형태(혹시 남아있을 수 있음)
    if isinstance(item, (list, tuple)) and len(item) >= 2:
        last = item[-1]
        return last if isinstance(last, (int, float)) else None

    if isinstance(item, (int, float)):
        return item

    return None


def _merge_scores(base: dict, new: dict) -> dict:
    merged = {rub: dict(base.get(rub, {})) for rub in TOP6}
    for rub, criteria in new.items():
        if rub not in merged:
            merged[rub] = {}
        for crit, elements in (criteria or {}).items():
            if crit not in merged[rub]:
                merged[rub][crit] = {}
            for elem_key, elem_data in (elements or {}).items():
                if elem_key not in merged[rub][crit]:
                    merged[rub][crit][elem_key] = elem_data
    return merged


# ── 평균 계산 로직 ─────────────────────────────────────────────
def _calculate_averages(scores: dict) -> Dict[str, Any]:
    """
    요소별 C/Q 평균 → 엘리먼트 평균 → 크리테리온 평균 → 루브릭 평균 → overall
    """
    element_avgs, crit_avg, rub_avg = {}, {}, {}
    for rub in TOP6:
        if rub not in scores:
            continue
        element_avgs[rub], crit_avg[rub] = {}, {}
        for crit, elements in scores[rub].items():
            element_avgs[rub][crit] = {}
            element_scores = []
            for element_key, element_data in elements.items():
                c_scores, q_scores = [], []
                for factor_key, factor_value in element_data.items():
                    score = _safe_num(factor_value)
                    if score is None:
                        continue
                    if factor_key.startswith("C"):
                        c_scores.append(score)
                    elif factor_key.startswith("Q"):
                        q_scores.append(score)

                c_avg = round(sum(c_scores) / len(c_scores), 2) if c_scores else "N/A"
                q_avg = round(sum(q_scores) / len(q_scores), 2) if q_scores else "N/A"

                if isinstance(c_avg, (int, float)) and isinstance(q_avg, (int, float)):
                    element_avg = round((c_avg + q_avg) / 2, 2)
                elif isinstance(c_avg, (int, float)):
                    element_avg = c_avg
                elif isinstance(q_avg, (int, float)):
                    element_avg = q_avg
                else:
                    element_avg = "N/A"

                element_avgs[rub][crit][element_key] = {"c_avg": c_avg, "q_avg": q_avg, "element_avg": element_avg}
                if isinstance(element_avg, (int, float)):
                    element_scores.append(element_avg)

            crit_avg[rub][crit] = round(sum(element_scores) / len(element_scores), 2) if element_scores else "N/A"

        rv = [v for v in crit_avg[rub].values() if isinstance(v, (int, float))]
        rub_avg[rub] = round(sum(rv) / len(rv), 2) if rv else "N/A"

    overall_vals = [v for v in rub_avg.values() if isinstance(v, (int, float))]
    overall = round(sum(overall_vals) / len(overall_vals), 2) if overall_vals else "N/A"
    return {"ok": True, "element_avgs": element_avgs, "crit_avg": crit_avg, "rub_avg": rub_avg, "overall": overall}


# ── LiteLLM 호출(메시지 그대로 전송) ─────────────────────────────────
async def _llm_call(msgs: List[Dict[str, str]], model: str, kind: str):
    """
    - messages를 "그대로" 전송(보정 없음)
    - response_format이 있으면 Pydantic 검증
    - 예외는 상위 전파
    """
    timings: Dict[str, float] = {}
    t_total_start = time.time()

    t0 = time.time()
    kwargs: Dict[str, Any] = {"model": model, "messages": msgs}

    response_format = RESPONSE_FORMAT_MAP.get(kind)
    if response_format:
        kwargs["response_format"] = response_format

    t1 = time.time()
    timings["kwargs_setup"] = t1 - t0

    response = await litellm.acompletion(**kwargs)

    t2 = time.time()
    timings["llm_api_call"] = t2 - t1

    content = response.choices[0].message.content

    t3 = time.time()
    timings["extract_content"] = t3 - t2

    if response_format:
        m = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)
        json_str = m.group(1) if m else content.strip()

        t4 = time.time()
        timings["json_regex"] = t4 - t3

        parsed = response_format.model_validate_json(json_str)

        t5 = time.time()
        timings["pydantic_validate"] = t5 - t4
        timings["total"] = t5 - t_total_start

        print(
            f"    [LLM_CALL] kwargs={timings['kwargs_setup']:.3f}s | "
            f"API={timings['llm_api_call']:.2f}s | "
            f"extract={timings['extract_content']:.4f}s | "
            f"regex={timings['json_regex']:.4f}s | "
            f"pydantic={timings['pydantic_validate']:.3f}s | "
            f"TOTAL={timings['total']:.2f}s"
        )

        return parsed

    t_end = time.time()
    timings["total"] = t_end - t_total_start
    print(
        f"    [LLM_CALL] kwargs={timings['kwargs_setup']:.3f}s | "
        f"API={timings['llm_api_call']:.2f}s | "
        f"TOTAL={timings['total']:.2f}s"
    )
    return content.strip()


async def _eval_task(
    model: str,
    sid: int,
    kind: str,
    prompt_fn,
    query: str,
    report: str,
    core_criteria: str,
    needs_core: bool,
):
    """
    - prompt_fn은 (SYSTEM_PROMPT, USER_PROMPT) 튜플을 반환한다고 가정
    - 어떤 예외든 MAX_RETRY 재시도(+백오프), 초과 시 예외
    """
    timings: Dict[str, float] = {}
    t_task_start = time.time()

    print(f"[{time.strftime('%H:%M:%S')}] [Sample {sid}] {kind} START")

    # 1) 프롬프트 생성
    t0 = time.time()
    system_prompt, user_prompt = (
        prompt_fn(query, report, core_criteria) if needs_core else prompt_fn(query, report)
    )
    t1 = time.time()
    timings["prompt_generation"] = t1 - t0
    print(f"    [PROMPT_GEN] {timings['prompt_generation']:.3f}s")

    msgs = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    for attempt in range(1, MAX_RETRY + 1):
        try:
            # 2) LLM 호출
            t2 = time.time()
            parsed_obj = await _llm_call(msgs, model, kind)
            t3 = time.time()
            timings["llm_call_total"] = t3 - t2

            # 3) Pydantic → dict
            result_dict = parsed_obj.model_dump(by_alias=True)
            t4 = time.time()
            timings["model_dump"] = t4 - t3
            print(f"    [MODEL_DUMP] {timings['model_dump']:.3f}s")

            # 4) 최소 검증
            if "scores" not in result_dict:
                raise ValueError("parse fail: missing 'scores' root key")

            scores = result_dict["scores"]

            t5 = time.time()
            timings["validation"] = t5 - t4
            timings["total_task"] = t5 - t_task_start

            print(
                f"[{time.strftime('%H:%M:%S')}] [Sample {sid}] ✓ {kind} SUCCESS "
                f"(attempt={attempt}) "
                f"[prompt={timings['prompt_generation']:.2f}s | "
                f"llm={timings['llm_call_total']:.2f}s | "
                f"dump={timings['model_dump']:.3f}s | "
                f"TOTAL={timings['total_task']:.2f}s]"
            )

            return {"sample_id": sid, "kind": kind, "ok": True, "scores": scores}

        except Exception as e:
            print(f"[Sample {sid}] ✗ {kind} error on attempt {attempt}: {e}")
            if attempt >= MAX_RETRY:
                raise RuntimeError(f"[Sample {sid}] {kind} failed after {MAX_RETRY} attempts: {e}") from e

            delay = BACKOFF[min(attempt - 1, len(BACKOFF) - 1)] + random.random()
            print(f"[Sample {sid}] ↻ retry in {delay:.2f}s")
            await asyncio.sleep(delay)

    raise RuntimeError(f"[Sample {sid}] {kind} unexpected exit from retry loop")


# ── main --------------------------------------------------------------------
async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default="gpt5_deep")
    ap.add_argument("--eval_model", default="gpt-5.2")
    ap.add_argument("--samples", type=str, default="1-3", help="예: '1,2,3' 또는 '1-5,8'")
    ap.add_argument("--root", default="data/micro1_csai")
    ap.add_argument("--output_dir", default="output_test")
    ap.add_argument("--env", default=".env")
    ap.add_argument("--max_concurrency", type=int, default=0)
    args = ap.parse_args()

    # 샘플 리스트 파싱
    try:
        sample_ids = _parse_samples(args.samples)
        if not sample_ids:
            sys.exit("no samples parsed from --samples")
    except Exception as e:
        sys.exit(f"invalid --samples: {e}")

    from dotenv import load_dotenv

    load_dotenv(args.env)

    # LiteLLM API 키 설정
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
    os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY", "")

    t_start = time.time()

    root = Path(args.root)
    out_dir = Path(args.output_dir) / args.prefix / "others"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 작업 생성
    tasks: List[asyncio.Task] = []
    qmap: Dict[int, str] = {}
    reports: Dict[int, str] = {}
    cores: Dict[int, str] = {}
    selected_samples: List[int] = []

    for i in sample_ids:
        f = root / str(i)
        qf, rf, cf = f / "query.md", f / f"{args.prefix}_{i}.md", f / "core_criteria.md"
        if not (qf.exists() and rf.exists() and cf.exists()):
            print(f"⚠ Skip sample {i}: missing files in {f}")
            continue

        qmap[i] = qf.read_text(encoding="utf-8")
        reports[i] = rf.read_text(encoding="utf-8")
        cores[i] = cf.read_text(encoding="utf-8")
        selected_samples.append(i)

        for spec in PROMPT_SPECS:
            tasks.append(
                asyncio.create_task(
                    _eval_task(
                        args.eval_model,
                        i,
                        spec["kind"],
                        spec["fn"],
                        qmap[i],
                        reports[i],
                        cores[i],
                        spec["needs_core"],
                    )
                )
            )

    if not tasks:
        sys.exit("no runnable tasks (check --samples and file existence)")

    # 동시성 제한
    if args.max_concurrency and args.max_concurrency > 0:
        sem = asyncio.Semaphore(args.max_concurrency)

        async def _wrap(coro):
            async with sem:
                return await coro

        tasks = [asyncio.create_task(_wrap(t)) for t in tasks]

    # 실행
    print(f"\n{'='*60}\n📊 EVALUATION START")
    print(f"Total tasks: {len(tasks)}")
    print(f"Max concurrency: {args.max_concurrency if args.max_concurrency else 'unlimited'}")
    print(f"{'='*60}\n")

    t_eval_start = time.time()
    results = await asyncio.gather(*tasks)
    t_eval_end = time.time()

    print(f"\n{'='*60}\n⏱️  EVALUATION COMPLETED in {t_eval_end - t_eval_start:.2f}s")
    print(f"{'='*60}\n💾 SAVING PER-SAMPLE RESULTS\n{'='*60}")

    # 샘플별 결과 묶기
    by_sample: Dict[int, Dict[str, Any]] = defaultdict(dict)
    for r in results:
        sid = r["sample_id"]
        by_sample[sid][r["kind"]] = r

    for sid in sorted(by_sample.keys()):
        save_timings: Dict[str, float] = {}
        t_save_start = time.time()

        # 1) 병합
        parts = by_sample[sid]
        merged_scores = {rub: {} for rub in TOP6}
        for _, r in parts.items():
            merged_scores = _merge_scores(merged_scores, r["scores"])
        t1 = time.time()
        save_timings["merge"] = t1 - t_save_start

        # 2) 검증
        if not _validate_full(merged_scores):
            raise RuntimeError(f"final validate fail for sample {sid}: REQUIRED structure incomplete")
        t2 = time.time()
        save_timings["validate"] = t2 - t1

        # 3) 평균 계산
        avg = _calculate_averages(merged_scores)
        t3 = time.time()
        save_timings["calculate_avg"] = t3 - t2

        # 4) dict 생성
        out = {
            "sample_id": sid,
            "scores": merged_scores,
            "element_avgs": avg["element_avgs"],
            "criteria_avgs": avg["crit_avg"],
            "score_avgs": avg["rub_avg"],
            "score": avg["overall"],
        }
        t4 = time.time()
        save_timings["dict_create"] = t4 - t3

        # 5) JSON 직렬화 + 파일 쓰기
        json_str = json.dumps(out, ensure_ascii=False, indent=2)
        t5 = time.time()
        save_timings["json_dumps"] = t5 - t4

        (out_dir / f"{sid:04d}.json").write_text(json_str, "utf-8")
        t6 = time.time()
        save_timings["file_write"] = t6 - t5
        save_timings["total"] = t6 - t_save_start

        print(
            f"   ✓ Sample {sid:04d} (score={out['score']}) "
            f"[merge={save_timings['merge']:.3f}s | "
            f"valid={save_timings['validate']:.4f}s | "
            f"avg={save_timings['calculate_avg']:.3f}s | "
            f"dict={save_timings['dict_create']:.4f}s | "
            f"json={save_timings['json_dumps']:.3f}s | "
            f"write={save_timings['file_write']:.4f}s | "
            f"TOTAL={save_timings['total']:.3f}s]"
        )

    elapsed = time.time() - t_start
    mins, secs = divmod(int(elapsed), 60)
    hours, mins = divmod(mins, 60)
    dur_text = f"{hours}h {mins}m {secs}s" if hours else f"{mins}m {secs}s"

    print(f"\n{'='*60}\n✅ COMPLETE")
    print(f"   Samples requested : {len(selected_samples)}")
    print(f"   Samples processed : {len(by_sample)}")
    print(f"   Evaluation time   : {t_eval_end - t_eval_start:.2f}s")
    print(f"   Total duration    : {dur_text}")
    print(f"   Output directory  : {out_dir}\n{'='*60}\n")

    # 남은 태스크 정리
    pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    if pending:
        print(f"🧹 Cleaning up {len(pending)} background tasks...")
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)

    print("✅ Cleanup complete")


if __name__ == "__main__":
    asyncio.run(main())
    print("🔚 Script finished")
