# Energy Loss Characteristics of Heavy Charged Particles in Matter

## Range–Energy Relations, Stopping Power, and Spatial Energy Deposition

---

## Abstract

The interaction of heavy charged particles with matter is governed primarily by continuous energy loss through electromagnetic interactions with atomic electrons. Unlike light charged particles, heavy ions such as alpha particles exhibit well-defined trajectories, finite ranges, and strongly localized energy deposition culminating in a pronounced Bragg peak. This paper presents a systematic analysis of the relationship between a particle’s energy, its position along its trajectory, and its stopping power, with a particular emphasis on empirical range–energy relations. After rigorously defining particle range, stopping power, and the Bragg curve, we review commonly used empirical formulas connecting initial energy to total range in a given medium. These relations are then used to derive a practical methodology for determining the residual energy as a function of penetration depth. Finally, the stopping power as a function of position or residual energy is obtained by differentiating the inverse range–energy relationship. This approach provides a self-consistent framework for calculating spatial energy loss profiles without explicit reliance on microscopic collision models, and it forms the basis of many practical applications in radiation detection, dosimetry, and particle transport calculations.

---

## 1. Introduction

The study of energy loss mechanisms of charged particles in matter occupies a central position in nuclear physics, radiation physics, and applied fields such as medical physics and space science. When a charged particle traverses a material medium, it interacts electromagnetically with atomic electrons and nuclei, gradually losing kinetic energy until it comes to rest. For heavy charged particles—defined here as particles with mass much larger than the electron mass, such as alpha particles, protons, and heavier ions—the dominant energy loss mechanism over most of the trajectory is inelastic Coulomb interaction with bound and free electrons [1].

A defining feature of heavy charged particle transport is the existence of a finite and relatively well-defined range. In contrast to photons or neutrons, which undergo stochastic scattering and absorption events, heavy charged particles follow nearly straight paths, with only small angular deviations, until their energy is exhausted. This property allows the introduction of macroscopic quantities such as stopping power and range, which encapsulate the cumulative effect of microscopic interactions [2].

The energy loss per unit path length, or stopping power, is not constant along the trajectory. Instead, it increases as the particle slows down, reaching a maximum near the end of the range. This behavior gives rise to the Bragg curve, a characteristic spatial distribution of energy deposition that is exploited in applications ranging from particle identification in detectors to targeted dose delivery in ion-beam therapy [3].

While the Bethe theory provides a microscopic description of stopping power at sufficiently high energies, practical calculations often rely on empirical or semi-empirical relationships between particle energy and range. Such range–energy relations are particularly useful because they allow the inversion of the problem: given a known range, one may infer the initial or residual energy, and from this deduce the local stopping power [4].

The objective of this paper is to provide a systematic and self-contained analysis of energy loss characteristics of heavy charged particles based on empirical range–energy relations. The discussion proceeds from fundamental definitions to practical computational methodologies, emphasizing the connection between energy, position, and stopping power.

---

## 2. Fundamental Concepts of Energy Loss in Matter

### 2.1 Stopping Power

The stopping power of a material for a charged particle is defined as the mean rate of energy loss per unit path length,

[
S(E) \equiv -\frac{dE}{dx},
]

where ( E ) is the kinetic energy of the particle and ( x ) is the distance traveled in the medium. The negative sign indicates that the particle’s energy decreases with increasing path length. Stopping power is typically expressed in units of MeV/cm or MeV·cm²/g when normalized by material density [1].

For heavy charged particles, stopping power arises predominantly from ionization and excitation of atoms in the medium. Nuclear stopping, involving elastic collisions with target nuclei, contributes significantly only at very low energies near the end of the range [2]. Over most of the trajectory, electronic stopping dominates.

The dependence of stopping power on particle velocity leads to a characteristic increase in ( -dE/dx ) as the particle slows down. This behavior is central to the formation of the Bragg peak.

### 2.2 Particle Range

