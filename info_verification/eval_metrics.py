from .claim_verifier import VerifiedClaim, VerificationResult
import pandas as pd
import numpy as np
from typing import Dict, List
from .report_utils import clean_url

def compute_claim_metrics(verified_claims: list[VerifiedClaim]) -> dict:
    """
    - Claim Accuracy
    - Verificable Claims Ratio (Citation Ratio)
    """
    # Filter out claims of type "B3" (Recap or summary claims)
    total_len = len(verified_claims)
    claims = []
    claim_type_counts = {}

    for claim in verified_claims:
        # Update for new claim types (v10):
        # A: Cited Claim
        # B: Uncited - Same Section/Paragraph (Backtracked to citations)
        # C: Uncited - Previous Section/Paragraph (Backtracked to citations)
        # D: Uncited - Recap/Structural
        # E: Uncited - Citation not Required (Common knowledge / Opinion)
        # F: No-Citation - Unknown Source (Missing citation)

        is_common = claim.claim.claim_type == "E" 
        is_internal = claim.claim.claim_type == "D" 
        is_external = claim.claim.claim_type in ["A", "B", "C", "F"] 

        if claim.claim.claim_type not in claim_type_counts:
            claim_type_counts[claim.claim.claim_type] = 0
        claim_type_counts[claim.claim.claim_type] += 1

        result, _ = claim.final_result_and_explanation()

        claims.append(dict(
            claim_type=claim.claim.claim_type,
            result=result,
            supported=result == "supported",
            error=result == "error",
            is_numeric=claim.claim.numeric,
            is_common=is_common,
            is_internal=is_internal,
            is_external=is_external,
        ))

    return dict(
        total_claims=total_len,
        claim_type_counts=claim_type_counts,
        claims=claims,
    )


def compute_citation_metrics(verified_claims: list[VerifiedClaim]) -> dict:
    """
    - Citation Accuracy
    """
    num_citations = 0
    num_supported = 0
    num_error_citations = 0

    for claim in verified_claims:
        # Only A, B, C are expected to have citations after backtracking
        if claim.claim.claim_type not in ["A", "B", "C"]:
            continue

        for verification in claim.verifications:
            num_citations += 1

            if verification.result == "error":
                num_error_citations += 1    
            if verification.result == "supported":
                num_supported += 1

    return dict(
        num_supported=num_supported,
        num_error_citations=num_error_citations,
        num_citations=num_citations
    )
# -----------------------------
# Helpers: HHI-based balance -> 0~10
# -----------------------------
def _hhi_from_counts(counts: list[int]) -> float:
    total = sum(counts)
    if total <= 0:
        return 0.0
    ps = [c / total for c in counts]
    return float(sum(p * p for p in ps))

def _hhi_balance_score_0_10(counts: list[int]) -> float:
    """
    HHI 기반 '균형(balance)' 점수.
    - 입력 counts: 레퍼런스별 인용횟수(지원된 인용만 권장)
    - 출력: 0~10 (10=완전 균등, 0=완전 몰빵)
    레퍼런스 수(n)에 대해 정규화해 문서간 비교 가능하게 함.
    """
    counts = [c for c in counts if c > 0]
    n = len(counts)
    if n == 0:
        return 0.0
    if n == 1:
        return 0.0  # 하나에 몰빵

    hhi = _hhi_from_counts(counts)
    # HHI의 이론적 범위: [1/n, 1]
    hhi_norm = (hhi - 1 / n) / (1 - 1 / n)  # 0(균등)~1(몰빵)
    score = 10 * (1 - hhi_norm)             # 10(균등)~0(몰빵)
    return float(max(0.0, min(10.0, score)))


