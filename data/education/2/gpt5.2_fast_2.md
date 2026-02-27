# Interface Design, Accountability, and Teachers’ Responsible Use of AI in Student Assessment: An Empirical 2×2 Factorial Study

## Abstract

As artificial intelligence (AI) tools become increasingly integrated into educational assessment, concerns have emerged regarding teachers’ overreliance on algorithmic recommendations and susceptibility to automation bias. This study investigates how interface design and accountability strategies influence teachers’ responsible use of AI-supported assessment systems. We propose and empirically evaluate a 2×2 factorial experiment manipulating (1) the presence versus absence of AI confidence displays and (2) the presence versus absence of decision justification requirements. Using simulated student assessment tasks with systematically varied AI accuracy, we examine how these factors individually and jointly affect teachers’ judgment accuracy, calibration, and reliance patterns. The study’s results-oriented goal is to identify interface and accountability configurations that reduce inappropriate automation bias while preserving the benefits of AI decision support. The paper contributes a theoretically grounded experimental design, a detailed measurement strategy, and actionable implications for the design of responsible AI systems in educational assessment.

---

## 1. Introduction

### 1.1 AI in Educational Assessment

AI-based tools are increasingly used to support educational assessment tasks such as grading, formative feedback, and risk identification [1]. These systems promise efficiency, consistency, and scalability, particularly in contexts where teachers face growing workloads and large class sizes. However, the introduction of AI into assessment processes also raises critical concerns about professional judgment, fairness, and responsibility [2].

Unlike domains such as medicine or aviation, educational assessment involves interpretive judgment that is deeply contextual, value-laden, and consequential for students’ academic trajectories [3]. Teachers are not merely end-users of AI outputs; they remain ethically and professionally accountable for assessment decisions. This makes the responsible use of AI tools in education a central research and design challenge.

### 1.2 Automation Bias and Overreliance

A well-documented risk in human–AI interaction is **automation bias**, defined as the tendency for users to over-trust and follow automated recommendations, even when those recommendations are incorrect [4]. Automation bias has been observed across domains, including decision support systems, clinical diagnostics, and algorithmic forecasting [5].

In educational assessment, automation bias may manifest when teachers accept AI-generated grades, classifications, or risk flags without sufficient scrutiny. Such overreliance can amplify errors, obscure bias embedded in training data, and weaken teachers’ engagement with evidence [6]. Addressing automation bias is therefore essential for ensuring that AI systems support rather than undermine professional responsibility.

### 1.3 Interface Design and Accountability as Mitigation Strategies

Prior research suggests two broad classes of interventions for mitigating automation bias: **interface-level design features** and **organizational or procedural accountability mechanisms**.

Interface design features, such as confidence displays, explanations, or uncertainty visualizations, shape how users interpret and rely on AI outputs [7]. While confidence displays can help users calibrate trust, they may also increase overreliance if confidence is perceived as authority rather than uncertainty information [8].

Accountability strategies, such as requiring users to justify decisions or record rationales, have been shown to increase deliberation and reduce uncritical acceptance of automated advice [9]. In educational contexts, decision justification aligns with professional norms of reflective practice and documentation [10].

However, limited empirical work has examined how these two factors interact in teacher–AI assessment settings, particularly under conditions where AI recommendations vary in correctness.

### 1.4 Research Objectives

This study addresses this gap by proposing and empirically testing a 2×2 factorial design that manipulates:

1. **Interface feature**: AI confidence display (present vs. absent)
2. **Accountability strategy**: Decision justification requirement (present vs. absent)

The central objective is to determine how these factors influence teachers’ assessment decisions when AI recommendations are correct versus incorrect, and to identify configurations that best support responsible AI use.

---

## 2. Theoretical Background

### 2.1 Human–AI Trust and Calibration

Trust in AI systems is not inherently problematic; rather, **miscalibrated trust**—either overtrust or undertrust—is the primary concern [11]. Appropriate trust calibration occurs when users rely on AI when it is reliable and override it when it is not [12].

Interface cues such as confidence scores are often intended to support calibration by communicating system uncertainty. However, empirical findings are mixed. In some cases, confidence displays improve discrimination between reliable and unreliable outputs [13]; in others, they increase compliance regardless of accuracy [14].

### 2.2 Accountability and Decision-Making

Accountability theory posits that individuals who expect to justify their decisions engage in more systematic, effortful reasoning [15]. Decision justification requirements can shift users from heuristic to analytic processing, reducing susceptibility to biases [16].

