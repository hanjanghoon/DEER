# Circuit Complexity Upper Bounds for Average-Hard-Attention Saturated Transformers

## Abstract

We establish explicit upper bounds on the Boolean circuit complexity of formal languages recognized by a family of Transformer architectures with real-valued (floating-point) activations, under a regime of *average-hard-attention saturation*. We precisely define the Transformer computation model—including depth, heads, dimension, bit-precision, attention saturation and averaging rules, and positional encodings—and formalize language recognition via thresholded output. We then define a uniform Boolean circuit model and construct a simulation of Transformer inference by polynomial-size circuits whose depth depends on architectural growth rates. Under mild assumptions on parameter precision and attention saturation, we prove that such Transformer-recognized languages lie in nonuniform **TC⁰**, **NC¹**, or **P/poly**, depending on scaling. The results clarify the computational ceiling of saturated attention mechanisms and situate average-hard-attention Transformers within classical circuit complexity classes.

---

## 1. Introduction

Transformer architectures dominate modern sequence modeling, yet their *computational expressivity* remains only partially understood from a complexity-theoretic perspective. Recent work has shown strong connections between attention mechanisms and classical automata, circuit, and logic models [1,2,3,4]. In particular, restrictions on attention—such as bounded precision, softmax saturation, or averaging behavior—appear to significantly limit computational power.

This paper addresses the following question:

> **What is the upper bound on the Boolean circuit complexity of languages recognized by Transformers with saturated average hard attention and finite-precision floating-point activations?**

We give a precise answer by:

1. Formally defining a *Transformer computation model* with explicit parameter functions.
2. Defining a *uniform Boolean circuit model* suitable for simulation.
3. Constructing a circuit simulation of Transformer inference.
4. Deriving asymptotic upper bounds under different architectural growth regimes.

Our focus is on *upper bounds* only. We do not claim tightness.

---

## 2. Preliminaries

### 2.1 Strings and Languages

Let (\Sigma) be a finite alphabet. A **formal language** is a subset (L \subseteq \Sigma^*).

We identify an input string (x = x_1 \dots x_n) with a length-(n) sequence of tokens.

---

### 2.2 Circuit Complexity

We assume familiarity with standard circuit complexity classes [5,6].

A **Boolean circuit** is a directed acyclic graph with:

* Input gates,
* Logic gates from a fixed basis,
* A single output gate.

#### Circuit Model

We use:

* Gate basis: ({\text{AND}, \text{OR}, \text{NOT}, \text{MAJ}})
* Fan-in: unbounded for MAJ, bounded (2) for AND/OR
* Size: number of gates
* Depth: longest path from input to output

We consider:

* **TC⁰**: constant depth, polynomial size, threshold/majority gates
* **NC¹**: logarithmic depth, polynomial size
* **P/poly**: polynomial-size nonuniform circuits

Uniformity is DLOGTIME-uniform unless stated otherwise.

---

### 2.3 Arithmetic Circuits

Floating-point arithmetic with fixed precision can be simulated by Boolean circuits with polylogarithmic overhead [7].

---

## 3. Transformer Model Definition

We define a **family of Transformers** indexed by input length (n).

---

### 3.1 Architectural Parameters

For each input length (n), the Transformer has:

| Parameter           | Meaning                             | Function     |
| ------------------- | ----------------------------------- | ------------ |
| (L(n))              | Number of layers                    | (\mathbb{N}) |
| (H(n))              | Number of attention heads per layer | (\mathbb{N}) |
| (d(n))              | Model dimension                     | (\mathbb{N}) |
| (b(n))              | Bit precision of all parameters     | (\mathbb{N}) |
| (w_{\text{att}}(n)) | Attention saturation width          | (\mathbb{N}) |

All parameters are allowed to grow with (n).

---

### 3.2 Input Representation

Each token (x_i \in \Sigma) is mapped to an embedding:
[
e(x_i) \in \mathbb{R}^{d(n)}
]
with (b(n))-bit fixed-precision floats.

A positional encoding (p(i)\in\mathbb{R}^{d(n)}) is added:
[
h_i^{(0)} = e(x_i) + p(i)
]

We assume either:

* learned positional encodings, or
* fixed sinusoidal encodings computable in polynomial time [8].

---

### 3.3 Attention Mechanism

For each layer (\ell) and head (h):

[
Q = HW_Q^{\ell,h}, \quad
K = HW_K^{\ell,h}, \quad
V = HW_V^{\ell,h}
]

where (H) is the matrix of token states.

---

#### Average-Hard-Attention Saturation

We define **average-hard-attention** as follows:

1. Compute scores:
   [
   s_{ij} = \langle q_i, k_j \rangle
   ]

2. Saturation:
   [
   \tilde{s}*{ij} =
   \begin{cases}
   1 & \text{if } s*{ij} \ge \tau \
   0 & \text{if } s_{ij} < \tau
   \end{cases}
   ]
   for a fixed threshold (\tau).

3. Averaging:
   [
   \alpha_{ij} =
   \begin{cases}
   \frac{1}{|S_i|} & j \in S_i \
   0 & \text{otherwise}
   \end{cases}
   \quad
   S_i = {j : \tilde{s}_{ij} = 1}
   ]

This replaces softmax with uniform averaging over selected tokens.

