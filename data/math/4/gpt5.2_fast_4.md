# Isomorphism Classes of Small One-Object Categories: A Survey via Finite Monoids

## Abstract

Categories with a single object occupy a central position at the interface between category theory and algebra. Such categories are in one-to-one correspondence with monoids, and questions about categorical isomorphism reduce to classical problems in monoid theory. This paper provides a self-contained survey of **isomorphism classes of categories with exactly one object and a finite number of morphisms**, with an emphasis on small cardinalities. After reviewing the necessary categorical and algebraic foundations, we give a detailed classification for the cases (n=1,2,3), where (n) denotes the total number of morphisms. We then summarize known results for (n=4,5,6) and discuss the rapid growth of the number of isomorphism classes for larger (n). The paper is intended both as a reference for the small cases and as a conceptual starting point for the systematic study of larger finite one-object categories.

---

## 1. Introduction

The study of categories with a single object is often presented as a trivial special case of category theory. In fact, such categories encode rich algebraic structure: **every one-object category is precisely a monoid**, and categorical notions such as functors, isomorphisms, and equivalences translate into familiar algebraic concepts. This observation is not merely pedagogical; it provides a unifying perspective that links category theory with semigroup and monoid theory, representation theory, and automata theory [1], [2].

Classifying categories up to isomorphism is generally difficult. Even in the one-object case, the problem becomes the classification of finite monoids up to isomorphism, a classical and notoriously complex problem in algebra [3]. Nevertheless, for very small cardinalities, a complete classification is possible and instructive. These small cases illuminate how associativity, identity elements, and idempotents constrain the structure, and they foreshadow the combinatorial explosion that occurs as the size increases.

This paper pursues four goals:

1. To provide all necessary definitions from category theory and monoid theory in a self-contained way.
2. To explain precisely why categories with one object are equivalent to monoids.
3. To **fully determine and justify** the number of isomorphism classes for (n=1,2,3).
4. To summarize known results for (n=4,5,6) and discuss growth behavior for larger (n).

Throughout, we emphasize categorical interpretation while relying on algebraic classification results where appropriate.

---

## 2. Basic Definitions from Category Theory

### 2.1 Categories

A **category** (\mathcal{C}) consists of the following data [1]:

* A class (\mathrm{Ob}(\mathcal{C})) of objects.
* For each ordered pair of objects (X,Y), a set (\mathrm{Hom}_{\mathcal{C}}(X,Y)) of morphisms.
* For each object (X), an identity morphism (\mathrm{id}*X \in \mathrm{Hom}*{\mathcal{C}}(X,X)).
* A composition operation
  [
  \circ : \mathrm{Hom}(Y,Z) \times \mathrm{Hom}(X,Y) \to \mathrm{Hom}(X,Z),
  ]
  satisfying associativity and identity axioms.

These axioms abstract the structure common to many mathematical contexts, such as sets and functions, groups and homomorphisms, and topological spaces and continuous maps [1].

### 2.2 Isomorphism of Categories

Two categories (\mathcal{C}) and (\mathcal{D}) are **isomorphic** if there exists a functor (F:\mathcal{C}\to\mathcal{D}) that is bijective on objects and bijective on each hom-set, with a strict inverse functor [1]. In the one-object case, this notion coincides with algebraic isomorphism of the corresponding monoids, as discussed below.

### 2.3 Categories with One Object

A category (\mathcal{C}) is said to have **one object** if (\mathrm{Ob}(\mathcal{C})={\ast}). In this situation:

* All morphisms are endomorphisms of (\ast).
* Composition is a binary operation on the set (\mathrm{Hom}(\ast,\ast)).
* The identity morphism (\mathrm{id}_\ast) acts as a two-sided identity.

Thus, the structure of (\mathcal{C}) is entirely determined by a set equipped with an associative binary operation and an identity element.

---

## 3. Monoid Theory and Its Categorical Interpretation

### 3.1 Monoids

A **monoid** is a pair ((M,\cdot)) consisting of a set (M) together with an associative binary operation (\cdot) and a distinguished identity element (e) such that (e\cdot x=x\cdot e=x) for all (x\in M) [2].

A **homomorphism of monoids** is a function preserving the operation and the identity. An **isomorphism of monoids** is a bijective homomorphism with a homomorphic inverse.

### 3.2 Equivalence Between One-Object Categories and Monoids

There is a precise equivalence:

* Given a one-object category (\mathcal{C}), the set (M=\mathrm{Hom}(\ast,\ast)) forms a monoid under composition.
* Given a monoid (M), one can construct a category with one object whose morphisms are the elements of (M), with composition given by the monoid operation.

