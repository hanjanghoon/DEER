# Computational Scaling Properties of Transformer Pretraining

## A Technical Analysis of FLOPs, Architectural Parameters, and Context Length Expansion

---

## Abstract

Transformer-based language models have become the dominant paradigm for large-scale language modeling, with pretraining costs now reaching hundreds of millions to trillions of floating-point operations (FLOPs). Understanding how computational cost scales with architectural parameters is therefore central to model design, hardware planning, and research prioritization. This report provides a comprehensive technical analysis of the computational scaling properties of standard transformer architectures during pretraining. We focus on the dependence of total FLOPs on context length (L), model dimension (d_{\text{model}}), feed-forward dimension (d_{\text{ff}}), number of layers, and number of training tokens. Particular emphasis is placed on the distinct scaling behaviors of self-attention and feed-forward network (FFN) components.

As a central case study, we analyze a scenario in which the pretraining context length is increased from (L) to (4L) while the total number of training tokens is held constant. We derive the resulting change in total computational cost, show how the quadratic dependence of attention on sequence length dominates under fixed-token budgets, and discuss the practical implications for long-context language model training. Throughout, we ground the analysis in established transformer formulations and empirical scaling literature.

---

# 1. Introduction

The rapid growth of large language models (LLMs) has been enabled not only by algorithmic innovations but also by careful management of computational resources. Since the introduction of the Transformer architecture, self-attention–based models have demonstrated superior scaling behavior compared to recurrent or convolutional alternatives, particularly in parallel training regimes [1]. However, this scalability comes with nontrivial computational trade-offs, especially as models grow in width, depth, and context length.

Pretraining a transformer-based language model typically involves minimizing an autoregressive or masked language modeling objective over a very large corpus of tokens. The total training cost is therefore determined by two interacting factors:

1. **The cost per token**, which depends on the architecture.
2. **The total number of tokens processed**, which is often fixed by data availability or training budget.

Recent trends—such as extending context lengths to tens or hundreds of thousands of tokens—raise fundamental questions about how computational cost scales and whether such extensions are feasible under fixed budgets [2]. This report aims to provide a clear, quantitative account of these scaling properties.

---

# 2. Standard Transformer Architecture Overview

## 2.1 High-Level Structure

A standard transformer language model consists of a stack of (N) identical layers. Each layer typically includes:

1. A multi-head self-attention (MHSA) sublayer.
2. A position-wise feed-forward network (FFN).
3. Residual connections and layer normalization.

Let:

* (L) denote the context length (sequence length).
* (d_{\text{model}}) denote the model (hidden) dimension.
* (d_{\text{ff}}) denote the inner dimension of the feed-forward network.
* (h) denote the number of attention heads.

In most practical architectures, (d_{\text{ff}}) is proportional to (d_{\text{model}}), often (d_{\text{ff}} \approx 4 d_{\text{model}}) [1].

---

## 2.2 Token and Layer-Level Computation

The computational cost of pretraining can be decomposed into:

* FLOPs per layer per sequence.
* FLOPs per token.
* FLOPs per training step (batch).
* Total FLOPs over all training tokens.

This decomposition allows us to isolate how individual architectural choices affect scaling.

---

# 3. FLOPs Accounting Methodology

## 3.1 Definition of FLOPs

We adopt the standard convention that one floating-point multiply-add (FMA) counts as two FLOPs. This convention is widely used in analyses of transformer training cost [3].

## 3.2 Scope of Analysis

We focus on:

* Forward pass FLOPs.
* Backward pass FLOPs, which are approximately a constant multiple of the forward pass.

Empirically, the backward pass typically costs about 2× the forward pass, yielding a total of roughly 3× forward FLOPs per training step [3]. Since this factor applies uniformly, we focus on forward-pass scaling and apply a constant multiplier where needed.

---

# 4. Computational Cost of Self-Attention

## 4.1 Linear Projections: Q, K, V

For each token, queries, keys, and values are computed via linear projections:
[
Q = XW_Q,\quad K = XW_K,\quad V = XW_V,
]
where (X \in \mathbb{R}^{L \times d_{\text{model}}}).

Each projection costs:
[
\mathcal{O}(L \cdot d_{\text{model}}^2).
]

Across Q, K, and V:
[
\text{FLOPs}*{\text{QKV}} \sim 3 L d*{\text{model}}^2.
]

---

## 4.2 Attention Score Computation

Attention scores are computed as:
[
A = \frac{QK^\top}{\sqrt{d_k}},
]
where (Q, K \in \mathbb{R}^{L \times d_k}) and (d_k = d_{\text{model}} / h).

This matrix multiplication costs:
[
\mathcal{O}(L^2 d_{\text{model}}).
]

This quadratic dependence on (L) is the defining feature of standard self-attention [1].

---

## 4.3 Attention-Value Product

Multiplying attention weights by values:
[
\text{softmax}(A) V
]
also costs:
[
\mathcal{O}(L^2 d_{\text{model}}).
]

---

## 4.4 Output Projection

The concatenated attention output is projected back to (d_{\text{model}}), costing:
[
\mathcal{O}(L d_{\text{model}}^2).
]

---

## 4.5 Total Self-Attention FLOPs per Layer

Combining all components:
[
\text{FLOPs}*{\text{attn}} \sim \mathcal{O}(L d*{\text{model}}^2 + L^2 d_{\text{model}}).
]

For sufficiently large (L), the (L^2 d_{\text{model}}) term dominates.

---

# 5. Computational Cost of Feed-Forward Networks

## 5.1 Structure of the FFN

A standard FFN consists of two linear transformations with a nonlinearity:
[
\text{FFN}(x) = \sigma(xW_1) W_2,
]
where:

* (W_1 \in \mathbb{R}^{d_{\text{model}} \times d_{\text{ff}}}),
* (W_2 \in \mathbb{R}^{d_{\text{ff}} \times d_{\text{model}}}).

---

## 5.2 FLOPs per Token

Per token, the FFN cost is:
[
\mathcal{O}(d_{\text{model}} d_{\text{ff}}).
]

---

## 5.3 FLOPs per Sequence

For a sequence of length (L):
[
\text{FLOPs}*{\text{ffn}} \sim \mathcal{O}(L d*{\text{model}} d_{\text{ff}}).
]

Crucially, this term scales **linearly** with (L), unlike attention.

---

# 6. Total FLOPs per Layer and per Token

## 6.1 Per-Layer FLOPs

Summing attention and FFN costs:
[
\text{FLOPs}*{\text{layer}} \sim \mathcal{O}(L^2 d*{\text{model}} + L d_{\text{model}}^2 + L d_{\text{model}} d_{\text{ff}}).
]

In common regimes where (d_{\text{ff}} \propto d_{\text{model}}), this simplifies to:
[
\text{FLOPs}*{\text{layer}} \sim \mathcal{O}(L^2 d*{\text{model}} + L d_{\text{model}}^2).
]

---

## 6.2 FLOPs per Token

Dividing by (L):
[
\text{FLOPs}*{\text{token}} \sim \mathcal{O}(L d*{\text{model}} + d_{\text{model}}^2).
]

This expression highlights that:

* Attention cost per token grows linearly with (L).
* FFN cost per token is independent of (L).

---

# 7. Total Pretraining Cost Under a Fixed Token Budget

## 7.1 Total Training Tokens

Let:

* (T) be the total number of tokens seen during pretraining.
* (L) be the context length.

The number of sequences processed is:
[
\frac{T}{L}.
]

---

## 7.2 Total FLOPs

Total training FLOPs scale as:
[
\text{FLOPs}*{\text{total}} \sim \frac{T}{L} \cdot N \cdot \text{FLOPs}*{\text{layer}}.
]

Substituting:
[
\text{FLOPs}*{\text{total}} \sim T N \left( L d*{\text{model}} + d_{\text{model}}^2 \right).
]

---

# 8. Case Study: Increasing Context Length from (L) to (4L)

## 8.1 Assumptions

We consider:

* Total tokens (T) fixed.
* Model depth (N), (d_{\text{model}}), and (d_{\text{ff}}) fixed.
* Standard quadratic self-attention.

---

## 8.2 Original Cost

[
\text{FLOPs}*{\text{orig}} \sim T N \left( L d*{\text{model}} + d_{\text{model}}^2 \right).
]

---

## 8.3 New Cost with Context Length (4L)

[
\text{FLOPs}*{\text{new}} \sim T N \left( 4L d*{\text{model}} + d_{\text{model}}^2 \right).
]

---

## 8.4 Relative Change in FLOPs

The ratio is:
[
\frac{\text{FLOPs}*{\text{new}}}{\text{FLOPs}*{\text{orig}}}
============================================================

\frac{4L d_{\text{model}} + d_{\text{model}}^2}{L d_{\text{model}} + d_{\text{model}}^2}.
]

---

## 8.5 Attention-Dominated Regime

When (L d_{\text{model}} \gg d_{\text{model}}^2), i.e., long-context regimes:
[
\frac{\text{FLOPs}*{\text{new}}}{\text{FLOPs}*{\text{orig}}} \approx 4.
]

Thus, **quadrupling context length approximately quadruples total compute**, even though the number of training tokens is unchanged.

---

## 8.6 FFN-Dominated Regime

When (d_{\text{model}}^2 \gg L d_{\text{model}}), i.e., short contexts:
[
\frac{\text{FLOPs}*{\text{new}}}{\text{FLOPs}*{\text{orig}}} \approx 1.
]

In this regime, increasing context length has little effect on total cost.

---

# 9. Practical Implications for Large Language Model Training

## 9.1 Compute Budget Allocation

These results explain why long-context pretraining is expensive even under fixed-token budgets and why many production models limit pretraining context length while enabling longer contexts only at inference time [2].

---

## 9.2 Architectural Innovations

The quadratic scaling of attention has motivated:

* Sparse attention mechanisms.
* Linear attention variants.
* State-space and recurrent alternatives.

These approaches aim to reduce or eliminate the (L^2) term [4].

---

## 9.3 Data Efficiency vs. Compute Efficiency

Longer contexts may improve sample efficiency but can degrade compute efficiency. Optimal training strategies must balance these effects, as suggested by empirical scaling laws [3].

---

# 10. Conclusion

This report has presented a detailed analysis of the computational scaling properties of transformer-based language model pretraining. By decomposing FLOPs into attention and feed-forward components, we showed that self-attention introduces a linear-in-(L) cost per token and dominates total compute in long-context regimes. In the central case study, increasing context length from (L) to (4L) while holding total tokens constant results in an approximately 4× increase in total computational cost when attention dominates.

These findings underscore the fundamental trade-offs involved in extending context length and highlight why architectural innovation in attention mechanisms remains a central research direction for scalable language modeling.

---

## References
[1] Vaswani et al., Attention Is All You Need – https://arxiv.org/abs/1706.03762
[2] Dao et al., FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness – https://arxiv.org/abs/2205.14135
[3] Kaplan et al., Scaling Laws for Neural Language Models – https://arxiv.org/abs/2001.08361
[4] Tay et al., Efficient Transformers: A Survey – https://arxiv.org/abs/2009.06732
