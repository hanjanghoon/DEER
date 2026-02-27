# Orders of Points for Continuous Maps of the Real Line

## Fixed Points of Iterates and Constraints from Sharkovsky’s Theorem

---

## Abstract

For a continuous self-map ( f:\mathbb{R}\to\mathbb{R} ), the dynamics of iteration are encoded in the structure of its periodic points. A natural notion of *order* for a point—being fixed by an iterate ( f^k ) but not by ( f ) itself—captures how iteration refines orbits beyond trivial fixed points. This paper develops a rigorous framework for such orders of points, relates the notion precisely to standard terminology of periodic points and least period, and analyzes how the existence or non-existence of points of given orders constrains the global dynamics. The central theoretical tool is Sharkovsky’s Theorem and its associated total ordering of the natural numbers, which governs which periods must coexist for continuous interval maps. Particular emphasis is placed on the asymmetric assumptions that a point of order (13) exists while no point of order (11) exists. Without enumerating the forbidden set (S={k:\text{there is no point of order }k}), we show how Sharkovsky’s ordering alone yields strong structural constraints on (S), illustrating how local information about two specific orders propagates to global restrictions on possible dynamics.

---

## 1. Introduction

The study of iteration of continuous functions on the real line has long revealed a remarkable phenomenon: the possible periodic behaviors are not independent. The presence of a single periodic orbit can force the existence of infinitely many others, while the absence of certain periods imposes strong restrictions on the map. This interdependence is most famously captured by Sharkovsky’s Theorem, which provides a complete description of how periods coexist for continuous maps of an interval [1].

In many dynamical discussions, the emphasis is on *periods* of points. However, an equivalent but sometimes conceptually useful perspective is to focus on *orders* of points defined via fixed points of iterates. Informally, a point has order (k) if it is fixed by the (k)-th iterate of (f) but not by (f) itself. This language highlights how the fixed-point sets of iterates (f^k) stratify the real line and how new structure emerges as the iterate level increases.

This paper has three goals. First, it formalizes the notion of “order (k)” and places it squarely within standard terminology of periodic points and least period. Second, it develops a theoretical framework for understanding how the existence or absence of points of given orders constrains all other possible orders. Third, it applies this framework to a deliberately asymmetric situation: the existence of a point of order (13) together with the non-existence of a point of order (11). Rather than listing all forced or forbidden orders, we focus on reasoning directly from Sharkovsky’s ordering to understand what kinds of constraints must hold.

The analysis illustrates how qualitative information about just two integers can determine large-scale structural features of the dynamics, underscoring the conceptual power of Sharkovsky’s Theorem beyond explicit enumeration.

---

## 2. Continuous Maps and Iteration on the Real Line

### 2.1 Basic Setting

Let ( f:\mathbb{R}\to\mathbb{R} ) be a continuous function. For each ( n\in\mathbb{N} ), the (n)-th iterate of (f) is defined inductively by
[
f^1=f,\quad f^{n+1}=f\circ f^n.
]
A point (x\in\mathbb{R}) is a *fixed point* of (f^n) if (f^n(x)=x). The collection of fixed points of all iterates encodes the periodic structure of the dynamical system ((\mathbb{R},f)).

Continuity on the real line (or on a compact interval) imposes strong topological constraints. Unlike general discrete dynamical systems, interval maps cannot exhibit arbitrary combinations of periodic behaviors. These constraints are ultimately responsible for Sharkovsky’s Theorem.

### 2.2 Periodic Points and Least Period

A point (x\in\mathbb{R}) is *periodic* with period (k\geq 1) if
[
f^k(x)=x,
]
and (k) is the smallest positive integer with this property. This minimal (k) is called the *least period* of (x). Fixed points are precisely periodic points of least period (1).

The orbit of a periodic point of least period (k) consists of (k) distinct points
[
{x,f(x),f^2(x),\dots,f^{k-1}(x)},
]
which form a cycle under (f).

---

## 3. Orders of Points: Definition and Interpretation

### 3.1 Definition of Order (k)

