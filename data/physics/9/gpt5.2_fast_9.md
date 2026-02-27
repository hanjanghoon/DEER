# Particle Dynamics and Contact Networks in Disordered Solids Near the Jamming Transition

## Abstract

The jamming transition in disordered particulate systems represents a fundamental route by which rigidity emerges in the absence of crystalline order. Near this transition, systems exhibit pronounced structural and dynamical heterogeneity that cannot be captured by average quantities alone. In this paper, we present a systematic analysis of particle dynamics and contact networks in jammed hard-sphere–like systems, with a particular focus on the classification of particles according to their local contact environment. We review the theoretical foundations of jamming, including isostaticity, caging, and the onset of mechanical rigidity. We then analyze the topology of contact networks in jammed solids, emphasizing the coordination number distribution and its deviations from the isostatic mean. Building on this framework, we classify particles into fully constrained and under-constrained subsets and show how this distinction underlies heterogeneous dynamics near jamming. Special attention is given to particles with approximately ( z \simeq d+1 ) contacts, which are weakly constrained, exhibit enhanced mobility, and play a central role in relaxation processes. We identify these particles with the class known in the literature as *rattlers* and *quasi-rattlers*, and discuss their structural signatures and dynamical consequences. The paper synthesizes results from theory, simulation, and experiment to provide a unified picture of how local contact topology governs dynamics in jammed disordered solids.

---

## 1. Introduction

Disordered solids such as granular materials, colloidal suspensions, foams, and emulsions can undergo a transition from a fluid-like to a rigid state without crystallizing. This phenomenon, known as the *jamming transition*, has emerged as a unifying concept connecting a broad class of amorphous systems across length scales and interaction types [1]. Unlike conventional phase transitions driven by symmetry breaking, jamming is primarily a geometric and mechanical transition, characterized by the formation of a mechanically stable contact network that constrains particle motion.

A defining feature of jammed systems is the coexistence of rigidity and disorder. Even in mechanically stable packings, local environments vary widely: some particles are strongly constrained by many contacts, while others possess fewer constraints and retain a degree of mobility. This heterogeneity manifests both structurally, in the distribution of contact numbers, and dynamically, in the form of intermittent motion and localized rearrangements [2]. Understanding how these local variations arise and how they influence macroscopic behavior is a central challenge in the physics of amorphous solids.

In this paper, we focus on the nature of particle dynamics and contact networks near the jamming transition, with an emphasis on classifying particles by their local coordination. Of particular interest are under-constrained particles with coordination numbers close to ( z \approx d+1 ) in ( d ) dimensions. These particles are neither fully rigidly embedded in the force-bearing network nor completely free, and they play a disproportionate role in low-frequency vibrational modes and relaxation processes [3].

The structure of the paper is as follows. In Section 2, we provide a rigorous overview of the jamming transition in hard-sphere systems, including isostaticity, caging, and rigidity. Section 3 analyzes the topology of contact networks in jammed solids, focusing on coordination statistics. Section 4 introduces a classification of particles based on their local contact environment. Section 5 provides a detailed characterization of under-constrained particles and identifies their established terminology in the literature. We conclude with a discussion of broader implications and open questions.

---

## 2. The Jamming Transition in Hard-Sphere Systems

### 2.1 Definition and Control Parameters

The jamming transition refers to the point at which a disordered assembly of particles becomes mechanically rigid as a control parameter is varied. In hard-sphere systems, the relevant control parameter is typically the packing fraction ( \phi ), defined as the fraction of space occupied by the particles. As ( \phi ) increases, particle motion becomes increasingly restricted until, at a critical packing fraction ( \phi_J ), the system develops a finite shear modulus and resists deformation [1].

Jamming can also be induced by lowering temperature or applied stress, leading to the concept of a jamming phase diagram with axes corresponding to density, temperature, and stress [1]. In the idealized limit of athermal, frictionless hard spheres at zero temperature and zero stress, jamming occurs at a sharply defined density ( \phi_J ).

### 2.2 Isostaticity and Mechanical Stability

A central concept in jamming theory is *isostaticity*. For a system of ( N ) frictionless spherical particles in ( d ) dimensions, each particle has ( d ) translational degrees of freedom, giving a total of ( Nd ) degrees of freedom. Mechanical stability requires that the number of independent constraints provided by interparticle contacts matches the number of degrees of freedom (minus trivial global translations).

Each frictionless contact provides a single constraint, corresponding to the non-overlap condition along the normal direction. Denoting the total number of contacts by ( N_c ), the isostatic condition is
[
N_c = Nd - d,
]
which, in the thermodynamic limit, implies an average coordination number
[
z = \frac{2N_c}{N} = 2d.
]
At the jamming transition, frictionless sphere packings are observed to be precisely isostatic, with ( z \to 2d ) as ( \phi \to \phi_J^+ ) [4].

Isostaticity marks the boundary between floppy systems, which possess zero-energy deformation modes, and rigid systems, which do not. This marginal stability has profound consequences for vibrational spectra, response functions, and dynamics near jamming [5].

### 2.3 Caging and Dynamical Arrest

