# The Parameterized Counting Complexity of

(#\mathsf{Sub}_{\mathcal{G}}(\mathcal{H}))
over Somewhere-Dense Host Classes

## Abstract

We investigate the parameterized counting problem (#\mathsf{Sub}*{\mathcal{G}}(\mathcal{H})), which asks to count the number of subgraphs of a host graph (G \in \mathcal{G}) that are isomorphic to a given pattern graph (H \in \mathcal{H}), parameterized by (|H|). We focus on the regime where (\mathcal{G}) is a subgraph-closed, somewhere-dense graph class that is not equal to the class of all graphs, and where (\mathcal{H}) is recursively enumerable. We present a complexity classification that delineates the boundary between fixed-parameter tractability and parameterized counting hardness, emphasizing how structural properties of both the host class and the pattern family interact. Our analysis situates (#\mathsf{Sub}*{\mathcal{G}}(\mathcal{H})) within the broader landscape of parameterized counting complexity, drawing connections to the theory of sparse and dense graph classes, homomorphism-based counting, and known dichotomy results. A mathematical outline supporting the classification is provided, along with an illustrative example that serves as a consistency check for the theory.

---

## 1. Introduction

Counting subgraph patterns is a central problem in theoretical computer science, with applications ranging from database query evaluation and network analysis to bioinformatics and graph mining. Given a host graph (G) and a smaller pattern graph (H), one seeks to count how many subgraphs of (G) are isomorphic to (H). When the pattern size (|H|) is treated as a parameter, this gives rise to a parameterized counting problem that generalizes classical decision problems such as (\mathsf{Subgraph\ Isomorphism}) and counting problems such as (#\mathsf{Clique}).

In full generality, the problem is computationally intractable: counting (k)-cliques is (#\mathsf{W[1]})-hard when parameterized by (k) [1]. However, substantial progress has been made in identifying graph classes and pattern restrictions under which counting becomes fixed-parameter tractable (FPT). In particular, the theory of sparse graph classes—especially nowhere-dense classes—has led to powerful meta-theorems showing tractability of first-order model checking and related counting problems [2,3].

This paper examines the complementary setting: host graph classes (\mathcal{G}) that are **somewhere dense** but still **subgraph-closed** and strictly smaller than the class of all graphs. Such classes occupy an intermediate position between sparse and fully general graphs. Typical examples include graphs excluding a fixed clique minor but allowing dense regions at bounded depth, or graph classes containing arbitrarily large complete graphs as shallow minors but not as subgraphs.

Our goal is to understand how this intermediate structural richness affects the parameterized counting problem

[
#\mathsf{Sub}_{\mathcal{G}}(\mathcal{H}):\quad
(G,H) \mapsto #{\text{subgraphs of } G \text{ isomorphic to } H},
]

parameterized by (|H|), where (G \in \mathcal{G}) and (H \in \mathcal{H}), with (\mathcal{H}) recursively enumerable.

---

## 2. Preliminaries and Definitions

### 2.1 Graphs and Subgraph Isomorphism

All graphs considered are finite, simple, and undirected. A graph (H) is a **subgraph** of a graph (G) if (V(H) \subseteq V(G)) and (E(H) \subseteq E(G)). Two graphs are **isomorphic** if there exists a bijection between their vertex sets preserving adjacency.

The subgraph counting problem asks for the number of vertex subsets (S \subseteq V(G)) such that the induced subgraph (G[S]) is isomorphic to (H). Throughout this paper, “subgraph” refers to not necessarily induced subgraphs unless explicitly stated.

### 2.2 Parameterized Counting Complexity

A parameterized counting problem is said to be **fixed-parameter tractable (FPT)** if it can be solved in time (f(k)\cdot |x|^{O(1)}), where (k) is the parameter and (x) is the input instance. The class (#\mathsf{W[1]}) captures parameterized counting problems believed not to admit such algorithms, with (#\mathsf{Clique}) as a canonical complete problem [1].

### 2.3 Somewhere-Dense Graph Classes

A class of graphs (\mathcal{G}) is **nowhere dense** if, informally, it does not contain arbitrarily large complete graphs as shallow minors [2]. A class is **somewhere dense** if it fails this condition, i.e., there exists a fixed radius (r) such that for every (t), the (t)-clique appears as an (r)-shallow minor in some graph of the class [3].

We assume throughout that:

* (\mathcal{G}) is subgraph-closed,
* (\mathcal{G}) is somewhere dense,
* (\mathcal{G} \neq) the class of all graphs.

---

## 3. Problem Definition

### 3.1 The Problem (#\mathsf{Sub}_{\mathcal{G}}(\mathcal{H}))

**Input:** A graph (G \in \mathcal{G}) and a graph (H \in \mathcal{H}).
**Parameter:** (|H|).
**Output:** The number of subgraphs of (G) that are isomorphic to (H).

The restriction to (G \in \mathcal{G}) reflects a promise on the host graph class, while (\mathcal{H}) specifies the allowable patterns.

### 3.2 Scope of the Analysis

We do not assume any structural restriction on (\mathcal{H}) beyond recursive enumerability. This ensures that (\mathcal{H}) can encode arbitrarily complex families of patterns, including cliques, bicliques, and other dense graphs.

---

## 4. Complexity Classification Claim

### 4.1 Main Claim

**Claim (Informal Classification).**
Let (\mathcal{G}) be a subgraph-closed, somewhere-dense graph class not equal to the class of all graphs, and let (\mathcal{H}) be recursively enumerable. Then:

1. If (\mathcal{H}) contains graphs of unbounded treewidth, then (#\mathsf{Sub}_{\mathcal{G}}(\mathcal{H})) is (#\mathsf{W[1]})-hard parameterized by (|H|).
2. If (\mathcal{H}) has bounded treewidth, then (#\mathsf{Sub}_{\mathcal{G}}(\mathcal{H})) is fixed-parameter tractable.

This classification holds under standard parameterized reductions and assumes no collapse of the parameterized counting hierarchy.

### 4.2 Interpretation

The claim mirrors known dichotomies for counting homomorphisms and subgraphs in unrestricted graphs [4,5], but the host-class restriction requires careful justification. Somewhere-denseness is sufficient to simulate the hardness constructions used for general graphs, while subgraph-closure ensures that dense patterns can be embedded without violating the class constraints.

---

## 5. Influence of Host-Class Properties

### 5.1 Subgraph-Closure

Subgraph-closure is crucial for hardness. If (\mathcal{G}) contains a graph (G), it must contain all its subgraphs. This property prevents artificial exclusion of hard instances once a sufficiently complex graph is present.

### 5.2 Somewhere-Denseness vs. Nowhere-Denseness

For nowhere-dense classes, subgraph counting for bounded-treewidth patterns is FPT, and even some unbounded-treewidth patterns can be handled under additional restrictions [2,6]. In contrast, somewhere-dense classes admit dense local configurations, enabling parameterized reductions from (#\mathsf{Clique}) and related problems [3,7].

### 5.3 Exclusion of All Graphs

The assumption (\mathcal{G} \neq) all graphs prevents trivialization of the classification. However, known results show that many hardness constructions already apply to proper subclasses of all graphs, provided they are somewhere dense and subgraph-closed [7].

---

## 6. Influence of Pattern Structure

### 6.1 Treewidth as the Key Parameter

Treewidth has emerged as the decisive structural parameter for subgraph and homomorphism counting [4,5]. Bounded-treewidth patterns admit dynamic programming algorithms whose complexity depends exponentially on (|H|) but only polynomially on (|G|).

### 6.2 Unbounded Treewidth and Hardness

If (\mathcal{H}) contains graphs of unbounded treewidth, then it can encode cliques or grid-like structures. Counting such patterns subsumes (#\mathsf{Clique}), yielding (#\mathsf{W[1]})-hardness even under severe host restrictions [1,5].

---

## 7. Mathematical Outline of the Classification

### 7.1 Hardness Argument (Outline)

1. Use somewhere-denseness to obtain, for some fixed radius (r), large cliques as shallow minors in (\mathcal{G}) [3].
2. Exploit subgraph-closure to extract dense subgraphs suitable for embedding patterns from (\mathcal{H}).
3. Reduce (#\mathsf{Clique}) or (#\mathsf{Grid}) to (#\mathsf{Sub}_{\mathcal{G}}(\mathcal{H})) via parameter-preserving reductions.
4. Conclude (#\mathsf{W[1]})-hardness.

### 7.2 Tractability Argument (Outline)

1. Assume (\mathcal{H}) has bounded treewidth (t).
2. For fixed (H), use a tree decomposition of width (t).
3. Apply standard subgraph counting dynamic programming over (G), with running time (f(|H|)\cdot |G|^{O(1)}) [4].
4. Host-class restrictions do not impede this algorithm, yielding FPT.

---

## 8. Illustrative Example

Consider (\mathcal{G}) as the class of graphs excluding (K_{5}) as a subgraph but allowing it as a minor. This class is somewhere dense and subgraph-closed. Let (\mathcal{H}) be the family of all cliques.

* For (H = K_{k}), counting subgraphs isomorphic to (H) corresponds to counting (k)-cliques.
* Since (\mathcal{H}) has unbounded treewidth, the problem is (#\mathsf{W[1]})-hard by the classification.
* If instead (\mathcal{H}) consists of all trees, then treewidth is 1, and counting is FPT.

This aligns with both known results and the stated claim.

---

## 9. Discussion and Broader Context

The classification highlights a robust phenomenon: once a host class admits sufficient local density, the complexity of counting subgraphs is governed almost entirely by the structure of the pattern. This complements meta-theorems for sparse graphs and reinforces treewidth as a unifying concept across decision and counting variants.

Open questions remain regarding finer gradations within somewhere-dense classes, such as the impact of bounded expansion at specific depths or additional logical restrictions on (\mathcal{H}).

---

## 10. Conclusion

We have presented a structured complexity classification for (#\mathsf{Sub}_{\mathcal{G}}(\mathcal{H})) over subgraph-closed, somewhere-dense host classes. The analysis demonstrates that bounded treewidth of patterns yields fixed-parameter tractability, while unbounded treewidth leads to parameterized counting hardness. This result situates the problem firmly within the broader theory of parameterized counting complexity and underscores the deep interplay between graph structure and computational tractability.

---

## References

[1] Flum, J., Grohe, M. Parameterized Complexity Theory. Springer. - https://link.springer.com/book/10.1007/978-3-540-29953-9
[2] Nešetřil, J., Ossona de Mendez, P. Sparsity: Graphs, Structures, and Algorithms. Springer. - https://link.springer.com/book/10.1007/978-3-642-27875-4
[3] Nešetřil, J., Ossona de Mendez, P. “Grad and classes with bounded expansion I.” European Journal of Combinatorics, 29(3), 760–776. - https://doi.org/10.1016/j.ejc.2007.07.003
[4] Curticapean, R., Dell, H., Marx, D. “Homomorphisms are a good basis for counting small subgraphs.” SIAM Journal on Computing, 47(4), 1302–1342. - https://epubs.siam.org/doi/10.1137/17M111994X
[5] Curticapean, R. “Counting subgraphs isomorphic to a given graph.” ICALP 2016. - https://drops.dagstuhl.de/opus/volltexte/2016/6237/
[6] Grohe, M., Kreutzer, S., Siebertz, S. “Deciding first-order properties of nowhere dense graphs.” Journal of the ACM, 64(3). - https://dl.acm.org/doi/10.1145/3051095
[7] Dvořák, Z. “On recognizing nowhere dense graph classes.” Journal of Combinatorial Theory, Series B, 100(5), 698–720. - https://doi.org/10.1016/j.jctb.2010.05.002
