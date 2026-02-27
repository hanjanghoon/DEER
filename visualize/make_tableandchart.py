#!/usr/bin/env python3
"""
make_tableandchart_domain.py
────────────────────────────────────────────────────────────────────────────────
• output/<domain>/<model>/final/<task_id>.json → 도메인별 평균 점수 계산 → 시각화(PNG)·Excel
• 각 도메인별로 모든 task 파일들의 평균을 계산하여 모델 비교
• 전체 통합 결과 + 도메인별 결과 생성
• CSAI 도메인을 AI(1-5)와 CS(6-10)로 분리 처리
• 레이아웃
    ① Radar  (1 행 전체폭)
    ② Overall-bar (1 행 전체폭)
    ③ Rubric-bar (아래 2 열씩)

사용법:
    아래 설정 섹션을 수정한 후 실행: python make_tableandchart_domain.py
"""
from __future__ import annotations
import json, math, sys
from math import ceil
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import numpy as np
import pandas as pd

# ══════════════════════════════════════════════════════════════════════════════
# 📝 설정 섹션 - 여기를 수정하세요!
# ══════════════════════════════════════════════════════════════════════════════

# ── 데이터 경로 설정 ──────────────────────────────────────────
ROOT_DIR = "output"          # 도메인 폴더들이 있는 루트 디렉토리
OUTPUT_DIR = "visualize"     # 결과를 저장할 디렉토리

# ── 도메인 설정 ──────────────────────────────────────────────
# 분석할 도메인 목록 (원하지 않는 도메인은 주석 처리)
# 주의: "ai"와 "cs"는 실제로는 "csai" 폴더를 참조합니다
DOMAINS = [
    "ai",            # ← CSAI의 1-5번 task (AI)
    "bio",           # ← bio 도메인 처리
    "chem",          # ← chem 도메인 처리
    "cs",            # ← CSAI의 6-10번 task (CS)
    "economics",
    "education",
    "engineer",
    "history",
    "linguistics",
    "math",
    "philosophy",
    "physics",
    "psychology"
]

# 예시: 일부만 처리하려면
# DOMAINS = [
#     "bio",
#     # "chem",      # ← 주석 처리하면 제외
#     "ai",
# ]

# ── 모델 그룹 정의 및 선택 ────────────────────────────────────
# 원하지 않는 그룹 전체를 주석 처리하세요
MODEL_GROUPS = {
    "fast": [        # ← fast 그룹 (이 줄부터 ], 까지 주석 처리하면 제외)
        # "qwen3-235b-fast",
        # "gemini-2.5-pro-fast",
        # "claude_opus4.1_fast",
        "gpt5.2_fast",
    ],
    # "think": [       # ← think 그룹
    #     "qwen3-235b-think",
    #     "gemini-2.5-pro-think",
    #     "claude_opus4.1_think",
    #     "gpt5.2_think",
    # ],
    # "think_search": [ # ← think_search 그룹
    #     "qwen3-235b-think_search",
    #     "claude_opus4.1_think_search",
    #     "gpt5.2_think_search",
    # ],
    # "deep": [        # ← deep 그룹
    #     "webthinker",
    #     "qwen3-235b-deep",
    #     "gemini-2.5-pro_deep",
    #     "claude_opus4.1_deep",
    #     "gpt5_deep",
    #     # "chatexaone_251208_deepresearch"
    # ],
}

# ── 시각화 설정 ──────────────────────────────────────────────
DPI = 150          # 이미지 해상도 (150~300 권장)
SHOW_PLOT = False  # True면 화면에 표시

# ══════════════════════════════════════════════════════════════════════════════
# ⚙️ 내부 설정 - 수정하지 마세요
# ══════════════════════════════════════════════════════════════════════════════

# 모든 모델 목록 생성 (MODEL_GROUPS에서 자동 수집)
ALL_MODELS = []
for group_name, models in MODEL_GROUPS.items():
    ALL_MODELS.extend(models)

