# Geometric Convergence of Value Iteration in Markov Decision Processes

## Abstract

Value iteration is a foundational dynamic programming algorithm for solving Markov Decision Processes (MDPs). Its convergence properties are central to both the theoretical understanding of optimal control and the practical design of reinforcement learning systems. This report investigates the precise conditions under which value iteration converges geometrically to the optimal value function. We provide formal definitions of MDPs, Bellman operators, and geometric (linear) convergence, and analyze how discounting, reward boundedness, and contraction properties jointly ensure convergence. We examine cases where convergence is guaranteed, situations where it may fail or slow dramatically, and practical factors affecting empirical behavior. We also discuss limitations of classical theory and highlight open questions related to undiscounted, average-reward, and large-scale settings.

---

## 1. Introduction

Markov Decision Processes (MDPs) provide a mathematically rigorous framework for sequential decision-making under uncertainty. Since the seminal work of Bellman, dynamic programming methods—most notably **value iteration**—have been central tools for computing optimal policies and value functions [1].

A key theoretical guarantee of value iteration is **convergence** to the optimal value function under suitable assumptions. Even more important for practice is the *rate* of convergence. In many settings, value iteration is known to converge **geometrically** (also called linearly), meaning that the error decreases by a constant multiplicative factor at each iteration. This property underpins complexity bounds, stopping criteria, and algorithmic design in reinforcement learning [2].

However, geometric convergence is not automatic. It depends delicately on discounting, reward structure, and the contraction properties of the Bellman optimality operator. Moreover, several important classes of problems—such as undiscounted or average-reward MDPs—fall outside the standard theory.

This report provides a comprehensive investigation of the conditions governing geometric convergence of value iteration. Our goals are:

* To precisely define the mathematical objects involved.
* To explain why discounting induces contraction and geometric convergence.
* To analyze failure modes and slow-convergence regimes.
* To connect theory with practical considerations.
* To identify limitations and open research directions.

---

## 2. Markov Decision Processes: Definitions and Preliminaries

### 2.1 Definition of a Markov Decision Process

A (finite) Markov Decision Process is defined by a tuple
[
\mathcal{M} = (\mathcal{S}, \mathcal{A}, P, R, \gamma),
]
where:

* (\mathcal{S}) is a finite set of states.
* (\mathcal{A}) is a finite set of actions.
* (P(s' \mid s, a)) is the transition probability from state (s) to state (s') given action (a).
* (R(s, a)) is the immediate reward received when taking action (a) in state (s).
* (\gamma \in [0,1]) is the discount factor.

We assume the MDP is **time-homogeneous** and **fully observable** [1].

### 2.2 Policies and Value Functions

A (stationary, deterministic) policy is a mapping (\pi : \mathcal{S} \to \mathcal{A}).

The **state-value function** of a policy (\pi) is defined as
[
V^\pi(s) = \mathbb{E}*\pi\left[ \sum*{t=0}^\infty \gamma^t R(s_t, a_t) \mid s_0 = s \right].
]

The **optimal value function** is
[
V^*(s) = \sup_\pi V^\pi(s).
]

When (\gamma < 1) and rewards are bounded, (V^\pi) and (V^*) are well-defined and finite [2].

---

## 3. The Bellman Optimality Operator

### 3.1 Definition

The Bellman optimality operator (T : \mathbb{R}^{|\mathcal{S}|} \to \mathbb{R}^{|\mathcal{S}|}) is defined as
[
(TV)(s) = \max_{a \in \mathcal{A}} \left[ R(s,a) + \gamma \sum_{s' \in \mathcal{S}} P(s' \mid s,a) V(s') \right].
]

The optimal value function (V^*) is a fixed point of (T):
[
V^* = T V^*.
]

This equation is known as the **Bellman optimality equation** [1].

### 3.2 Norms and Metric Structure

Convergence analysis typically uses the **supremum norm**:
[
|V|*\infty = \max*{s \in \mathcal{S}} |V(s)|.
]

This norm induces a complete metric space on (\mathbb{R}^{|\mathcal{S}|}), which is crucial for fixed-point arguments [3].

---

## 4. Value Iteration Algorithm

### 4.1 Algorithm Definition

Value iteration is defined recursively by
[
V_{k+1} = T V_k,
]
starting from an arbitrary initial function (V_0).

In practice, (V_0) is often initialized to zero or to a heuristic estimate.

### 4.2 Objective

The goal is to compute (V^*) by repeated application of the Bellman operator:
[
\lim_{k \to \infty} V_k = V^*.
]

The central question of this report is: **under what conditions does this convergence occur geometrically?**

---

## 5. Geometric Convergence: Definition and Meaning

### 5.1 Definition of Geometric Convergence

A sequence ({V_k}) converges geometrically to (V^*) if there exist constants (C > 0) and (\rho \in (0,1)) such that
[
|V_k - V^*|_\infty \le C \rho^k \quad \text{for all } k.
]

This implies that the error decreases exponentially fast in the number of iterations [4].

### 5.2 Why Geometric Convergence Matters

Geometric convergence provides:

* Explicit iteration complexity bounds.
* Reliable stopping criteria.
* Predictable numerical behavior.
* Robustness to initialization.

These properties are essential in large-scale and approximate dynamic programming [2].

---

## 6. Discounting and Contraction Properties

### 6.1 Bellman Operator as a Contraction

The key theoretical result is that when (\gamma \in [0,1)), the Bellman optimality operator (T) is a **(\gamma)-contraction** under the sup norm:
[
|T V - T W|*\infty \le \gamma |V - W|*\infty.
]

This follows from:

* Linearity of expectation.
* Boundedness of transition probabilities.
* The non-expansiveness of the max operator [1].

### 6.2 Banach Fixed-Point Theorem

By the Banach fixed-point theorem, any contraction mapping on a complete metric space has:

* A unique fixed point.
* Iterative convergence from any starting point.
* Geometric convergence rate governed by the contraction modulus (\gamma) [3].

Thus, for discounted MDPs with (\gamma < 1),
[
|V_k - V^*|_\infty \le \gamma^k |V_0 - V^*|_\infty.
]

This establishes **geometric convergence**.

---

## 7. Role of Rewards and Boundedness

### 7.1 Bounded Rewards

If rewards are bounded, i.e.,
[
|R(s,a)| \le R_{\max},
]
then the value function is also bounded:
[
|V^*|*\infty \le \frac{R*{\max}}{1 - \gamma}.
]

This ensures that value iteration remains numerically stable [2].

### 7.2 Unbounded Rewards

If rewards are unbounded, the value function may diverge even when (\gamma < 1). In such cases:

* Fixed points may not exist.
* Contraction arguments fail.
* Value iteration may oscillate or diverge [5].

---

## 8. Circumstances Guaranteeing Geometric Convergence

Geometric convergence of value iteration is guaranteed under the following conditions:

1. **Finite state and action spaces**.
2. **Discount factor (\gamma < 1)**.
3. **Bounded rewards**.
4. **Exact Bellman updates** (no approximation error).

Under these assumptions, convergence is global, monotone (under suitable initialization), and geometric [1][2].

---

## 9. Circumstances Where Convergence May Fail

### 9.1 Undiscounted MDPs ((\gamma = 1))

When (\gamma = 1), the Bellman operator is no longer a contraction:
[
|T V - T W|*\infty \le |V - W|*\infty.
]

In this case:

* Fixed points may not be unique.
* Value iteration may converge slowly, oscillate, or diverge.
* Special structural assumptions are required (e.g., stochastic shortest path problems) [6].

### 9.2 Average-Reward MDPs

In average-reward formulations, the objective is to maximize long-run average reward rather than discounted return. Classical value iteration does not directly apply, and geometric convergence generally fails without algorithmic modification [7].

### 9.3 Approximate Value Iteration

In practice, Bellman updates are often approximate due to:

* Function approximation.
* Sampling error.
* Truncated backups.

Approximation errors can destroy contraction properties, leading to:

* Bias.
* Error floors.
* Divergence in off-policy settings [8].

---

## 10. Practical Factors Affecting Convergence Speed

### 10.1 Discount Factor Close to One

As (\gamma \to 1), the contraction modulus approaches one, and convergence becomes arbitrarily slow:
[
|V_k - V^*|_\infty \approx \gamma^k.
]

This phenomenon is well-documented in practice and motivates alternatives such as policy iteration or acceleration techniques [2].

### 10.2 State Space Structure

The effective convergence rate may depend on:

* Transition graph diameter.
* Presence of nearly absorbing states.
* Reward sparsity.

Even with theoretical geometric convergence, empirical convergence may appear slow [9].

---

## 11. Illustrative Example

Consider a two-state MDP with rewards (R(s,a) \in [0,1]) and discount factor (\gamma = 0.9). Value iteration converges geometrically with rate (0.9), halving the error approximately every 7 iterations:
[
0.9^7 \approx 0.48.
]

If (\gamma = 0.99), the same error reduction requires about 69 iterations:
[
0.99^{69} \approx 0.5.
]

This example illustrates how discounting controls convergence speed [2].

---

## 12. Limitations and Open Questions

### 12.1 Large and Continuous State Spaces

In continuous or high-dimensional state spaces, exact value iteration is infeasible. Whether approximate methods retain geometric convergence remains an open and context-dependent question [8].

### 12.2 Beyond Discounting

Finding alternative conditions that guarantee contraction without discounting—such as weighted norms or span seminorms—remains an active area of research [7].

### 12.3 Interaction with Learning Dynamics

In reinforcement learning, value iteration is often embedded in stochastic approximation schemes. Understanding how geometric convergence interacts with sampling noise is an open problem [10].

---

## 13. Conclusion

Geometric convergence of value iteration is a powerful and elegant result rooted in contraction mapping theory. Discounting, bounded rewards, and finite state spaces jointly ensure that the Bellman operator is a contraction, yielding fast and reliable convergence to the optimal value function.

However, this theory has sharp boundaries. When discounting is removed, rewards are unbounded, or approximations are introduced, geometric convergence can fail. Understanding and extending convergence guarantees beyond the classical discounted setting remains a central challenge in modern reinforcement learning and optimal control.

---

## References
[1] Richard S. Sutton and Andrew G. Barto, Reinforcement Learning: An Introduction – http://incompleteideas.net/book/the-book.html
[2] Dimitri P. Bertsekas, Dynamic Programming and Optimal Control, Vol. I – https://www.athenasc.com/dpbook.html
[3] Walter Rudin, Principles of Mathematical Analysis – https://www.mheducation.com/highered/product/principles-mathematical-analysis-rudin/M9780070542358.html
[4] Heinz H. Bauschke and Patrick L. Combettes, Convex Analysis and Monotone Operator Theory in Hilbert Spaces – https://link.springer.com/book/10.1007/978-3-319-48311-5
[5] Martin L. Puterman, Markov Decision Processes: Discrete Stochastic Dynamic Programming – https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887
[6] Bertsekas and Tsitsiklis, Neuro-Dynamic Programming – https://www.athenasc.com/ndpbook.html
[7] Peter A. Schweitzer and Abraham Seidmann, “Generalized Polynomial Convergence of Value Iteration” – https://doi.org/10.1287/opre.33.4.953
[8] Tsitsiklis and Van Roy, “An Analysis of Temporal-Difference Learning with Function Approximation” – https://web.mit.edu/jnt/www/Papers/J090-97-td.pdf
[9] Littman, Dean, and Kaelbling, “On the Complexity of Solving Markov Decision Problems” – https://dl.acm.org/doi/10.5555/645528.657613
[10] Borkar, Stochastic Approximation: A Dynamical Systems Viewpoint – https://www.springer.com/gp/book/9788132227952
