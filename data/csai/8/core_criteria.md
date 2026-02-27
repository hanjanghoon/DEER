1. Standing assumptions and formal definitions
The report must operate under the declared setup host class $\mathcal{G}$ is somewhere-dense, subgraph-closed, and not all graphs; pattern class $\mathcal{H}$ is recursively enumerable; the parameter is $|H|$ and precisely define the notions used (the concrete definition of “somewhere-dense,” subgraph-closedness, and how membership in $\mathcal{H}$ is accessed), treat $G\in\mathcal{G}$ as a promise, and fix the parameterized resource model $f(|H|)\cdot |G|^{O(1)}$ for all algorithmic bounds.

2. Counting semantics and multiplicity
The report must explicitly fix whether counting is for subgraphs or induced subgraphs and whether occurrences are labelled injective embeddings or unlabelled (quotiented by $\mathrm{Aut}(H)$); the chosen convention must govern all claims, proofs, and the example, with multiplicities handled consistently under that convention.

3. Main classification claim with explicit scope
The report must state a single precise parameterized-counting classification (e.g., $#\mathrm{FPT}$, $#\mathrm{W}[1]$-hard, or complete) and the exact scope over $\mathcal{G}$ and $\mathcal{H}$ for which it holds, including any structural preconditions on $H$ or promise aspects on $G$, without prescribing a particular outcome.

4. Host–pattern influence and scope partitioning
The report must relate host properties tied to somewhere-denseness and subgraph-closure and pattern structure to the classification and explicitly declare whether the claim is uniform or partitioned into subcases; if partitioned, it must state the partition criteria and ensure each side is supported by appropriate arguments under the fixed counting semantics.

5. Methodological adequacy for hardness or tractability
For hardness or completeness claims, the report must provide a parameter-faithful counting reduction whose soundness and target-class membership are verified under the fixed semantics; for $#\mathrm{FPT}$ claims, it must present a constructive fixed-parameter algorithm with an explicit $f(|H|)\cdot |G|^{O(1)}$ bound and a correctness argument; randomized methods are acceptable if the success-probability model is specified and integrated coherently in the analysis.

6. Parameter and complexity accounting
The report must make explicit how resource bounds depend on $|H|$ and separate parameter-dependent factors from polynomial dependence on $|G|$; any reliance on structural measures of $H$ (e.g., $\mathrm{tw}(H)$, $\mathrm{vc}(H)$, $|E(H)|$) must be stated transparently, and multiplicity constants arising from unlabelled counting must be accounted for correctly.

7. Access model and promise compliance
The report must state what is assumed available about $\mathcal{G}$ and $\mathcal{H}$ during algorithms or reductions (e.g., promise $G\in\mathcal{G}$, how $H\in\mathcal{H}$ is presented) and ensure every step of the argument respects these access assumptions without implicitly requiring stronger oracles or recognition procedures.

8. Illustrative example (representative sanity check)
The report must include a small, correct example either a tiny host pattern instance or a brief reduction/algorithm trace that demonstrates the core mechanism driving the classification within the stated scope, with the fixed counting semantics applied consistently and without substituting for the general argument.

9. Assumptions, limitations, and sensitivity
The report must list the assumptions the classification relies on (host promise, access to $\mathcal{H}$, counting semantics, parameter model) and explain how the result would change under reasonable variations (e.g., induced vs. non-induced, labelled vs. unlabelled, moving to nowhere-dense hosts), identifying any boundaries where the claim would fail.

10. Reproducibility of the technical argument
The report must present definitions, claims, and proof/algorithmic skeletons in sufficient technical detail that an expert can reconstruct the classification under the fixed semantics and assumptions, with no unstated side conditions or gaps that would preclude independent verification.
