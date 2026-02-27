# Relaxed Simulation Induced by Component-Wise Abstraction over Finite Product State Spaces

## Abstract

Component-wise (Cartesian) abstraction is one of the most widely used approximation techniques in program analysis, model checking, and symbolic verification. By decomposing a structured state space into independent coordinate domains and recomposing them via a Cartesian product, one obtains scalable but imprecise approximations of system behavior. This paper studies a specific operational semantics induced by such abstractions, which we call *relaxed simulation*. Relaxed simulation over-approximates concrete trajectories by iteratively collecting component-level information and recombining it into sets of possible states.

We present a detailed and self-contained analysis of the computational and semantic properties of relaxed simulation over finite product state spaces. Using a precise formal scenario as a running case study, we analyze soundness, precision loss, worst-case complexity, and the central role of locality and independence assumptions. We further examine algorithmic mitigation strategies that partially recover precision while preserving tractability, with a detailed discussion of their assumptions, trade-offs, and limitations. The results place relaxed simulation within the broader theory of abstract interpretation and simulation relations, clarifying both its power and its fundamental limits.

---

## 1. Introduction

State-space explosion is a central obstacle in the analysis of complex dynamical systems, programs, and transition systems. When a system state consists of many interacting components, the concrete state space typically grows exponentially in the number of components. Component-wise abstraction—also known as Cartesian abstraction or independent attribute abstraction—addresses this problem by projecting global states onto individual coordinates and reasoning about each coordinate independently.

Such abstractions are ubiquitous. They appear in abstract interpretation of programs, where variable domains are approximated independently [1]; in symbolic model checking, where Boolean variables are abstracted without relational constraints [2]; and in planning and AI, where relaxed planning graphs ignore negative interactions between actions [3]. Despite their prevalence, the semantic consequences of these abstractions are often only partially articulated.

This paper focuses on a particular operational semantics induced by Cartesian abstraction, which we call *relaxed simulation*. Informally, relaxed simulation proceeds as follows: starting from a concrete initial state, we extract its component values, then repeatedly apply the concrete transition function to all states consistent with the accumulated component information, collecting new component values as they arise. This process monotonically grows a set of possible component values, thereby defining an over-approximation of all reachable states.

The goal of this paper is to provide a rigorous and comprehensive analysis of relaxed simulation in a finite setting. We aim to answer the following questions:

* **Soundness:** In what sense does relaxed simulation over-approximate concrete behavior?
* **Precision:** What information is lost, and why is this loss intrinsic?
* **Complexity:** How does the abstraction affect computational complexity?
* **Locality:** How do independence and interaction between components influence accuracy?
* **Mitigation:** What algorithmic strategies can improve precision, and at what cost?

To ground the discussion, we adopt a precise formal scenario based on finite product state spaces and deterministic transition maps. This scenario is sufficiently simple to allow formal analysis, yet expressive enough to capture the essential phenomena observed in practice.

---

## 2. Formal Scenario and Definitions

### 2.1 Concrete State Space

Let ( V_1, \dots, V_n ) be pairwise-disjoint finite sets. Each ( V_k ) represents the domain of a component or coordinate. The concrete state space is the Cartesian product

[
\mathbb{S} = V_1 \times \cdots \times V_n.
]

An element ( s \in \mathbb{S} ) is written as ( s = (s_1, \dots, s_n) ), where ( s_k \in V_k ).

We consider a deterministic transition map

[
f : \mathbb{S} \to \mathbb{S}.
]

Given an initial state ( s_0 \in \mathbb{S} ), the concrete trajectory is defined by ordinary iteration:

[
s_{i+1} = f(s_i).
]

Because ( \mathbb{S} ) is finite, trajectories are ultimately periodic.

---

### 2.2 Union Domain and Component Extraction

Define the *union domain*

[
\mathbb{D} = \bigcup_{k=1}^n V_k.
]

We define a decomposition operator

[
\mathscr{D} : 2^{\mathbb{S}} \to 2^{\mathbb{D}},
]

which extracts component values from a set of states. For a singleton state ( s = (s_1,\dots,s_n) ),

[
\mathscr{D}({s}) = {s_1, \dots, s_n}.
]

For a general set ( S \subseteq \mathbb{S} ), ( \mathscr{D}(S) ) is the union of component values appearing in any state in ( S ). Intuitively, ( \mathscr{D} ) forgets correlations between components.