As the system approaches jamming from below, particle motion becomes increasingly constrained by neighbors, leading to the formation of transient cages. Within a cage, a particle undergoes small-amplitude vibrations but cannot diffuse over long distances. The characteristic cage size decreases as ( \phi ) approaches ( \phi_J ), and the structural relaxation time diverges [6].

The caging effect is closely linked to the development of a contact network. Below jamming, contacts are transient and constantly rearranged; above jamming, a persistent network of contacts emerges that supports stress. The transition thus corresponds to a qualitative change in the nature of particle trajectories, from diffusive to localized.

### 2.4 Emergence of Rigidity

Above ( \phi_J ), the system exhibits finite elastic moduli and can sustain shear and compressive stresses. The rigidity of the jammed solid arises from the percolation of force-bearing contacts throughout the system [7]. Importantly, this rigidity does not require long-range order: jammed packings are typically amorphous, with only short-range positional correlations.

Near the jamming point, elastic properties display anomalous scaling with distance from ( \phi_J ). For example, the shear modulus scales differently from the bulk modulus, reflecting the marginal nature of the contact network [5]. These anomalies are intimately connected to the proximity to isostaticity.

---

## 3. Contact Network Topology in Jammed Solids

### 3.1 Definition of the Contact Network

The contact network of a jammed solid is defined by a graph whose nodes represent particles and whose edges represent interparticle contacts that carry force. This network encodes the mechanical constraints of the system and provides a natural framework for analyzing rigidity and heterogeneity [8].

In frictionless systems, contacts are typically identified by particle overlaps (in soft-sphere models) or by near-touching configurations (in hard-sphere models). The resulting network is disordered and spatially heterogeneous.

### 3.2 Average Coordination Number

The average coordination number ( z ) is a key descriptor of the contact network. As discussed in Section 2.2, ( z ) approaches ( 2d ) at the jamming transition for frictionless spheres. Above jamming, ( z ) increases with packing fraction as additional contacts are formed under compression [4].

The scaling of excess coordination ( \Delta z = z - 2d ) with distance from jamming has been studied extensively and is found to follow a power law ( \Delta z \sim (\phi - \phi_J)^{1/2} ) in many models [5]. This scaling reflects the nonlinear geometry of particle contacts and has important implications for mechanical response.

### 3.3 Distribution of Contact Numbers

While the average coordination number provides a useful global measure, it obscures significant local variability. The distribution ( P(z_i) ) of individual particle coordination numbers ( z_i ) is broad, especially near jamming [9]. Even in isostatic packings, some particles have fewer than ( 2d ) contacts, while others have more.

This heterogeneity arises from geometric disorder and the presence of particles that do not participate fully in the force-bearing network. Analyzing ( P(z_i) ) reveals distinct subpopulations of particles with qualitatively different mechanical roles.

### 3.4 Spatial Correlations and Network Heterogeneity

Contact networks exhibit spatial correlations that go beyond random graph models. Regions of high coordination tend to form rigid backbones, while low-coordination regions are associated with soft spots and potential sites of rearrangement [10]. These correlations are linked to low-frequency vibrational modes and localized excitations.

Network-based measures, such as betweenness centrality or local rigidity indices, have been used to identify structurally weak regions that correlate with dynamical activity [11]. Such analyses reinforce the idea that local contact topology is a key determinant of particle dynamics.

---

## 4. Classification of Particles in the Jammed State

### 4.1 Fully Constrained Particles

Fully constrained particles are those that are embedded in the rigid backbone of the jammed solid. In frictionless systems, these particles typically have coordination numbers ( z_i \ge 2d ) and participate in multiple force chains. Their motion is strongly restricted, and they primarily undergo small-amplitude vibrations around fixed positions [12].

These particles dominate the elastic response of the system and carry the majority of the applied stress. In terms of vibrational modes, they contribute mainly to higher-frequency excitations associated with stiff regions of the network.

### 4.2 Under-Constrained Particles

In contrast, under-constrained particles have fewer contacts than required for local isostatic stability. Their coordination numbers satisfy ( z_i < 2d ), and in many cases cluster around values close to ( d+1 ) [3]. Such particles are weakly coupled to the rigid backbone and retain a degree of freedom to move within local cages.

Under-constrained particles are not necessarily free; rather, they are marginally stable and can undergo relatively large displacements without significantly perturbing the global structure. Their presence is a natural consequence of disorder and the global isostatic constraint.

### 4.3 Rattlers and Quasi-Rattlers

The most extreme case of under-constrained particles are those with too few contacts to be mechanically stable even locally. In frictionless sphere packings, particles with fewer than ( d+1 ) contacts cannot be force-balanced and are effectively free to move within cages formed by neighbors. These particles are known as *rattlers* [4].

Particles with ( z_i \approx d+1 ) occupy an intermediate category. They are marginally stable and often referred to as *quasi-rattlers* or weakly constrained particles in the literature [3,9]. While not completely free, they exhibit enhanced mobility compared to the rigid backbone.

---

## 5. Dynamics and Role of Under-Constrained Particles

### 5.1 Typical Contact Number and Geometry

