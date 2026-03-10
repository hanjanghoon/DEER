#!/usr/bin/env python3
"""
make_tableandchart.py
────────────────────────────────────────────────────────────────────────────────
• output/<domain>/<model>/final/<task_id>.json → Calculate average score per domain → Visualize(PNG)/Excel
• Calculate the average of all task files for each domain to compare models
• Generate overall combined results + domain-specific results
• Process CSAI domain separated into AI (1-5) and CS (6-10)
• Layout
    ① Radar (1 row full width)
    ② Overall-bar (1 row full width)
    ③ Rubric-bar (2 columns below)

Usage:
    Modify the settings section below and run: python make_tableandchart.py
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
# 📝 Settings Section - Modify this!
# ══════════════════════════════════════════════════════════════════════════════

# ── Data Path Settings ──────────────────────────────────────────
ROOT_DIR = "output"          # Root directory containing domain folders
OUTPUT_DIR = "visualize"     # Directory to save results

# ── Domain Settings ──────────────────────────────────────────────
# List of domains to analyze (comment out unwanted domains)
# Note: "ai" and "cs" actually refer to the "csai" folder
DOMAINS = [
    "ai",            # ← CSAI tasks 1-5 (AI)
    "bio",           # ← bio domain
    "chem",          # ← chem domain
    "cs",            # ← CSAI tasks 6-10 (CS)
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

# Example: To process only a few
# DOMAINS = [
#     "bio",
#     # "chem",      # ← comment out to exclude
#     "ai",
# ]

# ── Model Group Definition and Selection ────────────────────────────────────
# Comment out an entire group if unwanted
MODEL_GROUPS = {
    "fast": [        # ← fast group (comment out from here down to ], to exclude)
        # "qwen3-235b-fast",
        # "gemini-2.5-pro-fast",
        # "claude_opus4.1_fast",
        "gpt5.2_fast",
    ],
    # "think": [       # ← think group
    #     "qwen3-235b-think",
    #     "gemini-2.5-pro-think",
    #     "claude_opus4.1_think",
    #     "gpt5.2_think",
    # ],
    # "think_search": [ # ← think_search group
    #     "qwen3-235b-think_search",
    #     "claude_opus4.1_think_search",
    #     "gpt5.2_think_search",
    # ],
    # "deep": [        # ← deep group
    #     "webthinker",
    #     "qwen3-235b-deep",
    #     "gemini-2.5-pro_deep",
    #     "claude_opus4.1_deep",
    #     "gpt5_deep",
    #     # "chatexaone_251208_deepresearch"
    # ],
}

# ── Visualization Settings ──────────────────────────────────────────────
DPI = 150          # Image resolution (150-300 recommended)
SHOW_PLOT = False  # True to display on screen

# ══════════════════════════════════════════════════════════════════════════════
# ⚙️ Internal Settings - Do not modify
# ══════════════════════════════════════════════════════════════════════════════

# Create all models list (auto collected from MODEL_GROUPS)
ALL_MODELS = []
for group_name, models in MODEL_GROUPS.items():
    ALL_MODELS.extend(models)

# ══════════════════════════════════════════════════════════════
# Abbreviated Labels
# ══════════════════════════════════════════════════════════════
SHORT = {
    # New structure
    "request_fulfillment":    "fulfillment",
    "analytical_soundness":   "analytical",
    "structural_coherence":   "structure",
    "format_style":           "format",
    
    # Kept existing
    "information_integrity":  "info_integrity",
    "information_sufficiency":"info_sufficiency",
    "ethics_compliance":      "ethics",
}
# ── Detailed criteria abbreviation labels (kept existing + added new items) ──
CRITERIA_SHORT = {
    # request_fulfillment (new)
    "completeness": "completeness",
    "scope": "scope",
    "helpfulness": "helpfulness",

    # analytical_soundness (new)
    "quantification": "quantification",
    "reasoning": "reasoning",

    # structural_coherence (new)
    "introduction": "intro",
    "body": "body",
    "conclusion": "conclusion",
    "section": "section",

    # format_style (new)
    "report_format": "report_fmt",
    "writing_quality": "writing",
    "paragraph_quality": "paragraph",
    "readability": "readability",

    # information_integrity (kept existing)
    "claim_factuality": "claim_acc",
    "citation_validity": "citation_acc",
    "reference_accuracy": "ref_accuracy",
    "reference_quality": "ref_quality",
    "reference_diversity": "ref_diversity",

    # information_sufficiency (kept existing)
    "source_support": "support",
    "information": "info_amount",
    "citations": "cites_amount",
    "references": "refs_amount",

    # ethics_compliance (new structure)
    "sensitive_handling": "sensitive",
    "safety_impact": "safety",
    "perspective_balance": "balance"
}


# Priority list to preserve the key order defined in the SHORT dictionary
_ORDER_PREF = list(SHORT.keys())

# ── Definition of criteria order inside each rubric ──────────────────────
CRITERIA_ORDER = {
    # New structure
    "request_fulfillment": ["completeness", "scope", "helpfulness"],
    "analytical_soundness": ["quantification", "reasoning"],
    "structural_coherence": ["introduction", "body", "conclusion", "section"],
    "format_style": ["report_format", "writing_quality", "paragraph_quality", "readability"],
    
    # Kept existing
    "information_integrity": ["claim_factuality", "citation_validity", "reference_accuracy", "reference_quality", "reference_diversity"],
    "information_sufficiency": ["source_support", "information", "citations", "references"],
    
    # New structure (removed sensitive_issues)
    "ethics_compliance": ["sensitive_handling", "safety_impact", "perspective_balance"]
}

# ── Number Conversion Helper ─────────────────────────────────────────

def _to_num(v):
    """Convert to a number. None if unconvertible or missing."""
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

# ── Domain Mapping Helper ─────────────────────────────────────────

def get_physical_domain(domain: str) -> str:
    """Convert logical domain name to physical folder name"""
    if domain in ["ai", "cs"]:
        return "csai"
    return domain

def get_task_filter(domain: str) -> tuple[int, int] | None:
    """Return task number filter (start, end) based on domain, or None"""
    if domain == "ai":
        return (1, 5)  # 01.json ~ 05.json
    elif domain == "cs":
        return (6, 10)  # 06.json ~ 10.json
    return None

# ── Per-domain Data Loading ─────────────────────────────────────

def load_domain_summary(domain_path: Path, model_name: str, task_filter: tuple[int, int] | None = None) -> dict | None:
    """
    Read all *.json files in domain_path/<model>/final/ and calculate the average
    
    Args:
        domain_path: Domain path
        model_name: Model name
        task_filter: (start, end) task number range filter. Include all tasks if None
    
    Returns:
        {
            "score_avgs": {...},
            "criteria_avgs": {...},
            "task_count": N  # Number of task files read
        }
    """
    model_dir = domain_path / model_name / "final"
    if not model_dir.is_dir():
        return None
    
    all_scores = []
    all_criteria = {}
    
    # Read all json files
    json_files = list(model_dir.glob("*.json"))
    if not json_files:
        return None
    
    for json_file in json_files:
        # Task number filtering
        if task_filter is not None:
            try:
                # Extract number from filename (e.g.: "01.json" -> 1, "003.json" -> 3)
                task_num = int(json_file.stem.lstrip('0') or '0')
                start, end = task_filter
                if not (start <= task_num <= end):
                    continue  # Skip if out of range
            except ValueError:
                continue  # Skip if not a number
        
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            all_scores.append(data.get("score_avgs", {}))
            
            # Collect criteria_avgs
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
    
    # Calculate score_avgs average
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
    Scan specified model data of a specific domain
    For AI/CS, filter by task number in csai folder
    
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

# ── Calculate Overall Domain Average ─────────────────────────────────────

def aggregate_domains(domain_summaries: Dict[str, Dict[str, dict]]) -> Dict[str, dict]:
    """
    Average the results of multiple domains by model to generate an overall combined result
    
    Args:
        domain_summaries: {domain_name: {model_name: summary_dict}}
    
    Returns:
        {model_name: aggregated_summary_dict}
    """
    # Collect all models list
    all_models = set()
    for domain_data in domain_summaries.values():
        all_models.update(domain_data.keys())
    
    aggregated = {}
    
    for model in all_models:
        # Collect data of this model across all domains
        model_scores = []
        model_criteria = {}
        
        for domain, domain_data in domain_summaries.items():
            if model not in domain_data:
                continue
            
            summary = domain_data[model]
            model_scores.append(summary["score_avgs"])
            
            # Collect criteria_avgs
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
        
        # Calculate criteria_avgs average
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
    """Draw grouped bar charts."""
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
    Excel export:
      - overview: TOP rubrics + MEAN column (Major category)
      - <rubric>: Sheet per rubric + MEAN column (Subcategory)
      - criteria_all: All detailed criteria + MEAN_ALL column
      - Add group name row between each group
      - Display rounded to 2 decimal places
    """
    def _label_crit(rub: str, ck: str) -> str:
        left = SHORT.get(rub, rub)
        right = CRITERIA_SHORT.get(ck, ck)
        return f"{left}/{right}"
    
    def _format_value(val):
        """Format value to 2 decimal places"""
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return np.nan  # ← Return np.nan
        return round(val, 2)


    flat_cols = []
    for rub in top_keys:
        cks = crit.get(rub, [])
        for ck in cks:
            flat_cols.append((rub, ck, _label_crit(rub, ck)))

    path.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(path, engine="openpyxl") as w:
        # ── overview (Major category: score_avgs) ──────────────────
        rows = []
        for group_name, models_in_group in MODEL_GROUPS.items():
            # Add group header row
            group_row = {"model": group_name}
            for a in top_keys:
                group_row[a] = None
            group_row["MEAN"] = None
            rows.append(group_row)
            
            # Models in group
            for m in models_in_group:
                if m not in summary:
                    continue
                row = {"model": m}
                for a in top_keys:
                    row[a] = _format_value(summary[m]["score_avgs"].get(a, math.nan))
                rows.append(row)
        
        df_over = pd.DataFrame(rows).set_index("model")
        # Calculate MEAN (excluding group header)
        for idx in df_over.index:
            if idx in MODEL_GROUPS:  # Skip if group header
                continue
            df_over.loc[idx, "MEAN"] = _format_value(df_over.loc[idx, top_keys].mean(skipna=True))
        
        sheet_name = f"{sheet_prefix}overview" if sheet_prefix else "overview"
        df_over.to_excel(w, sheet_name)

        # ── rubric-wise (Sheet per rubric - Subcategory) ──────────
        for rub in top_keys:
            rows = []
            cks = crit.get(rub, [])
            
            for group_name, models_in_group in MODEL_GROUPS.items():
                # Add group header row
                group_row = {"model": group_name}
                for ck in cks:
                    group_row[ck] = None
                if cks:
                    group_row["MEAN"] = None
                rows.append(group_row)
                
                # Models in group
                for m in models_in_group:
                    if m not in summary:
                        continue
                    row = {"model": m}
                    src = summary[m]["criteria_avgs"].get(rub, {})
                    for ck in cks:
                        row[ck] = _format_value(src.get(ck, math.nan))
                    rows.append(row)
            
            df_rub = pd.DataFrame(rows).set_index("model")
            # Calculate MEAN (excluding group header)
            if len(cks) > 0:
                for idx in df_rub.index:
                    if idx in MODEL_GROUPS:  # Skip if group header
                        continue
                    df_rub.loc[idx, "MEAN"] = _format_value(df_rub.loc[idx, cks].mean(skipna=True))
            
            rename_map = {ck: CRITERIA_SHORT.get(ck, ck) for ck in cks}
            if "MEAN" in df_rub.columns:
                rename_map["MEAN"] = "MEAN"
            sheet_name = f"{sheet_prefix}{rub}" if sheet_prefix else rub
            df_rub.rename(columns=rename_map).to_excel(w, sheet_name[:31])

        # ── criteria_all (All subcategories) ─────────────────────
        rows_all = []
        for group_name, models_in_group in MODEL_GROUPS.items():
            # Add group header row
            group_row = {"model": group_name}
            for rub, ck, _disp in flat_cols:
                group_row[_disp] = None
            group_row["MEAN_ALL"] = None
            rows_all.append(group_row)
            
            # Models in group
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
        # Calculate MEAN_ALL (excluding group header)
        if crit_cols_display:
            for idx in df_all.index:
                if idx in MODEL_GROUPS:  # Skip if group header
                    continue
                df_all.loc[idx, "MEAN_ALL"] = _format_value(df_all.loc[idx, crit_cols_display].mean(skipna=True))

        sheet_name = f"{sheet_prefix}criteria_all" if sheet_prefix else "criteria_all"
        df_all.to_excel(w, sheet_name[:31])

        # ── Auto column width ────────────────────────────────
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

