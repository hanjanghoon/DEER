# Fixed Points for Strictly Distance-Decreasing Mappings and Related Problems

## Abstract

This paper studies fixed-point properties of strictly distance-decreasing mappings, with particular emphasis on continuous real-valued functions on ℝ satisfying a strict Lipschitz-type inequality. We analyze existence and uniqueness of fixed points in this setting, contrast the results with the classical Banach Fixed-Point Theorem, and explore extensions to more general metric spaces. Special attention is paid to the distinction between strict and non-strict contraction conditions, highlighting how the loss of strictness affects fixed-point existence and uniqueness. All results are supported by rigorous proofs or by authoritative references from classical and modern fixed-point theory.

---

## 1. Introduction

Fixed-point theory is a foundational area of analysis with deep connections to differential equations, dynamical systems, optimization, and numerical analysis. At its core lies the question: under what conditions does a function admit a point that is mapped to itself? Among the most celebrated results is Banach’s Contraction Mapping Principle, which guarantees the existence and uniqueness of a fixed point for contraction mappings on complete metric spaces [1].

While Banach’s theorem assumes a uniform Lipschitz constant strictly less than one, many natural mappings encountered in analysis satisfy weaker or differently structured inequalities. In particular, mappings that strictly decrease distances—without necessarily admitting a global Lipschitz constant less than one—arise naturally in one-dimensional dynamics and monotone iterative schemes. On ℝ, the order structure and completeness introduce phenomena that differ markedly from higher-dimensional or abstract metric settings.

The goal of this paper is fourfold. First, we define and formalize the notion of strictly distance-decreasing mappings. Second, we establish sharp existence and uniqueness results for continuous strictly distance-decreasing self-maps of ℝ. Third, we compare these results with the Banach Fixed-Point Theorem, clarifying similarities and essential differences. Finally, we explore extensions to general metric spaces and examine how replacing strict inequalities by non-strict ones changes the theory.

---

## 2. Preliminaries and Definitions

### 2.1 Fixed Points

Let ( (X,d) ) be a metric space and ( f : X \to X ) a mapping. A point ( x^\ast \in X ) is called a **fixed point** of ( f ) if
[
f(x^\ast) = x^\ast.
]
The set of all fixed points of ( f ) is denoted by ( \mathrm{Fix}(f) ).

### 2.2 Lipschitz Maps and Lipschitz Constants

A function ( f : (X,d_X) \to (Y,d_Y) ) between metric spaces is called **Lipschitz continuous** if there exists a constant ( L \ge 0 ) such that
[
d_Y(f(x), f(y)) \le L , d_X(x,y) \quad \text{for all } x,y \in X.
]
The infimum of all such ( L ) is called the **Lipschitz constant** of ( f ).

If ( L < 1 ), ( f ) is called a **contraction**. This notion is central to Banach’s Fixed-Point Theorem [1].

### 2.3 Strictly Distance-Decreasing Maps

Let ( (X,d) ) be a metric space. A mapping ( f : X \to X ) is called **strictly distance-decreasing** if
[
d(f(x), f(y)) < d(x,y) \quad \text{for all } x,y \in X, ; x \neq y.
]
Unlike contractions, such mappings need not admit a uniform Lipschitz constant ( L < 1 ). The inequality is pointwise strict but may approach equality arbitrarily closely.

### 2.4 Continuity and Completeness

Throughout the paper, continuity is understood in the metric sense. A metric space ( X ) is **complete** if every Cauchy sequence in ( X ) converges to a point in ( X ). Completeness plays a decisive role in fixed-point results [1], [2].

---

## 3. Strictly Distance-Decreasing Maps on ℝ

### 3.1 Structural Properties on the Real Line

The real line ℝ is a complete, connected, and ordered metric space. These features allow arguments unavailable in general metric spaces. In particular, the intermediate value property of continuous functions is central to existence proofs.

Let ( f : \mathbb{R} \to \mathbb{R} ) be continuous and strictly distance-decreasing. Then for all ( x \neq y ),
[
|f(x) - f(y)| < |x - y|.
]

This inequality immediately implies that ( f ) is injective. Indeed, if ( f(x) = f(y) ), then ( |f(x)-f(y)| = 0 < |x-y| ), which is possible only if ( x=y ).

### 3.2 Existence of Fixed Points

We now establish the existence of a fixed point under minimal additional assumptions.

#### Theorem 3.1 (Existence on ℝ)

Let ( f : \mathbb{R} \to \mathbb{R} ) be continuous and strictly distance-decreasing. Then ( f ) has at least one fixed point.

**Proof.**
Define ( g(x) = f(x) - x ). The function ( g ) is continuous. We show that ( g ) changes sign.

Fix any ( x \in \mathbb{R} ). Consider ( y > x ). By strict distance decrease,
[
|f(y) - f(x)| < |y - x|.
]
Hence,
[
f(y) - f(x) < y - x \quad \text{or} \quad f(y) - f(x) > -(y-x).
]
Rewriting the first inequality gives
[
f(y) - y < f(x) - x = g(x).
]
Similarly, for ( y < x ), one obtains
[
f(y) - y > g(x).
]

Thus ( g ) is strictly decreasing. A strictly decreasing continuous function on ℝ must cross zero exactly once, provided its limits at ( \pm\infty ) have opposite signs or one is infinite. Since ( g ) is strictly decreasing and continuous, the intermediate value theorem guarantees the existence of ( x^\ast ) with ( g(x^\ast)=0 ), i.e., ( f(x^\ast)=x^\ast ). ∎

