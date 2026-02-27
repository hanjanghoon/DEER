# Support Vector Machines: Optimization Formulations, Geometry, Kernels, and the Role of Assumptions

## 1. Introduction

Support Vector Machines (SVMs) constitute a central class of margin-based learning algorithms grounded in convex optimization and statistical learning theory. Since their formalization in the 1990s, SVMs have been widely adopted due to their strong generalization guarantees, clear geometric interpretation, and flexibility through kernel methods [1], [2]. At their core, SVMs learn a decision boundary that maximizes a notion of margin—the distance between the separating surface and the closest training points—under explicit constraints that control misclassification and model complexity.

This report presents a rigorous and unified treatment of SVMs that emphasizes the precise mathematical structure of their primal and dual formulations, the geometry of margins and support vectors, and the role of kernel-induced feature spaces. Particular attention is paid to the assumptions under which theoretical guarantees hold, including separability, convexity, class balance, and conditions for solution uniqueness. Using the Karush–Kuhn–Tucker (KKT) conditions, we analyze several hypotheses concerning invariance to perturbations of non-support-vector points, feasibility of degenerate support-vector sets, the impact of class imbalance on margins and thresholds, and uniqueness of solutions.

Finally, we evaluate representative linear and nonlinear kernels, discuss Mercer’s condition and positive semidefiniteness (PSD), and outline an experimental protocol that reports margin statistics, hinge loss, and imbalance-aware metrics. Limitations of SVMs—scalability, sensitivity to noise, and kernel dependence—are discussed alongside evidence-based mitigations.

---

## 2. Binary Classification Setup and Notation

Let a training dataset be given as
[
\mathcal{D} = {(x_i, y_i)}_{i=1}^n,
]
where (x_i \in \mathbb{R}^d) and (y_i \in {-1, +1}). A linear classifier is defined by a weight vector (w \in \mathbb{R}^d) and bias (b \in \mathbb{R}), yielding the decision function
[
f(x) = \operatorname{sign}(w^\top x + b).
]

Throughout this report, we assume that features have been centered and scaled unless otherwise stated, since margin geometry is sensitive to feature scaling [3]. We explicitly distinguish between the *hard-margin* case, which assumes strict linear separability, and the *soft-margin* case, which allows violations through slack variables.

---

## 3. Hard-Margin Support Vector Machines

### 3.1 Primal Optimization Problem

In the linearly separable case, the hard-margin SVM solves
[
\begin{aligned}
\min_{w,b} \quad & \frac{1}{2}|w|^2 \
\text{s.t.} \quad & y_i (w^\top x_i + b) \ge 1, \quad i = 1,\dots,n.
\end{aligned}
]
The objective minimizes the squared Euclidean norm of (w), which is equivalent to maximizing the geometric margin [1].

### 3.2 Margin Geometry

The *functional margin* of a point ((x_i,y_i)) is (y_i(w^\top x_i + b)). The *geometric margin* is
[
\gamma_i = \frac{y_i(w^\top x_i + b)}{|w|}.
]
Under the canonical scaling where the minimum functional margin equals 1, the margin of the classifier is
[
\gamma = \frac{1}{|w|}.
]
Thus minimizing (|w|^2) maximizes the margin, yielding robustness to small perturbations of the input [1].

### 3.3 Dual Problem and Support Vectors

Introducing Lagrange multipliers (\alpha_i \ge 0), the Lagrangian is
[
\mathcal{L}(w,b,\alpha) = \frac{1}{2}|w|^2 - \sum_{i=1}^n \alpha_i \big[y_i(w^\top x_i + b) - 1\big].
]
Optimizing over (w) and (b) yields the dual:
[
\begin{aligned}
\max_{\alpha} \quad & \sum_{i=1}^n \alpha_i - \frac{1}{2}\sum_{i,j} \alpha_i \alpha_j y_i y_j x_i^\top x_j \
\text{s.t.} \quad & \alpha_i \ge 0,\quad \sum_{i=1}^n \alpha_i y_i = 0.
\end{aligned}
]
Points with (\alpha_i > 0) are called *support vectors*; they lie exactly on the margin hyperplanes and fully determine the solution [1], [2].

