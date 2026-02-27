1. Formal problem statement & notation
State hard- and soft-margin SVMs in primal/dual form, define $\mathbf{w}, b, \xi_i, C, \alpha_i, K$, Gram matrix, and clearly distinguish linear vs. kernelized regimes so every later claim anchors to this setup.

2. Assumptions tied to claims
List and justify assumptions—separability vs. non-separability, class imbalance level, noise/outlier model, kernel family, regularization/solver choices—and explicitly link each major conclusion or counterexample to the assumptions under which it holds or fails.

3. KKT-driven hypothesis testing
Derive the dual and KKT conditions (primal/dual feasibility, complementary slackness, $0\!\le\!\alpha_i\!\le\!C$, and stationarity) and use them to test the hypotheses on one-class support-vector feasibility, imbalance effects, and uniqueness; apply the soft-margin characterization (if $0<\alpha_i<C$ then $y_i f(x_i)=1$; if $\alpha_i=C$ then $y_i f(x_i)\le 1$; if $\alpha_i=0$ then $y_i f(x_i)\ge 1$) and $\sum_i \alpha_i y_i=0$ to reason about edge cases. Include a boundary-invariance check: show, via KKT/hinge conditions or a controlled perturbation experiment, that moving/adding points with $y_i f(x_i) > 1$ leaves $\boldsymbol{w}, b$ unchanged until they cross the margin.

4. Kernel validity & RKHS impact
 Kernel use is justified by verifying PSD/Mercer (or by exhibiting a failure mode that yields an ill-posed objective); the representer theorem is invoked to ground solutions in the span of training points; the kernel trick is made explicit—computations depend only on inner products K(xi,xj)K(x_i,x_j), so infinite-dimensional RKHS embeddings (e.g., RBF) are tractable without explicit feature maps; the analysis explains how kernel choice affects Gram-matrix conditioning, margin geometry, support-vector count, and potential non-uniqueness or instability of the solution, with all conclusions tied back to the stated assumptions and the hypotheses under test.

5. Uniqueness & degeneracy
 Use strict convexity where applicable to justify uniqueness. State other conditions for uniqueness (full-rank Gram matrix for dual view, non-degenerate geometry for primal view) and for non-uniqueness (duplicated/parallel points, rank deficiency), and provide at least one concrete diagnostic (e.g., multiple optimal dual solutions or flat directions) to detect it. Identify SVM settings where strict convexity fails (e.g., duplicated points, non-full-rank Gram).

6. Data issues & evaluation metrics
 Analyze class imbalance and label/outlier noise theoretically and (if used) empirically, showing how priors and costs shift margins/thresholds; report margin statistics, hinge loss, and at least one imbalance-aware metric (balanced accuracy or PR-AUC), not raw accuracy alone.

7. Scalability & practical mitigations
 Quantify computational requirements by solver class (e.g., SMO/coordinate-descent/linear solvers) with order-of-growth in $n, d$, and number of support vectors; pair limitations (scaling, noise sensitivity, kernel conditioning) with evidence-based mitigations such as class-weighted $C$, threshold calibration, or approximate kernels.

8. Reproducibility of empirical parts
If experiments are included, specify dataset construction (class ratios, noise/outliers), preprocessing, hyperparameter selection protocol and ranges, and random-seed control, so an independent expert can reproduce all quantitative findings.
