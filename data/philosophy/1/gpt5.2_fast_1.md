# Critical-Level Views and the Weak Non-Sadism Condition

## An Analysis of Arrhenius’s Sixth Impossibility Theorem in Population Ethics

---

## Abstract

Critical-level views occupy a central position in contemporary population ethics as attempts to avoid the Repugnant Conclusion while preserving intuitively attractive constraints on aggregation. However, Gustaf Arrhenius’s Sixth Impossibility Theorem demonstrates that no population axiology can simultaneously satisfy a set of seemingly weak and compelling conditions, including the **Weak Non-Sadism** condition. This paper analyzes in detail how **critical-level utilitarian and critical-level generalized axiologies** violate Weak Non-Sadism. I reconstruct the logical structure of the theorem, explain why the introduction of a positive critical level systematically generates non-sadistic failures, and assess whether this conflict reflects a deeper incoherence in critical-level axiology or a defensible trade-off rooted in substantive ethical commitments about lives barely worth living. I argue that the violation is not a mere artifact of aggregation rules but arises from deeper normative assumptions about the moral relevance of population size and threshold-relative value. The result exposes a fault line in population ethics between avoiding repugnance and respecting minimal non-sadistic dominance constraints.

---

# 1. Introduction

Population ethics concerns the evaluation and comparison of outcomes that differ in both **population size** and **individual well-being**. Unlike standard distributive ethics, population ethics must determine whether adding people with positive lives is morally good, neutral, or bad, and under what conditions. Since Derek Parfit’s formulation of the **Repugnant Conclusion**, population ethics has been dominated by attempts to reconcile intuitive judgments with formal consistency constraints [1].

Among the most influential responses are **critical-level views**, which modify total utilitarianism by introducing a critical threshold of well-being. Roughly, adding a person whose well-being is below this threshold decreases overall value, while adding a person above it increases value. These views are attractive because they avoid the Repugnant Conclusion while retaining a form of additive aggregation [2].

However, Gustaf Arrhenius’s impossibility theorems pose a severe challenge. His **Sixth Impossibility Theorem** shows that no population axiology can satisfy a collection of conditions that many regard as jointly compelling, including **Weak Pareto**, **Continuity**, **Independence**, **Non-Elitism**, and **Weak Non-Sadism** [3].

This paper focuses on the specific tension between **critical-level views** and **Weak Non-Sadism**. While critical-level axiologies are often presented as humane and non-sadistic, Arrhenius shows that they necessarily entail rankings where outcomes with *fewer but much worse-off people* are judged better than outcomes with *many people whose lives are all positive and decent*. This violates even the weak form of non-sadism.

The central questions of this paper are:

1. Why does introducing a positive critical level logically lead to violations of Weak Non-Sadism?
2. Does this violation indicate an internal inconsistency in critical-level axiology?
3. Or does it reflect a substantive ethical commitment about how we treat lives barely worth living?

---

# 2. Background: Population Axiology and Critical-Level Views

## 2.1 Population Axiology

A **population axiology** is a function that assigns values or rankings to possible populations, where populations are multisets of individuals with associated well-being levels [4]. Let a population ( P = { w_1, \dots, w_n } ), where ( w_i ) denotes the lifetime well-being of individual ( i ).

Axiologies differ in how they treat:

* Population size
* Zero or barely positive well-being
* Trade-offs between number and quality of lives

Total utilitarianism evaluates populations by summing well-being:
[
V(P) = \sum_{i=1}^n w_i
]
This view famously implies the Repugnant Conclusion: for any population of very happy people, there exists a much larger population of people with lives barely worth living that is better [1].

## 2.2 Critical-Level Utilitarianism

**Critical-Level Utilitarianism (CLU)** modifies total utilitarianism by introducing a critical level ( c ):
[
V(P) = \sum_{i=1}^n (w_i - c)
]
Adding a person increases value only if their well-being exceeds ( c ) [2].

Critical-level views aim to:

* Avoid the Repugnant Conclusion
* Preserve additive aggregation
* Capture intuitions about neutrality around existence

Generalized critical-level views allow non-linear transformations but preserve the idea of a positive threshold [5].

---

# 3. Arrhenius’s Sixth Impossibility Theorem

## 3.1 Structure of the Theorem

Arrhenius proves that no population axiology can satisfy the following conditions simultaneously [3]:

1. **Weak Pareto**: If everyone is better off in one population than another, it is better.
2. **Continuity**: Small changes in well-being cannot cause large jumps in value.
3. **Independence**: The ranking of two populations depends only on differences between them.
4. **Non-Elitism**: Value does not depend only on the best-off individuals.
5. **Weak Non-Sadism**: Roughly, outcomes with many people living good lives should not be worse than outcomes with fewer people living much worse lives.

The theorem does not rely on extreme or controversial axioms. Each condition is independently motivated and widely endorsed.

## 3.2 Weak Non-Sadism Explained

**Weak Non-Sadism** states that for sufficiently large numbers, a population of people with lives worth living should be better than a population of fewer people with much worse lives, even if those worse lives are still positive [3].

Formally, there exist well-being levels ( a > b > 0 ) such that for sufficiently large ( n ), a population of ( n ) people at level ( b ) is better than a population of ( m ) people at level ( a ), where ( m \ll n ).

The intuition is minimal: morality should not prefer *fewer people doing much better* to *vastly many people doing reasonably well* when no one is suffering.

---

