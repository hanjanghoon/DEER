from pydantic import BaseModel, Field
from typing import Union, Literal

# 점수 타입: 0-10 정수 또는 "N/A"
ScoreType = Union[int, Literal["N/A"]]


# ============================================================================
# 공통 ScoreFactor 클래스
# ============================================================================

class ScoreFactor(BaseModel):
    """개별 평가 항목: {description, score}"""
    description: str = Field(..., description="Detailed description of the evaluation issue or compliance")
    score: ScoreType = Field(..., description="Score from 0-10 or 'N/A'")


# ============================================================================
# 1. REQUEST FULFILLMENT
# ============================================================================

# Completeness Section
class CompletenessCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")
    C1_2: ScoreFactor = Field(alias="C1-2")
    Q1_1: ScoreFactor = Field(alias="Q1-1")
    Q1_2: ScoreFactor = Field(alias="Q1-2")

class CompletenessCriterion2(BaseModel):
    C2_1: ScoreFactor = Field(alias="C2-1")
    C2_2: ScoreFactor = Field(alias="C2-2")
    Q2_1: ScoreFactor = Field(alias="Q2-1")
    Q2_2: ScoreFactor = Field(alias="Q2-2")

class CompletenessSection(BaseModel):
    field_1: CompletenessCriterion1 = Field(alias="1")
    field_2: CompletenessCriterion2 = Field(alias="2")


# Scope Section
class ScopeCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")
    C1_2: ScoreFactor = Field(alias="C1-2")
    C1_3: ScoreFactor = Field(alias="C1-3")
    C1_4: ScoreFactor = Field(alias="C1-4")
    Q1_1: ScoreFactor = Field(alias="Q1-1")
    Q1_2: ScoreFactor = Field(alias="Q1-2")

class ScopeSection(BaseModel):
    field_1: ScopeCriterion1 = Field(alias="1")


# Helpfulness Section
class HelpfulnessCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")
    Q1_1: ScoreFactor = Field(alias="Q1-1")
    Q1_2: ScoreFactor = Field(alias="Q1-2")

class HelpfulnessCriterion2(BaseModel):
    C2_1: ScoreFactor = Field(alias="C2-1")
    C2_2: ScoreFactor = Field(alias="C2-2")
    Q2_1: ScoreFactor = Field(alias="Q2-1")
    Q2_2: ScoreFactor = Field(alias="Q2-2")

class HelpfulnessCriterion3(BaseModel):
    C3_1: ScoreFactor = Field(alias="C3-1")

class HelpfulnessSection(BaseModel):
    field_1: HelpfulnessCriterion1 = Field(alias="1")
    field_2: HelpfulnessCriterion2 = Field(alias="2")
    field_3: HelpfulnessCriterion3 = Field(alias="3")


# Request Fulfillment Category
class RequestFulfillmentCategory(BaseModel):
    completeness: CompletenessSection
    scope: ScopeSection
    helpfulness: HelpfulnessSection

class RequestFulfillmentScores(BaseModel):
    request_fulfillment: RequestFulfillmentCategory

class RequestFulfillmentResponse(BaseModel):
    scores: RequestFulfillmentScores


# ============================================================================
# 2. ANALYTICAL SOUNDNESS
# ============================================================================

# Quantification Section
class QuantificationCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")

class QuantificationCriterion2(BaseModel):
    C2_1: ScoreFactor = Field(alias="C2-1")
    C2_2: ScoreFactor = Field(alias="C2-2")
    Q2_1: ScoreFactor = Field(alias="Q2-1")

class QuantificationCriterion3(BaseModel):
    C3_1: ScoreFactor = Field(alias="C3-1")
    Q3_1: ScoreFactor = Field(alias="Q3-1")

class QuantificationCriterion4(BaseModel):
    C4_1: ScoreFactor = Field(alias="C4-1")

class QuantificationCriterion5(BaseModel):
    C5_1: ScoreFactor = Field(alias="C5-1")