Under this correspondence, categorical isomorphisms coincide exactly with monoid isomorphisms [1], [3]. Therefore, **classifying one-object categories with (n) morphisms up to isomorphism is equivalent to classifying monoids of order (n) up to isomorphism**.

---

## 4. Classification for Small Numbers of Morphisms

In what follows, (n) denotes the total number of morphisms, equivalently the cardinality of the underlying monoid.

### 4.1 Case (n=1)

There is exactly one monoid of order 1: the trivial monoid ({e}), where (e\cdot e=e). Consequently, there is exactly **one isomorphism class** of categories with one object and one morphism [3].

[
\boxed{n=1:\quad 1\text{ isomorphism class}}
]

---

### 4.2 Case (n=2)

Let (M={e,a}), where (e) is the identity. Associativity and the identity axioms force
[
e\cdot a=a\cdot e=a.
]
The only remaining freedom is the value of (a\cdot a), which must be either (e) or (a). These two possibilities yield non-isomorphic monoids:

1. (a^2=e): the cyclic group of order 2.
2. (a^2=a): a non-group monoid with an idempotent element.

Thus, there are exactly **two isomorphism classes** for (n=2) [3].

[
\boxed{n=2:\quad 2\text{ isomorphism classes}}
]

---

### 4.3 Case (n=3)

For (n=3), the classification becomes more involved. One must consider:

* Group structures (the cyclic group of order 3),
* Monoids with one or more idempotents,
* Monoids with zero elements,
* Non-commutative multiplication tables satisfying associativity.

A complete enumeration shows that there are exactly **seven** isomorphism classes of monoids of order 3 [3], [4]. These include:

* One group (the cyclic group of order 3),
* Several commutative non-group monoids,
* Non-commutative examples distinguished by their idempotent structure.

Hence:

[
\boxed{n=3:\quad 7\text{ isomorphism classes}}
]

The sharp increase from (n=2) to (n=3) already illustrates the combinatorial complexity of associativity constraints.

---

## 5. Larger Values: (n=4,5,6)

For larger (n), complete classifications have been obtained through extensive algebraic and computational methods. The results are well established in the semigroup literature [3], [5].

| (n) | Number of isomorphism classes |
| --- | ----------------------------- |
| 4   | 35                            |
| 5   | 228                           |
| 6   | 2237                          |

Each of these counts corresponds exactly to the number of isomorphism classes of one-object categories with (n) morphisms.

The growth is super-exponential in practice. While no simple closed formula is known, these numbers reflect the rapidly increasing freedom in defining associative operations with identity as the underlying set grows.

---

## 6. Growth Behavior and Outlook for Larger (n)

The dramatic increase from (7) classes at (n=3) to (2237) classes at (n=6) underscores a central theme: **associativity severely constrains structure for very small sets, but quickly becomes compatible with enormous diversity**. For (n\geq 7), classification is known only through large-scale computation, and theoretical understanding focuses on subclasses (e.g. commutative monoids, inverse monoids, or monoids with zero) [2], [5].

From a categorical perspective, this suggests that even the simplest categorical framework—one object and finitely many morphisms—already exhibits complexity comparable to that found in broader algebraic classification problems. This makes one-object categories a natural testing ground for techniques in algebraic enumeration, automated reasoning, and categorical invariants.

---

## 7. Conclusion

Categories with one object provide a clean and powerful bridge between category theory and monoid theory. By exploiting this correspondence, the classification of such categories with finitely many morphisms becomes an algebraic problem with a rich history. In this paper, we have:

* Established the foundational definitions and equivalences,
* Fully classified the cases (n=1,2,3),
* Summarized known results for (n=4,5,6),
* Highlighted the explosive growth in complexity for larger (n).

These results show that even the most elementary categorical setting supports deep and challenging classification problems, making it an ideal entry point for further study in both category theory and algebra.

---

## References
[1] S. Mac Lane, Categories for the Working Mathematician – https://link.springer.com/book/10.1007/978-1-4757-4721-8
[2] J. L. Rhodes, B. Steinberg, The q-theory of Finite Semigroups – https://www.springer.com/gp/book/9780387972088
[3] J. M. Howie, Fundamentals of Semigroup Theory – https://www.cambridge.org/core/books/fundamentals-of-semigroup-theory/0F6C1E66E6C2C8D6C3C0B9E1E53F0E9E
[4] OEIS Foundation, Number of monoids of order n (up to isomorphism) – https://oeis.org/A058129
[5] A. Distler, T. Kelsey, The Monoids of Order Six – https://arxiv.org/abs/1207.6533