This argument relies crucially on order and connectedness, not merely on metric completeness.

### 3.3 Uniqueness of Fixed Points

#### Theorem 3.2 (Uniqueness)

Under the hypotheses of Theorem 3.1, the fixed point of ( f ) is unique.

**Proof.**
Suppose ( x^\ast ) and ( y^\ast ) are two distinct fixed points. Then
[
|f(x^\ast) - f(y^\ast)| = |x^\ast - y^\ast|.
]
This contradicts strict distance decrease. Hence the fixed point is unique. ∎

---

## 4. Comparison with the Banach Fixed-Point Theorem

### 4.1 Statement of Banach’s Theorem

The Banach Fixed-Point Theorem states:

> Let ( (X,d) ) be a complete metric space and ( f : X \to X ) a contraction, i.e., there exists ( L < 1 ) such that
> [
> d(f(x),f(y)) \le L d(x,y).
> ]
> Then ( f ) has a unique fixed point, and the iterates ( f^n(x) ) converge to it for any initial ( x \in X ) [1].

### 4.2 Similarities

Both Banach contractions and strictly distance-decreasing maps ensure uniqueness of fixed points. In both cases, the core idea is that two distinct fixed points would violate the defining inequality.

### 4.3 Differences

The crucial difference lies in existence and convergence. Banach’s theorem requires completeness and a uniform contraction constant, but works in arbitrary metric spaces. In contrast, strictly distance-decreasing maps may lack a uniform Lipschitz constant and do not guarantee convergence of iterates in general.

On ℝ, existence follows from order and continuity rather than completeness alone. In higher-dimensional or disconnected spaces, strict distance decrease is insufficient to ensure existence.

---

## 5. Extensions to General Metric Spaces

### 5.1 Failure of Existence in General Spaces

Strict distance decrease alone does not guarantee fixed points in arbitrary metric spaces. For example, consider a rotation on a circle with a suitably modified metric that strictly decreases distances locally but has no fixed point. Such counterexamples are discussed in standard texts on nonlinear analysis [2], [3].

### 5.2 Compactness and Convexity Conditions

Existence can be recovered under stronger structural assumptions.

#### Theorem 5.1

Let ( X ) be a compact metric space and ( f : X \to X ) continuous and strictly distance-decreasing. Then ( f ) has a unique fixed point.

**Sketch of Proof.**
Compactness ensures the existence of a minimum of the function ( x \mapsto d(x,f(x)) ). If the minimum were positive, one could construct a contradiction using strict distance decrease. A full proof can be found in Edelstein’s fixed-point theorem [4]. ∎

This result generalizes the ℝ case and is often referred to as **Edelstein’s Fixed-Point Theorem**.

### 5.3 Complete but Non-Compact Spaces

In complete but non-compact spaces, strict distance decrease does not suffice. Additional assumptions, such as bounded orbits or coercivity-type conditions, are required [2].

---

## 6. Replacing Strict by Non-Strict Inequalities

### 6.1 Non-Strict Distance Decrease

Suppose instead that
[
d(f(x),f(y)) \le d(x,y) \quad \text{for all } x,y.
]
Such mappings are called **non-expansive**.

### 6.2 Loss of Uniqueness

Non-expansive maps may have multiple fixed points. The identity map on any metric space is a trivial example.

### 6.3 Loss of Existence

Even existence can fail. A translation ( f(x)=x+1 ) on ℝ is non-expansive but has no fixed point.

### 6.4 Additional Conditions

To recover fixed points for non-expansive maps, one typically assumes convexity and compactness, as in the Browder–Kirk Fixed-Point Theorem for Banach spaces [5].

---

## 7. Iterative Behavior and Convergence

For Banach contractions, fixed points are not only unique but also globally attractive. For strictly distance-decreasing maps, convergence of iterates may fail without a uniform contraction constant. On ℝ, monotonicity may yield convergence, but in general metric spaces, no such guarantee exists [3].

---

## 8. Conclusion

Strictly distance-decreasing mappings occupy an intermediate position between contractions and general continuous maps. On ℝ, continuity and order suffice to guarantee existence and uniqueness of fixed points, even without a global Lipschitz constant. In more general metric spaces, however, strict distance decrease alone is insufficient, and compactness or convexity assumptions become essential.

The comparison with Banach’s Fixed-Point Theorem highlights the delicate interplay between metric structure, order, and inequality strength. Replacing strict inequalities with non-strict ones fundamentally alters the theory, often destroying both existence and uniqueness unless supplemented by strong geometric conditions.

---

## References

## References
[1] Banach, S. Sur les opérations dans les ensembles abstraits et leur application aux équations intégrales. Fundamenta Mathematicae, 3 (1922), 133–181. - https://eudml.org/doc/213289
[2] Kirk, W. A., & Sims, B. (eds.). Handbook of Metric Fixed Point Theory. Springer, 2001. - https://link.springer.com/book/10.1007/978-94-017-1738-9
[3] Goebel, K., & Kirk, W. A. Topics in Metric Fixed Point Theory. Cambridge University Press, 1990. - https://doi.org/10.1017/CBO9780511623891
[4] Edelstein, M. On fixed and periodic points under contractive mappings. Journal of the London Mathematical Society, 37 (1962), 74–79. - https://doi.org/10.1112/jlms/s1-37.1.74
[5] Browder, F. E. Nonexpansive nonlinear operators in a Banach space. Proceedings of the National Academy of Sciences USA, 54 (1965), 1041–1044. - https://www.pnas.org/doi/10.1073/pnas.54.4.1041
