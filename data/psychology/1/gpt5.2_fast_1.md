# Knowledge Acquisition, Perceived Knowledge Gaps, and the Self-Stabilisation of Intrinsic Motivation Across Learning Stages

## Abstract

Intrinsic motivation is widely recognized as a central driver of sustained learning, exploration, and skill development. Yet motivation is not static: it fluctuates as learners acquire knowledge, confront uncertainty, and reassess what they do and do not know. This report develops and evaluates a testable theoretical account of how **knowledge acquisition**, **perceived knowledge gaps**, and **intrinsic motivation** interact dynamically across different learning stages. Building on empirical and theoretical work in educational psychology, cognitive science, and curiosity research, the report argues that perceived knowledge gaps function as a *regulatory signal* that can stabilize intrinsic motivation over time. Specifically, as learners progress, increases in knowledge tend to *both* reduce absolute ignorance and sharpen awareness of remaining gaps, producing a self-stabilising feedback loop in which interest is maintained rather than extinguished.

The report proposes a **Stage-Sensitive Gap–Interest Model (SGIM)** that formalizes how learning progress modulates perceived gaps and motivational intensity across novice, intermediate, and advanced phases. The model yields concrete, testable predictions about curiosity, engagement, and dropout risk at each stage. Empirical operationalizations and experimental designs are discussed. Finally, the report explores implications for instructional design, adaptive feedback systems, and curiosity-driven learning environments, arguing that effective educational systems should actively manage perceived knowledge gaps rather than merely transmit information.

---

## 1. Introduction

### 1.1 Motivation as a Dynamic Property of Learning

Learning is not merely a matter of information transfer or skill acquisition; it is also a motivational process. A learner’s willingness to persist, explore, and tolerate difficulty depends critically on intrinsic motivation—engagement driven by interest, enjoyment, or perceived value rather than external rewards [1]. Traditional accounts often treat motivation as a relatively stable trait or as an outcome influenced by environmental incentives. However, accumulating evidence suggests that motivation fluctuates systematically during learning itself, shaped by the learner’s evolving understanding of the domain [2].

One particularly robust phenomenon is that learning can *increase* interest even as it reduces ignorance. This appears paradoxical: if curiosity is driven by not knowing, why does acquiring knowledge often deepen rather than extinguish motivation? This report addresses this puzzle by focusing on the learner’s **perception of knowledge gaps**, rather than objective ignorance alone.

### 1.2 Knowledge Gaps and Curiosity

The idea that curiosity arises from perceived gaps between what one knows and what one wants to know has a long history. Loewenstein’s information-gap theory proposes that curiosity is triggered when individuals become aware of a gap in their knowledge that they find salient and potentially closable [3]. Importantly, this awareness often *requires* some prior knowledge; complete ignorance may not generate curiosity at all.

This observation suggests that learning and curiosity are mutually reinforcing. Initial knowledge enables gap perception, which fuels curiosity, which in turn motivates further learning. However, this loop does not operate uniformly across all learning stages. Novices, intermediates, and experts differ in how they perceive gaps, evaluate progress, and regulate motivation.

### 1.3 Goals and Structure of the Report

The goals of this report are fourfold:

1. To synthesize existing research on intrinsic motivation, curiosity, and perceived knowledge gaps.
2. To propose a **testable theoretical model** explaining how learning progress modulates gap perception and intrinsic motivation across stages.
3. To derive empirical predictions and methodological approaches for evaluating this model.
4. To explore implications for instructional design, feedback systems, and curiosity-driven learning environments.

The report proceeds by reviewing relevant literature, introducing the Stage-Sensitive Gap–Interest Model, discussing empirical testability, and finally considering broader applications.

---

## 2. Conceptual Foundations

### 2.1 Intrinsic Motivation

Intrinsic motivation refers to engagement in an activity for its inherent satisfaction rather than for separable outcomes [1]. Self-Determination Theory (SDT) identifies autonomy, competence, and relatedness as basic psychological needs underlying intrinsic motivation [1]. Of these, **perceived competence** is particularly relevant for learning dynamics, as it directly relates to how learners interpret their progress and remaining challenges.

Empirical studies consistently show that intrinsic motivation predicts deeper learning strategies, persistence, and transfer [2]. However, SDT does not by itself specify how perceptions of competence evolve as knowledge accumulates, nor how awareness of ignorance might simultaneously undermine and support motivation.

### 2.2 Knowledge Acquisition and Metacognition