class QuantificationSection(BaseModel):
    field_1: QuantificationCriterion1 = Field(alias="1")
    field_2: QuantificationCriterion2 = Field(alias="2")
    field_3: QuantificationCriterion3 = Field(alias="3")
    field_4: QuantificationCriterion4 = Field(alias="4")
    field_5: QuantificationCriterion5 = Field(alias="5")


# Reasoning Section
class ReasoningCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")
    C1_2: ScoreFactor = Field(alias="C1-2")
    Q1_1: ScoreFactor = Field(alias="Q1-1")

class ReasoningCriterion2(BaseModel):
    C2_1: ScoreFactor = Field(alias="C2-1")
    C2_2: ScoreFactor = Field(alias="C2-2")
    Q2_1: ScoreFactor = Field(alias="Q2-1")

class ReasoningCriterion3(BaseModel):
    C3_1: ScoreFactor = Field(alias="C3-1")
    C3_2: ScoreFactor = Field(alias="C3-2")
    Q3_1: ScoreFactor = Field(alias="Q3-1")

class ReasoningCriterion4(BaseModel):
    C4_1: ScoreFactor = Field(alias="C4-1")
    Q4_1: ScoreFactor = Field(alias="Q4-1")

class ReasoningCriterion5(BaseModel):
    C5_1: ScoreFactor = Field(alias="C5-1")
    C5_2: ScoreFactor = Field(alias="C5-2")
    Q5_1: ScoreFactor = Field(alias="Q5-1")

class ReasoningCriterion6(BaseModel):
    C6_1: ScoreFactor = Field(alias="C6-1")
    Q6_1: ScoreFactor = Field(alias="Q6-1")

class ReasoningSection(BaseModel):
    field_1: ReasoningCriterion1 = Field(alias="1")
    field_2: ReasoningCriterion2 = Field(alias="2")
    field_3: ReasoningCriterion3 = Field(alias="3")
    field_4: ReasoningCriterion4 = Field(alias="4")
    field_5: ReasoningCriterion5 = Field(alias="5")
    field_6: ReasoningCriterion6 = Field(alias="6")


# Analytical Soundness Category
class AnalyticalSoundnessCategory(BaseModel):
    quantification: QuantificationSection
    reasoning: ReasoningSection

class AnalyticalSoundnessScores(BaseModel):
    analytical_soundness: AnalyticalSoundnessCategory

class AnalyticalSoundnessResponse(BaseModel):
    scores: AnalyticalSoundnessScores


# ============================================================================
# 3. STRUCTURAL COHERENCE
# ============================================================================

# Introduction Section
class IntroductionCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")
    Q1_1: ScoreFactor = Field(alias="Q1-1")
    Q1_2: ScoreFactor = Field(alias="Q1-2")
    Q1_3: ScoreFactor = Field(alias="Q1-3")

class IntroductionCriterion2(BaseModel):
    Q2_1: ScoreFactor = Field(alias="Q2-1")

class IntroductionCriterion3(BaseModel):
    C3_1: ScoreFactor = Field(alias="C3-1")
    Q3_1: ScoreFactor = Field(alias="Q3-1")

class IntroductionCriterion4(BaseModel):
    Q4_1: ScoreFactor = Field(alias="Q4-1")

class IntroductionSection(BaseModel):
    field_1: IntroductionCriterion1 = Field(alias="1")
    field_2: IntroductionCriterion2 = Field(alias="2")
    field_3: IntroductionCriterion3 = Field(alias="3")
    field_4: IntroductionCriterion4 = Field(alias="4")


# Body Section
class BodyCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")
    C1_2: ScoreFactor = Field(alias="C1-2")
    C1_3: ScoreFactor = Field(alias="C1-3")
    C1_4: ScoreFactor = Field(alias="C1-4")

class BodyCriterion2(BaseModel):
    C2_1: ScoreFactor = Field(alias="C2-1")
    C2_2: ScoreFactor = Field(alias="C2-2")