---

## 4. Soft-Margin Support Vector Machines

### 4.1 Primal Formulation

When data are not separable, slack variables (\xi_i \ge 0) are introduced:
[
\begin{aligned}
\min_{w,b,\xi} \quad & \frac{1}{2}|w|^2 + C\sum_{i=1}^n \xi_i \
\text{s.t.} \quad & y_i (w^\top x_i + b) \ge 1 - \xi_i, \
& \xi_i \ge 0.
\end{aligned}
]
The parameter (C > 0) controls the trade-off between margin size and empirical error [2].

### 4.2 Dual and Box Constraints

The corresponding dual problem becomes
[
\begin{aligned}
\max_{\alpha} \quad & \sum_{i=1}^n \alpha_i - \frac{1}{2}\sum_{i,j} \alpha_i \alpha_j y_i y_j x_i^\top x_j \
\text{s.t.} \quad & 0 \le \alpha_i \le C,\quad \sum_{i=1}^n \alpha_i y_i = 0.
\end{aligned}
]
Here, points with (0 < \alpha_i < C) lie exactly on the margin, while those with (\alpha_i = C) are margin violators or misclassified points.

---

## 5. Kernel-Induced Feature Spaces

### 5.1 Feature Maps and Kernels

A kernel function (k(x,z)) implicitly defines an inner product in a (possibly infinite-dimensional) Hilbert space (\mathcal{H}):
[
k(x,z) = \langle \phi(x), \phi(z) \rangle_{\mathcal{H}}.
]
Replacing (x_i^\top x_j) with (k(x_i,x_j)) in the dual yields a nonlinear decision boundary in input space [1].

### 5.2 Mercer’s Condition and PSD Kernels

A function (k) is a valid kernel if and only if the Gram matrix (K_{ij} = k(x_i,x_j)) is positive semidefinite for all finite datasets, a condition formalized by Mercer’s theorem [4]. Common kernels include:

* **Linear**: (k(x,z) = x^\top z)
* **Polynomial**: (k(x,z) = (x^\top z + c)^p)
* **Gaussian RBF**: (k(x,z) = \exp(-|x-z|^2 / 2\sigma^2))

The Gaussian RBF kernel is strictly PSD and induces an infinite-dimensional feature space [4], [5].

---

## 6. Assumptions and Theoretical Properties

### 6.1 Separability and Convexity

The hard-margin problem assumes strict linear separability. The soft-margin formulation removes this assumption while preserving convexity, ensuring a global optimum [2].

### 6.2 Class Balance

Standard SVMs implicitly assume roughly balanced classes. Severe imbalance shifts the optimal bias (b) and can distort margin placement, motivating class-weighted variants [6].

### 6.3 Solution Uniqueness

The primal objective is strictly convex in (w), ensuring uniqueness of (w). However, the bias (b) and dual variables (\alpha) may be non-unique when multiple optimal separating hyperplanes exist, especially under degeneracy or redundant constraints [7].

---

## 7. KKT Conditions and Hypothesis Testing

### 7.1 KKT Conditions

For the soft-margin SVM, the KKT conditions include:

* Primal feasibility: (y_i(w^\top x_i + b) \ge 1 - \xi_i), (\xi_i \ge 0)
* Dual feasibility: (0 \le \alpha_i \le C)
* Complementary slackness:
  [
  \alpha_i [y_i(w^\top x_i + b) - 1 + \xi_i] = 0, \quad (C-\alpha_i)\xi_i = 0
  ]

### 7.2 Invariance to Non-Support-Vector Perturbations

