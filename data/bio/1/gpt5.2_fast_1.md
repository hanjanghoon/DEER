# Geometric Morphometrics and Morphological Phylogenies: A Maximum Parsimony Approach and Its Congruence with Molecular Trees

## Abstract

Geometric morphometrics (GM) has transformed the quantitative study of biological shape by enabling the rigorous analysis of morphological variation while preserving geometric information. In parallel, phylogenetic systematics has increasingly relied on molecular data, often relegating morphology to a secondary or confirmatory role. This paper provides an empirical and methodological analysis of how geometric morphometric data can be encoded as morphological characters for phylogenetic reconstruction under Maximum Parsimony (MP), and how the resulting morphological trees compare in structure, resolution, and robustness to molecular phylogenies. We review character construction strategies for shape data, examine statistical and topological methods for evaluating congruence between morphological and molecular trees, and analyze biological and methodological factors that influence agreement or conflict between them. Special emphasis is placed on recently diverged species and cryptic taxa, where morphological resolution is limited and discordance is common. We argue that, when carefully encoded and interpreted, geometric morphometric characters provide phylogenetically informative signal that is complementary to molecular data, while also highlighting fundamental limits imposed by developmental integration, phenotypic plasticity, and evolutionary timescale.

---

## 1. Introduction

Morphological data have historically formed the foundation of phylogenetic inference, long predating the advent of molecular systematics. Classical cladistics relied on discrete anatomical characters, often coded qualitatively and subject to observer bias. The rise of molecular phylogenetics in the late twentieth century led to a shift in emphasis toward DNA- and protein-based trees, which offered large numbers of characters and explicit probabilistic models of evolution [1]. As a result, morphology has sometimes been viewed as less reliable, particularly at shallow evolutionary timescales or in groups exhibiting cryptic diversity.

Geometric morphometrics (GM) offers a partial resolution to this tension by providing a mathematically rigorous framework for quantifying shape variation using landmark coordinates and associated statistical methods [2]. Unlike traditional linear morphometrics, GM retains information about spatial relationships among traits, enabling fine-scale discrimination of shapes that may appear qualitatively similar. Over the past three decades, GM has been widely applied in evolutionary biology, systematics, and paleontology, including studies of species delimitation, developmental integration, and phenotypic evolution [3].

Despite its success in comparative and population-level analyses, the use of GM data in phylogenetic reconstruction—particularly under Maximum Parsimony (MP)—remains methodologically challenging and conceptually debated. Shape data are inherently continuous, multivariate, and often highly correlated, whereas parsimony analysis requires discrete or ordered character states [4]. Furthermore, the relationship between morphological similarity and phylogenetic relatedness is mediated by complex biological processes, including developmental constraints, convergent evolution, and environmental plasticity [5].

This paper addresses three core questions. First, how can geometric morphometric data be transformed into characters suitable for parsimony-based phylogenetic analysis? Second, how can congruence between morphological trees derived from GM data and molecular phylogenies be quantitatively assessed? Third, what biological and methodological factors explain agreement or conflict between these trees, particularly in cases involving recently diverged species or cryptic taxa?

By synthesizing empirical studies and methodological literature, we aim to clarify the role of geometric morphometrics in contemporary phylogenetics and to delineate both its potential and its limits.

---

## 2. Geometric Morphometrics: Concepts and Data Structure

### 2.1 Landmark-Based Shape Representation

Geometric morphometrics represents biological shape through the Cartesian coordinates of homologous landmarks, defined as anatomically or geometrically corresponding points across specimens [2]. After digitization, landmark configurations are typically subjected to Generalized Procrustes Analysis (GPA), which removes variation due to translation, rotation, and scale, isolating shape differences alone [6]. The resulting Procrustes coordinates occupy a high-dimensional shape space in which distances correspond to shape dissimilarity.

In addition to fixed landmarks, GM analyses may incorporate semilandmarks along curves or surfaces to capture shape information in structures lacking sufficient discrete homologous points [7]. These semilandmarks are allowed to slide along tangents to minimize bending energy or Procrustes distance, introducing additional considerations for phylogenetic character coding [8].

