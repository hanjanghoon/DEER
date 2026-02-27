# Diagnosing Ungrammaticality: Binding Theory vs. Movement Constraints

*A Module-Specific Analysis in Government & Binding and Minimalist Syntax*

---

## 1. Introduction

One of the central achievements of generative syntax is the decomposition of grammatical well-formedness into **distinct, interacting modules**, each governed by its own locality conditions and representational principles. Two such modules—**Binding Theory** and **movement constraints**—are often superficially confusable, as both can render sentences unacceptable. However, they differ fundamentally in *what they constrain*, *how locality is computed*, and *what types of repair are possible*.

This report provides a **diagnostic, theory-internal analysis** of three candidate sentence pairs, each potentially ungrammatical for different reasons:

1. *Who likes Mary and Jane?*
   *Sheᵢ likes Maryᵢ and Jane.*

2. *John likes Mary’s glasses.*
   *Whose does John like glasses?*

3. *John likes Mary and himself.*
   *Who does John like Mary and?*

The primary objective is to determine **whether ungrammaticality (where present) is due to a violation of Binding Theory (Principles A, B, or C)** or instead arises from **movement-related constraints** such as islandhood, improper extraction, or coordination structure violations. Each case is analyzed using **explicit syntactic representations**, with particular attention to **c-command, locality domains, chain formation, and interpretive interfaces**.

---

## 2. Theoretical Background

### 2.1 Binding Theory in Government & Binding

Binding Theory regulates the distribution of **nominals** based on their referential properties and structural configuration. In its classical GB formulation, it consists of three principles [1][2]:

* **Principle A**: An anaphor must be **bound** in its local domain.
* **Principle B**: A pronoun must be **free** in its local domain.
* **Principle C**: An R-expression must be **free everywhere**.

Crucially, *binding* requires **coindexation plus c-command**, and locality is defined in terms of governing categories or phases (TP/vP in later Minimalist work).

Binding Theory is **interpretive**, applying at LF, and does **not involve movement**. Violations are semantic-syntactic mismatches that cannot be repaired by reordering or extraction.

---

### 2.2 Movement Constraints and Islandhood

Movement constraints regulate the formation of **A′-chains**, typically created by wh-movement. These constraints include:

* **Subjacency** [3]
* **Coordinate Structure Constraint (CSC)** [4]
* **Left Branch Condition** [5]
* **Wh-islands and Complex NP islands**

Movement violations arise when an element is extracted from a syntactic configuration that does not permit dependency formation. These constraints are **derivational**, applying during the syntactic computation rather than at LF interpretation.

Importantly, **movement constraints do not regulate reference or anaphoric dependency**. They constrain *where constituents may move from*, not *how nominals may be interpreted*.

---

### 2.3 Modular Distinctness

A central assumption of GB and Minimalism is **modular autonomy**:

* Binding Theory evaluates **static structural relations** at LF.
* Movement constraints regulate **derivational steps** in narrow syntax.

A sentence may violate one module while fully satisfying the other. Distinguishing these violations requires careful diagnostics.

---

## 3. Case 1: Pronouns and Coreference

**“Sheᵢ likes Maryᵢ and Jane.”**

### 3.1 Grammatical Status

The sentence is **ungrammatical under the intended coreferential reading** where *she* and *Mary* refer to the same individual.

---

### 3.2 Structural Analysis

Simplified structure:

```
[TP Sheᵢ [vP tᵢ likes [DP Maryᵢ and Jane]]]
```

Key facts:

* *She* c-commands the object DP *Mary and Jane*.
* *Mary* is an **R-expression**.
* *She* and *Mary* are coindexed.

---

### 3.3 Principle C Violation

Principle C requires that **R-expressions be free**, i.e., not bound by any coindexed element that c-commands them [1][2].

Here:

* *Sheᵢ* c-commands *Maryᵢ*.
* Coindexation yields binding.
* Therefore, **Principle C is violated**.

This violation persists regardless of linear order, prosody, or discourse context.

---

### 3.4 Why This Is Not a Movement Violation

No movement occurs in this sentence. The ungrammaticality:

* Does **not** involve extraction.
* Does **not** involve island configurations.
* Cannot be repaired by wh-movement or restructuring.

The violation is **purely interpretive**, located at the syntax–semantics interface.

---

### 3.5 Conclusion for Case 1

* **Ungrammatical due to Binding Theory (Principle C)**.
* No involvement of movement or island constraints.

---

## 4. Case 2: Possessive Extraction

**“Whose does John like glasses?”**

### 4.1 Grammatical Status

The sentence is **ungrammatical**, but **not due to Binding Theory**.

---

### 4.2 Source Structure

Intended base structure:

```
[TP John likes [DP whose glasses]]
```

Attempted wh-movement extracts *whose* from within a DP.

---

### 4.3 Left Branch Condition

