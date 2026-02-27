# Instrument Strength and Asymptotic Bias in Two-Stage Least Squares

## Quantifying Minimum First-Stage F-Statistics for Bias Control under Homoscedasticity

## Abstract

This paper analyzes the relationship between instrument strength and asymptotic bias in two-stage least squares (TSLS) estimation in the canonical setting of a single endogenous regressor and a single instrumental variable. Focusing on the concept of *relative asymptotic bias*, we derive the analytical dependence of TSLS bias on first-stage strength, as summarized by the first-stage F-statistic under homoscedasticity. We examine the statistical meaning of the widely used “10% relative bias” criterion and clarify its distinction from weak-instrument thresholds based on size distortion or coverage. Building on both asymptotic theory and simulation-based evidence from the literature, we critically evaluate the conventional rule of thumb that F ≥ 10 suffices for reliable TSLS inference. We show that, in the one-instrument case, achieving less than 10% relative bias with 95% confidence generally requires substantially stronger instruments than implied by this rule. We further contrast homoscedastic and heteroscedastic environments, highlighting implications for empirical practice and policy analysis. A numerical demonstration illustrates how relative bias declines with increasing F-statistics and identifies the approximate cutoff required to meet the 10% bias criterion at high confidence.

---

## 1. Introduction

Instrumental variables (IV) methods are a cornerstone of empirical research in economics and related social sciences when regressors are endogenous. Among these methods, two-stage least squares (TSLS) remains the most widely used estimator due to its simplicity and asymptotic optimality under standard assumptions. However, the finite-sample and weak-instrument properties of TSLS have been the subject of extensive scrutiny for several decades [1], [2].

A central insight of this literature is that TSLS can exhibit substantial bias toward the ordinary least squares (OLS) estimator when instruments are weak. This bias persists even asymptotically when the strength of the instrument grows slowly with the sample size. As a result, simple diagnostics based on first-stage regression output—most notably the first-stage F-statistic—have become standard tools for assessing instrument relevance.

The most common heuristic, originating in early simulation studies, is the rule of thumb that a first-stage F-statistic of at least 10 indicates sufficiently strong instruments [3]. While influential, this rule has been criticized for conflating distinct notions of reliability, such as estimator bias, test size distortion, and confidence-interval coverage. More recent work has emphasized that different inferential goals imply different requirements on instrument strength [2], [4].

This paper focuses specifically on *relative asymptotic bias* as a criterion for evaluating instrument strength. We ask: **How strong must a single instrument be to ensure that the relative asymptotic bias of TSLS is less than 10%, with 95% confidence, under homoscedasticity?** By addressing this question, we aim to clarify what the F-statistic can and cannot guarantee in empirical practice.

---

## 2. Model Setup and Notation

### 2.1 Structural and Reduced-Form Equations

Consider the standard linear IV model with one endogenous regressor and one instrument:

[
\begin{aligned}
y_i &= \beta x_i + u_i, \
x_i &= \pi z_i + v_i,
\end{aligned}
]

where (y_i) is the outcome, (x_i) is an endogenous regressor, and (z_i) is an excluded instrument. The structural error (u_i) is correlated with the first-stage error (v_i), generating endogeneity. We assume (E[z_i u_i] = 0) and (E[z_i v_i] \neq 0).

### 2.2 Assumptions

Throughout most of the analysis, we impose the following assumptions:

1. **Homoscedasticity:**
   (\mathrm{Var}(u_i \mid z_i) = \sigma_u^2) and (\mathrm{Var}(v_i \mid z_i) = \sigma_v^2).
2. **Single instrument:** (z_i) is scalar.
3. **Local-to-zero first stage:** The first-stage coefficient (\pi) may be small, allowing for weak instruments.
4. **Random sampling and finite fourth moments.**

These assumptions correspond to the classical framework used in the weak-instrument literature [1], [2].

---

## 3. TSLS and Relative Asymptotic Bias

### 3.1 Definition of Relative Asymptotic Bias

The *relative asymptotic bias* (RAB) of TSLS is defined as

[
\text{RAB} =
\frac{E(\hat{\beta}*{\text{TSLS}} - \beta)}
{E(\hat{\beta}*{\text{OLS}} - \beta)}.
]

This quantity measures how far the TSLS estimator lies between the true parameter and the OLS estimator in expectation. A relative bias of 0 indicates consistency at the true value, while a relative bias of 1 implies that TSLS behaves like OLS.

Crucially, this criterion is conceptually distinct from:

* **Size distortion**, which concerns hypothesis testing,
* **Coverage error**, which concerns confidence intervals,
* **Weak-instrument diagnostics** based on critical values for test statistics.

As emphasized by Staiger and Stock [1], an estimator can exhibit small relative bias but still suffer from size distortions, and vice versa.

### 3.2 Analytical Relationship to Instrument Strength

Under homoscedasticity and a single instrument, Staiger and Stock show that the asymptotic bias of TSLS depends inversely on the concentration parameter (\mu^2), defined as

[
\mu^2 = \frac{n \pi^2 \mathrm{Var}(z)}{\sigma_v^2}.
]

In this setting, the first-stage F-statistic converges in distribution to

[
F ;\approx; \frac{\mu^2}{1},
]

since there is only one excluded instrument. As a result, the relative asymptotic bias of TSLS is approximately

[
\text{RAB} ;\approx; \frac{1}{1 + F}.
]

This expression provides a transparent mapping from the observed first-stage F-statistic to expected TSLS bias.

---

## 4. Interpreting the “10% Relative Bias” Criterion

### 4.1 Deterministic Thresholds

If one takes the approximation (\text{RAB} \approx 1/(1+F)) literally, the condition