In educational assessment, accountability is already embedded in practices such as rubric-based grading and moderation. Integrating justification requirements into AI-assisted assessment may therefore reinforce existing professional norms rather than impose external constraints [17].

### 2.3 Interaction Effects Between Interface and Accountability

Recent work in human–AI interaction suggests that interface features and accountability mechanisms may interact in non-additive ways [18]. For example, confidence displays may increase automation bias in low-accountability contexts but have neutral or positive effects when users are required to justify their decisions.

Understanding these interaction effects is essential for responsible AI design, as single-factor interventions may fail or backfire when deployed in isolation.

---

## 3. Research Questions and Hypotheses

### 3.1 Research Questions

* **RQ1**: How does the presence of an AI confidence display affect teachers’ reliance on AI recommendations in assessment tasks?
* **RQ2**: How does a decision justification requirement affect teachers’ assessment accuracy and resistance to automation bias?
* **RQ3**: How do interface design and accountability strategies interact under conditions of correct versus incorrect AI recommendations?

### 3.2 Hypotheses

* **H1**: AI confidence displays will increase reliance on AI recommendations, particularly when accountability is absent.
* **H2**: Decision justification requirements will reduce automation bias by increasing teachers’ likelihood of overriding incorrect AI recommendations.
* **H3**: The combination of confidence display and justification will yield better trust calibration than either feature alone.
* **H4**: Differences between conditions will be more pronounced when AI recommendations are incorrect than when they are correct.

---

## 4. Methodology

### 4.1 Experimental Design

The study employs a **2×2 between-subjects factorial design**:

| Interface Feature          | Accountability Strategy | Condition |
| -------------------------- | ----------------------- | --------- |
| Confidence Display Absent  | Justification Absent    | C1        |
| Confidence Display Present | Justification Absent    | C2        |
| Confidence Display Absent  | Justification Present   | C3        |
| Confidence Display Present | Justification Present   | C4        |

Participants are randomly assigned to one condition.

### 4.2 Participants

Participants are in-service secondary school teachers recruited through professional networks and online teacher communities. Eligibility criteria include at least two years of assessment experience and no prior exposure to the experimental system.

A target sample size of approximately 200 teachers (50 per condition) is selected to ensure adequate power for detecting medium-sized main and interaction effects [19].

### 4.3 Assessment Task and AI System

Participants complete a series of simulated student assessment tasks involving short written responses. For each task:

* Teachers review a student response.
* An AI system provides a recommended grade and brief rationale.
* In confidence-display conditions, the AI also provides a numerical confidence score.

AI recommendations are experimentally manipulated to be **correct** or **incorrect** relative to an expert-validated benchmark, with accuracy balanced across tasks.

### 4.4 Accountability Manipulation

In justification-present conditions, teachers must provide a brief written justification for their final assessment decision before proceeding. In justification-absent conditions, no such requirement is imposed.

---

## 5. Measurement Strategy

### 5.1 Dependent Variables

1. **Assessment Accuracy**: Whether the teacher’s final decision matches the expert benchmark.
2. **AI Reliance Rate**: Proportion of trials in which the teacher adopts the AI recommendation.
3. **Override Rate (Incorrect AI)**: Frequency of rejecting incorrect AI recommendations.
4. **Calibration Index**: Difference in reliance rates between correct and incorrect AI conditions.
5. **Decision Time**: Time spent per assessment task.

### 5.2 Automation Bias Operationalization

Automation bias is operationalized as **acceptance of incorrect AI recommendations**, consistent with prior research [4][5]. Lower acceptance rates indicate more responsible AI use.

### 5.3 Statistical Analysis Plan

Analyses include:

* Two-way ANOVAs for main and interaction effects.
* Mixed-effects logistic regression to model trial-level decisions.
* Planned contrasts comparing incorrect-AI trials across conditions.

---

## 6. Results-Oriented Goal Statement

The primary goal of this study is to **identify interface and accountability configurations that maximize teachers’ ability to appropriately rely on AI when it is correct and override it when it is incorrect**.

Specifically, the study seeks to determine whether:

* Confidence displays alone increase overreliance.
* Justification requirements alone reduce automation bias.
* The combination of confidence display and justification yields superior trust calibration and assessment accuracy.

The results will directly inform design guidelines for responsible AI-assisted assessment systems.

---

## 7. Discussion

### 7.1 Expected Findings and Interpretation

Based on prior literature, we expect that confidence displays without accountability will increase automation bias, particularly in incorrect-AI conditions [8][14]. Decision justification is expected to reduce this effect by promoting reflective evaluation [15].

