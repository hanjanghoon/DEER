#!/usr/bin/env python3
"""
integrate_score.py  (모든 루브릭 통합)
────────────────────────────────────────────
- others/<sid>.json 들로 others/summary.json 생성(재생성)
- fact/<sid>.json   들로 fact/summary.json   생성(재생성)
- fact/summary.json  +  others/summary.json  →  final.json
- fact/<sid>.json    +  others/<sid>.json    →  final/<sid>.json
- 출력 키는 score_avgs / criteria_avgs 두 개뿐.
- 정규화:
    - integrity            → information_integrity
    - sufficiency          → information_sufficiency
- 특수 처리 (information_integrity):
    - reference_quality = avg(reproducibility, information_reliability, recency [, 기존 reference_quality])
    - IQ 원천 키(IQ_KEYS)는 최종 출력에서 제거

CLI:
    --prefix       필수 (예: exaone_deep)
    --output_dir   기본 'output_eval'
    --samples      샘플 리스트/범위 (예: "1,2,5-7")  ← 이것만 지원
"""
from __future__ import annotations
import argparse, json, re, statistics
from pathlib import Path
from typing import Dict, List, Union, Tuple, Any

Num = Union[int, float]
IQ_KEYS = ("reproducibility", "reliability", "recency")

# ── helpers ───────────────────────────────────────────────
def _read(p: Path) -> Dict:
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

def _is_num(x: Any) -> bool:
    return isinstance(x, (int, float))

def _mean(vals: List[Num]) -> Union[Num, str]:
    nums = [v for v in vals if _is_num(v)]
    return round(statistics.mean(nums), 2) if nums else "N/A"

def _norm_rubric(name: str) -> str:
    if name == "integrity":
        return "information_integrity"
    if name == "sufficiency":
        return "information_sufficiency"
    return name

