#!/usr/bin/env python3
"""
make_report_score_fact_v2.py  (순서 보존판 + ethics_compliance 추가)
────────────────────────────────────────────────────────────
• compute_metrics 새 스키마 대응
• 0-10 점수 변환
• ethics_compliance (fair_use, direct_quote) 추가
• (변경) summary.json 생성 제거 → 샘플별 JSON만 저장
"""
from __future__ import annotations

import argparse, asyncio, json, re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Union

from dotenv import load_dotenv
from info_verification.eval_main import evaluate_report
import nltk

# ────────────────────────── 샘플 리스트 파서 ────────────────────────────────
def _parse_samples(arg: str) -> List[int]:
    """
    '1,2,5-8' → [1,2,5,6,7,8]
    """
    if not arg:
        return []
    toks = re.split(r"[,\s]+", arg.strip())
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

# ────────────────────────── 1. metric 경로 매핑 ───────────────────────────────
CRIT_MAP: Dict[str, Dict[str, Tuple[str, ...]]] = {
    # integrity
    "claim_factuality": {
        "external_claim_accuracy": ("integrity", "claim_factuality", "external_claim_accuracy"),
    },
    "citation_validity": {
        "citation_accuracy": ("integrity", "citation_validity", "citation_accuracy"),
    },
    "reference_accuracy": {
        "supported_per_shown": ("integrity", "reference_accuracy", "supported_per_shown"),
    },
    "reference_quality":{
        "reproducibility": ("integrity", "reference_quality", "reproducibility"),
        "reliability":  ("integrity", "reference_quality", "reliability"),
    },
    "reference_diversity": {
        # "citations_CV": ("integrity", "reference_diversity", "citations_CV"),
        "diversity_hhi": ("integrity", "reference_diversity", "diversity_hhi"),
    },
    # sufficiency
    "source_support": {
        "externally_verifiable_claims_ratio": ("sufficiency", "source_support", "externally_verifiable_claims_ratio"),
    },
    "information": {"information": ("sufficiency", "information")},
    "citations":   {"citations":   ("sufficiency", "citations")},
    "references":  {"references":  ("sufficiency", "references")},
    # ethics_compliance
    # "responsible_info": {
    #     "fair_use": ("ethics_compliance", "responsible_info", "fair_use"),
    #     "direct_quote": ("ethics_compliance", "responsible_info", "direct_quote"),
    # },
}

INTEGRITY_CATS = ["claim_factuality","citation_validity","reference_accuracy","reference_quality","reference_diversity"]
SUFFICIENCY_CATS = ["source_support","information","citations","references"]
# ETHIC_CATS = ["responsible_info"]

# ────────────────────────── 2. 점수 변환 헬퍼 ────────────────────────────────
def _clip(v: float, lo: float, hi: float) -> float: return max(lo, min(hi, v))
_AMOUNT_DIVISORS = {"information": 15, "citations": 10, "references": 4}

