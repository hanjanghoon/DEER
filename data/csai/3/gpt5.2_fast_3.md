# On the Equivalence Between L1-Constrained and L1-Penalized Lasso Regression

## Abstract

Lasso regression can be formulated either as a constrained optimization problem with an explicit bound on the ℓ₁-norm of the coefficient vector or as a penalized optimization problem in which the ℓ₁-norm appears as a regularization term in the objective. Although these two formulations are often treated as interchangeable in practice, their equivalence is subtle and depends on precise mathematical conditions. This report provides a rigorous investigation of the relationship between the L1-constrained and L1-penalized Lasso formulations. We explicitly state both optimization problems, derive the associated Lagrangian and Karush–Kuhn–Tucker (KKT) conditions, and analyze when a one-to-one correspondence between the constraint radius ( t ) and penalty parameter ( \lambda ) exists. We distinguish cases in which the constraint is binding versus slack, examine the behavior of solution paths as parameters vary, and discuss edge cases involving degeneracy, non-uniqueness, and scaling. The analysis is grounded in convex optimization theory and clarifies both theoretical and practical implications for model selection and numerical optimization.

---

## 1. Introduction

The Lasso (Least Absolute Shrinkage and Selection Operator) occupies a central position in modern statistical learning and convex optimization due to its ability to perform simultaneous estimation and variable selection in high-dimensional linear models [1]. Since its introduction, two mathematically equivalent-looking but operationally distinct formulations have been widely used. One formulation constrains the ℓ₁-norm of the coefficient vector, while the other penalizes the ℓ₁-norm in the objective function.

In applied work, these formulations are often treated as interchangeable, with the choice between them considered a matter of convenience or algorithmic preference. However, from an optimization-theoretic standpoint, the equivalence between constrained and penalized formulations is not automatic. It hinges on convex duality, constraint qualification, and the behavior of optimal Lagrange multipliers. In particular, while it is commonly stated that there exists a mapping between the constraint radius ( t ) and the penalty parameter ( \lambda ), this mapping need not be one-to-one in all regimes, and it may fail entirely in certain edge cases.

The goal of this report is to provide a rigorous and self-contained analysis of the relationship between the L1-constrained and L1-penalized Lasso formulations. We explicitly write down both problems, state standard preprocessing assumptions on the design matrix and response, derive the Lagrangian and KKT conditions, and analyze under what mathematical conditions the two formulations yield identical solution sets. We further examine how solution paths evolve as parameters change and discuss implications for non-uniqueness, degeneracy, and numerical solvers.

---

## 2. Problem Setup and Preprocessing Assumptions

### 2.1 Linear Regression Model

Let ( X \in \mathbb{R}^{n \times p} ) denote a fixed design matrix and ( y \in \mathbb{R}^n ) a response vector. We consider the standard linear regression model
[
y = X\beta + \varepsilon,
]
where ( \beta \in \mathbb{R}^p ) is the coefficient vector and ( \varepsilon ) is an error term.

### 2.2 Standardization and Centering

To simplify the analysis and ensure comparability across coordinates, it is standard to assume that the columns of ( X ) are centered and scaled such that
[
\frac{1}{n} \sum_{i=1}^n X_{ij} = 0, \quad \frac{1}{n} \sum_{i=1}^n X_{ij}^2 = 1,
]
for each feature ( j = 1, \dots, p ), and that the response vector ( y ) is centered so that ( \sum_{i=1}^n y_i = 0 ) [2]. Under these assumptions, no intercept term is required, and the ℓ₁ penalty treats all coefficients symmetrically.

While these preprocessing steps are not strictly required for theoretical equivalence, they simplify interpretation and avoid trivial rescalings of ( \lambda ) or ( t ) induced by feature scaling.

---

## 3. The L1-Penalized (Regularized) Lasso Formulation

### 3.1 Optimization Problem

The L1-penalized Lasso problem is defined as
[
\min_{\beta \in \mathbb{R}^p}
; \frac{1}{2} |y - X\beta|_2^2 + \lambda |\beta|_1,
]
where ( \lambda \ge 0 ) is a regularization parameter.

### 3.2 Convexity and Existence of Solutions