# -----------------------------
# Reference metrics (UPDATED)
# -----------------------------
def compute_reference_metrics(
    verified_claims: list["VerifiedClaim"],
    references: dict[str, str],
    context_informations: dict[str, list["VerificationResult"]],
) -> dict:
    context_metrics = {}

    cited_counts: dict[str, int] = {}              # 모든 인용 시도(used) 카운트
    supported_cited_counts: dict[str, int] = {}    # ✅ supported 인용만 카운트(다양성/균형 계산용)

    supported_references = set()
    used_references = set()
    error_references = set()
    reliable_references = set()

    unique_references = set(clean_url(url) for url in references.values())

    for claim in verified_claims:
        for verification in claim.verifications:
            url = clean_url(verification.url)

            # supported/error set
            if verification.result == "supported":
                supported_references.add(url)
                supported_cited_counts[url] = supported_cited_counts.get(url, 0) + 1  # ✅
            if verification.result == "error":
                error_references.add(url)
            if verification.reliable:
                reliable_references.add(url)

            # used counts/sets (기존 유지)
            cited_counts[url] = cited_counts.get(url, 0) + 1
            used_references.add(url)

    # 기존 CV용 mean/std는 유지(원하면 나중에 제거 가능)
    all_counts = list(cited_counts.values())
    citations_mean = float(np.mean(all_counts)) if all_counts else 0.0
    citations_std = float(np.std(all_counts)) if all_counts else 0.0

    # ✅ supported-only balance (HHI 기반 0~10)
    supported_counts = list(supported_cited_counts.values())
    balance_supported_0_10 = _hhi_balance_score_0_10(supported_counts)

    context_metrics.update({
        "num_references": len(references),
        "num_unique_references": len(unique_references),

        "num_supported": len(supported_references),
        "num_used": len(used_references),
        "num_error": len(error_references),
        "num_reliable": len(reliable_references & supported_references),

        "supported_references": list(supported_references),
        "used_references": list(used_references),
        "error_references": list(error_references),

        "cited_counts": cited_counts,
        "citations_mean": citations_mean,
        "citations_std": citations_std,

        # ✅ 새로 추가
        "supported_cited_counts": supported_cited_counts,           # 디버깅용(선택)
        "balance_supported_0_10": float(balance_supported_0_10),     # 핵심: supported-only 균형 점수
    })

    return context_metrics


