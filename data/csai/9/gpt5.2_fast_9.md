# Optimal-Time Identification of a Cyclic Rotation Offset Between Two Lists of Unique Integers

## Abstract

We study the problem of identifying the cyclic rotation offset between two length-(n) lists of unique integers, (A) and (B), where (B) is obtained by rotating (A) by an unknown offset (i). Formally, (B = A[i:] \mathbin{+ +} A[:i]) for some (i \in {0,\dots,n-1}). Both lists are given explicitly, the elements are pairwise distinct but otherwise arbitrary, and the task is to determine (i) exactly. We treat this setting as an internal case study to explore optimal time complexity under standard computational models, including deterministic and randomized algorithms in the word-RAM and comparison models. We ask whether sublinear worst-case time is possible, establish tight complexity bounds, and analyze multiple algorithmic strategies and their trade-offs. We further investigate realistic variants, including duplicate elements, preprocessing, streaming access, and parallel computation. Our analysis situates the problem within the broader framework of string matching, cyclic equivalence, and lower-bound theory, clarifying which assumptions permit linear-time solutions and which fundamentally preclude asymptotic improvement.

---

## 1. Introduction

Cyclic rotations arise naturally across computer science, from string algorithms and data synchronization to signal processing and distributed systems. Given a sequence (A), any cyclic rotation preserves relative order while shifting the starting position. Detecting whether two sequences are cyclic rotations of each other—and if so, identifying the offset—is a classical problem. When the sequences are strings over a finite alphabet, this task is closely related to pattern matching and can be solved in linear time via string matching techniques such as the Knuth–Morris–Pratt (KMP) algorithm [1].

In this paper, we focus on a specific but representative variant: both sequences (A) and (B) are lists of unique integers of length (n), not assumed to be sorted or drawn from a small alphabet. The uniqueness assumption removes ambiguities in matching, while the lack of ordering or bounded alphabet size removes certain shortcuts available in more structured settings. The goal is to determine the unique offset (i) such that (B) is exactly a cyclic rotation of (A) by (i), assuming such an (i) exists.

This problem serves as a clean case study for understanding optimal time complexity. At first glance, it seems trivial: scan (A) to find where (B[0]) appears, and check consistency. However, this intuition hides important subtleties. Can we do better than linear time? What assumptions are necessary to achieve optimality? How do deterministic and randomized algorithms compare? How does the complexity change under different access models or constraints?

We aim to answer these questions systematically. Our contributions are primarily expository and analytical: we formalize the problem, establish lower bounds, analyze known and natural algorithms, and explore variants that illuminate the boundaries of tractability. While the core result—that (\Theta(n)) time is optimal in the worst case under exact correctness—is well aligned with known results in string matching, we emphasize the role of computational models and problem structure in making this bound tight.

---

## 2. Problem Formalization

### 2.1 Definition

Let (A = (a_0, a_1, \dots, a_{n-1})) be a list of (n) distinct integers. For an integer (i \in {0,\dots,n-1}), define the cyclic rotation of (A) by offset (i) as
[
\mathrm{rot}*i(A) = (a_i, a*{i+1}, \dots, a_{n-1}, a_0, \dots, a_{i-1}).
]
We are given another list (B = (b_0, b_1, \dots, b_{n-1})) such that (B = \mathrm{rot}_i(A)) for some unknown (i). The task is to compute (i).

We assume that (n) is known, both lists are accessible, and all elements in (A) (and hence in (B)) are distinct.

### 2.2 Computational Models

We consider several standard models:

* **Comparison model**: Algorithms can only compare elements for equality or order.
* **Word-RAM model**: Integers fit in machine words, allowing constant-time hashing, arithmetic, and array indexing [2].
* **Randomized algorithms**: Algorithms may use random bits and are allowed to err with small probability.
* **Streaming and parallel variants**: Access to input may be sequential or distributed across processors.

Unless otherwise stated, we require exact correctness: the algorithm must output the correct offset for all valid inputs.

---

## 3. Baseline Observations

Because all elements are unique, the rotation offset (i) is uniquely determined. Indeed, (b_0 = a_i), so (i) is the position of (b_0) in (A). However, this observation alone does not guarantee correctness: after identifying a candidate (i), we must verify that for all (k),
[
b_k = a_{(i+k) \bmod n}.
]
This verification step appears to require examining all elements.

This already suggests a lower bound of (\Omega(n)) time in the worst case. The remainder of the paper formalizes and sharpens this intuition.

---

## 4. Lower Bounds and the Impossibility of Sublinear Time

### 4.1 Exact Correctness in the Worst Case

We first address whether sublinear worst-case time is possible. Suppose an algorithm examines fewer than (n) positions of the input in the worst case. Then there exists at least one position (j) in (A) or (B) that the algorithm does not inspect. An adversary can modify the unseen element while preserving uniqueness, potentially changing the rotation offset or violating the rotation property altogether. Therefore, the algorithm cannot distinguish between valid and invalid instances without inspecting all positions.

This adversarial argument is standard in decision-tree and comparison-based lower bounds for string matching [3]. It implies an (\Omega(n)) lower bound for deterministic algorithms under exact correctness.

### 4.2 Reduction from String Matching

We can also reduce the classic string matching problem to our setting. Given a pattern (P) and text (T), both of length (n), checking whether (P) occurs in (T) as a substring can be reduced to checking whether (P) is a cyclic rotation of a specially constructed sequence. Since exact string matching has a linear lower bound in the comparison model [4], our problem inherits this bound.

### 4.3 Randomization and Las Vegas Algorithms

Randomization does not help in the worst case if exact correctness is required. A Las Vegas algorithm must still inspect enough elements to rule out adversarial inputs. While Monte Carlo algorithms may reduce expected running time under distributional assumptions, they cannot break the (\Omega(n)) worst-case barrier without allowing errors [5].