# ══════════════════════════════════════════════════════════════
# 축약 레이블
# ══════════════════════════════════════════════════════════════
SHORT = {
    # 새로운 구조
    "request_fulfillment":    "fulfillment",
    "analytical_soundness":   "analytical",
    "structural_coherence":   "structure",
    "format_style":           "format",
    
    # 기존 유지
    "information_integrity":  "info_integrity",
    "information_sufficiency":"info_sufficiency",
    "ethics_compliance":      "ethics",
}
# ── 세부 기준(criteria) 축약 레이블 (기존 유지 + 새 항목 추가) ──
CRITERIA_SHORT = {
    # request_fulfillment (새)
    "completeness": "completeness",
    "scope": "scope",
    "helpfulness": "helpfulness",

    # analytical_soundness (새)
    "quantification": "quantification",
    "reasoning": "reasoning",

    # structural_coherence (새)
    "introduction": "intro",
    "body": "body",
    "conclusion": "conclusion",
    "section": "section",

    # format_style (새)
    "report_format": "report_fmt",
    "writing_quality": "writing",
    "paragraph_quality": "paragraph",
    "readability": "readability",

    # information_integrity (기존 유지)
    "claim_factuality": "claim_acc",
    "citation_validity": "citation_acc",
    "reference_accuracy": "ref_accuracy",
    "reference_quality": "ref_quality",
    "reference_diversity": "ref_diversity",

    # information_sufficiency (기존 유지)
    "source_support": "support",
    "information": "info_amount",
    "citations": "cites_amount",
    "references": "refs_amount",

    # ethics_compliance (새 구조)
    "sensitive_handling": "sensitive",
    "safety_impact": "safety",
    "perspective_balance": "balance"
}


# SHORT 사전에 정의된 키 순서를 보존하기 위한 우선순위 목록
_ORDER_PREF = list(SHORT.keys())

# ── 각 루브릭 내부 criteria 순서 정의 ──────────────────────
CRITERIA_ORDER = {
    # 새로운 구조
    "request_fulfillment": ["completeness", "scope", "helpfulness"],
    "analytical_soundness": ["quantification", "reasoning"],
    "structural_coherence": ["introduction", "body", "conclusion", "section"],
    "format_style": ["report_format", "writing_quality", "paragraph_quality", "readability"],
    
    # 기존 유지
    "information_integrity": ["claim_factuality", "citation_validity", "reference_accuracy", "reference_quality", "reference_diversity"],
    "information_sufficiency": ["source_support", "information", "citations", "references"],
    
    # 새 구조 (sensitive_issues 제거)
    "ethics_compliance": ["sensitive_handling", "safety_impact", "perspective_balance"]
}

# ── 숫자 변환 헬퍼 ─────────────────────────────────────────