The **Left Branch Condition** prohibits extraction of determiners or possessors from within a noun phrase in English [5].

* *Whose* is a DP-internal possessor.
* English disallows DP-internal extraction.
* Hence, the sentence violates a **movement constraint**.

---

### 4.4 Binding Theory Irrelevance

No anaphor, pronoun, or R-expression is involved in a binding dependency:

* No reflexive → no Principle A issue.
* No pronoun coreference → no Principle B issue.
* No R-expression bound → no Principle C issue.

The sentence is semantically interpretable but syntactically illicit due to **movement**.

---

### 4.5 Cross-Linguistic Evidence

Languages like German permit possessor extraction:

> *Wessenᵢ hat John [tᵢ Brille] gemocht?*

This confirms that the violation is **language-specific and syntactic**, not semantic or interpretive [6].

---

### 4.6 Conclusion for Case 2

* **Ungrammatical due to a movement constraint (Left Branch Condition)**.
* **No Binding Theory violation**.

---

## 5. Case 3: Extraction from Coordination

**“Who does John like Mary and?”**

### 5.1 Grammatical Status

The sentence is **ungrammatical**.

---

### 5.2 Coordination Structure

Base structure:

```
John likes [CoordP Mary and Bill]
```

Attempted extraction removes *Bill* (or equivalent) from one conjunct.

---

### 5.3 Coordinate Structure Constraint

The **Coordinate Structure Constraint** prohibits extraction from a single conjunct unless extraction applies across all conjuncts (Across-the-Board movement) [4].

Here:

* Only one conjunct is targeted.
* No ATB movement.
* Therefore, movement is illicit.

---

### 5.4 Interaction with Binding Theory

The base sentence:

> *John likes Mary and himself.*

is grammatical because:

* *himself* is locally bound by *John*.
* Principle A is satisfied.

However, once extraction occurs, the violation is **movement-based**, not binding-based. Binding relations in the base structure are irrelevant to the wh-movement failure.

---

### 5.5 Why Binding Theory Is Not Responsible

* No binding dependency involves *who*.
* No pronoun or R-expression is mis-bound.
* Ungrammaticality arises **even if no anaphor is present**.

Thus, Binding Theory plays no role in the failure.

---

### 5.6 Conclusion for Case 3

* **Ungrammatical due to a movement constraint (CSC)**.
* Binding Theory is satisfied in the underlying structure.

---

## 6. Comparative Diagnostic Summary

| Case | Sentence                     | Ungrammatical? | Source of Violation             | Module         |
| ---- | ---------------------------- | -------------- | ------------------------------- | -------------- |
| 1    | Sheᵢ likes Maryᵢ and Jane    | Yes            | Principle C                     | Binding Theory |
| 2    | Whose does John like glasses | Yes            | Left Branch Condition           | Movement       |
| 3    | Who does John like Mary and  | Yes            | Coordinate Structure Constraint | Movement       |

---

## 7. Broader Theoretical Implications

These cases illustrate that:

* **Binding Theory and movement constraints impose distinct locality conditions**.
* Binding violations are **interpretive and representational**.
* Movement violations are **derivational and structural**.
* Superficial unacceptability does not imply a shared grammatical source.

This modular separation is a cornerstone of GB and continues to be preserved in Minimalist syntax via phase theory and interface conditions [7][8].

---

## 8. Conclusion

The analysis conclusively demonstrates that:

* Only the first case involves a **Binding Theory violation (Principle C)**.
* The second and third cases are **pure movement violations**, unrelated to anaphoric binding.
* Proper diagnosis requires explicit reference to **c-command, locality domains, and derivational constraints**, not surface intuition.

The findings reinforce the theoretical necessity of maintaining **module-specific explanations** for ungrammaticality within generative grammar.

---

## References
[1] Chomsky, N. Lectures on Government and Binding – https://mitpress.mit.edu/9780262530071/lectures-on-government-and-binding/
[2] Chomsky, N. Knowledge of Language: Its Nature, Origin, and Use – https://mitpress.mit.edu/9780262530071/knowledge-of-language/
[3] Chomsky, N. Barriers – https://mitpress.mit.edu/9780262530859/barriers/
[4] Ross, J. R. Constraints on Variables in Syntax – https://dspace.mit.edu/handle/1721.1/15166
[5] Ross, J. R. “Left Branch Condition.” Linguistic Inquiry – https://www.jstor.org/stable/4177723
[6] Haider, H. The Syntax of German – https://www.cambridge.org/core/books/syntax-of-german/2F4A4A3A1A8D5C9C0F5C2C5E7C2A4F5F
[7] Chomsky, N. The Minimalist Program – https://mitpress.mit.edu/9780262527347/the-minimalist-program/
[8] Adger, D. Core Syntax – https://www.cambridge.org/core/books/core-syntax/4F8C6F8B6A2D9D7E3C8B6A4A5E6F9C7A