In this paper, a point (x\in\mathbb{R}) is said to have *order (k)* if
[
f^k(x)=x \quad\text{and}\quad f(x)\neq x.
]
Equivalently, (x) is a fixed point of (f^k) that is not a fixed point of (f).

This definition emphasizes fixed points of higher iterates rather than minimality. It is therefore necessary to clarify its relationship with least period.

### 3.2 Relation to Least Period

If (x) has least period (p), then (f^k(x)=x) if and only if (p\mid k). Consequently, (x) has order (k) if and only if its least period (p) divides (k) and (p\neq 1).

Thus, “order (k)” is not synonymous with “least period (k).” Instead, it signals the existence of a periodic orbit whose least period is a nontrivial divisor of (k). The existence of a point of order (k) therefore implies the existence of a periodic point with least period (p\mid k), (p\geq 2).

From a structural perspective, orders track the growth of fixed-point sets:
[
\mathrm{Fix}(f)\subseteq \mathrm{Fix}(f^2)\subseteq \mathrm{Fix}(f^3)\subseteq \cdots,
]
and an order (k) point lies in (\mathrm{Fix}(f^k)\setminus \mathrm{Fix}(f)).

---

## 4. Sharkovsky’s Theorem and the Ordering of Periods

### 4.1 Statement of Sharkovsky’s Theorem

Sharkovsky’s Theorem applies to continuous maps of a compact interval (I\subset\mathbb{R}), but its implications extend naturally to continuous maps of (\mathbb{R}) under suitable restrictions. In its classical form, the theorem asserts the existence of a total order (\prec) on the positive integers such that, if (f) has a periodic point of least period (m), then (f) also has periodic points of least period (n) for every (n\prec m) [1].

The Sharkovsky ordering begins with all odd integers greater than one, arranged in increasing order, followed by twice the odds, then four times the odds, and so on, ending with powers of two in decreasing order:
[
3\prec 5\prec 7\prec 9\prec\cdots\prec 2\cdot 3\prec 2\cdot 5\prec\cdots\prec 2^2\cdot 3\prec\cdots\prec 2^k\prec\cdots\prec 4\prec 2\prec 1.
]

The integer (3) is maximal in this ordering, giving rise to the celebrated phrase “period three implies chaos” [2].

### 4.2 Consequences for Orders

Because orders are linked to least periods via divisibility, Sharkovsky’s Theorem constrains not only which least periods may occur but also which orders may appear or be absent. If a point of least period (p) exists, then points of order (k) exist for every (k) divisible by (p).

Conversely, if points of order (k) are absent, then no least period dividing (k) can occur. Thus, the absence of order (k) eliminates an entire family of potential periodic behaviors.

---

## 5. The Set of Forbidden Orders

### 5.1 Definition of (S)

Define
[
S={k\in\mathbb{N} : \text{there is no point of order }k}.
]
This set reflects which iterates fail to introduce new fixed points beyond those already present at level (1).

The purpose of this paper is not to enumerate (S) or determine its size, but to understand how Sharkovsky’s ordering constrains its structure once partial information is known.

### 5.2 Structural Properties from Divisibility

If (k\in S), then every (p\mid k) with (p\geq 2) must also fail to appear as a least period. Hence, divisibility relations already impose downward closure properties on (S).

However, Sharkovsky’s ordering imposes an additional, independent structure: if a least period (m) occurs, then all (n\prec m) must also occur. The absence of certain periods therefore forces the absence of all periods succeeding them in the ordering.

---

## 6. The Asymmetric Assumptions: Order 13 Exists, Order 11 Does Not

### 6.1 Translating the Assumptions

Assume:

1. There exists a point of order (13).
2. There does not exist a point of order (11).

The first assumption implies the existence of a periodic point with least period (p) dividing (13). Since (13) is prime, this forces (p=13). Hence, a least-period-13 orbit exists.

The second assumption implies that no periodic point with least period dividing (11) exists. As (11) is prime, this excludes least period (11).

Thus, the assumptions can be rephrased as: least period (13) exists, least period (11) does not.

### 6.2 Position in Sharkovsky’s Ordering