---

### 2.3 Recomposition Operator

We define a recomposition operator

[
\mathscr{C} : 2^{\mathbb{D}} \to 2^{\mathbb{S}},
]

according to the following rules:

1. **Fill missing coordinates:**
   If a coordinate ( k ) has no element of ( V_k ) in the set ( \sigma \subseteq \mathbb{D} ), then all values in ( V_k ) are allowed.

2. **Branch on multi-valued coordinates:**
   If ( \sigma \cap V_k ) contains multiple values, then each is treated as a possible value of coordinate ( k ).

3. **Unique product:**
   If for every coordinate ( k ), ( \sigma \cap V_k ) is a singleton ( {v_k} ), then
   [
   \mathscr{C}(\sigma) = {(v_1,\dots,v_n)}.
   ]

Formally,

[
\mathscr{C}(\sigma) = \prod_{k=1}^n W_k,
]

where

[
W_k =
\begin{cases}
\sigma \cap V_k, & \text{if } \sigma \cap V_k \neq \emptyset, \
V_k, & \text{otherwise}.
\end{cases}
]

---

### 2.4 Relaxed Iteration

We define the relaxed simulation sequence ( (\sigma_i)_{i \ge 0} \subseteq 2^{\mathbb{D}} ) as follows:

[
\sigma_0 = \mathscr{D}({s_0}),
]

[
\sigma_{i+1} = \sigma_i ;\cup; \bigcup_{s \in \mathscr{C}(\sigma_i)} \mathscr{D}({f(s)}).
]

This iteration monotonically accumulates component values that can appear in any state consistent with previously observed component values.

---

## 3. Semantic Interpretation: Relaxed Simulation

### 3.1 Simulation versus Relaxed Simulation

In classical transition-system theory, a *simulation relation* preserves step-by-step behavior between systems [4]. Relaxed simulation departs from this notion: it does not track states, but rather component-level possibilities. The abstraction breaks the one-to-one correspondence between concrete trajectories and abstract trajectories.

Relaxed simulation can be viewed as an abstract semantics in the sense of abstract interpretation [1]. The abstract domain is ( 2^{\mathbb{D}} ), ordered by set inclusion, and the abstract transition is induced by the recomposition–transition–decomposition pipeline.

---

### 3.2 Soundness

**Proposition 1 (Soundness).**
For all ( i \ge 0 ), and for all concrete states ( s_i ) reachable after ( i ) concrete steps,
[
\mathscr{D}({s_i}) \subseteq \sigma_i.
]

*Sketch.* The proof is by induction on ( i ). The base case holds by definition of ( \sigma_0 ). For the inductive step, note that ( s_i \in \mathscr{C}(\sigma_{i-1}) ) by the inductive hypothesis, hence ( \mathscr{D}(f(s_i)) \subseteq \sigma_i ).

Soundness means that relaxed simulation is a safe over-approximation of reachable component values. No concrete behavior is missed.

---

### 3.3 Semantic Meaning

The limit ( \sigma_\infty = \bigcup_i \sigma_i ) represents the set of all component values that can appear in *some* reachable concrete state, possibly at different times and under different correlations. Importantly, ( \mathscr{C}(\sigma_\infty) ) may contain states that are *never* reachable concretely.

---

## 4. Precision and Information Loss

### 4.1 Loss of Correlation

The primary source of imprecision is the loss of correlation between components. Once two values ( v \in V_i ) and ( w \in V_j ) appear independently, the abstraction assumes they may co-occur, even if no concrete state realizes that combination.

This phenomenon is well known in Cartesian abstractions [1,5].

---

### 4.2 Spurious States and Trajectories

A *spurious state* is a state in ( \mathscr{C}(\sigma_i) ) that is not reachable in the concrete system. Relaxed simulation may generate entire spurious trajectories, whose component values are individually feasible but globally inconsistent.

In the worst case, ( \mathscr{C}(\sigma_\infty) = \mathbb{S} ), even if the concrete reachable set is small.

---

### 4.3 Precision Characterization

Relaxed simulation is exact if and only if the transition function ( f ) is *component-wise independent*, i.e.,

[
f(s_1,\dots,s_n) = (f_1(s_1),\dots,f_n(s_n)).
]

In this case, no correlations exist to lose, and the abstraction is complete. Any deviation from this independence introduces potential imprecision.

---

## 5. Computational Complexity