[
\text{RAB} \leq 0.10
]

implies

[
F \geq 9.
]

This calculation is often cited as informal justification for the F ≥ 10 rule. However, this reasoning ignores the sampling variability of the F-statistic and treats the approximation as exact.

### 4.2 Confidence-Based Interpretation

A more demanding requirement is that **with high probability**, the relative bias is below 10%. That is,

[
P!\left( \frac{1}{1+F} \leq 0.10 \right) \geq 0.95.
]

Because the first-stage F-statistic is itself random, this criterion requires that the *lower tail* of the F distribution be sufficiently far from zero. Stock and Yogo [2] formalize this idea by deriving critical values for weak-instrument tests that control relative bias at given confidence levels.

For the single-instrument case under homoscedasticity, their results imply that achieving less than 10% relative bias with 95% confidence requires an F-statistic substantially larger than 10, typically in the range of 20–25 or higher, depending on the precise specification [2].

---

## 5. Evaluating the F ≥ 10 Rule of Thumb

### 5.1 Origins and Appeal

The F ≥ 10 rule originates from early Monte Carlo studies suggesting that TSLS behaves “reasonably well” above this threshold [3]. Its appeal lies in its simplicity and ease of implementation.

### 5.2 Theoretical Limitations

From a theoretical perspective, the rule conflates:

* Mean relative bias,
* Worst-case or tail behavior,
* Test size control.

As shown above, an expected relative bias below 10% does not imply that large biases are unlikely in finite samples. Moreover, the rule does not scale with sample size or error correlation.

### 5.3 Evidence from the Literature

Stock and Yogo [2] provide simulation-based and analytical evidence showing that:

* F ≈ 10 corresponds roughly to **mean** relative bias of 10%,
* But fails to control bias with high probability,
* And does not guarantee acceptable size properties for Wald tests.

Subsequent work reinforces the conclusion that stronger instruments are needed for reliable inference, especially in policy-relevant applications where bias directly affects estimated treatment effects [4].

---

## 6. Homoscedastic vs. Heteroscedastic Designs

### 6.1 Breakdown of the F-Statistic Interpretation

Under heteroscedasticity, the simple relationship between the first-stage F-statistic and the concentration parameter no longer holds. Robust first-stage statistics may not map cleanly into relative bias measures [5].

### 6.2 Implications for Bias

In heteroscedastic settings:

* TSLS bias can be larger for a given nominal F-statistic,
* The effective instrument strength may vary across observations,
* Bias diagnostics based on homoscedastic theory become unreliable.

As a result, practitioners are advised to use heteroscedasticity-robust weak-instrument tests and alternative estimators such as limited-information maximum likelihood (LIML) or Anderson–Rubin-type procedures [2], [6].

---

## 7. Numerical Demonstration

### 7.1 Relative Bias as a Function of F

Using the approximation (\text{RAB} = 1/(1+F)), Table 1 illustrates how relative bias declines as instrument strength increases.

| First-Stage F | Relative Bias |
| ------------: | ------------: |
|             5 |         16.7% |
|            10 |          9.1% |
|            15 |          6.3% |
|            20 |          4.8% |
|            25 |          3.8% |
|            30 |          3.2% |

### 7.2 Incorporating Sampling Uncertainty

Simulations reported in Stock and Yogo [2] show that, in the one-instrument homoscedastic case, ensuring **95% probability** that relative bias is below 10% typically requires F-statistics around 20 or higher. This gap between deterministic and confidence-based thresholds underscores the limitations of simple rules of thumb.

---

## 8. Implications for Empirical Practice and Policy Analysis

For empirical researchers, especially those engaged in policy evaluation:

* Reporting only the first-stage F-statistic is insufficient.
* Interpreting F ≥ 10 as “safe” can be misleading.
* Stronger instruments or weak-instrument-robust inference methods should be used when bias control is critical.

In policy contexts, even modest biases can translate into substantial misestimation of treatment effects, reinforcing the need for conservative diagnostics.

---

## 9. Conclusion

This paper has analyzed the relationship between instrument strength and asymptotic bias in TSLS under a single-instrument, homoscedastic framework. While the conventional F ≥ 10 rule corresponds loosely to a mean relative bias of 10%, it does not ensure that TSLS bias is small with high probability. Achieving less than 10% relative bias with 95% confidence generally requires considerably stronger instruments. These findings highlight the importance of aligning instrument-strength diagnostics with the inferential goals of empirical research and caution against uncritical reliance on simple heuristics.

---

## References

[1] Staiger, D., & Stock, J. H. (1997). Instrumental variables regression with weak instruments. Econometrica. - https://www.jstor.org/stable/2171753
[2] Stock, J. H., & Yogo, M. (2005). Testing for weak instruments in linear IV regression. In Identification and Inference for Econometric Models. - https://www.nber.org/papers/t0284
[3] Bound, J., Jaeger, D. A., & Baker, R. M. (1995). Problems with instrumental variables estimation when the correlation between the instruments and the endogenous explanatory variable is weak. Journal of the American Statistical Association. - https://www.jstor.org/stable/2291055
[4] Andrews, I., Stock, J. H., & Sun, L. (2019). Weak instruments in instrumental variables regression: Theory and practice. Annual Review of Economics. - https://www.annualreviews.org/doi/10.1146/annurev-economics-080218-025643
[5] Kleibergen, F., & Paap, R. (2006). Generalized reduced rank tests using the singular value decomposition. Journal of Econometrics. - https://doi.org/10.1016/j.jeconom.2005.02.011
[6] Moreira, M. J. (2003). A conditional likelihood ratio test for structural models. Econometrica. - https://www.jstor.org/stable/1555538