# 4. How Critical-Level Views Violate Weak Non-Sadism

## 4.1 The Role of the Critical Level

Suppose a critical level ( c > 0 ). Consider two populations:

* **Population A**: ( m ) people with well-being ( a ), where ( a > c )
* **Population B**: ( n ) people with well-being ( b ), where ( 0 < b < c )

Under CLU:
[
V(A) = m(a - c)
]
[
V(B) = n(b - c)
]

Since ( b - c < 0 ), adding more people at level ( b ) makes the population worse. No matter how large ( n ) is, ( V(B) ) decreases without bound.

Thus, **Population A is always better than Population B**, even when ( n ) is enormous.

## 4.2 The Non-Sadistic Failure

This ranking directly violates Weak Non-Sadism. Population B consists entirely of people with positive lives, yet it is deemed worse than a population with far fewer people simply because their lives fall below an arbitrarily chosen threshold.

The violation does not depend on extreme assumptions. It follows structurally from the critical-level subtraction. As Arrhenius emphasizes, any axiology that assigns *negative marginal value* to lives below a positive threshold will generate such cases [3].

## 4.3 Generalized Critical-Level Views

One might hope that non-linear aggregation avoids the problem. However, Arrhenius shows that generalized critical-level views retain the same structural feature: a region of positive well-being where additional lives decrease value [5].

As long as:

* There exists a positive range of well-being where adding people worsens outcomes
* Aggregation is population-sensitive

Weak Non-Sadism fails.

---

# 5. Is the Violation Merely Technical?

## 5.1 Aggregation vs. Ethical Commitments

One response is to treat the violation as a technical artifact of aggregation rules. On this view, Weak Non-Sadism encodes an implicit totalist bias that critical-level theorists are free to reject.

However, this underestimates the depth of the conflict. Weak Non-Sadism does not require totalism; it only prohibits rankings that resemble sadistic preferences for fewer lives over many decent ones [6].

The violation arises not from additivity per se, but from the **normative claim that some positive lives are bad to add**.

## 5.2 Lives Barely Worth Living

Critical-level views are motivated by the intuition that some lives, while positive, do not make the world better when added. This reflects a commitment to **existential neutrality** or **threshold-relative value** [2].

But once such a threshold is introduced, it becomes inevitable that sufficiently many “sub-critical” lives collectively count as a moral disaster—even if no individual suffers.

The non-sadistic intuition, by contrast, treats the sheer number of decent lives as morally significant.

---

# 6. Deeper Inconsistency or Acceptable Trade-Off?

## 6.1 Inconsistency Worries

One might argue that critical-level views are internally unstable: they reject sadism at the individual level but generate it at the collective level.

However, the inconsistency is not formal. Critical-level axiologies are mathematically coherent and extensionally consistent.

The problem is **normative tension**, not logical contradiction.

## 6.2 Accepting the Trade-Off

Some philosophers argue that violating Weak Non-Sadism is a price worth paying to avoid the Repugnant Conclusion [7]. On this view, morality may legitimately regard vast populations of barely good lives as worse than smaller populations of very good lives.

This position treats non-sadism not as a foundational constraint, but as a defeasible intuition.

## 6.3 The Cost of Thresholds

The deeper lesson of Arrhenius’s theorem is that **any attempt to block repugnance via thresholds introduces counterintuitive dominance failures elsewhere**.

Critical-level views must choose:

* Reject Weak Non-Sadism
* Accept the Repugnant Conclusion
* Abandon other core axioms (e.g., continuity or independence)

There is no escape without revisionary commitments.

---

# 7. Conclusion

Arrhenius’s Sixth Impossibility Theorem reveals that critical-level views systematically violate Weak Non-Sadism due to their core commitment to a positive critical threshold. This violation is not a technical flaw but a direct consequence of treating some positive lives as negatively contributing to overall value.

The conflict exposes a fundamental tension in population ethics: between respecting minimal non-sadistic dominance principles and avoiding the Repugnant Conclusion. Critical-level axiologies resolve this tension by rejecting Weak Non-Sadism, thereby endorsing a controversial stance on the moral insignificance—or disvalue—of lives barely worth living.

Whether this is a fatal flaw or a defensible trade-off remains a substantive ethical question. What Arrhenius decisively shows is that population ethics cannot have everything at once.

---

## References

[1] Derek Parfit, Reasons and Persons – https://global.oup.com/academic/product/reasons-and-persons-9780198249085
[2] Torbjörn Tännsjö, Population Ethics: The Challenge of Future Generations – https://www.oxfordscholarship.com/view/10.1093/019924485X.001.0001
[3] Gustaf Arrhenius, “An Impossibility Theorem for Welfarist Axiologies” – https://www.stafforini.com/docs/Arrhenius%20-%20An%20Impossibility%20Theorem%20for%20Welfarist%20Axiologies.pdf
[4] Gustaf Arrhenius, Population Ethics: The Challenge of Future Generations – https://www.oxfordhandbooks.com/view/10.1093/oxfordhb/9780195374995.001.0001
[5] Wlodek Rabinowicz, “Critical-Level Utilitarianism” – https://doi.org/10.1093/analys/61.3.230
[6] Nils Holtug, “On the Value of Coming into Existence” – https://doi.org/10.1111/j.1468-5930.2001.tb00114.x
[7] John Rawls, A Theory of Justice (population ethics appendix discussions) – https://www.hup.harvard.edu/books/9780674017726