### 5.1 State Explosion in Recomposition

Although ( \sigma_i \subseteq \mathbb{D} ) is polynomially bounded in size, ( \mathscr{C}(\sigma_i) ) can be exponentially large in ( n ). In the worst case,

[
|\mathscr{C}(\sigma_i)| = \prod_{k=1}^n |V_k|.
]

Thus, naïvely enumerating ( \mathscr{C}(\sigma_i) ) defeats the purpose of abstraction.

---

### 5.2 Iteration Bound

Because ( \mathbb{D} ) is finite, the sequence ( \sigma_i ) stabilizes in at most ( |\mathbb{D}| ) iterations. This guarantees termination but not efficiency.

---

### 5.3 Comparison with Concrete Simulation

Concrete simulation explores at most ( |\mathbb{S}| ) states. Relaxed simulation replaces this with potentially exponential recomposition at each step, but with polynomially bounded abstract state size. This trade-off mirrors classical results in abstract interpretation: cheaper storage, more expensive abstract transitions [1].

---

## 6. The Role of Locality

### 6.1 Local Transitions

If ( f ) updates each component based only on a small neighborhood of other components, then correlations are limited. Locality significantly improves the practical precision of relaxed simulation.

Such locality assumptions underpin many scalable analyses, including predicate abstraction with small predicate scopes [6].

---

### 6.2 Dependency Graphs

One can associate a dependency graph where an edge ( i \to j ) indicates that component ( j ) depends on component ( i ) in ( f ). Sparse dependency graphs correlate with higher precision.

---

## 7. Algorithmic Mitigation Strategies

### 7.1 Relational Refinement via Block Abstraction

**Idea.** Group strongly interacting components into blocks and apply Cartesian abstraction only between blocks, not within them.

---

### 7.2 Assumptions

* The dependency structure is known or can be inferred.
* Interactions within blocks are dense; across blocks are sparse.

---

### 7.3 Trade-offs

* **Precision:** Improves by preserving intra-block correlations.
* **Complexity:** Abstract domain grows exponentially in block size.
* **Scalability:** Requires careful block size selection.

This approach is standard in abstract interpretation under the name *reduced product* or *block abstraction* [1,7].

---

### 7.4 Limitations

* Worst-case complexity remains exponential.
* Incorrect block choices may yield little benefit.
* Dynamic interactions may violate static dependency assumptions.

---

## 8. Discussion and Broader Context

Relaxed simulation closely resembles *may-analysis* in program analysis and *relaxed planning graphs* in AI planning [3]. In all these settings, ignoring negative or relational constraints yields tractable but optimistic approximations.

From a semantic perspective, relaxed simulation computes a least fixed point in a coarse abstract domain. Its imprecision is not a flaw of implementation but a fundamental consequence of abstraction choice.

---

## 9. Conclusion

We have presented a detailed analysis of relaxed simulation induced by component-wise abstraction over finite product state spaces. The abstraction is sound, terminating, and often useful in practice, but inherently imprecise when components interact. Locality and independence play a decisive role in determining accuracy, while mitigation strategies such as block abstraction offer principled trade-offs.

Understanding these properties clarifies when relaxed simulation is appropriate and how it can be systematically improved, situating it firmly within the broader theory of abstract interpretation and simulation semantics.

---

## References

[1] Patrick Cousot and Radhia Cousot, Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints – https://doi.org/10.1145/512950.512973
[2] Edmund M. Clarke, Orna Grumberg, and Doron A. Peled, Model Checking – https://mitpress.mit.edu/9780262032704/model-checking/
[3] Jörg Hoffmann and Bernhard Nebel, The FF Planning System: Fast Plan Generation Through Heuristic Search – https://doi.org/10.1613/jair.855
[4] Robin Milner, Communication and Concurrency – https://www.cs.cornell.edu/home/halpern/courses/6150/book.pdf
[5] David Schmidt, Abstract Interpretation in the Operational Semantics Hierarchy – https://doi.org/10.1016/S1571-0661(05)80006-7
[6] Thomas Ball, Rupak Majumdar, Todd Millstein, and Sriram Rajamani, Automatic Predicate Abstraction of C Programs – https://doi.org/10.1145/872035.872049
[7] Roberto Giacobazzi and Francesco Ranzato, Reduced Products in Abstract Interpretation – https://doi.org/10.1016/S0304-3975(97)00074-9