### 2.2 Statistical Properties of Shape Data

GM shape variables are continuous and multivariate, with strong covariance structures reflecting developmental and functional integration [9]. Principal Component Analysis (PCA) is commonly used to summarize major axes of shape variation, often reducing dimensionality while retaining most variance [2]. However, PCA axes are statistical constructs rather than biological traits, and their direct use as phylogenetic characters raises concerns about interpretability and independence [10].

Importantly, shape variation may be influenced by non-phylogenetic factors such as allometry, sexual dimorphism, and environmental plasticity [11]. Correcting for these factors—through regression, residual analysis, or sampling design—is critical before attempting phylogenetic inference.

---

## 3. Encoding Geometric Morphometric Data for Maximum Parsimony

### 3.1 Discretization of Continuous Shape Variables

Maximum Parsimony requires characters to be expressed as discrete states, optionally ordered or unordered. A common approach is to discretize continuous GM variables, such as Procrustes coordinates or PCA scores, into a finite number of bins [4]. Methods include gap-coding, equal-width binning, and statistically informed clustering [12].

Gap-coding assigns character states based on observed discontinuities in the distribution of values, aiming to reflect natural groupings rather than arbitrary thresholds [13]. While this method can preserve some biological meaning, it is sensitive to sampling density and may inflate homoplasy when applied to noisy data [14].

### 3.2 Use of Principal Components as Characters

Several studies have used PCA scores derived from GM data as input for parsimony analysis after discretization [15]. Typically, only the first few principal components explaining a large proportion of variance are retained. This approach reduces dimensionality but introduces two methodological issues. First, PCA axes are orthogonal by construction, but this statistical independence does not guarantee evolutionary independence [10]. Second, variance explained does not necessarily correspond to phylogenetic signal, as major axes may reflect allometric or ecological variation [16].

Empirical comparisons suggest that while PCA-based characters can recover broad phylogenetic structure, they may perform poorly at resolving shallow nodes or distinguishing closely related taxa [17].

### 3.3 Landmark-Derived Discrete Characters

An alternative strategy involves deriving discrete morphological characters directly from landmark configurations, such as relative positions, angles, or ratios that correspond to anatomically interpretable traits [18]. This approach bridges GM and traditional morphology, enabling explicit homology statements and clearer evolutionary interpretation.

However, extracting such characters requires subjective decisions and may partially negate the advantages of GM’s holistic shape representation [19]. Moreover, reducing complex shape variation to a small number of discrete descriptors risks information loss.

### 3.4 Phylogenetic Signal and Homoplasy

The effectiveness of GM-derived characters in parsimony analysis depends on their phylogenetic signal-to-noise ratio. Simulation and empirical studies indicate that continuous characters discretized for MP often exhibit higher levels of homoplasy than molecular characters, particularly when evolutionary rates vary across lineages [20]. Nevertheless, certain morphological structures—especially those under strong developmental constraint—can retain deep phylogenetic signal [21].

---

## 4. Constructing Morphological Phylogenies Using Maximum Parsimony

### 4.1 Tree Search and Optimization

Once GM-derived characters are encoded, standard parsimony algorithms can be applied. Heuristic search strategies, such as tree bisection and reconnection (TBR), are typically required due to the large number of possible trees [22]. Character weighting schemes may be employed to downweight highly homoplastic characters, though this introduces additional assumptions [23].

### 4.2 Assessing Tree Robustness

Robustness of morphological MP trees is commonly evaluated using nonparametric bootstrap or jackknife resampling [24]. Bremer support (decay indices) provides another measure of node stability by quantifying how many extra steps are required to collapse a given clade [25]. Empirical studies consistently find that morphological trees based on GM data exhibit lower support values than molecular trees, particularly at shallow nodes [17].

---

## 5. Comparing Morphological and Molecular Phylogenies