def compute_metrics(
    verified_claims: list[VerifiedClaim],
    references: dict[str, dict],
    context_informations: dict,
) -> dict:
    claim_metrics = compute_claim_metrics(verified_claims)
    citation_metrics = compute_citation_metrics(verified_claims)
    reference_metrics = compute_reference_metrics(verified_claims, references, context_informations)

    for url, info in context_informations.items():
        info.pop("context", None)  # Remove context if it exists

    claim_df = pd.DataFrame(claim_metrics["claims"])

    # Integrity metrics
    ## Claim Factuality
    # All types A-F are considered part of the report content
    verifiable_claims = claim_df[claim_df.claim_type.isin(["A", "B", "C", "D", "E"])]
    
    # supported or internal (D) or common (E)
    # F counts as denominator but not numerator (accuracy penalty)
    df_accurate = verifiable_claims[verifiable_claims.supported | verifiable_claims.is_internal | verifiable_claims.is_common]
    claim_accuracy = len(df_accurate) / len(verifiable_claims) if not verifiable_claims.empty else 0.0


    external_verifiable_claims = claim_df[claim_df.claim_type.isin(["A", "B", "C"])]
    external_claim_accuracy = external_verifiable_claims.supported.mean() if not external_verifiable_claims.empty else 0.0

    external_numeric_claims = external_verifiable_claims[external_verifiable_claims.is_numeric]
    external_numeric_claim_accuracy = external_numeric_claims.supported.mean() if not external_numeric_claims.empty else 0.0

    ## Citation Validity
    citation_accuracy = citation_metrics["num_supported"] / citation_metrics["num_citations"] if citation_metrics["num_citations"] > 0 else 0.0

    ## Reference Accuracy
    supported_per_shown = reference_metrics["num_supported"] / reference_metrics["num_unique_references"] if reference_metrics["num_unique_references"] > 0 else 0.0
    supported_per_used = reference_metrics["num_supported"] / reference_metrics["num_used"] if reference_metrics["num_used"] > 0 else 0.0
    used_per_shown = reference_metrics["num_used"] / reference_metrics["num_unique_references"] if reference_metrics["num_unique_references"] > 0 else 0.0

    ## Reproducibility Ratio
    reproducibility_ratio = 1 - (reference_metrics["num_error"] / reference_metrics["num_used"]) if reference_metrics["num_used"] > 0 else 0.0

    ## Reliability Ratio
    reliability_ratio = reference_metrics["num_reliable"] / reference_metrics["num_used"] if reference_metrics["num_used"] > 0 else 0.0

    # Informaation Sufficiency
    ## Source Support
    claim_types = claim_metrics["claim_type_counts"]
    num_verifiable_claims = (claim_types.get("A", 0) + claim_types.get("B", 0) + claim_types.get("C", 0) + claim_types.get("D", 0))
    num_externally_verifiable_claims = (claim_types.get("A", 0) + claim_types.get("B", 0))
    num_unverifiable_claims = claim_types.get("C", 0)

    verified_claims_ratio = num_verifiable_claims / (num_verifiable_claims + num_unverifiable_claims) if (num_verifiable_claims + num_unverifiable_claims) > 0 else 0.0
    externally_verifiable_claims_ratio = num_externally_verifiable_claims / (num_externally_verifiable_claims + num_unverifiable_claims) if (num_externally_verifiable_claims + num_unverifiable_claims) > 0 else 0.0

    average_citations_per_claim = (citation_metrics["num_citations"] / num_externally_verifiable_claims if num_externally_verifiable_claims > 0 else 0.0) 

    ## Source Diversity
    # Check for division by zero
    if citation_metrics["num_supported"] > 0:
        unique_reference = reference_metrics["num_supported"] / citation_metrics["num_supported"]
    else:
        unique_reference = 0.0

    citations_CV = reference_metrics["citations_std"] / reference_metrics["citations_mean"] if reference_metrics["citations_mean"] > 0 else 0.0
    
  # ✅ 최종 diversity 점수: supported-only balance(0~10) × supported_per_shown(0~1)
    reference_diversity_final_0_10 = reference_metrics["balance_supported_0_10"] 
    reference_diversity_final_0_10 = float(max(0.0, min(10.0, reference_diversity_final_0_10)))

    ## Volume metrics
    amount_of_information = len(df_accurate)
    amount_of_citations = citation_metrics["num_supported"]
    amount_of_references = reference_metrics["num_supported"]


    return {
        "raw": {
            "claim_metrics": claim_metrics,
            "citation_metrics": citation_metrics,
            "reference_metrics": reference_metrics,
        },
        "integrity": {
            "claim_factuality": {
                "claim_accuracy": claim_accuracy,
                "external_claim_accuracy": external_claim_accuracy,
                "external_numeric_claim_accuracy": external_numeric_claim_accuracy
            },
            "citation_validity": {
                "citation_accuracy": citation_accuracy,
            },
            "reference_accuracy": {
                "supported_per_shown": supported_per_shown,
                "supported_per_used": supported_per_used,
                "used_per_shown": used_per_shown,
            },
            "reference_quality": {
                "reproducibility": reproducibility_ratio,
                "reliability": reliability_ratio,
            },
            "reference_diversity": {
                "unique_reference":  unique_reference,
                "citations_CV": citations_CV,
                "diversity_hhi": reference_diversity_final_0_10,
            },
        },
        "sufficiency": {
            "source_support": {
                "verified_claims_ratio": verified_claims_ratio,
                "externally_verifiable_claims_ratio": externally_verifiable_claims_ratio,
                "average_citations_per_claim": average_citations_per_claim,
            },
            
            "information": amount_of_information,
            "citations": amount_of_citations,
            "references": amount_of_references,
            
        },
    }