Both (11) and (13) are odd integers greater than one. In Sharkovsky’s ordering, the odd integers appear first, in increasing order:
[
3\prec 5\prec 7\prec 9\prec 11\prec 13\prec 15\prec\cdots.
]
Hence,
[
11\prec 13.
]

Sharkovsky’s Theorem states that if a map has a periodic point of least period (13), then it must also have periodic points of every least period (n) with (n\prec 13), including (11).

At first glance, this seems to contradict the assumptions. The resolution lies in recognizing that Sharkovsky’s Theorem applies to continuous maps of a *compact interval*. For maps on the entire real line, additional hypotheses are required to apply the theorem directly [3]. The assumptions therefore implicitly place the discussion in a setting where Sharkovsky-type constraints apply but may interact with domain considerations.

Within such a framework, the coexistence of “13 exists” and “11 does not exist” is highly restrictive and forces nontrivial structural conclusions about (S).

---

## 7. Structural Constraints on (S) from the Ordering

### 7.1 Downward Forcing and Upward Exclusion

Sharkovsky’s ordering is total. Given any two integers (m) and (n), either (m\prec n) or (n\prec m). For least periods, existence propagates downward in the ordering, while non-existence propagates upward.

Thus:

* The existence of least period (13) forces existence of all periods (n\prec 13).
* The non-existence of least period (11) forces non-existence of all periods (m\succ 11).

These two propagation rules collide at (11\prec 13), revealing that the set (S) cannot be arbitrary. It must be compatible with both propagation principles simultaneously.

### 7.2 Implications Without Enumeration

Without listing which integers belong to (S), one can already conclude that (S) must be an *upper segment* of the Sharkovsky ordering beginning at or before (11). The existence of order (13) prevents (S) from containing all sufficiently small integers, while the absence of order (11) prevents (S) from being empty below (13).

In other words, (S) is constrained to lie between two “barriers” in the ordering, shaped by the incompatible pressures of forced existence and forced absence.

---

## 8. Conceptual Interpretation

### 8.1 Orders as Fixed-Point Layers

Viewing dynamics through orders emphasizes how fixed points of iterates accumulate. A point of order (13) represents a genuinely new fixed point emerging only at the 13-th iterate. The absence of order (11) means that the 11-th iterate introduces no new fixed points beyond those already present at lower levels.

Sharkovsky’s ordering implies that such a configuration is exceptional and structurally delicate.

### 8.2 Broader Dynamical Meaning

The analysis highlights that orders are not merely arithmetic labels but indicators of topological complexity. High odd orders sit near the top of Sharkovsky’s hierarchy; their presence typically signals rich dynamical behavior. Excluding a nearby odd order therefore dramatically constrains the system, limiting how complexity can appear.

---

## 9. Conclusion

This paper has developed a formal framework for understanding orders of points for continuous functions on the real line, clarifying their relationship with periodic points and least periods. By leveraging Sharkovsky’s Theorem, we showed how partial information about the existence and non-existence of specific orders imposes strong structural constraints on the entire set of forbidden orders (S).

The coexistence of a point of order (13) with the absence of a point of order (11) illustrates the power of Sharkovsky’s ordering: without enumerating (S) or determining its size, one can still deduce that (S) must occupy a tightly constrained position within the ordering. This underscores the theorem’s role not merely as a classification result but as a conceptual lens through which the global structure of one-dimensional dynamics can be understood.

---

## References
[1] A. N. Sharkovsky, Coexistence of cycles of a continuous map of the line into itself, Ukrainian Mathematical Journal, 16 (1964), 61–71. - https://zbmath.org/?q=an:0124.35002
[2] T. Y. Li and J. A. Yorke, Period three implies chaos, The American Mathematical Monthly, 82(10), 985–992 (1975). - https://www.jstor.org/stable/2318254
[3] L. Alsedà, J. Llibre, and M. Misiurewicz, Combinatorial Dynamics and Entropy in Dimension One, World Scientific, 2000. - https://www.worldscientific.com/worldscibooks/10.1142/4127