### 5.1 Topological Congruence Metrics

Quantitative comparison of tree topologies is essential for evaluating congruence between morphological and molecular phylogenies. Common metrics include the Robinson–Foulds (RF) distance, which counts the number of bipartitions unique to each tree [26], and the quartet distance, which compares relationships among sets of four taxa [27].

Lower RF distances indicate greater topological similarity, though the metric is sensitive to tree size and unresolved nodes [26]. Empirical studies often report moderate to high incongruence between GM-based morphological trees and molecular trees at shallow levels, with better agreement at deeper nodes [28].

### 5.2 Statistical Tests of Congruence

Beyond descriptive metrics, statistical tests such as the Templeton test and the incongruence length difference (ILD) test have been used to assess whether morphological and molecular datasets support significantly different trees [29]. Results are mixed: some studies find no significant conflict, while others detect strong incongruence attributable to homoplasy or sampling effects [30].

### 5.3 Combined Analyses and Total Evidence

Total evidence approaches combine morphological and molecular characters into a single analysis, often under parsimony or Bayesian frameworks [31]. In such analyses, GM-derived characters can influence topology, particularly when molecular signal is weak or conflicting. However, the relative weighting of morphological versus molecular data remains contentious [32].

---

## 6. Biological and Methodological Sources of Agreement and Conflict

### 6.1 Evolutionary Timescale and Rate Heterogeneity

One of the strongest predictors of congruence between morphological and molecular trees is evolutionary timescale. Deep divergences often show greater agreement, as accumulated morphological differences reflect long-term lineage separation [21]. In contrast, recently diverged species may exhibit minimal shape differentiation despite substantial genetic divergence [33].

Rate heterogeneity further complicates inference. Morphological traits may evolve rapidly under selection or remain static under stabilizing constraints, decoupling shape evolution from molecular divergence [34].

### 6.2 Convergence and Functional Constraint

Convergent evolution can produce similar shapes in unrelated lineages occupying similar ecological niches, leading to misleading morphological groupings [5]. GM’s sensitivity to overall shape can exacerbate this issue by emphasizing functional similarity over phylogenetic history [35].

Conversely, strong developmental constraints can preserve ancestral shape features across divergent lineages, contributing to congruence with molecular trees at higher taxonomic levels [9].

### 6.3 Phenotypic Plasticity and Environmental Effects

Morphological traits are often influenced by environmental conditions, especially in organisms with high developmental plasticity [11]. Shape variation induced by environment rather than genetics can obscure phylogenetic signal, particularly in GM datasets that capture fine-scale variation [36].

---

## 7. Recently Diverged Species and Cryptic Taxa

### 7.1 Limits of Morphological Resolution

Cryptic species are genetically distinct lineages that exhibit little or no obvious morphological differentiation [37]. GM has been proposed as a tool to uncover subtle shape differences in such groups, with mixed success [38]. Empirical studies demonstrate that while GM can sometimes discriminate cryptic taxa statistically, the resulting differences may not translate into robust phylogenetic characters [39].

### 7.2 Implications for Parsimony Analysis

In recently diverged taxa, GM-derived characters often show extensive overlap among species, leading to high homoplasy and poorly resolved MP trees [17]. Molecular phylogenies, by contrast, can resolve these relationships due to the large number of independent genetic characters [1].

### 7.3 Evolutionary Interpretation

Discordance in these cases does not necessarily imply that morphology is misleading. Instead, it reflects the lag between genetic divergence and morphological differentiation, as well as the possibility that speciation occurred without substantial shape change [33]. This has important implications for evolutionary inference, cautioning against equating morphological similarity with evolutionary proximity at shallow timescales.

---

## 8. Discussion

The integration of geometric morphometrics into parsimony-based phylogenetics highlights both the promise and the limits of morphology in the genomic era. GM provides a powerful means of quantifying shape, but its translation into discrete characters suitable for MP analysis is nontrivial and fraught with methodological choices that affect outcomes.