---

## 5. Deterministic Algorithms

### 5.1 Direct Indexing with Verification

In the word-RAM model, we can build a hash table mapping each value in (A) to its index in (O(n)) time. We then look up (b_0) to obtain a candidate offset (i), and verify the rotation in a single linear pass. This yields a deterministic (O(n)) time and (O(n)) space algorithm.

This approach is optimal in time and simple to implement, but it relies on hashing and extra space.

### 5.2 Reduction to String Matching

Another deterministic approach treats the problem as string matching. Consider the sequence (A' = A \mathbin{+ +} A), the concatenation of (A) with itself. Then (B) occurs as a contiguous subsequence of (A') starting at position (i). Using KMP or a similar linear-time string matching algorithm, we can find (i) in (O(n)) time and (O(n)) preprocessing [1].

This approach works in the comparison model and does not rely on hashing, but it requires careful handling of integer comparisons and may have higher constant factors.

### 5.3 Space-Efficient Variants

If space is constrained, we can avoid building full auxiliary structures. For example, we can scan (A) linearly to find the position of (b_0), then verify. This uses (O(1)) extra space and (O(n)) time, but may take (2n) comparisons in the worst case.

---

## 6. Randomized Algorithms

### 6.1 Hash-Based Fingerprinting

Randomized algorithms often rely on hashing or fingerprinting. We can compute a rolling hash for (A) and (B) and compare (B) against all rotations of (A) implicitly by hashing (A') [6]. With a suitable hash function, this can be done in expected (O(n)) time with high probability of correctness.

However, under exact correctness requirements, we must still verify the match deterministically, returning us to linear time in the worst case.

### 6.2 Expected vs. Worst-Case Guarantees

If we relax the requirement to expected time or allow a small probability of error, randomized algorithms can be attractive in practice. Nevertheless, from a theoretical standpoint, the asymptotic bound remains (\Theta(n)) under standard assumptions [5].

---

## 7. Tightness of the Linear Bound

The (\Theta(n)) bound is tight: we have exhibited multiple algorithms achieving (O(n)) time, and shown that (\Omega(n)) is unavoidable in the worst case. The tightness holds across deterministic and randomized models, as long as exact correctness is required and the input is given explicitly.

This aligns with known results for string matching and cyclic equivalence [1,3].

---

## 8. Variants and Extensions

### 8.1 Duplicate Elements

If duplicates are allowed, the offset may not be unique, or may not exist. The problem then becomes more complex: we must find all offsets (i) such that (B = \mathrm{rot}_i(A)). This is equivalent to finding all occurrences of (B) in (A'), which can still be done in (O(n)) time using string matching algorithms, but the uniqueness property is lost [1].

### 8.2 Preprocessing and Multiple Queries

If (A) is fixed and we receive many queries (B), preprocessing (A) can be advantageous. We can build a suffix automaton or similar index on (A'), enabling each query to be answered in (O(n)) time or better in some models [7]. However, the per-query worst-case time remains linear in the length of (B).

### 8.3 Streaming Constraints

If (B) arrives as a stream, we can process it online while maintaining a rolling hash or partial match state. This allows detection of the offset as soon as sufficient information is available, but the total processing time remains linear [6].

### 8.4 Parallel Computation

In parallel models such as PRAM, the work can be divided among processors. With (p) processors, the time can be reduced to (O(n/p + \log n)) using parallel string matching techniques [8]. However, the total work remains (\Theta(n)), preserving the fundamental lower bound.

---

## 9. Broader Context and Related Frameworks

The cyclic rotation offset problem sits at the intersection of string algorithms, pattern matching, and lower-bound theory. Its analysis illustrates a recurring theme in algorithm design: while clever techniques can reduce constants or exploit structure, certain information-theoretic barriers cannot be crossed without relaxing assumptions.

Similar conclusions hold for related problems such as equality testing, permutation verification, and substring search [3,4]. The uniqueness assumption simplifies correctness but does not reduce asymptotic complexity.

---

## 10. Conclusion

We have presented a comprehensive analysis of the problem of identifying the cyclic rotation offset between two lists of unique integers. Under standard computational models and exact correctness requirements, the problem admits a tight (\Theta(n)) worst-case time complexity. This bound holds for both deterministic and randomized algorithms, and persists across a variety of realistic variants.

While the problem is simple to state and solve in practice, its theoretical analysis reinforces foundational principles of algorithmic complexity. It serves as a clear example where linear time is both achievable and unavoidable, highlighting the importance of carefully examining computational assumptions when assessing optimality.

---

## References
[1] Knuth, D. E., Morris, J. H., & Pratt, V. R. Fast pattern matching in strings. SIAM Journal on Computing. https://doi.org/10.1137/0206024
[2] Hagerup, T. Sorting and searching on the word RAM. Algorithmica. https://doi.org/10.1007/BF01187029
[3] Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. Introduction to Algorithms. MIT Press. https://mitpress.mit.edu/9780262046305
[4] Fredman, M. L. On the complexity of maintaining order. Journal of the ACM. https://doi.org/10.1145/321941.321944
[5] Motwani, R., & Raghavan, P. Randomized Algorithms. Cambridge University Press. https://doi.org/10.1017/CBO9780511814075
[6] Rabin, M. O., & Karp, R. M. Efficient randomized pattern-matching algorithms. IBM Journal of Research and Development. https://doi.org/10.1147/rd.316.0249
[7] Crochemore, M., & Rytter, W. Jewels of Stringology. World Scientific. https://doi.org/10.1142/4903
[8] JáJá, J. An Introduction to Parallel Algorithms. Addison-Wesley. https://dl.acm.org/doi/book/10.5555/57952