def _to_num(v):
    """숫자로 변환. 변환 불가/결측은 None."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        if v.strip().upper() == "N/A":
            return None
        try:
            return float(v)
        except ValueError:
            return None
    return None

# ── 도메인 매핑 헬퍼 ─────────────────────────────────────────

def get_physical_domain(domain: str) -> str:
    """논리적 도메인명을 물리적 폴더명으로 변환"""
    if domain in ["ai", "cs"]:
        return "csai"
    return domain

def get_task_filter(domain: str) -> tuple[int, int] | None:
    """도메인에 따른 task 번호 필터 반환 (start, end) 또는 None"""
    if domain == "ai":
        return (1, 5)  # 01.json ~ 05.json
    elif domain == "cs":
        return (6, 10)  # 06.json ~ 10.json
    return None

# ── 도메인별 데이터 로딩 ─────────────────────────────────────

def load_domain_summary(domain_path: Path, model_name: str, task_filter: tuple[int, int] | None = None) -> dict | None:
    """
    domain_path/<model>/final/*.json 파일들을 모두 읽어서 평균 계산
    
    Args:
        domain_path: 도메인 경로
        model_name: 모델 이름
        task_filter: (start, end) task 번호 범위 필터. None이면 모든 task 포함
    
    Returns:
        {
            "score_avgs": {...},
            "criteria_avgs": {...},
            "task_count": N  # 읽은 task 파일 개수
        }
    """
    model_dir = domain_path / model_name / "final"
    if not model_dir.is_dir():
        return None
    
    all_scores = []
    all_criteria = {}
    
    # 모든 json 파일 읽기
    json_files = list(model_dir.glob("*.json"))
    if not json_files:
        return None
    
    for json_file in json_files:
        # task 번호 필터링
        if task_filter is not None:
            try:
                # 파일명에서 번호 추출 (예: "01.json" -> 1, "003.json" -> 3)
                task_num = int(json_file.stem.lstrip('0') or '0')
                start, end = task_filter
                if not (start <= task_num <= end):
                    continue  # 범위 밖이면 스킵
            except ValueError:
                continue  # 숫자가 아니면 스킵
        
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            all_scores.append(data.get("score_avgs", {}))
            
            # criteria_avgs 수집
            criteria_data = data.get("criteria_avgs", {})
            for rubric, crit_dict in criteria_data.items():
                if rubric not in all_criteria:
                    all_criteria[rubric] = {}
                for crit_key, val in crit_dict.items():
                    if crit_key not in all_criteria[rubric]:
                        all_criteria[rubric][crit_key] = []
                    all_criteria[rubric][crit_key].append(val)
        except Exception as e:
            print(f"Warning: Failed to load {json_file}: {e}")
            continue
    
    if not all_scores:
        return None
    
    # score_avgs 평균 계산
    score_avgs = {}
    all_keys = set()
    for s in all_scores:
        all_keys.update(s.keys())
    
    for key in all_keys:
        vals = [s.get(key) for s in all_scores if key in s]
        vals = [_to_num(v) for v in vals]
        vals = [v for v in vals if v is not None and not math.isnan(v)]
        if vals:
            score_avgs[key] = sum(vals) / len(vals)
    
    # criteria_avgs 평균 계산
    criteria_avgs = {}
    for rubric, crit_dict in all_criteria.items():
        criteria_avgs[rubric] = {}
        for crit_key, vals in crit_dict.items():
            nums = [_to_num(v) for v in vals]
            nums = [v for v in nums if v is not None and not math.isnan(v)]
            if nums:
                criteria_avgs[rubric][crit_key] = sum(nums) / len(nums)
    
    return {
        "score_avgs": score_avgs,
        "criteria_avgs": criteria_avgs,
        "task_count": len(all_scores)
    }

def scan_domain(root: Path, domain: str, models_list: List[str]) -> dict:
    """
    특정 도메인의 지정된 모델 데이터 스캔
    AI/CS의 경우 csai 폴더에서 task 번호로 필터링
    
    Returns:
        {model_name: summary_dict, ...}
    """
    physical_domain = get_physical_domain(domain)
    task_filter = get_task_filter(domain)
    
    domain_path = root / physical_domain
    if not domain_path.is_dir():
        print(f"Warning: Domain directory not found: {domain_path}")
        return {}
    
    out = {}
    for model_name in models_list:
        summary = load_domain_summary(domain_path, model_name, task_filter)
        if summary:
            out[model_name] = summary
            if task_filter:
                print(f"  {domain}/{model_name}: {summary['task_count']} tasks (filtered {task_filter[0]}-{task_filter[1]})")
            else:
                print(f"  {domain}/{model_name}: {summary['task_count']} tasks")
    
    return out

# ── 전체 도메인 평균 계산 ─────────────────────────────────────

def aggregate_domains(domain_summaries: Dict[str, Dict[str, dict]]) -> Dict[str, dict]:
    """
    여러 도메인의 결과를 모델별로 평균내어 전체 통합 결과 생성
    
    Args:
        domain_summaries: {domain_name: {model_name: summary_dict}}
    
    Returns:
        {model_name: aggregated_summary_dict}
    """
    # 모든 모델 목록 수집
    all_models = set()
    for domain_data in domain_summaries.values():
        all_models.update(domain_data.keys())
    
    aggregated = {}
    
    for model in all_models:
        # 이 모델이 포함된 모든 도메인의 데이터 수집
        model_scores = []
        model_criteria = {}
        
        for domain, domain_data in domain_summaries.items():
            if model not in domain_data:
                continue
            
            summary = domain_data[model]
            model_scores.append(summary["score_avgs"])
            
            # criteria_avgs 수집
            for rubric, crit_dict in summary["criteria_avgs"].items():
                if rubric not in model_criteria:
                    model_criteria[rubric] = {}
                for crit_key, val in crit_dict.items():
                    if crit_key not in model_criteria[rubric]:
                        model_criteria[rubric][crit_key] = []
                    model_criteria[rubric][crit_key].append(val)
        
        # score_avgs 평균 계산
        score_avgs = {}
        all_keys = set()
        for s in model_scores:
            all_keys.update(s.keys())
        
        for key in all_keys:
            vals = [s.get(key) for s in model_scores if key in s]
            vals = [_to_num(v) for v in vals]
            vals = [v for v in vals if v is not None and not math.isnan(v)]
            if vals:
                score_avgs[key] = sum(vals) / len(vals)
        
        # criteria_avgs 평균 계산
        criteria_avgs = {}
        for rubric, crit_dict in model_criteria.items():
            criteria_avgs[rubric] = {}
            for crit_key, vals in crit_dict.items():
                nums = [_to_num(v) for v in vals]
                nums = [v for v in nums if v is not None and not math.isnan(v)]
                if nums:
                    criteria_avgs[rubric][crit_key] = sum(nums) / len(nums)
        
        aggregated[model] = {
            "score_avgs": score_avgs,
            "criteria_avgs": criteria_avgs,
        }
    
    return aggregated

# ── plotting helpers ────────────────────────────────────

def setup_radar(ax, labels):
    ang = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(ang)
    ax.set_xticklabels([SHORT.get(l, l) for l in labels], fontsize=7)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 6, 10])
    ax.set_yticklabels(["2", "6", "10"], fontsize=5)
    ax.grid(True, lw=.3)
    return ang

def draw_radar(ax, ang, vals, *, color, label):
    nums = [_to_num(v) for v in vals]
    vv = [0 if (v is None or (isinstance(v, float) and math.isnan(v))) else v for v in nums]
    ax.plot(ang + ang[:1], vv + vv[:1], color=color, lw=1.2, marker="o", ms=2, label=label)

def dynamic_ylim(vals):
    vv = [v for v in vals if isinstance(v, (int, float)) and not math.isnan(v)]
    if not vv:
        return 0, 10
    lo, hi = min(vv), max(vv)
    pad = max(.5, (hi - lo) * .15)
    lo = max(0, math.floor((lo - pad) * 2) / 2)
    hi = min(10, math.ceil((hi + pad) * 2) / 2)
    if hi - lo < 2:
        mid = (lo + hi) / 2
        lo, hi = mid - 1, mid + 1
    return lo, hi

def draw_bar(ax, xlab, models, summary, *, rubric=None, colors, title, show_legend=False):
    """그룹형 막대그래프를 그립니다."""
    x = np.arange(len(xlab))
    n_models = len(models)
    width = 0.8 / n_models
    allv = []

    for idx, m in enumerate(models):
        if rubric:
            crit_map = summary.get(m, {}).get("criteria_avgs", {}).get(rubric, {})
            y = [crit_map.get(c, math.nan) for c in xlab]
        else:
            y = [summary.get(m, {}).get("score_avgs", {}).get(c, math.nan) for c in xlab]

        nums = [_to_num(v) for v in y]
        y_plot = [0 if (v is None or (isinstance(v, float) and math.isnan(v))) else v for v in nums]
        offsets = x + (idx - (n_models - 1) / 2) * width
        ax.bar(offsets, y_plot, width=width, color=colors[m], label=m, alpha=0.8)
        allv += [v for v in nums if (v is not None and not (isinstance(v, float) and math.isnan(v)))]

        if all((v is None) or (isinstance(v, float) and math.isnan(v)) for v in nums):
            ax.text(0.5, 0.5, "no data", ha="center", va="center",
                    transform=ax.transAxes, fontsize=9, alpha=0.7)

    lo, hi = dynamic_ylim(allv)
    ax.set_ylim(lo, hi)
    ax.set_yticks(np.arange(lo, hi + .001, .5))
    ax.set_yticklabels([f"{t:g}" for t in np.arange(lo, hi + .001, .5)], fontsize=6)
    ax.set_xticks(x)

    if rubric:
        ax.set_xticklabels([CRITERIA_SHORT.get(t, t) for t in xlab], rotation=30, ha="right", fontsize=8)
    else:
        ax.set_xticklabels([SHORT.get(t, t) for t in xlab], rotation=30, ha="right", fontsize=8)

    ax.grid(axis="y", lw=.3, alpha=.5)
    ax.set_title(title, fontsize=10)

    if show_legend and len(models) > 1:
        ax.legend(fontsize=6, loc='upper right')

# ── Excel helpers ────────────────────────────────────────

def _auto(ws):
    from openpyxl.utils import get_column_letter
    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = \
            min(40, max(4, max(len(str(c.value)) if c.value else 0 for c in col) + 2))

def export_excel(summary, path: Path, top_keys: List[str], crit: Dict[str, List[str]], sheet_prefix=""):
    """
    Excel 내보내기:
      - overview: TOP 루브릭들 + MEAN 열 (대분류)
      - <rubric>: 루브릭별 시트 + MEAN 열 (소분류)
      - criteria_all: 모든 세부 기준 + MEAN_ALL 열
      - 각 그룹 사이에 그룹명 행 추가
      - 소수점 둘째자리까지 표시
    """
    def _label_crit(rub: str, ck: str) -> str:
        left = SHORT.get(rub, rub)
        right = CRITERIA_SHORT.get(ck, ck)
        return f"{left}/{right}"
    
    def _format_value(val):
        """값을 소수점 둘째자리로 포맷팅"""
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return np.nan  # ← np.nan 반환
        return round(val, 2)


    flat_cols = []
    for rub in top_keys:
        cks = crit.get(rub, [])
        for ck in cks:
            flat_cols.append((rub, ck, _label_crit(rub, ck)))

    path.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(path, engine="openpyxl") as w:
        # ── overview (대분류: score_avgs) ──────────────────
        rows = []
        for group_name, models_in_group in MODEL_GROUPS.items():
            # 그룹 헤더 행 추가
            group_row = {"model": group_name}
            for a in top_keys:
                group_row[a] = None
            group_row["MEAN"] = None
            rows.append(group_row)
            
            # 그룹 내 모델들
            for m in models_in_group:
                if m not in summary:
                    continue
                row = {"model": m}
                for a in top_keys:
                    row[a] = _format_value(summary[m]["score_avgs"].get(a, math.nan))
                rows.append(row)
        
        df_over = pd.DataFrame(rows).set_index("model")
        # MEAN 계산 (그룹 헤더 제외)
        for idx in df_over.index:
            if idx in MODEL_GROUPS:  # 그룹 헤더면 스킵
                continue
            df_over.loc[idx, "MEAN"] = _format_value(df_over.loc[idx, top_keys].mean(skipna=True))
        
        sheet_name = f"{sheet_prefix}overview" if sheet_prefix else "overview"
        df_over.to_excel(w, sheet_name)

        # ── rubric-wise (각 루브릭 시트 - 소분류) ──────────
        for rub in top_keys:
            rows = []
            cks = crit.get(rub, [])
            
            for group_name, models_in_group in MODEL_GROUPS.items():
                # 그룹 헤더 행 추가
                group_row = {"model": group_name}
                for ck in cks:
                    group_row[ck] = None
                if cks:
                    group_row["MEAN"] = None
                rows.append(group_row)
                
                # 그룹 내 모델들
                for m in models_in_group:
                    if m not in summary:
                        continue
                    row = {"model": m}
                    src = summary[m]["criteria_avgs"].get(rub, {})
                    for ck in cks:
                        row[ck] = _format_value(src.get(ck, math.nan))
                    rows.append(row)
            
            df_rub = pd.DataFrame(rows).set_index("model")
            # MEAN 계산 (그룹 헤더 제외)
            if len(cks) > 0:
                for idx in df_rub.index:
                    if idx in MODEL_GROUPS:  # 그룹 헤더면 스킵
                        continue
                    df_rub.loc[idx, "MEAN"] = _format_value(df_rub.loc[idx, cks].mean(skipna=True))
            
            rename_map = {ck: CRITERIA_SHORT.get(ck, ck) for ck in cks}
            if "MEAN" in df_rub.columns:
                rename_map["MEAN"] = "MEAN"
            sheet_name = f"{sheet_prefix}{rub}" if sheet_prefix else rub
            df_rub.rename(columns=rename_map).to_excel(w, sheet_name[:31])

        # ── criteria_all (모든 소분류) ─────────────────────
        rows_all = []
        for group_name, models_in_group in MODEL_GROUPS.items():
            # 그룹 헤더 행 추가
            group_row = {"model": group_name}
            for rub, ck, _disp in flat_cols:
                group_row[_disp] = None
            group_row["MEAN_ALL"] = None
            rows_all.append(group_row)
            
            # 그룹 내 모델들
            for m in models_in_group:
                if m not in summary:
                    continue
                row = {"model": m}
                for rub, ck, _disp in flat_cols:
                    val = summary[m]["criteria_avgs"].get(rub, {}).get(ck, math.nan)
                    row[_disp] = _format_value(val)
                rows_all.append(row)

        df_all = pd.DataFrame(rows_all).set_index("model")
        crit_cols_display = [disp for _, _, disp in flat_cols]
        # MEAN_ALL 계산 (그룹 헤더 제외)
        if crit_cols_display:
            for idx in df_all.index:
                if idx in MODEL_GROUPS:  # 그룹 헤더면 스킵
                    continue
                df_all.loc[idx, "MEAN_ALL"] = _format_value(df_all.loc[idx, crit_cols_display].mean(skipna=True))

        sheet_name = f"{sheet_prefix}criteria_all" if sheet_prefix else "criteria_all"
        df_all.to_excel(w, sheet_name[:31])

        # ── 열 너비 자동화 ────────────────────────────────
        for ws in w.book.worksheets:
            _auto(ws)

# ── sheet builders ──────────────────────────────────────

def _base(rows_rub: int, dpi: int):
    height = [2] + [1] + [1] * rows_rub
    fig = plt.figure(figsize=(12, (sum(height)) * 3), dpi=dpi, constrained_layout=True)
    grid = gs.GridSpec(2 + rows_rub, 2, hspace=0.8, wspace=0.4, height_ratios=height)
    return fig, grid

def combined_sheet(models, summary, out, dpi, show, top_keys, crit, title_suffix=""):
    rows_rub = ceil(len(top_keys) / 2)
    fig, grid = _base(rows_rub, dpi)
    cmap = plt.get_cmap("tab10")
    colors = {m: cmap(i % 10) for i, m in enumerate(models)}

    ax_r = fig.add_subplot(grid[0, :], polar=True)
    ang = setup_radar(ax_r, top_keys)
    for m in models:
        draw_radar(ax_r, ang,
                   [summary[m]["score_avgs"].get(a, math.nan) for a in top_keys],
                   color=colors[m], label=m)
    ax_r.set_title("overview radar", fontsize=10)
    ax_r.legend(loc="upper left", bbox_to_anchor=(1.22, 1.02), frameon=False, fontsize=6)

    draw_bar(fig.add_subplot(grid[1, :]), top_keys, models, summary,
             colors=colors, title="overall bar", show_legend=True)

    for i, rub in enumerate(top_keys):
        r = 2 + i // 2
        c = i % 2
        draw_bar(fig.add_subplot(grid[r, c]), crit[rub], models, summary,
                 rubric=rub, colors=colors, title=f"{rub} bar", show_legend=True)

    fig.legend(handles=[plt.Line2D([], [], lw=2, color=colors[m], label=m) for m in models],
               loc="center left", bbox_to_anchor=(1.03, 0.5), frameon=False, fontsize=7)

    fig.suptitle(f"Model comparison{title_suffix}", y=.97, fontsize=14)
    plt.subplots_adjust(top=0.95)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=dpi)
    if show:
        plt.show()
    plt.close(fig)

# ── 정렬 헬퍼 ──────────────────────────────────────────────

def _sort_criteria_keys(rubric: str, raw_keys: List[str]) -> List[str]:
    """각 루브릭별로 정의된 criteria 순서를 적용하는 함수."""
    if rubric in CRITERIA_ORDER:
        ordered = [k for k in CRITERIA_ORDER[rubric] if k in raw_keys]
        remaining = [k for k in raw_keys if k not in CRITERIA_ORDER[rubric]]
        return ordered + remaining
    else:
        return sorted(raw_keys)

def _sort_top_keys(raw_keys: List[str]) -> List[str]:
    """SHORT 딕셔너리의 키 순서를 우선적으로 적용한 정렬 함수."""
    ordered = [k for k in _ORDER_PREF if k in raw_keys]
    remaining = [k for k in raw_keys if k not in _ORDER_PREF]
    return ordered + remaining

# ── main ─────────────────────────────────────────────────

def main():
    root = Path(ROOT_DIR)
    if not root.exists():
        sys.exit(f"❌ Root directory not found: {root}")

    # 도메인 목록 (상단 하드코딩에서 가져오기)
    domains = DOMAINS
    
    if not domains:
        sys.exit("❌ No domains specified in DOMAINS. Please check the configuration at the top of the script.")

    # 처리할 모델 목록 (상단 하드코딩에서 자동 생성)
    models = ALL_MODELS
    
    if not models:
        sys.exit("\n❌ No models specified in MODEL_GROUPS. Please check the configuration at the top of the script.")
    
    print(f"\n{'='*60}")
    print(f"📂 Active domains: {', '.join(domains)}")
    print(f"   Note: 'ai' and 'cs' are split from 'csai' folder")
    print(f"📊 Selected models ({len(models)}):")
    print(f"{'='*60}")
    for m in models:
        print(f"  • {m}")

    # 각 도메인별로 데이터 수집
    domain_summaries = {}
    print(f"\n{'='*60}")
    print("📂 Loading data from domains...")
    print(f"{'='*60}")
    
    for domain in domains:
        print(f"\n[{domain.upper()}]")
        summary = scan_domain(root, domain, models)
        if summary:
            domain_summaries[domain] = summary
        else:
            print(f"  ⚠️  No data found")

    if not domain_summaries:
        sys.exit("\n❌ No data found in any domain")

    # 전체 통합 결과 생성 (모든 도메인 평균)
    print(f"\n{'='*60}")
    print("🔄 Aggregating all domains...")
    print(f"{'='*60}")
    aggregated_summary = aggregate_domains(domain_summaries)
    
    # 실제 데이터가 있는 모델만 필터링 (MODEL_GROUPS 순서 유지)
    present_models = []
    for group_name, group_models in MODEL_GROUPS.items():
        for m in group_models:
            if m in aggregated_summary:
                present_models.append(m)
    print(f"✓ Models with data: {len(present_models)}")

    if not present_models:
        sys.exit("\n❌ No models with data found")

    # TOP/CRIT 키 생성
    raw_top_keys = sorted({k for m in present_models for k in aggregated_summary[m].get("score_avgs", {}).keys()})
    top_keys = _sort_top_keys(raw_top_keys)

    crit: Dict[str, List[str]] = {}
    for rub in top_keys:
        keys = {k for m in present_models for k in aggregated_summary[m]["criteria_avgs"].get(rub, {}).keys()}
        crit[rub] = _sort_criteria_keys(rub, list(keys))

    # 출력 디렉토리
    outdir = Path(OUTPUT_DIR)
    outdir.mkdir(parents=True, exist_ok=True)

    # ═══════════════════════════════════════════════════════
    # 1. 전체 통합 결과 (모든 도메인 평균)
    # ═══════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("📊 Generating overall results (all domains combined)...")
    print(f"{'='*60}")
    
    # 전체 시각화
    print("  🎨 Creating visualization...")
    combined_sheet(
        present_models, 
        aggregated_summary, 
        outdir / "overall_comparison.png", 
        DPI, 
        SHOW_PLOT, 
        top_keys, 
        crit,
        title_suffix=" - ALL DOMAINS"
    )
    print(f"  ✓ Saved: {outdir / 'overall_comparison.png'}")

    # 전체 Excel
    print("  📄 Creating Excel...")
    excel_path = outdir / "evaluation_overall.xlsx"
    export_excel(
        aggregated_summary, 
        excel_path, 
        top_keys, 
        crit
    )
    print(f"  ✓ Saved: {excel_path}")

    # ═══════════════════════════════════════════════════════
    # 2. 도메인별 결과
    # ═══════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("📊 Generating domain-specific results...")
    print(f"{'='*60}")

    for domain in domains:
        if domain not in domain_summaries:
            continue
        
        print(f"\n[{domain.upper()}]")
        domain_data = domain_summaries[domain]
        domain_models = [m for m in present_models if m in domain_data]
        
        if not domain_models:
            print(f"  ⚠️  No models with data")
            continue

        domain_outdir = outdir / domain
        domain_outdir.mkdir(parents=True, exist_ok=True)

        # 도메인 시각화
        print(f"  🎨 Creating visualization...")
        combined_sheet(
            domain_models, 
            domain_data, 
            domain_outdir / f"{domain}_comparison.png", 
            DPI, 
            SHOW_PLOT, 
            top_keys, 
            crit,
            title_suffix=f" - {domain.upper()}"
        )
        print(f"  ✓ Saved: {domain_outdir / f'{domain}_comparison.png'}")

        # 도메인 Excel
        print(f"  📄 Creating Excel...")
        excel_path = domain_outdir / f"evaluation_{domain}.xlsx"
        export_excel(
            domain_data, 
            excel_path, 
            top_keys, 
            crit
        )
        print(f"  ✓ Saved: {excel_path}")

    print(f"\n{'='*60}")
    print("✅ All processing completed!")
    print(f"📁 Results saved to: {outdir.absolute()}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()