The most responsible use pattern is hypothesized to emerge in the **confidence + justification** condition, where uncertainty information is available but filtered through accountable reasoning.

### 7.2 Implications for AI Design in Education

The findings will suggest that interface transparency alone is insufficient for responsible AI use. Instead, **design must integrate accountability mechanisms that align with professional norms**.

For educational technology developers, this implies embedding lightweight justification prompts and carefully framing confidence information as probabilistic rather than authoritative.

### 7.3 Limitations and Future Work

The study uses simulated tasks and short-term exposure. Longitudinal research is needed to examine learning effects and habitual reliance patterns [20]. Additionally, future work should explore other interface features such as explanations and counterfactuals.

---

## 8. Conclusion

This study advances empirical research on responsible AI use in education by systematically examining how interface design and accountability strategies shape teachers’ assessment decisions. Through a rigorous 2×2 factorial experiment, it provides evidence-based guidance for mitigating automation bias while preserving the benefits of AI support. The findings will contribute to both educational practice and the broader field of human-centered AI design.

---

## References
[1] Holmes, W., Bialik, M., & Fadel, C. (2019). Artificial Intelligence in Education: Promises and Implications for Teaching and Learning. https://curriculumredesign.org/wp-content/uploads/AIED-Book.pdf
[2] Williamson, B., & Eynon, R. (2020). Historical threads, missing links, and future directions in AI in education. Learning, Media and Technology. https://doi.org/10.1080/17439884.2020.1798995
[3] Brookhart, S. M. (2017). How to Use Grading to Improve Learning. https://www.ascd.org/books/how-to-use-grading-to-improve-learning
[4] Parasuraman, R., & Riley, V. (1997). Humans and automation: Use, misuse, disuse, abuse. Human Factors. https://doi.org/10.1518/001872097778543886
[5] Mosier, K. L., & Skitka, L. J. (1996). Human decision makers and automated decision aids. Human Factors. https://doi.org/10.1518/001872096778827116
[6] Araujo, T., Helberger, N., Kruikemeier, S., & de Vreese, C. (2020). In AI we trust? Communications of the ACM. https://doi.org/10.1145/3313126
[7] Kaur, H., et al. (2020). Interpreting interpretability. CHI 2020 Proceedings. https://doi.org/10.1145/3313831.3376219
[8] Zhang, Y., et al. (2020). Effect of confidence information on human-AI decision making. AAAI. https://ojs.aaai.org/index.php/AAAI/article/view/5633
[9] Lerner, J. S., & Tetlock, P. E. (1999). Accounting for the effects of accountability. Psychological Bulletin. https://doi.org/10.1037/0033-2909.125.2.255
[10] Black, P., & Wiliam, D. (2009). Developing the theory of formative assessment. Educational Assessment. https://doi.org/10.1080/10627190903043464
[11] Hoff, K. A., & Bashir, M. (2015). Trust in automation. Human Factors. https://doi.org/10.1177/0018720814547570
[12] Lee, J. D., & See, K. A. (2004). Trust in automation. Human Factors. https://doi.org/10.1518/hfes.46.1.50_30392
[13] van der Waa, J., et al. (2021). Trust and reliance in AI-assisted decision making. Human–Computer Interaction. https://doi.org/10.1080/07370024.2021.1902367
[14] Logg, J. M., Minson, J. A., & Moore, D. A. (2019). Algorithm appreciation. Management Science. https://doi.org/10.1287/mnsc.2018.3105
[15] Tetlock, P. E. (1985). Accountability: A social check on the fundamental attribution error. Social Psychology Quarterly. https://www.jstor.org/stable/3033833
[16] Simonson, I., & Nye, P. (1992). The effect of accountability on judgment. Organizational Behavior and Human Decision Processes. https://doi.org/10.1016/0749-5978(92)90002-8
[17] Klenowski, V. (2011). Assessment for learning in the accountability era. Assessment in Education. https://doi.org/10.1080/0969594X.2011.572680
[18] Buçinca, Z., Lin, P., Gajos, K. Z., & Glassman, E. L. (2021). Proxy tasks and trust. CHI 2021. https://doi.org/10.1145/3411764.3445215
[19] Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences. https://www.routledge.com/Statistical-Power-Analysis-for-the-Behavioral-Sciences/Cohen/p/book/9780805802832
[20] Dietvorst, B. J., Simmons, J. P., & Massey, C. (2015). Algorithm aversion. Journal of Experimental Psychology. https://doi.org/10.1037/xge0000033