def _parse_samples(arg: str | None) -> List[str]:
    """
    '1,2,5-7' → ['0001','0002','0005','0006','0007'] 로 반환
    (파일명 스템과 호환되도록 4자리 zero-pad)
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
                raise SystemExit(f"invalid range in --samples: '{t}'")
            ids.extend(range(a_i, b_i + 1))
        else:
            ids.append(int(t))
    return [f"{i:04d}" for i in sorted(set(ids))]

# ── others summary 생성에 필요한 계산기 ─────────────────────────────
def _safe_num_from_factor(v) -> Union[float, None]:
    """
    허용 형식:
      - {..., "score": <number>} → dict에서 score 키 추출
      - [..., <number>] → 마지막이 숫자면 점수
      - 숫자 자체
      - 그 외 / 'N/A' -> None
    """
    if _is_num(v):
        return float(v)
    if isinstance(v, dict) and "score" in v and _is_num(v["score"]):
        return float(v["score"])
    if isinstance(v, (list, tuple)) and len(v) >= 2 and _is_num(v[-1]):
        return float(v[-1])
    return None

def compute_others_summary(others_dir: Path, sids: List[str]) -> Dict:
    """
    others/<sid>.json 들의 "scores"를 사용해 요약 생성:
      1) factor(C*/Q*) 평균 → element c_avg/q_avg → element_avg
      2) criterion 평균 = element_avg들의 평균
      3) rubric 평균 = criterion 평균들의 평균
    반환 구조: {"criteria_avgs": {rub: {crit: avg}}, "score_avgs": {rub: avg}}
    
    scores 형식 지원:
      - 기존 형식: {"rubric": {"criterion": {"element": {"factor": {...}}}}}
      - 새 형식: {"rubric": {"criterion": {"sample_id": {"element": {"factor": {...}}}}}}
    """
    # rub -> crit -> elem -> {C*/Q*: [scores]}
    bucket: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]] = {}

    for sid in sids:
        p = others_dir / f"{sid}.json"
        if not p.exists():
            continue
        data = _read(p)
        scores = data.get("scores", {})
        for rub, crits in scores.items():
            rub_b = bucket.setdefault(rub, {})
            for crit, elems in (crits or {}).items():
                crit_b = rub_b.setdefault(crit, {})
                
                # elems가 dict인지 확인
                if not isinstance(elems, dict):
                    continue
                
                # elems의 첫 번째 value를 검사하여 중첩 구조인지 판단
                if not elems:
                    continue
                    
                sample_values = list(elems.values())
                if not sample_values or not isinstance(sample_values[0], dict):
                    continue
                
                first_value = sample_values[0]
                if not first_value:
                    continue
                    
                first_key = list(first_value.keys())[0]
                
                # 첫 번째 키가 숫자로 시작하거나 C/Q로 시작하면 element, 아니면 sample_id
                is_nested = not (first_key and (first_key[0].isdigit() or first_key.startswith("C") or first_key.startswith("Q")))
                
                if is_nested:
                    # 새 형식: {"sample_id": {"element": {"factor": {...}}}}
                    for sample_id, elements in elems.items():
                        if not isinstance(elements, dict):
                            continue
                        for elem, factors in elements.items():
                            if not isinstance(factors, dict):
                                continue
                            elem_b = crit_b.setdefault(elem, {})
                            for fkey, fval in factors.items():
                                s = _safe_num_from_factor(fval)
                                if s is not None:
                                    elem_b.setdefault(fkey, []).append(s)
                else:
                    # 기존 형식: {"element": {"factor": {...}}}
                    for elem, factors in elems.items():
                        if not isinstance(factors, dict):
                            continue
                        elem_b = crit_b.setdefault(elem, {})
                        for fkey, fval in factors.items():
                            s = _safe_num_from_factor(fval)
                            if s is not None:
                                elem_b.setdefault(fkey, []).append(s)

    # factor 평균 → element_avg → criterion 평균
    criteria_avgs: Dict[str, Dict[str, Num]] = {}
    for rub, crits in bucket.items():
        criteria_avgs[rub] = {}
        for crit, elems in crits.items():
            element_avgs: List[float] = []
            for _elem, fdict in elems.items():
                c_vals = [statistics.mean(v) for k, v in fdict.items() if k.startswith("C") and v] or []
                q_vals = [statistics.mean(v) for k, v in fdict.items() if k.startswith("Q") and v] or []
                c_avg = statistics.mean(c_vals) if c_vals else None
                q_avg = statistics.mean(q_vals) if q_vals else None
                if c_avg is not None and q_avg is not None:
                    e = (c_avg + q_avg) / 2.0
                else:
                    e = c_avg if c_avg is not None else q_avg
                if e is not None:
                    element_avgs.append(e)
            criteria_avgs[rub][crit] = round(statistics.mean(element_avgs), 2) if element_avgs else "N/A"

    # rubric 평균
    score_avgs = {rub: _mean([v for v in crits.values() if _is_num(v)]) for rub, crits in criteria_avgs.items()}
    return {"criteria_avgs": criteria_avgs, "score_avgs": score_avgs}

# ── fact summary 생성기 ───────────────────────────────────────────────
def compute_fact_summary(fact_dir: Path, sids: List[str]) -> Dict:
    """
    fact/<sid>.json 들의 'criteria_avgs'를 단순 평균해서 summary 생성.
    (rubric 정규화 포함)
    반환 구조: {"criteria_avgs": {rub: {crit: avg}}, "score_avgs": {rub: avg}}
    """
    buf: Dict[str, Dict[str, List[Num]]] = {}  # rub -> crit -> [vals]

    for sid in sids:
        p = fact_dir / f"{sid}.json"
        if not p.exists():
            continue
        data = _read(p)
        ca = data.get("criteria_avgs", {})
        for rub, crits in (ca or {}).items():
            rub_std = _norm_rubric(rub)
            if isinstance(crits, dict):
                for c, v in crits.items():
                    buf.setdefault(rub_std, {}).setdefault(c, []).append(v)

    criteria_avgs = {rub: {c: _mean(vals) for c, vals in crits.items()} for rub, crits in buf.items()}
    score_avgs = {rub: _mean([v for v in crits.values() if _is_num(v)]) for rub, crits in criteria_avgs.items()}
    return {"criteria_avgs": criteria_avgs, "score_avgs": score_avgs}


def _mean_num(vs):
    nums = [x for x in vs if _is_num(x)]
    return statistics.mean(nums) if nums else None


# ── 병합 로직 ────────────────────────────────────────────────────────
def merge_criteria(fact: Dict, others: Dict) -> Dict[str, Dict[str, Num]]:
    """
    fact/others의 criteria_avgs 전체를 루브릭 단위로 병합.
    동일 criterion은 평균. information_integrity는 reference_quality 재계산.
    """
    buf: Dict[str, Dict[str, List[Num]]] = {}

    def pull(src: Dict):
        for rub, crits in src.get("criteria_avgs", {}).items():
            rub_n = _norm_rubric(rub)
            if not isinstance(crits, dict):
                continue
            for c, v in crits.items():
                buf.setdefault(rub_n, {}).setdefault(c, []).append(v)

    pull(fact); pull(others)

    out: Dict[str, Dict[str, Num]] = {}
    for rub, crits in buf.items():
        if rub == "information_integrity":
            # recency는 reference_quality 보정에만 쓰고 최종 출력에서는 제거
            rec_list = crits.pop("recency", [])
            rq_list  = crits.get("reference_quality", [])

            rec = rec_list[0] if rec_list and _is_num(rec_list[0]) else None
            rq  = rq_list[0]  if rq_list  and _is_num(rq_list[0])  else None

            if rec is not None and rq is not None:
                # reference_quality는 이미 fact에서 2개 평균된 값이라 가중치 2
                crits["reference_quality"] = [(rq * 2.0 + rec) / 3.0]

        # 나머지는 기존대로 리스트 -> 평균(원소 1개면 그대로)
        out[rub] = {c: _mean(vs) for c, vs in crits.items()}

    return out

def rubric_avgs(criteria: Dict[str, Dict[str, Num]]) -> Dict[str, Num]:
    return {rub: _mean([v for v in crits.values() if _is_num(v)])
            for rub, crits in criteria.items()}

def list_sids_under(base: Path) -> List[str]:
    s = set()
    for d in (base / "fact", base / "others"):
        if d.exists():
            for p in d.glob("*.json"):
                if p.name == "summary.json":
                    continue
                s.add(p.stem)
    return sorted(s)

# ── 샘플별 others criterion 추출 함수 (새 형식 지원) ──
def _criteria_from_others_sample(d: Dict) -> Dict[str, Dict[str, Num]]:
    """
    others 단일 샘플에서 criterion 평균 추출
    새 형식과 기존 형식 모두 지원
    """
    scores = d.get("scores", {})
    criteria: Dict[str, Dict[str, Num]] = {}
    
    for rub, crits in scores.items():
        criteria[rub] = {}
        for crit, elems in (crits or {}).items():
            if not isinstance(elems, dict):
                continue
            
            # 구조 판단
            if not elems:
                continue
            
            sample_values = list(elems.values())
            if not sample_values or not isinstance(sample_values[0], dict):
                continue
            
            first_value = sample_values[0]
            if not first_value:
                continue
            
            first_key = list(first_value.keys())[0]
            is_nested = not (first_key and (first_key[0].isdigit() or first_key.startswith("C") or first_key.startswith("Q")))
            
            element_avgs: List[float] = []
            
            if is_nested:
                # 새 형식: {"sample_id": {"element": {"factor": {...}}}}
                for sample_id, elements in elems.items():
                    if not isinstance(elements, dict):
                        continue
                    for _elem, fdict in elements.items():
                        if not isinstance(fdict, dict):
                            continue
                        c_vals = []; q_vals = []
                        for k, v in fdict.items():
                            s = _safe_num_from_factor(v)
                            if s is None:
                                continue
                            if k.startswith("C"):
                                c_vals.append(s)
                            elif k.startswith("Q"):
                                q_vals.append(s)
                        c_avg = statistics.mean(c_vals) if c_vals else None
                        q_avg = statistics.mean(q_vals) if q_vals else None
                        if c_avg is not None and q_avg is not None:
                            e = (c_avg + q_avg)/2.0
                        else:
                            e = c_avg if c_avg is not None else q_avg
                        if e is not None:
                            element_avgs.append(e)
            else:
                # 기존 형식: {"element": {"factor": {...}}}
                for _elem, fdict in elems.items():
                    if not isinstance(fdict, dict):
                        continue
                    c_vals = []; q_vals = []
                    for k, v in fdict.items():
                        s = _safe_num_from_factor(v)
                        if s is None:
                            continue
                        if k.startswith("C"):
                            c_vals.append(s)
                        elif k.startswith("Q"):
                            q_vals.append(s)
                    c_avg = statistics.mean(c_vals) if c_vals else None
                    q_avg = statistics.mean(q_vals) if q_vals else None
                    if c_avg is not None and q_avg is not None:
                        e = (c_avg + q_avg)/2.0
                    else:
                        e = c_avg if c_avg is not None else q_avg
                    if e is not None:
                        element_avgs.append(e)
            
            criteria[rub][crit] = round(statistics.mean(element_avgs), 2) if element_avgs else "N/A"
    
    return criteria

# ── main ─────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default='gpt5.2_deep', help="e.g., exaone_deep")
    ap.add_argument("--output_dir", default="output/csai")
    ap.add_argument("--samples", type=str,  default='1-10',
                    help="샘플 리스트/범위 (예: '1,2,5-7')")
    args = ap.parse_args()

    base = Path(args.output_dir) / args.prefix
    fact_dir = base / "fact"
    others_dir = base / "others"
    final_dir = base / "final"
    final_dir.mkdir(parents=True, exist_ok=True)

    # 1) 대상 샘플 확정
    requested = _parse_samples(args.samples)
    if not requested:
        raise SystemExit("no valid sample ids parsed from --samples")

    # 실제 존재하는 파일 기준으로 분리
    existing_others = [sid for sid in requested if (others_dir / f"{sid}.json").exists()]
    existing_fact   = [sid for sid in requested if (fact_dir   / f"{sid}.json").exists()]
    if not existing_others and not existing_fact:
        raise SystemExit("no matching fact/ or others/<sid>.json files for given --samples")

    # 2) others summary 생성(재생성) — others에 하나라도 있으면 생성
    if existing_others:
        others_summary = compute_others_summary(others_dir, existing_others)
        (others_dir / "summary.json").write_text(json.dumps(others_summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ others/summary.json saved → {others_dir / 'summary.json'}")
    else:
        others_summary = {"criteria_avgs": {}, "score_avgs": {}}
        print("ℹ️  no others samples among requested; skipping others summary generation.")

    # 3) fact summary 생성(재생성) — fact에 하나라도 있으면 생성
    if existing_fact:
        fact_summary = compute_fact_summary(fact_dir, existing_fact)
        (fact_dir / "summary.json").write_text(json.dumps(fact_summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ fact/summary.json saved → {fact_dir / 'summary.json'}")
    else:
        fact_summary = {"criteria_avgs": {}, "score_avgs": {}}
        print("ℹ️  no fact samples among requested; skipping fact summary generation.")

    # 4) summary 병합 → final.json
    merged_criteria = merge_criteria(fact_summary, others_summary)
    merged_scores = rubric_avgs(merged_criteria)
    final_summary = {"score_avgs": merged_scores, "criteria_avgs": merged_criteria}
    (base / "final.json").write_text(json.dumps(final_summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ final.json saved → {base / 'final.json'}")

    # 5) 샘플별 병합 → final/<sid>.json
    for sid in requested:
        fact = _read(fact_dir / f"{sid}.json")
        others = _read(others_dir / f"{sid}.json")

        fact_crit = {_norm_rubric(r): v for r, v in (fact.get("criteria_avgs") or {}).items()}
        others_crit = _criteria_from_others_sample(others) if others else {}

        merged_criteria_s = merge_criteria({"criteria_avgs": fact_crit}, {"criteria_avgs": others_crit})
        merged_scores_s = rubric_avgs(merged_criteria_s)

        outp = final_dir / f"{sid}.json"
        outp.write_text(json.dumps({"score_avgs": merged_scores_s, "criteria_avgs": merged_criteria_s},
                                   ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ sample saved → {outp}")

if __name__ == "__main__":
    main()