Knowledge acquisition is accompanied by changes in metacognitive awareness—learners’ ability to assess what they know and do not know. Early work on metacognition emphasized calibration accuracy and judgments of learning [4]. Later research highlighted systematic biases, such as the Dunning–Kruger effect, where novices overestimate their competence due to limited metacognitive insight [5].

As learners gain experience, metacognitive sensitivity improves, often leading to a temporary *decrease* in confidence as awareness of complexity grows. This phenomenon has been observed in domains ranging from science learning to skill acquisition [6].

### 2.3 Curiosity and the Information-Gap

Loewenstein’s information-gap theory formalizes curiosity as an aversive feeling caused by awareness of a gap between current and desired knowledge states [3]. Curiosity intensity depends on both the size of the gap and the learner’s belief that the gap is bridgeable. Empirical work shows that curiosity peaks at intermediate levels of uncertainty, following an inverted-U relationship [7].

Neuroscientific evidence supports this account: curiosity engages dopaminergic circuits associated with reward and learning, enhancing memory for information acquired under high curiosity states [8].

---

## 3. Learning Stages and Perceived Knowledge Gaps

### 3.1 Novice Stage: Opaque Ignorance

At the novice stage, learners possess minimal domain knowledge and limited metacognitive insight. Because they lack conceptual structure, they may be unaware of what they do not know. This “opaque ignorance” can result in low curiosity and unstable motivation, particularly if early failures undermine perceived competence [5].

Paradoxically, novices may also experience inflated confidence due to shallow understanding, masking true gaps. Motivation at this stage is often fragile and highly sensitive to external support and scaffolding [2].

### 3.2 Intermediate Stage: Salient Gaps and Rising Interest

As learners acquire foundational knowledge, they become capable of recognizing inconsistencies, open questions, and deeper structure. This stage is characterized by heightened perception of knowledge gaps and often by increased curiosity [7].

Empirical studies in science education show that learners report greater interest after acquiring basic conceptual frameworks, even though they become more aware of what they do not understand [6]. This suggests that gap perception, when coupled with a sense of progress, can stabilize or enhance intrinsic motivation.

### 3.3 Advanced Stage: Expanding Horizons

At advanced stages, learners often possess high competence and refined metacognitive skills. Knowledge gaps do not disappear; instead, they become more abstract and open-ended. Experts frequently report strong intrinsic motivation driven by long-term questions and unsolved problems [9].

However, if gaps are perceived as unbridgeable or progress stalls, motivation can decline. Thus, even at advanced levels, the balance between perceived gap size and perceived attainability remains critical.

---

## 4. The Stage-Sensitive Gap–Interest Model (SGIM)

### 4.1 Core Assumptions

The SGIM is built on four core assumptions:

1. **Perceived knowledge gaps, not objective ignorance, directly drive curiosity and interest** [3].
2. **Learning progress increases both knowledge and gap awareness**, especially after the novice stage [6].
3. **Intrinsic motivation depends on the interaction between perceived gap size and perceived attainability**, not on either alone [7].
4. **This interaction varies systematically across learning stages**.

### 4.2 Formal Description

Let:

* ( K ) = objective knowledge level
* ( G_p ) = perceived knowledge gap
* ( A ) = perceived attainability of closing the gap
* ( I ) = intrinsic motivation (interest)

The model proposes:

[
I = f(G_p, A)
]

with:

* ( \frac{\partial I}{\partial G_p} > 0 ) for moderate ( G_p )
* ( \frac{\partial I}{\partial G_p} < 0 ) for very large or very small ( G_p )
* ( \frac{\partial I}{\partial A} > 0 )

Perceived gap ( G_p ) is modeled as a function of knowledge:

[
G_p = g(K)
]

where ( g(K) ) is low at very low ( K ), increases at intermediate ( K ), and stabilizes or slowly increases at high ( K ).

### 4.3 Self-Stabilising Dynamics

The key claim of the SGIM is that learning progress can produce a **negative feedback loop** that stabilizes motivation:

1. Learning increases ( K ).
2. Increased ( K ) raises ( G_p ), enhancing curiosity.
3. Enhanced curiosity increases engagement, further increasing ( K ).

This loop stabilizes motivation as long as perceived attainability ( A ) remains sufficiently high. When ( A ) drops—due to excessive difficulty, lack of feedback, or contextual barriers—the loop breaks.

---

## 5. Empirical Testability

### 5.1 Operationalizing Key Variables