Under-constrained particles near jamming often have coordination numbers close to ( z \simeq d+1 ). This number corresponds to the minimum required for local force balance in frictionless systems, assuming generic, non-coplanar contact geometries [13]. Such particles are stabilized by just enough neighbors to prevent trivial motion but remain sensitive to perturbations.

Geometrically, these particles tend to reside in locally open regions of the packing, where available free volume is larger. Their contact angles are often highly asymmetric, contributing to marginal stability.

### 5.2 Characteristic Dynamics

The dynamics of under-constrained particles are markedly different from those of fully constrained ones. They exhibit larger vibrational amplitudes, intermittent hopping within cages, and strong coupling to low-frequency vibrational modes [3,14]. In simulations, these particles dominate the participation ratio of soft modes and are often implicated in the onset of plastic rearrangements under shear.

Time-resolved studies show that under-constrained particles are more likely to undergo irreversible displacements during relaxation or deformation, acting as nucleation sites for rearrangements [10]. Their motion is thus a key contributor to dynamical heterogeneity near jamming.

### 5.3 Identification in the Literature

In the established literature on jamming and granular matter, particles that do not belong to the force-bearing network are referred to as *rattlers* [4]. This term originally denoted particles that rattle freely inside cages without contributing to mechanical stability.

Particles with coordination numbers near ( d+1 ), which are marginally constrained but not fully free, are often grouped with rattlers or described as *quasi-rattlers* or *weakly constrained particles* [3,9]. While terminology varies, their defining features—low coordination, enhanced mobility, and strong coupling to soft modes—are well recognized.

---

## 6. Discussion and Outlook

The analysis presented in this paper highlights the central role of contact network heterogeneity in determining particle dynamics near the jamming transition. While global isostaticity provides a useful organizing principle, it is the local deviations from this condition that give rise to rich and complex behavior.

Under-constrained particles, particularly those with coordination numbers around ( d+1 ), emerge as key actors in the dynamics of jammed solids. Their marginal stability and enhanced mobility link structure to dynamics and provide a microscopic basis for understanding relaxation, plasticity, and low-frequency excitations in amorphous materials.

Open questions remain regarding the universality of these features across different interaction types, particle shapes, and frictional properties. Extending the classification framework to more complex systems, and connecting it to predictive theories of amorphous plasticity, represents a promising direction for future research.

---

## References
[1] Liu, A. J., & Nagel, S. R. “Jamming is not just cool any more.” Nature 396, 21–22 (1998). https://www.nature.com/articles/23819
[2] Weeks, E. R., et al. “Three-dimensional direct imaging of structural relaxation near the colloidal glass transition.” Science 287, 627–631 (2000). https://science.sciencemag.org/content/287/5453/627
[3] Wyart, M., et al. “Effects of coordination and pressure on sound attenuation, boson peak, and elasticity in amorphous solids.” Europhysics Letters 72, 486–492 (2005). https://iopscience.iop.org/article/10.1209/epl/i2005-10318-5
[4] O’Hern, C. S., et al. “Jamming at zero temperature and zero applied stress: The epitome of disorder.” Physical Review E 68, 011306 (2003). https://journals.aps.org/pre/abstract/10.1103/PhysRevE.68.011306
[5] van Hecke, M. “Jamming of soft particles: geometry, mechanics, scaling and isostaticity.” Journal of Physics: Condensed Matter 22, 033101 (2010). https://iopscience.iop.org/article/10.1088/0953-8984/22/3/033101
[6] Pusey, P. N., & van Megen, W. “Phase behaviour of concentrated suspensions of nearly hard colloidal spheres.” Nature 320, 340–342 (1986). https://www.nature.com/articles/320340a0
[7] Ellenbroek, W. G., et al. “Rigidity loss in disordered systems: Three scenarios.” Physical Review Letters 97, 258001 (2006). https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.97.258001
[8] Alexander, S. “Amorphous solids: their structure, lattice dynamics and elasticity.” Physics Reports 296, 65–236 (1998). https://www.sciencedirect.com/science/article/pii/S0370157397000959
[9] Silbert, L. E., et al. “Vibrations and diverging length scales near the unjamming transition.” Physical Review Letters 95, 098301 (2005). https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.95.098301
[10] Manning, M. L., & Liu, A. J. “Vibrational modes identify soft spots in a sheared disordered packing.” Physical Review Letters 107, 108302 (2011). https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.107.108302
[11] Bassett, D. S., et al. “Network analysis of jammed granular materials.” Physical Review E 86, 041306 (2012). https://journals.aps.org/pre/abstract/10.1103/PhysRevE.86.041306
[12] Goodrich, C. P., et al. “Finite-size scaling at the jamming transition.” Physical Review Letters 109, 095704 (2012). https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.109.095704
[13] Maxwell, J. C. “On the calculation of the equilibrium and stiffness of frames.” Philosophical Magazine 27, 294–299 (1864). https://www.tandfonline.com/doi/abs/10.1080/14786446408643668
[14] Brito, C., & Wyart, M. “Heterogeneous dynamics, marginal stability and soft modes in hard sphere glasses.” Journal of Statistical Mechanics P08020 (2007). https://iopscience.iop.org/article/10.1088/1742-5468/2007/08/P08020