class BodySection(BaseModel):
    field_1: BodyCriterion1 = Field(alias="1")
    field_2: BodyCriterion2 = Field(alias="2")


# Conclusion Section
class ConclusionCriterion1(BaseModel):
    Q1_1: ScoreFactor = Field(alias="Q1-1")

class ConclusionCriterion2(BaseModel):
    Q2_1: ScoreFactor = Field(alias="Q2-1")

class ConclusionSection(BaseModel):
    field_1: ConclusionCriterion1 = Field(alias="1")
    field_2: ConclusionCriterion2 = Field(alias="2")


# Section Section
class SectionCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")

class SectionCriterion2(BaseModel):
    C2_1: ScoreFactor = Field(alias="C2-1")
    C2_2: ScoreFactor = Field(alias="C2-2")
    C2_3: ScoreFactor = Field(alias="C2-3")
    Q2_1: ScoreFactor = Field(alias="Q2-1")

class SectionCriterion3(BaseModel):
    C3_1: ScoreFactor = Field(alias="C3-1")
    C3_2: ScoreFactor = Field(alias="C3-2")
    Q3_1: ScoreFactor = Field(alias="Q3-1")

class SectionSection(BaseModel):
    field_1: SectionCriterion1 = Field(alias="1")
    field_2: SectionCriterion2 = Field(alias="2")
    field_3: SectionCriterion3 = Field(alias="3")


# Structural Coherence Category
class StructuralCoherenceCategory(BaseModel):
    introduction: IntroductionSection
    body: BodySection
    conclusion: ConclusionSection
    section: SectionSection

class StructuralCoherenceScores(BaseModel):
    structural_coherence: StructuralCoherenceCategory

class StructuralCoherenceResponse(BaseModel):
    scores: StructuralCoherenceScores


# ============================================================================
# 4. FORMAT STYLE
# ============================================================================

# Report Format Section
class ReportFormatCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")
    C1_2: ScoreFactor = Field(alias="C1-2")

class ReportFormatCriterion2(BaseModel):
    C2_1: ScoreFactor = Field(alias="C2-1")
    C2_2: ScoreFactor = Field(alias="C2-2")

class ReportFormatCriterion3(BaseModel):
    C3_2: ScoreFactor = Field(alias="C3-2")

class ReportFormatSection(BaseModel):
    field_1: ReportFormatCriterion1 = Field(alias="1")
    field_2: ReportFormatCriterion2 = Field(alias="2")
    field_3: ReportFormatCriterion3 = Field(alias="3")


# Writing Quality Section
class WritingQualityCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")

class WritingQualityCriterion2(BaseModel):
    C2_1: ScoreFactor = Field(alias="C2-1")

class WritingQualityCriterion3(BaseModel):
    C3_1: ScoreFactor = Field(alias="C3-1")
    C3_2: ScoreFactor = Field(alias="C3-2")

class WritingQualityCriterion4(BaseModel):
    C4_1: ScoreFactor = Field(alias="C4-1")

class WritingQualitySection(BaseModel):
    field_1: WritingQualityCriterion1 = Field(alias="1")
    field_2: WritingQualityCriterion2 = Field(alias="2")
    field_3: WritingQualityCriterion3 = Field(alias="3")
    field_4: WritingQualityCriterion4 = Field(alias="4")


# Paragraph Quality Section
class ParagraphQualityCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")
    Q1_1: ScoreFactor = Field(alias="Q1-1")

class ParagraphQualityCriterion2(BaseModel):
    C2_1: ScoreFactor = Field(alias="C2-1")
    C2_2: ScoreFactor = Field(alias="C2-2")

class ParagraphQualityCriterion3(BaseModel):
    C3_1: ScoreFactor = Field(alias="C3-1")

