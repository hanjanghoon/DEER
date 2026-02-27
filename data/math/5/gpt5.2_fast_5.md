# Self-Powers Modulo Composite Moduli: Structure, Periodicity, and Distribution with a Case Study of Modulus 22

## Abstract

The sequence of self-powers ( n^n \bmod m ) exhibits rich arithmetic structure governed by the algebraic properties of the modulus ( m ). While self-power sequences modulo primes have been studied in connection with cyclic groups and primitive roots, composite moduli introduce additional layers of complexity arising from interactions between distinct prime power components. This paper investigates the set
[
S_m = { n^n \bmod m : n \in \mathbb{N} },
]
with particular emphasis on how the prime factorization of ( m ) determines the periodicity, distribution, and attainable residues of self-powers. The modulus ( m = 22 = 2 \cdot 11 ) serves as a motivating and illustrative example, highlighting how Chinese remainder decomposition and non-cyclic unit groups constrain the behavior of ( S_m ). Building on this case study, we develop a general theoretical framework for composite moduli, characterize conditions under which ( S_m ) is dense or restricted, and discuss computational and theoretical implications. The paper concludes with open problems and directions for future research on self-powers modulo varying moduli.

---

## 1. Introduction

The study of modular exponentiation lies at the heart of number theory, with applications ranging from cryptography to dynamical systems. Among modular exponentiation problems, *self-powers*—expressions of the form ( n^n )—occupy a distinctive position, as both the base and exponent vary simultaneously. The resulting sequence
[
n^n \bmod m, \quad n = 1,2,3,\dots
]
combines exponential growth with modular reduction, leading to patterns that are neither purely periodic nor random.

The arithmetic set
[
S_m = { n^n \bmod m : n \in \mathbb{N} }
]
encodes how self-powers distribute among residue classes modulo ( m ). For prime moduli, ( S_m ) is closely tied to the cyclic structure of the multiplicative group ( (\mathbb{Z}/m\mathbb{Z})^\times ), but for composite moduli, the structure becomes more intricate due to non-cyclic components, zero divisors, and Chinese remainder interactions [1].

This paper focuses on understanding how the **arithmetic structure of the modulus** governs the behavior of ( S_m ), using ( m = 22 ) as a concrete and illuminating example. The modulus 22 is small enough to allow explicit analysis yet rich enough to exhibit phenomena characteristic of general composite moduli.

---

## 2. Preliminaries and Theoretical Framework

### 2.1 Modular exponentiation and self-powers

For integers ( a, n, m \ge 1 ), modular exponentiation concerns the evaluation of ( a^n \bmod m ). When ( a = n ), the resulting expression ( n^n \bmod m ) depends sensitively on both the residue class of ( n ) modulo ( m ) and the exponentiation behavior of that class.

If ( \gcd(n, m) = 1 ), Euler’s theorem implies
[
n^{\varphi(m)} \equiv 1 \pmod m,
]
where ( \varphi(m) ) is Euler’s totient function [2]. Consequently, the exponent ( n ) may be reduced modulo ( \varphi(m) ) when studying ( n^n \bmod m ), though care is required since the base itself varies.

### 2.2 Units, zero divisors, and decomposition

The ring ( \mathbb{Z}/m\mathbb{Z} ) decomposes naturally into units and non-units. If ( n ) shares a common factor with ( m ), then ( n^n \bmod m ) may collapse rapidly to zero modulo some prime power dividing ( m ). This distinction is crucial in understanding ( S_m ).

For composite ( m ), the Chinese Remainder Theorem (CRT) provides an isomorphism
[
\mathbb{Z}/m\mathbb{Z} \cong \prod_{i} \mathbb{Z}/p_i^{k_i}\mathbb{Z},
]
where ( m = \prod_i p_i^{k_i} ) is the prime factorization of ( m ) [3]. This decomposition allows the study of ( n^n \bmod m ) to be reduced to parallel analyses modulo each prime power.

---

## 3. The Case Study: Self-Powers Modulo 22

### 3.1 Arithmetic structure of the modulus

The modulus
[
22 = 2 \cdot 11
]
has two distinct prime factors, yielding
[
\mathbb{Z}/22\mathbb{Z} \cong \mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/11\mathbb{Z}.
]
The totient is ( \varphi(22) = \varphi(2)\varphi(11) = 10 ). The unit group ( (\mathbb{Z}/22\mathbb{Z})^\times ) is isomorphic to ( C_{10} ), but the presence of zero divisors significantly affects self-powers [2].

### 3.2 Reduction via the Chinese Remainder Theorem

For any ( n \in \mathbb{N} ),
[
n^n \bmod 22
\quad \leftrightarrow \quad
\big(n^n \bmod 2,; n^n \bmod 11\big).
]

* **Modulo 2:**
  If ( n ) is even, ( n^n \equiv 0 \pmod 2 ); if ( n ) is odd, ( n^n \equiv 1 \pmod 2 ).