The range ( R ) of a charged particle is defined as the total path length the particle travels in a material before coming to rest. In an idealized continuous slowing down approximation (CSDA), the range is given by

[
R(E_0) = \int_{0}^{E_0} \frac{dE}{S(E)},
]

where ( E_0 ) is the initial kinetic energy of the particle [3].

In real materials, stochastic fluctuations in energy loss and multiple scattering lead to a distribution of ranges rather than a single value. However, for heavy charged particles, the range straggling is relatively small, and the CSDA range provides a useful and widely applied approximation [4].

### 2.3 The Bragg Curve

The Bragg curve describes the energy deposited per unit length as a function of penetration depth. Since stopping power increases as energy decreases, the energy deposition rises gradually along the trajectory and reaches a sharp maximum near the end of the range. Beyond this point, the particle comes to rest, and energy deposition drops abruptly to zero.

The qualitative form of the Bragg curve is a direct consequence of the velocity dependence of electronic stopping power [5]. Its existence has been experimentally confirmed for alpha particles, protons, and heavier ions in a wide variety of materials.

---

## 3. Empirical Range–Energy Relationships

### 3.1 Motivation for Empirical Formulas

Although stopping power can, in principle, be calculated from first principles using quantum mechanical collision theory, practical applications often rely on empirical or semi-empirical formulas. These formulas encapsulate experimental measurements of particle ranges in specific materials and provide simple functional relationships between range and energy [6].

Empirical range–energy relations are particularly valuable for heavy charged particles because their trajectories are well-defined and their ranges can be measured with high precision. Once a reliable ( R(E) ) relation is established for a given particle–material combination, it can be used to infer residual energy and stopping power at any point along the path.

### 3.2 Power-Law Range–Energy Relations

A commonly used empirical form for the range–energy relation of heavy charged particles is a power-law expression,

[
R = a E^n,
]

where ( a ) and ( n ) are material- and particle-dependent constants determined experimentally [2].

For alpha particles in air or light solids, the exponent ( n ) typically lies between 1.5 and 2, reflecting the non-linear dependence of stopping power on velocity. Such power-law relations provide good agreement with experimental data over limited energy ranges and are widely used in detector calibration and radiation protection calculations [7].

### 3.3 Polynomial and Tabulated Relations

For higher accuracy over broader energy intervals, polynomial fits or tabulated range–energy data are often employed. Databases such as those provided by NIST compile extensive experimental and theoretical stopping power and range data for a wide variety of ions and materials [8].

In these approaches, the range is expressed either as a polynomial in energy or as an interpolated function based on tabulated values. While less analytically transparent than power-law forms, these methods offer improved precision and are standard in computational transport codes.

---

## 4. Determination of Residual Energy as a Function of Position

### 4.1 Inversion of the Range–Energy Relation

Given a particle with initial energy ( E_0 ) and corresponding total range ( R_0 = R(E_0) ), the residual energy ( E(x) ) at a distance ( x ) along the path can be determined by considering the remaining range,

[
R_{\text{rem}}(x) = R_0 - x.
]

If the functional form of ( R(E) ) is known and invertible, the residual energy is obtained by solving

[
E(x) = R^{-1}(R_0 - x).
]

This inversion is straightforward for power-law relations and can be performed numerically for more complex empirical formulas [4].

### 4.2 Example: Power-Law Case

For a power-law range–energy relation ( R = a E^n ), the inverse function is

[
E = \left( \frac{R}{a} \right)^{1/n}.
]

Thus, the residual energy at position ( x ) is

[
E(x) = \left( \frac{R_0 - x}{a} \right)^{1/n}.
]

This expression explicitly links spatial position along the trajectory to particle energy, providing a practical means of reconstructing the energy profile from range data [7].

### 4.3 Physical Interpretation

The monotonic decrease of ( E(x) ) with increasing ( x ) reflects the continuous nature of energy loss for heavy charged particles. Near the end of the range, small changes in position correspond to large changes in energy, a feature that underlies the sharp rise in stopping power observed in the Bragg peak region [5].