The objective function is convex in ( \beta ) because it is the sum of a convex quadratic loss and a convex ℓ₁ norm. Therefore, a global minimizer exists for all ( \lambda \ge 0 ) [3]. For ( \lambda > 0 ), the problem is coercive, guaranteeing existence even when ( X ) is rank-deficient.

### 3.3 Subgradient Optimality Conditions

Because the ℓ₁ norm is not differentiable at zero, optimality conditions are expressed using subgradients. A vector ( \hat{\beta} ) is optimal if and only if
[
X^\top (X\hat{\beta} - y) + \lambda z = 0,
]
where ( z \in \partial |\hat{\beta}|_1 ), with
[
z_j =
\begin{cases}
\operatorname{sign}(\hat{\beta}_j), & \hat{\beta}_j \neq 0, \
\in [-1, 1], & \hat{\beta}_j = 0.
\end{cases}
]

These conditions characterize sparsity through the geometry of the ℓ₁ ball.

---

## 4. The L1-Constrained Lasso Formulation

### 4.1 Optimization Problem

The L1-constrained Lasso problem is defined as
[
\min_{\beta \in \mathbb{R}^p}
; \frac{1}{2} |y - X\beta|_2^2
\quad \text{subject to} \quad |\beta|_1 \le t,
]
where ( t \ge 0 ) is a constraint radius.

### 4.2 Feasibility and Convexity

The feasible set ( {\beta : |\beta|_1 \le t} ) is a closed, convex, and compact set. The objective function is continuous and convex, ensuring the existence of at least one optimal solution for all ( t \ge 0 ) [3].

---

## 5. Lagrangian Formulation and Duality

### 5.1 Lagrangian Construction

The Lagrangian for the constrained problem is
[
\mathcal{L}(\beta, \lambda) =
\frac{1}{2} |y - X\beta|_2^2 + \lambda (|\beta|_1 - t),
]
where ( \lambda \ge 0 ) is the Lagrange multiplier associated with the ℓ₁ constraint.

### 5.2 Connection to Penalized Formulation

For a fixed ( \lambda ), minimizing ( \mathcal{L}(\beta, \lambda) ) over ( \beta ) is equivalent to solving the penalized Lasso problem with penalty parameter ( \lambda ), up to the additive constant ( -\lambda t ). This observation underlies the commonly asserted equivalence between the two formulations.

---

## 6. Karush–Kuhn–Tucker Conditions

### 6.1 KKT Conditions for the Constrained Problem

A pair ( (\hat{\beta}, \hat{\lambda}) ) is optimal if and only if the following conditions hold:

1. **Primal feasibility**:
   [
   |\hat{\beta}|_1 \le t.
   ]

2. **Dual feasibility**:
   [
   \hat{\lambda} \ge 0.
   ]

3. **Complementary slackness**:
   [
   \hat{\lambda}(|\hat{\beta}|_1 - t) = 0.
   ]

4. **Stationarity**:
   [
   X^\top (X\hat{\beta} - y) + \hat{\lambda} z = 0,
   ]
   where ( z \in \partial |\hat{\beta}|_1 ).

### 6.2 Binding vs. Slack Constraints

If ( |\hat{\beta}|_1 < t ), the constraint is slack and complementary slackness implies ( \hat{\lambda} = 0 ). In this case, the solution coincides with the ordinary least squares estimator, provided it exists.

If ( |\hat{\beta}|_1 = t ), the constraint is binding and ( \hat{\lambda} > 0 ). Only in this regime does the constrained solution correspond to a penalized Lasso solution with ( \lambda = \hat{\lambda} ).

---

## 7. Parameter Correspondence Between ( t ) and ( \lambda )

### 7.1 Existence of a Correspondence

For every ( \lambda > 0 ), let ( \hat{\beta}(\lambda) ) denote a solution to the penalized problem and define ( t(\lambda) = |\hat{\beta}(\lambda)|_1 ). Then ( \hat{\beta}(\lambda) ) is feasible and optimal for the constrained problem with radius ( t(\lambda) ) [4].

Conversely, for a constrained problem with binding constraint and corresponding multiplier ( \hat{\lambda} > 0 ), the solution is optimal for the penalized problem with parameter ( \lambda = \hat{\lambda} ).