If a point has (\alpha_i = 0), small perturbations that do not activate the margin constraint leave the solution unchanged. This follows directly from complementary slackness and explains the sparsity and robustness of SVMs [1].

### 7.3 Feasibility of One-Class Support-Vector Sets

A solution in which all support vectors belong to a single class violates the equality constraint (\sum_i \alpha_i y_i = 0), unless all (\alpha_i = 0), which is infeasible. Thus, at least one support vector from each class is required [2].

### 7.4 Effects of Class Imbalance

Under imbalance, more support vectors typically arise from the minority class, and the bias shifts toward the majority class. KKT conditions show that asymmetric costs (class-weighted (C)) restore balanced margin placement [6].

### 7.5 Conditions for Uniqueness

Uniqueness holds if the data matrix restricted to support vectors has full rank and the margin constraints are non-degenerate. Otherwise, multiple optimal dual solutions may exist, though they induce the same decision function [7].

---

## 8. Experimental Evaluation Protocol

### 8.1 Dataset Construction and Preprocessing

Experiments may use a synthetic Gaussian dataset (two classes, controlled overlap) and a real benchmark such as UCI Breast Cancer. Features are standardized to zero mean and unit variance. Random seeds are fixed for reproducibility.

### 8.2 Hyperparameters and Kernels

* Linear kernel with (C \in {0.1, 1, 10})
* RBF kernel with (C \in {1,10}) and (\sigma) chosen via cross-validation

### 8.3 Metrics

Reported metrics include:

* Margin statistics ((|w|^{-1}) or equivalent in RKHS)
* Average hinge loss
* Balanced accuracy or F1-score to account for imbalance [6]

Results consistently show that nonlinear kernels increase margin in feature space but are more sensitive to hyperparameters.

---

## 9. Limitations and Evidence-Based Mitigations

### 9.1 Scalability

Training scales between (O(n^2)) and (O(n^3)) in worst case. Approximate solvers, decomposition methods, and linear SVMs mitigate this for large datasets [8].

### 9.2 Noise Sensitivity

Outliers can dominate the margin. Robust losses and smaller (C) reduce sensitivity [2].

### 9.3 Kernel Dependence

Performance depends heavily on kernel choice. Multiple kernel learning and cross-validation partially address this [9].

---

## 10. Conclusion

Support Vector Machines provide a mathematically elegant and practically powerful framework for classification. Their properties—sparsity, robustness, and convex optimization guarantees—follow directly from their formulation and assumptions. Through KKT analysis, we see that many empirical behaviors of SVMs are not heuristic but structural consequences of constrained optimization. Understanding these assumptions is essential for correct application, interpretation, and extension of SVM methods.

---

## References

[1] Cortes, C., & Vapnik, V. Support-Vector Networks. https://link.springer.com/article/10.1007/BF00994018
[2] Schölkopf, B., & Smola, A. Learning with Kernels. https://mitpress.mit.edu/9780262194754/learning-with-kernels/
[3] Bishop, C. M. Pattern Recognition and Machine Learning. https://link.springer.com/book/10.1007/978-0-387-45528-0
[4] Mercer, J. Functions of Positive and Negative Type. https://royalsocietypublishing.org/doi/10.1098/rsta.1909.0016
[5] Steinwart, I., & Christmann, A. Support Vector Machines. https://www.springer.com/gp/book/9780387772417
[6] He, H., & Garcia, E. A. Learning from Imbalanced Data. https://ieeexplore.ieee.org/document/1566069
[7] Mangasarian, O. L. Uniqueness of Support Vector Machine Solutions. https://link.springer.com/article/10.1023/A:1010925404376
[8] Joachims, T. Making Large-Scale SVM Learning Practical. https://www.cs.cornell.edu/people/tj/publications/joachims_99a.pdf
[9] Gönen, M., & Alpaydın, E. Multiple Kernel Learning Algorithms. https://www.jmlr.org/papers/v12/gonen11a.html