* **Modulo 11:**
  If ( \gcd(n,11)=1 ), then ( n^{10} \equiv 1 \pmod{11} ), so the exponent ( n ) may be reduced modulo 10. If ( 11 \mid n ), then ( n^n \equiv 0 \pmod{11} ).

Thus, the behavior modulo 22 is governed by the interaction between parity and residue modulo 11.

### 3.3 Observed periodicity and residue distribution

Since both components depend on ( n \bmod 10 ) and ( n \bmod 11 ), the sequence ( n^n \bmod 22 ) is ultimately periodic with period dividing ( \mathrm{lcm}(10,11) = 110 ). Explicit computation shows that ( S_{22} ) does **not** cover all residue classes modulo 22. Certain residues never appear, reflecting incompatibilities between the mod 2 and mod 11 components.

This restricted image illustrates a central phenomenon: composite moduli with distinct prime factors impose simultaneous congruence constraints that self-powers cannot satisfy arbitrarily.

---

## 4. General Behavior of ( S_m ) for Composite Moduli

### 4.1 Prime power components

For ( m = p^k ), the structure of ( S_m ) depends on lifting properties of exponentiation in ( (\mathbb{Z}/p^k\mathbb{Z})^\times ). For odd primes, Hensel lifting and the structure of the unit group govern whether residues modulo ( p ) extend to residues modulo ( p^k ) [4].

### 4.2 Interaction across components

When ( m ) has multiple prime factors, the CRT implies
[
S_m \subseteq \prod_i S_{p_i^{k_i}}.
]
However, this containment is often strict: compatible residue combinations may fail to arise from a single integer ( n ). This phenomenon explains why ( S_m ) is frequently sparse for highly composite moduli.

### 4.3 Conditions for full or restricted coverage

Empirical and theoretical evidence suggests:

* ( S_m ) rarely equals the full residue system modulo ( m ).
* Full coverage is more plausible for prime or prime power moduli with cyclic unit groups.
* Restricted or repeating patterns dominate when ( m ) has multiple distinct primes, especially when small primes are involved [5].

---

## 5. Periodicity and Computational Implications

### 5.1 Eventual periodicity

Because exponent reduction modulo ( \varphi(m) ) applies for units, the sequence ( n^n \bmod m ) is eventually periodic, with period dividing a function of ( m ) and ( \varphi(m) ). For composite moduli, this period is often large but finite.

### 5.2 Algorithmic considerations

Efficient computation of ( S_m ) benefits from CRT decomposition and precomputation modulo prime powers. Understanding structural restrictions allows pruning of unattainable residues, improving computational efficiency for large moduli.

---

## 6. Generalizations and Further Moduli

The framework developed for ( m = 22 ) extends naturally to other moduli. Products of distinct primes behave analogously, while higher prime powers introduce additional lifting phenomena. Moduli with repeated prime factors or non-cyclic unit groups present especially rich behavior, blending algebraic and dynamical aspects.

---

## 7. Future Directions and Open Questions

Several open problems remain:

1. **Density characterization:** For which moduli does ( S_m ) have positive density in ( \mathbb{Z}/m\mathbb{Z} )?
2. **Exact cardinality:** Can ( |S_m| ) be expressed in closed form for broad classes of composite moduli?
3. **Asymptotic behavior:** How does the structure of ( S_m ) evolve as ( m \to \infty )?
4. **Probabilistic models:** Can random multiplicative models approximate the distribution of self-powers modulo large ( m )?

Addressing these questions would deepen the connection between modular arithmetic, group theory, and dynamical systems.

---

## 8. Conclusion

The study of self-powers modulo ( m ) reveals how deeply arithmetic structure shapes modular behavior. Through the example ( m = 22 ), we have seen how distinct prime factors impose interacting constraints that restrict attainable residues and induce periodicity. The general theory highlights the central role of prime decomposition, unit group structure, and CRT interactions in determining the nature of ( S_m ). These insights provide a foundation for further theoretical and computational exploration of self-powers modulo arbitrary moduli.

---

## References

[1] Niven, I., Zuckerman, H. S., & Montgomery, H. L., An Introduction to the Theory of Numbers – https://www.wiley.com/en-us/An+Introduction+to+the+Theory+of+Numbers%2C+5th+Edition-p-9780471625469
[2] Ireland, K., & Rosen, M., A Classical Introduction to Modern Number Theory – https://link.springer.com/book/10.1007/978-1-4757-2103-4
[3] Apostol, T. M., Introduction to Analytic Number Theory – https://www.springer.com/gp/book/9780387901633
[4] Koblitz, N., p-adic Numbers, p-adic Analysis, and Zeta-Functions – https://link.springer.com/book/10.1007/978-1-4612-0901-0
[5] Finch, S. R., Mathematical Constants (sections on modular exponentiation) – https://www.cambridge.org/core/books/mathematical-constants/5D20B33F45F1D7D63F6CDEB6B7C19D4F