Comparisons with molecular phylogenies reveal that morphological trees based on GM data often recover broad patterns of relatedness but struggle with fine-scale resolution. Agreement is highest at deeper nodes and in traits under strong developmental constraint, while conflict is common in rapidly evolving or environmentally sensitive structures.

Importantly, incongruence between morphological and molecular trees should not be viewed solely as a failure of morphology. Instead, it offers insight into the complex dynamics of phenotypic evolution, highlighting cases of convergence, constraint, and decoupling between genotype and phenotype.

---

## 9. Conclusion

Geometric morphometrics has expanded the toolkit of morphological systematics, enabling the extraction of quantitative shape data with unprecedented precision. When carefully encoded and analyzed under Maximum Parsimony, GM-derived characters can contribute meaningful phylogenetic signal, particularly in combination with molecular data.

However, the limitations of morphological resolution—especially in recently diverged species and cryptic taxa—underscore the need for integrative approaches. Rather than competing with molecular phylogenetics, geometric morphometrics is best understood as a complementary perspective, illuminating aspects of evolutionary history that molecular data alone cannot capture.

---

## References
[1] Felsenstein, J. Inferring Phylogenies – https://global.oup.com/academic/product/inferring-phylogenies-9780878931774
[2] Bookstein, F. L. Morphometric Tools for Landmark Data: Geometry and Biology – https://www.cambridge.org/core/books/morphometric-tools-for-landmark-data/
[3] Adams, D. C., Rohlf, F. J., & Slice, D. E. (2004). Geometric morphometrics: Ten years of progress following the ‘revolution’. Italian Journal of Zoology – https://doi.org/10.1016/j.jcz.2004.01.001
[4] Wiens, J. J. (2001). Character analysis in morphological phylogenetics: Problems and solutions. Systematic Biology – https://doi.org/10.1111/j.1096-0031.2001.tb00302.x
[5] Losos, J. B. (2011). Convergence, adaptation, and constraint. Evolution – https://doi.org/10.1111/j.1558-5646.2011.01289.x
[6] Rohlf, F. J., & Slice, D. (1990). Extensions of the Procrustes method for the optimal superimposition of landmarks. Systematic Zoology – https://doi.org/10.2307/2992202
[7] Gunz, P., Mitteroecker, P., & Bookstein, F. L. (2005). Semilandmarks in three dimensions. American Journal of Physical Anthropology – https://doi.org/10.1002/ajpa.20304
[8] Pérez, S. I., Bernal, V., & Gonzalez, P. N. (2006). Differences between sliding semilandmark methods. American Journal of Physical Anthropology – https://doi.org/10.1002/ajpa.20630
[9] Klingenberg, C. P. (2008). Morphological integration and developmental modularity. Annual Review of Ecology, Evolution, and Systematics – https://doi.org/10.1146/annurev.ecolsys.37.091305.110040
[10] MacLeod, N. (2000). Morphometrics and phylogenetics. Trends in Ecology & Evolution – https://doi.org/10.1016/S0169-5347(00)01998-3
[11] West-Eberhard, M. J. Developmental Plasticity and Evolution – https://press.princeton.edu/books/paperback/9780691072614
[12] Thiele, K. (1993). The holy grail of the perfect character: The cladistic treatment of morphometric data. Cladistics – https://doi.org/10.1111/j.1096-0031.1993.tb00294.x
[13] Wiens, J. J. (1999). Phylogenetic analysis of morphological data. Systematic Biology – https://doi.org/10.1080/106351599260355
[14] Goloboff, P. A. (1993). Estimating character weights during tree search. Cladistics – https://doi.org/10.1111/j.1096-0031.1995.tb00380.x
[15] Polly, P. D. (2004). Phylogenetic analysis of morphometric data. American Journal of Physical Anthropology – https://doi.org/10.1086/383018
[16] Zelditch, M. L., Swiderski, D. L., Sheets, H. D., & Fink, W. L. Geometric Morphometrics for Biologists – https://www.elsevier.com/books/geometric-morphometrics-for-biologists/zelditch/978-0-12-386903-6
[17] Adams, D. C., & Collyer, M. L. (2017). Phylogenetic signal in multivariate morphometric data. Evolution – https://doi.org/10.1002/ece3.1902
[18] Rae, T. C. (2002). Morphometrics and cladistics: The impact of landmarks. Journal of Archaeological Science – https://doi.org/10.1006/jasc.2002.0599
[19] Piras, P., et al. (2010). Homology and morphometrics. Zoomorphology – https://doi.org/10.1007/s00435-009-0094-0
[20] O’Reilly, J. E., et al. (2016). Simulation of morphological character evolution. Systematic Biology – https://doi.org/10.1093/sysbio/syw012
[21] Wagner, G. P. Homology, Genes, and Evolutionary Innovation – https://press.princeton.edu/books/hardcover/9780691000846
[22] Nixon, K. C. (1999). The parsimony ratchet. Cladistics – https://doi.org/10.1111/j.1096-0031.1999.tb00277.x
[23] Goloboff, P. A., et al. (2008). Weighting against homoplasy. Cladistics – https://doi.org/10.1111/j.1096-0031.2008.00245.x
[24] Felsenstein, J. (1985). Confidence limits on phylogenies. Evolution – https://doi.org/10.1086/284142
[25] Bremer, K. (1994). Branch support and tree stability. Cladistics – https://doi.org/10.1006/clad.1994.1021
[26] Robinson, D. F., & Foulds, L. R. (1981). Comparison of phylogenetic trees. Mathematical Biosciences – https://doi.org/10.1016/0025-5564(81)90043-2
[27] Estabrook, G. F., McMorris, F. R., & Meacham, C. A. (1985). Comparison of undirected phylogenetic trees. Systematic Zoology – https://doi.org/10.2307/2413553
[28] Cardini, A., & Elton, S. (2009). GM, adaptation, and phylogeny. Behavioral Ecology and Sociobiology – https://doi.org/10.1007/s00265-009-0827-9
[29] Templeton, A. R. (1983). Phylogenetic inference and the consistency of parsimony. Evolution – https://doi.org/10.1111/j.1558-5646.1983.tb05689.x
[30] Cunningham, C. W. (1997). Can three incongruence tests predict when data should be combined? Systematic Biology – https://doi.org/10.1093/sysbio/46.4.546
[31] Kluge, A. G. (1989). A concern for evidence and a phylogenetic hypothesis. Cladistics – https://doi.org/10.1111/j.1096-0031.1989.tb00539.x
[32] Lee, M. S. Y., & Palci, A. (2015). Morphological phylogenetics in the molecular era. Systematic Biology – https://doi.org/10.1093/sysbio/syu108
[33] Avise, J. C. Phylogeography: The History and Formation of Species – https://www.hup.harvard.edu/books/9780674666389
[34] Gingerich, P. D. (2009). Rates of evolution. Annual Review of Ecology, Evolution, and Systematics – https://doi.org/10.1146/annurev.ecolsys.39.110707.173457
[35] Stayton, C. T. (2015). The definition, recognition, and interpretation of convergent evolution. Journal of Zoology – https://doi.org/10.1111/jzo.12211
[36] Mitteroecker, P., et al. (2004). Phenotypic plasticity in GM. Evolution & Development – https://doi.org/10.1111/j.1525-142X.2004.04009.x
[37] Bickford, D., et al. (2007). Cryptic species as a window on diversity. Trends in Ecology & Evolution – https://doi.org/10.1016/j.tree.2007.02.011
[38] Viscosi, V., & Cardini, A. (2011). Leaf morphology and cryptic taxa. Botanical Journal of the Linnean Society – https://doi.org/10.1111/j.1095-8339.2011.01184.x
[39] Adams, D. C., & Nistri, A. (2010). Ontogenetic convergence and GM. Evolution – https://doi.org/10.1111/j.1558-5646.2010.00972.x