class ParagraphQualitySection(BaseModel):
    field_1: ParagraphQualityCriterion1 = Field(alias="1")
    field_2: ParagraphQualityCriterion2 = Field(alias="2")
    field_3: ParagraphQualityCriterion3 = Field(alias="3")


# Readability Section
class ReadabilityCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")

class ReadabilityCriterion2(BaseModel):
    Q2_1: ScoreFactor = Field(alias="Q2-1")

class ReadabilitySection(BaseModel):
    field_1: ReadabilityCriterion1 = Field(alias="1")
    field_2: ReadabilityCriterion2 = Field(alias="2")


# Format Style Category
class FormatStyleCategory(BaseModel):
    report_format: ReportFormatSection
    writing_quality: WritingQualitySection
    paragraph_quality: ParagraphQualitySection
    readability: ReadabilitySection

class FormatStyleScores(BaseModel):
    format_style: FormatStyleCategory

class FormatStyleResponse(BaseModel):
    scores: FormatStyleScores


# ============================================================================
# 5. INFORMATION INTEGRITY & ETHICS COMPLIANCE
# ============================================================================

# Recency Section (Information Integrity)
class RecencyCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")
    C1_2: ScoreFactor = Field(alias="C1-2")
    C1_3: ScoreFactor = Field(alias="C1-3")

class RecencySection(BaseModel):
    field_1: RecencyCriterion1 = Field(alias="1")

class InformationIntegrityCategory(BaseModel):
    recency: RecencySection


# Sensitive Handling Section (Ethics Compliance)
class SensitiveHandlingCriterion1(BaseModel):
    Q1_1: ScoreFactor = Field(alias="Q1-1")
    Q1_2: ScoreFactor = Field(alias="Q1-2")

class SensitiveHandlingCriterion2(BaseModel):
    C2_1: ScoreFactor = Field(alias="C2-1")
    C2_2: ScoreFactor = Field(alias="C2-2")

class SensitiveHandlingSection(BaseModel):
    field_1: SensitiveHandlingCriterion1 = Field(alias="1")
    field_2: SensitiveHandlingCriterion2 = Field(alias="2")


# Safety Impact Section (Ethics Compliance)
class SafetyImpactCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")
    C1_2: ScoreFactor = Field(alias="C1-2")
    Q1_1: ScoreFactor = Field(alias="Q1-1")
    Q1_2: ScoreFactor = Field(alias="Q1-2")

class SafetyImpactCriterion2(BaseModel):
    C2_1: ScoreFactor = Field(alias="C2-1")

class SafetyImpactSection(BaseModel):
    field_1: SafetyImpactCriterion1 = Field(alias="1")
    field_2: SafetyImpactCriterion2 = Field(alias="2")


# Perspective Balance Section (Ethics Compliance)
class PerspectiveBalanceCriterion1(BaseModel):
    C1_1: ScoreFactor = Field(alias="C1-1")
    Q1_1: ScoreFactor = Field(alias="Q1-1")

class PerspectiveBalanceSection(BaseModel):
    field_1: PerspectiveBalanceCriterion1 = Field(alias="1")


# Ethics Compliance Category
class EthicsComplianceCategory(BaseModel):
    sensitive_handling: SensitiveHandlingSection
    safety_impact: SafetyImpactSection
    perspective_balance: PerspectiveBalanceSection


# Combined Information Integrity & Ethics Compliance
class InformationEthicsScores(BaseModel):
    information_integrity: InformationIntegrityCategory
    ethics_compliance: EthicsComplianceCategory

class InformationEthicsResponse(BaseModel):
    scores: InformationEthicsScores


# ============================================================================
# RESPONSE FORMAT MAP
# ============================================================================

RESPONSE_FORMAT_MAP = {
    "request_fulfillment": RequestFulfillmentResponse,
    "analytical_soundness": AnalyticalSoundnessResponse,
    "structural_coherence": StructuralCoherenceResponse,
    "format_style": FormatStyleResponse,
    "information_ethics": InformationEthicsResponse,
}