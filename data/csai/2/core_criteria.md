1. Formal model and parameters, and acceptance semantics
The report must precisely define the computational model “average-hard-attention saturated Transformers with float activations,” including input encoding, output, acceptance rule (with deterministic tie-breaking) and all scale parameters as functions of input length n, notably L(n) layers, H(n) heads per layer, width d(n), float precision b(n) (mantissa/exponent bounds), attention window watt​(n), and positional encoding type, and it must fix the circuit model used for the upper bound by explicitly stating gate basis, fan-in constraints, size/depth measures, and the uniformity notion (e.g., DLOGTIME-uniform vs. non-uniform).

2. Exact semantics of hard attention and aggregation
The report must formalize the hard-attention saturation mechanism with a deterministic tie-breaking rule for argmax, define how per-head outputs are produced and how multi-head outputs are averaged or combined, and specify whether residual connections, layer normalization, and the activation class are modeled, in a way that is compatible with finite-precision arithmetic throughout.

3. Primitive-to-circuit realizations with quantified costs
For every computation primitive used in the forward pass—linear/affine maps, comparisons/argmax (with tie-breaking), averaging across heads or positions, activations, and any normalization—the report must present an explicit circuit realization over the stated gate basis and provide asymptotic size and depth bounds as functions of n,L,H,d,b,wattn,L,H,d,b,w_{\text{att}}. The arithmetic/Boolean/threshold cost model for float operations at precision b(n) should be explicit, including any required bounds on weights or constants.

4. Layer and network composition accounting
The report must compose the primitive costs to derive explicit formulas or tight asymptotic expressions for per-layer depth/size and for the full L(n)L(n)L(n)-layer network, making clear how fan-in assumptions impact the accounting and exposing the dependence of total depth D(n) and size S(n) on L,H,d,b,watt​.

5. Regime-wise class placement with assumptions
Under clearly stated growth regimes for the parameters, the report must place the recognized language family in standard circuit classes, providing proofs for at least the regimes L(n)=O(1), L(n)=O(logn), and L(n)=poly(n), and it must state the exact assumptions (e.g., fan-in bounds, weight magnitude bounds, activation class, attention scope) required for each placement.

6. Finite-precision correctness and stability
The report must connect float precision b(n) and any minimal separation Δ (or an equivalent margin argument) to the correctness of comparisons and argmax under rounding, justify that rounding and normalization error do not invalidate the simulation across layers, and show that the chosen precision model suffices for the claimed class placements.

7. Architectural variants and impact on bounds
The report must analyze at least two salient architectural choices—specifically positional encoding (absolute vs. relative) and attention scope (windowed/local vs. full) and quantify or tightly argue how these choices alter the reduction, the accounting of D(n),S(n), and the resulting class placement under the same circuit assumptions.

8. Consistency with literature and standard inclusions
The report must situate its bounds relative to the standard inclusions AC0⊊TC0⊆NC1⊆P and to relevant transformer-expressivity results, explain any differences in assumptions, and ensure there is no contradiction with known lower/upper bounds for adjacent models.

9. Formal upper-bound statements and proofs
The report must present formal theorems or propositions that state the upper bounds and their assumptions for each analyzed regime and provide proof sketches or complete proofs that directly reference the primitive realizations and the composed depth/size accounting to justify the claims.

10. Reconstructability and verification
The report must list all modeling and circuit assumptions in one place (gate basis, fan-in, uniformity, precision and tie-breaking rules) and provide sufficient detail, such as explicit constructions or pseudocode to reconstruct the corresponding circuit families from the model parameters and to verify that each stated assumption and bound is met.