---

## 5. Calculation of Stopping Power as a Function of Position

### 5.1 Differentiation of the Range–Energy Relation

Once the residual energy ( E(x) ) is known, the stopping power as a function of position can be obtained from

[
-\frac{dE}{dx} = \left( \frac{dR}{dE} \right)^{-1}.
]

This relation follows directly from the definition of range as the integral of the inverse stopping power. By differentiating the empirical range–energy relation, one obtains the stopping power without explicitly invoking microscopic collision theory [6].

### 5.2 Power-Law Example

For ( R = a E^n ), differentiation yields

[
\frac{dR}{dE} = a n E^{n-1},
]

and thus

[
-\frac{dE}{dx} = \frac{1}{a n E^{n-1}}.
]

Substituting ( E(x) ) from the inverted relation produces an explicit expression for stopping power as a function of position. This formulation reproduces the qualitative shape of the Bragg curve, with stopping power increasing rapidly as ( E \to 0 ) near the end of the range [2].

### 5.3 Connection to the Bragg Curve

The divergence of ( -dE/dx ) as energy decreases explains the pronounced maximum in the Bragg curve. Although real physical effects such as range straggling and nuclear stopping smooth this divergence, the empirical range–energy framework captures the essential physics governing spatial energy deposition [3].

---

## 6. Discussion and Applications

### 6.1 Validity and Limitations

Empirical range–energy relations provide a powerful and practical means of analyzing heavy charged particle energy loss. However, their validity is limited to the energy ranges and materials for which they have been calibrated. At very low energies, nuclear stopping and charge-exchange effects may become significant, reducing the accuracy of purely electronic stopping models [8].

### 6.2 Applications in Radiation Physics

The methodology described in this paper underpins numerous applications, including alpha-particle spectroscopy, solid-state detector design, and ion-beam therapy. In medical physics, the precise control of the Bragg peak location relies on accurate range–energy relations to ensure that maximum dose is delivered to the target volume [9].

---

## 7. Conclusion

This paper has presented a systematic analysis of the energy loss characteristics of heavy charged particles in matter, emphasizing the relationship between energy, position, and stopping power as derived from empirical range–energy relations. By defining fundamental quantities such as stopping power and range, reviewing common empirical formulas, and demonstrating how these relations can be inverted and differentiated, we have established a coherent framework for calculating residual energy and specific energy loss along a particle’s trajectory. This approach provides both physical insight and practical utility, forming a cornerstone of applied radiation physics and charged-particle transport theory.

---

## References

[1] H. Bethe, Zur Theorie des Durchgangs schneller Korpuskularstrahlen durch Materie – https://doi.org/10.1007/BF01325375
[2] J. F. Ziegler, J. P. Biersack, and U. Littmark, The Stopping and Range of Ions in Solids – https://www.srim.org
[3] G. Knoll, Radiation Detection and Measurement – https://www.wiley.com/en-us/Radiation+Detection+and+Measurement-p-9780470131480
[4] F. Attix, Introduction to Radiological Physics and Radiation Dosimetry – https://doi.org/10.1002/9783527617135
[5] H. Bragg and R. Kleeman, On the α particles of radium, and their loss of range in passing through various atoms and molecules – https://royalsocietypublishing.org/doi/10.1098/rspa.1905.0004
[6] ICRU Report 49, Stopping Powers and Ranges for Protons and Alpha Particles – https://doi.org/10.1093/jicru/os25.2.Report49
[7] L. Pauling, The energy loss of heavy charged particles – https://doi.org/10.1103/PhysRev.54.899
[8] NIST PSTAR and ASTAR Databases – https://physics.nist.gov/PhysRefData/Star/Text/contents.html
[9] U. Amaldi and G. Kraft, Radiotherapy with beams of carbon ions – https://doi.org/10.1016/S0168-9002(05)00845-9