* **Knowledge (K):** domain-specific assessments, concept inventories.
* **Perceived Knowledge Gap (G_p):** self-report measures of uncertainty or “questions remaining,” confidence calibration tasks [4].
* **Perceived Attainability (A):** expectancy of success scales, self-efficacy measures [1].
* **Intrinsic Motivation (I):** interest/enjoyment scales, voluntary engagement time [2].

### 5.2 Experimental Designs

A longitudinal design can track learners across stages, measuring changes in ( K ), ( G_p ), and ( I ). Experimental manipulations can alter perceived gaps (e.g., presenting open questions vs. closed summaries) and attainability (e.g., adaptive hints).

The model predicts that interventions increasing gap salience will boost motivation at intermediate stages but may demotivate novices unless accompanied by scaffolding.

### 5.3 Falsifiable Predictions

1. Increasing gap salience will increase interest only when baseline knowledge exceeds a threshold.
2. For equal knowledge gains, learners with higher perceived attainability will show more stable motivation.
3. Artificially reducing perceived gaps (e.g., oversimplified explanations) will reduce long-term curiosity despite short-term satisfaction.

---

## 6. Implications for Instructional Design

### 6.1 Managing Gap Salience

Instruction should not aim to eliminate perceived gaps entirely. Instead, effective design strategically reveals gaps that are meaningful and tractable. Inquiry-based learning and problem-based learning exemplify this approach [10].

### 6.2 Adaptive Feedback Systems

Feedback that communicates progress while highlighting next-step gaps supports perceived competence and curiosity simultaneously. Adaptive learning systems can personalize gap exposure based on learner stage [11].

### 6.3 Curiosity-Driven Learning Environments

Curiosity-driven systems, including intelligent tutors and exploratory digital platforms, can leverage SGIM principles by dynamically adjusting challenge and uncertainty to maintain motivation [8].

---

## 7. Broader Implications and Future Directions

The SGIM has implications beyond formal education, including lifelong learning, scientific research training, and human–AI interaction. Systems that prematurely close gaps risk dampening curiosity, while systems that overwhelm learners risk disengagement.

Future research should integrate affective neuroscience, computational modeling, and educational data to refine stage-sensitive motivational dynamics. Understanding how perceived gaps stabilize motivation may be crucial for designing learning environments that sustain engagement in an era of abundant information.

---

## 8. Conclusion

This report has argued that intrinsic motivation in learning is dynamically regulated by the interplay between knowledge acquisition and perceived knowledge gaps. By proposing the Stage-Sensitive Gap–Interest Model, it provides a testable framework explaining how learning progress can stabilize interest across stages. Rather than viewing ignorance as a deficit to be eliminated, effective learning systems should treat perceived knowledge gaps as motivational resources—carefully managed to sustain curiosity, competence, and engagement over time.

---

## References

[1] Deci, E. L., & Ryan, R. M. Intrinsic Motivation and Self-Determination in Human Behavior – https://www.springer.com/gp/book/9780306420221
[2] Hidi, S., & Renninger, K. A. The Four-Phase Model of Interest Development – https://doi.org/10.1207/s15326985ep4102_1
[3] Loewenstein, G. The Psychology of Curiosity: A Review and Reinterpretation – https://doi.org/10.1037/0033-295X.102.1.75
[4] Dunlosky, J., & Metcalfe, J. Metacognition – https://www.sagepub.com/sites/default/files/upm-binaries/6097_Chapter_1.pdf
[5] Kruger, J., & Dunning, D. Unskilled and Unaware of It – https://doi.org/10.1037/0022-3514.77.6.1121
[6] Chi, M. T. H. Active-Constructive-Interactive: A Conceptual Framework – https://doi.org/10.1016/j.cedpsych.2009.04.001
[7] Kang, M. J., et al. The Wick in the Candle of Learning – https://doi.org/10.1177/0956797613489012
[8] Gruber, M. J., Gelman, B. D., & Ranganath, C. States of Curiosity Modulate Hippocampus-Dependent Learning – https://www.cell.com/neuron/fulltext/S0896-6273(14)00463-0
[9] Ericsson, K. A. Deliberate Practice and the Acquisition of Expert Performance – https://doi.org/10.1037/0033-295X.100.3.363
[10] Barrows, H. S. Problem-Based Learning in Medicine and Beyond – https://doi.org/10.1002/tl.37219966804
[11] VanLehn, K. The Relative Effectiveness of Human Tutoring, Intelligent Tutoring Systems, and Other Tutoring Systems – https://doi.org/10.1016/j.edurev.2010.05.002