# ── Sorting Helper ──────────────────────────────────────────────

def _sort_criteria_keys(rubric: str, raw_keys: List[str]) -> List[str]:
    """Function to apply defined criteria order for each rubric."""
    if rubric in CRITERIA_ORDER:
        ordered = [k for k in CRITERIA_ORDER[rubric] if k in raw_keys]
        remaining = [k for k in raw_keys if k not in CRITERIA_ORDER[rubric]]
        return ordered + remaining
    else:
        return sorted(raw_keys)

def _sort_top_keys(raw_keys: List[str]) -> List[str]:
    """Sorting function predominantly applying the key order of SHORT dictionary."""
    ordered = [k for k in _ORDER_PREF if k in raw_keys]
    remaining = [k for k in raw_keys if k not in _ORDER_PREF]
    return ordered + remaining

# ── main ─────────────────────────────────────────────────

def main():
    root = Path(ROOT_DIR)
    if not root.exists():
        sys.exit(f"❌ Root directory not found: {root}")

    # Domain list (fetch from hardcoding above)
    domains = DOMAINS
    
    if not domains:
        sys.exit("❌ No domains specified in DOMAINS. Please check the configuration at the top of the script.")

    # Target models list (auto generated from hardcoding above)
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

    # Collect data for each domain
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

    # Generate overall combined results (all domains average)
    print(f"\n{'='*60}")
    print("🔄 Aggregating all domains...")
    print(f"{'='*60}")
    aggregated_summary = aggregate_domains(domain_summaries)
    
    # Filter models with actual data (preserve MODEL_GROUPS order)
    present_models = []
    for group_name, group_models in MODEL_GROUPS.items():
        for m in group_models:
            if m in aggregated_summary:
                present_models.append(m)
    print(f"✓ Models with data: {len(present_models)}")

    if not present_models:
        sys.exit("\n❌ No models with data found")

    # Generate TOP/CRIT keys
    raw_top_keys = sorted({k for m in present_models for k in aggregated_summary[m].get("score_avgs", {}).keys()})
    top_keys = _sort_top_keys(raw_top_keys)

    crit: Dict[str, List[str]] = {}
    for rub in top_keys:
        keys = {k for m in present_models for k in aggregated_summary[m]["criteria_avgs"].get(rub, {}).keys()}
        crit[rub] = _sort_criteria_keys(rub, list(keys))

    # Output directory
    outdir = Path(OUTPUT_DIR)
    outdir.mkdir(parents=True, exist_ok=True)

    # ═══════════════════════════════════════════════════════
    # 1. Overall Combined Results (Average of all domains)
    # ═══════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("📊 Generating overall results (all domains combined)...")
    print(f"{'='*60}")
    
    # Overall visualization
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

    # Overall Excel
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
    # 2. Domain-specific Results
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

        # Domain visualization
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

        # Domain Excel
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