### 7.2 Non-Uniqueness and Flat Regions

The mapping ( \lambda \mapsto t(\lambda) ) is non-increasing but not necessarily strictly decreasing. In regions where the active set does not change, ( \hat{\beta}(\lambda) ) varies linearly in ( \lambda ), but the ℓ₁ norm may remain constant over an interval, leading to non-unique correspondences [5].

---

## 8. Solution Paths and Regularization Geometry

### 8.1 Penalized Path

As ( \lambda ) decreases from ( +\infty ) to ( 0 ), the penalized Lasso solution path traces a piecewise linear trajectory in coefficient space. Variables enter and leave the active set at discrete breakpoints, a property exploited by the LARS algorithm [6].

### 8.2 Constrained Path

As ( t ) increases from ( 0 ) to ( |\hat{\beta}_{\text{OLS}}|_1 ), the constrained solution path follows the boundary of the ℓ₁ ball until the constraint becomes slack. The path is also piecewise linear but parameterized differently.

### 8.3 Equivalence of Paths

When restricted to regions where the constraint is binding, the two paths coincide up to reparameterization. Differences arise only when the constraint becomes slack or when multiple solutions exist.

---

## 9. Edge Cases and Pathological Scenarios

### 9.1 Zero and Infinite Parameters

For ( \lambda = 0 ), the penalized problem reduces to ordinary least squares, while the constrained problem corresponds only if ( t ) is sufficiently large. For ( t = 0 ), the constrained solution is identically zero, corresponding to the penalized solution as ( \lambda \to \infty ).

### 9.2 Rank Deficiency and Non-Uniqueness

If ( X ) is rank-deficient, solutions may be non-unique. In such cases, multiple constrained radii may correspond to the same penalized solution set, and vice versa [3].

---

## 10. Numerical Considerations and KKT Diagnostics

In numerical implementations, equivalence is assessed up to solver tolerance. For a candidate solution ( \hat{\beta} ), one can compute KKT residuals
[
r_{\text{stat}} = |X^\top (X\hat{\beta} - y) + \lambda z|_\infty,
]
and primal feasibility gaps ( \max(0, |\hat{\beta}|_1 - t) ). Practical solvers report convergence when these quantities fall below predefined tolerances, typically on the order of ( 10^{-6} ) to ( 10^{-8} ) [7].

---

## 11. Implications for Practice and Theory

The analysis shows that the L1-constrained and L1-penalized Lasso formulations are equivalent only under binding constraints and appropriate dual correspondence. From a theoretical perspective, this clarifies the precise sense in which the two problems are “the same.” From a practical standpoint, it explains why cross-validation over ( \lambda ) and constraint-based formulations may yield subtly different models in finite samples or under numerical approximations.

---

## 12. Conclusion

The L1-constrained and L1-penalized Lasso formulations are connected through convex duality and the KKT conditions, but their equivalence is conditional rather than absolute. A one-to-one correspondence between ( t ) and ( \lambda ) exists only when the ℓ₁ constraint is binding and the associated Lagrange multiplier is positive. Understanding this distinction is essential for both theoretical clarity and reliable practical implementation. This report provides a rigorous foundation for interpreting and applying Lasso regression across different formulations.

---

## References

[1] Tibshirani, R. Regression Shrinkage and Selection via the Lasso – https://www.jstor.org/stable/2346178
[2] Hastie, T., Tibshirani, R., Friedman, J. The Elements of Statistical Learning – https://hastie.su.domains/ElemStatLearn/
[3] Boyd, S., Vandenberghe, L. Convex Optimization – https://web.stanford.edu/~boyd/cvxbook/
[4] Bertsekas, D. P. Nonlinear Programming – https://athenasc.com/nonlinbook.html
[5] Osborne, M. R., Presnell, B., Turlach, B. A. On the Lasso and its Dual – https://doi.org/10.1198/016214504000000818
[6] Efron, B., Hastie, T., Johnstone, I., Tibshirani, R. Least Angle Regression – https://projecteuclid.org/euclid.aos/1083178935
[7] Nocedal, J., Wright, S. Numerical Optimization – https://link.springer.com/book/10.1007/978-0-387-40065-5