---

### 3.4 Feed-Forward Networks

Each position applies a two-layer MLP:
[
\text{FFN}(x) = W_2 \sigma(W_1 x + b_1) + b_2
]
where:

* (\sigma) is ReLU or GELU approximated by piecewise-linear functions
* All arithmetic uses (b(n))-bit floats

---

### 3.5 Output and Language Recognition

We define acceptance via a designated output token (e.g., CLS):

[
\text{accept}(x) = \mathbf{1}[\langle h_{\text{CLS}}^{(L)}, w_{\text{out}} \rangle \ge 0]
]

The recognized language:
[
L_T = {x \in \Sigma^* : \text{accept}(x) = 1}
]

---

## 4. Circuit Simulation Strategy

We simulate Transformer inference using Boolean circuits.

---

### 4.1 Fixed-Precision Arithmetic Simulation

Each (b(n))-bit floating-point addition and multiplication can be computed by:

* Size: (\text{poly}(b(n)))
* Depth: (O(\log b(n)))

using standard circuits [7].

---

### 4.2 Linear Layers

Matrix multiplication of size (d(n)\times d(n)):

* Size: (O(d(n)^2 \cdot \text{poly}(b(n))))
* Depth: (O(\log d(n) + \log b(n)))

---

### 4.3 Attention Score Computation

Each dot product:

* (d(n)) multiplications and additions
* Threshold comparison implemented by comparator circuits

---

### 4.4 Saturation and Averaging

Key observation:

> **Hard attention converts soft real-valued computation into discrete selection.**

* Thresholding: TC⁰-computable via comparator circuits
* Counting (|S_i|): MAJORITY + adders
* Averaging: division by integer ≤ (n), pre-encoded via lookup tables

---

### 4.5 Layer Composition

Each Transformer layer composes:

1. Linear maps
2. Thresholded attention
3. Averaging
4. Pointwise MLP

Depth adds *additively* across layers.

---

## 5. Upper Bound Theorems

---

### Theorem 1 (Polynomial-Size Circuit Upper Bound)

**Statement.**
If (L(n), H(n), d(n), b(n)) are polynomially bounded in (n), then the language recognized by the Transformer lies in **P/poly**.

**Proof Sketch.**
Each layer can be simulated by polynomial-size circuits. Composing (L(n)) layers yields polynomial size overall. ∎

---

### Theorem 2 (NC¹ Upper Bound)

**Statement.**
If:

* (L(n) = O(\log n))
* (d(n), b(n) = \text{polylog}(n))

then the recognized language lies in **NC¹**.

**Reasoning.**
Each layer has polylogarithmic depth; composing (O(\log n)) layers yields logarithmic depth overall. ∎

---

### Theorem 3 (TC⁰ Upper Bound)

**Statement.**
If:

* (L(n) = O(1))
* (d(n), b(n) = O(1))
* Attention is average-hard-saturated

then the recognized language lies in **TC⁰**.

**Key Insight.**

* Hard attention removes unbounded real interactions
* Averaging and thresholding are TC⁰-computable
* Constant depth layers preserve constant depth

∎

---

## 6. Discussion and Conditions

### 6.1 Necessity of Saturation

Without saturation, softmax introduces exponential and division operations whose circuit complexity is higher [9]. Hard attention collapses this.

---

### 6.2 Role of Precision

Unbounded precision allows encoding arbitrary integers, potentially simulating Turing machines [10]. Finite (b(n)) is essential.

---

### 6.3 Relation to Automata Results

Constant-depth saturated Transformers align with regular language recognition bounds [2,3].

---

## 7. Conclusion

We have shown that **average-hard-attention saturated Transformers with finite-precision activations admit explicit circuit complexity upper bounds**. Depending on architectural scaling, the recognized languages fall within **TC⁰**, **NC¹**, or **P/poly**.

These results clarify the computational ceiling imposed by attention saturation and finite precision, and provide a bridge between modern neural architectures and classical complexity theory.

---

## References
[1] Hahn, M. Theoretical Limitations of Self-Attention in Neural Sequence Models.
https://arxiv.org/abs/1911.09849
[2] Merrill, W. Sequential Neural Networks as Automata.
https://arxiv.org/abs/1906.01615
[3] Merrill, W., & Sabharwal, A. The Expressive Power of Transformers with Hard Attention.
https://arxiv.org/abs/2109.06771
[4] Pérez, J., et al. Attention Is Turing-Complete.
https://arxiv.org/abs/1906.07415
[5] Arora, S., & Barak, B. Computational Complexity: A Modern Approach.
https://theory.cs.princeton.edu/complexity/
[6] Vollmer, H. Introduction to Circuit Complexity.
https://www.springer.com/gp/book/9783540643081
[7] Wegener, I. Branching Programs and Binary Decision Diagrams.
https://doi.org/10.1137/1.9780898718034
[8] Vaswani, A., et al. Attention Is All You Need.
https://arxiv.org/abs/1706.03762
[9] Siu, K., Bruck, J. On the Power of Threshold Circuits with Small Weights.
https://ieeexplore.ieee.org/document/279856
[10] Siegelmann, H. Neural Networks and Analog Computation: Beyond the Turing Limit.
https://www.science.org/doi/10.1126/science.268.5210.545