def amount_to_score(key: str, n: float) -> int: return 0 if n == 0 else min(int((n - 1) // _AMOUNT_DIVISORS[key]) + 1, 10)
def cv_to_score(cv: float) -> float:          return round(10 / (1 + max(cv, 0.)), 2)
def unique_ref_score(r: float) -> float:      return 10. if r >= .5 else round(20 * _clip(r, 0., .5), 2)
def avg_cpc_score(r: float) -> float:         return 0. if r <= 0 else round(min(r/3, 1.) * 10, 2)
def ratio_to_score(r: float) -> float:        return round(_clip(r, 0., 1.) * 10, 2)

def _safe_get(d: dict, path: Tuple[str, ...]) -> Union[float, None]:
    try:
        for k in path: d = d[k]
        return float(d)
    except (KeyError, TypeError, ValueError):
        return None

# ────────────────────────── 3. 샘플 평가 ──────────────────────────────────────
async def eval_and_score(sample_id: int, md_path: Path, eval_model: str) -> dict:
    # fact_result = await evaluate_report(md_path.read_text(), batch_size=20, extract_model=eval_model, verify_model=eval_model)
    fact_result = await evaluate_report(md_path.read_text(), batch_size=20, extract_model="gpt-5-mini", verify_model="gpt-5-mini")
    raw = fact_result["metrics"]
    # ethic_scores = raw.get('ethics_compliance', {}).get('responsible_info', {})

    scores, cat_avgs = {}, {}
    for cat in CRIT_MAP:
        scores[cat], vals = {}, []
        for crit in CRIT_MAP[cat]:
            v = _safe_get(raw, CRIT_MAP[cat][crit])
            if v is None: continue
            if   crit in _AMOUNT_DIVISORS:              s = amount_to_score(crit, v)
            elif crit == "citations_CV":                s = cv_to_score(v)
            elif crit == "unique_reference":            s = unique_ref_score(v)
            elif crit == "average_citations_per_claim": s = avg_cpc_score(v)
            elif crit == "diversity_hhi":               s = v
            else:                                       s = ratio_to_score(v)
            scores[cat][crit] = s
            vals.append(s)
        if vals: cat_avgs[cat] = round(sum(vals)/len(vals), 2)

    integ_av = {c: cat_avgs[c] for c in INTEGRITY_CATS if c in cat_avgs}
    suff_av  = {c: cat_avgs[c] for c in SUFFICIENCY_CATS if c in cat_avgs}
    # ethic_values = list(ethic_scores.values()) if ethic_scores else []
    # ethic_avg = round(sum(ethic_values) / len(ethic_values), 2) if ethic_values else "N/A"

    return {
        "sample_id": sample_id,
        "score_avgs": {
            "integrity": round(sum(integ_av.values())/len(integ_av), 2) if integ_av else "N/A",
            "sufficiency": round(sum(suff_av.values())/len(suff_av), 2)  if suff_av  else "N/A",
            # "ethics_compliance": ethic_avg,
        },
        "criteria_avgs": {
            "integrity": integ_av, 
            "sufficiency": suff_av,
            # "ethics_compliance": {"responsible_info": ethic_avg}
        },
        "scores": {
            "integrity": {k: scores[k] for k in INTEGRITY_CATS if k in scores},
            "sufficiency": {k: scores[k] for k in SUFFICIENCY_CATS if k in scores},
            # "ethics_compliance": {"responsible_info": ethic_scores}
        },
        "raw": raw
    }

# ────────────────────────── 4. 저장 (summary 제거) ───────────────────────────
# ────────────────────────── 4. 저장 (summary 제거) ───────────────────────────
async def main_async(args, sample_ids: List[int]):
    root = Path(args.root)
    out = (Path(args.output_root) / args.prefix / "fact").resolve()
    out.mkdir(parents=True, exist_ok=True)

    tasks = [
        eval_and_score(i, root / f"{i}/{args.prefix}_{i}.md", args.eval_model)
        for i in sample_ids
        if (root / f"{i}/{args.prefix}_{i}.md").exists()
    ]
    res = await asyncio.gather(*tasks)

    # 샘플별 결과만 저장 (summary.json 생성 없음)
    for r in res:
        sid = r["sample_id"]
        out_path = out / f"{sid:04d}.json"
        out_path.write_text(json.dumps(r, ensure_ascii=False, indent=2), "utf-8")
        print(f"✓ saved → {out_path}")

# ────────────────────────── 5. CLI ───────────────────────────────────────────
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prefix", default="gpt5_deep")
    p.add_argument("--samples", type=str, default="1", help="샘플 번호 리스트 (예: '1,2,5-7')")
    p.add_argument("--root", default="data/micro1_csai")
    p.add_argument("--output_root", default="output_test")
    p.add_argument("--env", default=".env")
    p.add_argument("--eval_model", default="gpt-4.1-mini")
    args = p.parse_args()

    load_dotenv(args.env)

    try:
        sample_ids = _parse_samples(args.samples)
        if not sample_ids:
            raise ValueError("no valid sample ids")
    except Exception as e:
        raise SystemExit(f"invalid --samples: {e}")

    asyncio.run(main_async(args, sample_ids))

if __name__ == "__main__":
    main()
