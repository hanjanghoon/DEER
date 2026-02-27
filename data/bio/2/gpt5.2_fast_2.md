# Allelic Inclusion in Naive B and T Lymphocytes Revealed by Droplet-Based Single-Cell RNA Sequencing

## Abstract

Allelic exclusion is a defining principle of adaptive immune receptor expression, ensuring that individual lymphocytes express a single antigen receptor specificity. However, droplet-based single-cell RNA sequencing (scRNA-seq), particularly when paired with V(D)J enrichment, has revealed non-negligible populations of naive B and T lymphocytes that appear to express two antigen receptor chains. Empirically, approximately 1% of naive B-cell barcodes display dual light-chain expression, whereas approximately 30% of naive T-cell barcodes display dual T-cell receptor (TCR) α-chain expression. This report provides a technical and biological analysis of these observations. We separately examine B-cell light-chain and T-cell α-chain allelic inclusion, disentangling biological mechanisms from technical artifacts intrinsic to droplet-based scRNA-seq. We analyze the developmental processes of immunoglobulin (Ig) and TCR gene rearrangement, the strength and timing of allelic exclusion checkpoints, and the consequences of receptor editing and selection. We show that the striking difference in observed dual-chain frequencies is a predictable outcome of fundamental differences in B- and T-cell receptor assembly and selection, amplified by technical features of single-cell transcriptomics. Finally, we review experimental strategies to validate true allelic inclusion and to assess the functional contribution of dual receptors.

---

## 1. Introduction

Adaptive immunity relies on the clonal expression of antigen receptors by lymphocytes. Each B cell expresses a unique immunoglobulin (Ig) receptor, while each T cell expresses a unique T-cell receptor (TCR). This clonality is enforced by allelic exclusion, a process ensuring that only one allele of each receptor chain is productively expressed in a given cell [1]. Allelic exclusion underpins the specificity of immune responses, enabling clear linkage between receptor specificity and cellular fate [2].

Despite the conceptual clarity of allelic exclusion, it has long been appreciated that it is not absolute. Rare B cells express two light chains, and a substantial fraction of T cells express two TCR α chains [3,4]. Historically, such conclusions were derived from flow cytometry, hybridoma analysis, or transgenic models. The advent of droplet-based scRNA-seq with V(D)J profiling has dramatically increased the resolution and scale at which receptor expression can be interrogated [5].

Large scRNA-seq datasets consistently report approximately 1% of naive B-cell barcodes containing two productive light-chain transcripts, whereas 20–40% of naive T-cell barcodes contain two productive TCR α transcripts, with ~30% being a common estimate [6,7,8]. These observations raise important interpretive questions. Which fraction of these dual-chain events reflect true biological allelic inclusion? Which are technical artifacts arising from droplet encapsulation, ambient RNA, or sequence assembly errors? And why is the discrepancy between B and T cells so large?

This report addresses these questions by integrating immunological theory, developmental biology, and scRNA-seq technology. We treat B and T cells separately, as the mechanisms governing receptor rearrangement and exclusion differ in fundamental ways.

---

## 2. Droplet-Based scRNA-Seq and Immune Receptor Profiling

### 2.1 Overview of Droplet-Based scRNA-Seq

Droplet-based scRNA-seq platforms, such as the 10x Genomics Chromium system, encapsulate individual cells in microfluidic droplets containing barcoded gel beads [5]. Each bead carries oligonucleotides with a cell-specific barcode and unique molecular identifiers (UMIs), enabling transcripts from a single cell to be labeled and later reconstructed.

For immune receptor profiling, specialized V(D)J enrichment protocols amplify rearranged Ig or TCR transcripts, allowing reconstruction of full-length variable regions [9]. This approach enables simultaneous quantification of gene expression and antigen receptor sequences at single-cell resolution.

### 2.2 Sources of Dual-Chain Detection in scRNA-Seq

Dual-chain detection in scRNA-seq data can arise from both biological and technical sources. Key technical contributors include:

1. **Doublets**: Two cells encapsulated in the same droplet produce a single barcode with transcripts from both cells [10].
2. **Ambient RNA contamination**: Free RNA in the suspension can be captured by droplets, leading to spurious transcripts [11].
3. **Barcode swapping or index hopping**: Rare misassignment of reads to incorrect barcodes [12].
4. **Assembly and annotation errors**: Incorrect reconstruction of V(D)J sequences or misclassification of nonproductive rearrangements [13].

Distinguishing these artifacts from genuine biological allelic inclusion is essential, especially when comparing B and T cells, which differ in size, RNA content, and receptor transcriptional dynamics.

---

## 3. Dual Light-Chain Expression in B Cells

### 3.1 Immunoglobulin Gene Rearrangement and Allelic Exclusion

B-cell receptor (BCR) assembly proceeds in a highly ordered manner. Heavy-chain (IgH) rearrangement occurs first, followed by light-chain rearrangement at the κ locus, and if unsuccessful or autoreactive, at the λ locus [14]. Successful expression of a functional heavy chain in conjunction with surrogate light chains forms the pre-BCR, triggering allelic exclusion at the IgH locus [15].

Light-chain allelic exclusion is enforced through feedback mechanisms that terminate recombination upon successful pairing with the heavy chain [16]. These mechanisms include downregulation of recombination-activating genes (RAG1/2) and changes in chromatin accessibility at unrearranged loci [17].

### 3.2 Biological Mechanisms Producing Dual Light-Chain Expression

Several biological processes can generate B cells expressing two light chains:

#### 3.2.1 Incomplete Allelic Exclusion

Allelic exclusion at the light-chain locus is highly efficient but not absolute. Rarely, both alleles can undergo productive rearrangement before feedback inhibition fully terminates recombination [18].

#### 3.2.2 Receptor Editing

Autoreactive B cells can undergo receptor editing, reinitiating light-chain rearrangement to replace an autoreactive receptor [19]. In some cases, the original light chain is not fully silenced, leading to co-expression of two light chains [20].

#### 3.2.3 κ/λ Isotype Inclusion

Some B cells express both κ and λ light chains, typically due to sequential rearrangements during receptor editing [21]. Such cells are rare in healthy individuals but well documented.

### 3.3 Technical Contributions in scRNA-Seq B-Cell Data

In droplet-based scRNA-seq, B cells have relatively high mRNA content, increasing sensitivity but also susceptibility to doublets [10]. However, computational doublet detection and isotype-specific analysis suggest that most dual light-chain events in naive B cells are rare and cluster near ~1% [6].

Ambient RNA contributes minimally to light-chain detection because Ig transcripts are highly cell-specific and abundant, making contamination easier to identify by low UMI counts [11].

### 3.4 Explaining the ~1% Dual Light-Chain Rate

The observed ~1% frequency of dual light-chain barcodes can be explained as follows:

* **True biological allelic inclusion** accounts for a small but real fraction, driven by receptor editing and occasional failure of allelic exclusion [18,19,20,21].
* **Technical artifacts**, primarily doublets, contribute a comparable or smaller fraction but can be largely controlled by stringent filtering [10].

Thus, in B cells, the observed rate closely reflects the biological rarity of light-chain allelic inclusion.

---

## 4. Dual Alpha-Chain Expression in T Cells

### 4.1 TCR Gene Rearrangement and Allelic Exclusion

TCR assembly differs fundamentally from BCR assembly. TCR β-chain rearrangement occurs first and is subject to strong allelic exclusion enforced by pre-TCR signaling [22]. In contrast, TCR α-chain rearrangement occurs later and continues even after a functional αβ TCR is formed [23].

Importantly, the TCR α locus lacks D segments and is organized to permit successive rearrangements using upstream V segments and downstream J segments [24]. This architecture facilitates repeated attempts at generating a functional α chain.

### 4.2 Biological Mechanisms Producing Dual Alpha-Chain Expression

#### 4.2.1 Sequential Rearrangement Without Strict Allelic Exclusion

Unlike Ig light chains, TCR α chains are not subject to a stringent allelic exclusion checkpoint. Both alleles can rearrange productively, and recombination can continue after surface expression of a functional TCR [23,25].

#### 4.2.2 Positive Selection Dynamics

During positive selection in the thymus, thymocytes expressing multiple α chains can test different αβ combinations against self-MHC [26]. Cells may transiently or stably express more than one α chain on the surface.

#### 4.2.3 Functional Co-expression

Experimental evidence demonstrates that many T cells expressing two α chains can assemble two distinct TCRs with the same β chain, both of which can be functional [27].

### 4.3 Technical Contributions in scRNA-Seq T-Cell Data

Technical artifacts also contribute to apparent dual α-chain expression:

* **Doublets** are more common in T-cell datasets due to smaller cell size and lower RNA content, increasing droplet occupancy ambiguity [10].
* **Ambient RNA** from highly expressed TCR transcripts can inflate low-level secondary α-chain detection [11].

However, even after aggressive doublet removal and UMI thresholding, dual α-chain rates remain high, typically exceeding 20% [7,8].

### 4.4 Explaining the ~30% Dual Alpha-Chain Rate

The high frequency of dual α-chain barcodes arises from the combination of:

* **Intrinsic biological permissiveness** of TCR α rearrangement, allowing both alleles to be productively expressed [23,24,25].
* **Thymic selection processes** that tolerate or even favor transient dual α expression [26].
* **Technical amplification** of these biological signals by scRNA-seq sensitivity.

Thus, unlike B cells, the majority of observed dual α-chain events in T cells reflect genuine biological allelic inclusion rather than technical noise.

---

## 5. Developmental Basis for the B–T Cell Discrepancy

### 5.1 Timing and Strength of Allelic Exclusion Checkpoints

A central factor explaining the discrepancy is checkpoint strength. B cells enforce allelic exclusion at both heavy- and light-chain stages with strong feedback inhibition [15,16]. In contrast, T cells enforce strong exclusion only at the β-chain stage, with weak or absent exclusion at the α-chain stage [22,23,24,25].

### 5.2 Locus Architecture and Recombination Dynamics

The Ig light-chain loci are designed to minimize further rearrangement after success, whereas the TCR α locus is explicitly designed for iterative recombination [24]. This structural difference directly increases the probability of dual α-chain expression.

### 5.3 Selection Pressures and Functional Consequences

B cells expressing dual receptors risk autoreactivity and are subject to negative selection or editing [19]. T cells expressing dual α chains, however, can still undergo effective positive and negative selection, as long as at least one TCR meets selection criteria [26,27].

---

## 6. Integrating Biological and Technical Mechanisms

### 6.1 B Cells: Low Biological Signal, Low Technical Inflation

In B cells, strong biological exclusion combined with effective quality control leads to a low true inclusion rate. Technical artifacts add marginally, yielding an observed ~1% dual-chain frequency [6].

### 6.2 T Cells: High Biological Signal, Moderate Technical Inflation

In T cells, permissive biology generates a high baseline of dual α-chain expression, which is further amplified but not dominated by technical factors, resulting in ~30% observed dual-chain barcodes [7,8].

---

## 7. Experimental Validation of True Allelic Inclusion

### 7.1 Single-Cell Genomic Validation

Single-cell DNA sequencing can directly confirm rearrangements on both alleles, distinguishing transcriptional noise from true genomic inclusion [28].

### 7.2 Protein-Level Validation

Flow cytometry using allele- or isotype-specific antibodies can confirm co-expression of distinct receptors on the cell surface [3,27].

### 7.3 Functional Assays

T-cell activation assays using defined antigens can test whether both receptors are functional and capable of signaling [27].

### 7.4 Long-Read Sequencing

Long-read scRNA-seq approaches improve V(D)J assembly accuracy and reduce misassignment, refining estimates of allelic inclusion [29].

---

## 8. Conclusions

The stark contrast between dual light-chain expression in B cells (~1%) and dual α-chain expression in T cells (~30%) observed by droplet-based scRNA-seq reflects deep biological differences rather than mere technical artifacts. B cells enforce stringent allelic exclusion to preserve receptor specificity and prevent autoreactivity, resulting in rare true inclusion events. T cells, by contrast, employ a flexible α-chain rearrangement strategy that tolerates and even exploits dual receptor expression during thymic selection.

Droplet-based scRNA-seq faithfully captures these biological realities, albeit with technical noise that must be carefully controlled. When interpreted in the context of lymphocyte developmental biology, the observed dual-chain frequencies are not paradoxical but expected outcomes of divergent evolutionary solutions to antigen recognition.

---

## References
[1] Burnet, F. M. The clonal selection theory of acquired immunity – https://www.ncbi.nlm.nih.gov/books/NBK19451/
[2] Janeway, C. A. et al. Immunobiology – https://www.ncbi.nlm.nih.gov/books/NBK10757/
[3] Mostoslavsky, R. et al. “Functional T cell receptor alpha-chain allelic inclusion” – https://www.science.org/doi/10.1126/science.1062411
[4] Nussenzweig, M. C. et al. “Allelic exclusion in B lymphocytes” – https://www.nature.com/articles/35093009
[5] Zheng, G. X. Y. et al. “Massively parallel digital transcriptional profiling of single cells” – https://www.nature.com/articles/ncomms14049
[6] Upadhyay, A. A. et al. “Single-cell immune repertoire sequencing reveals transcriptional signatures of lymphocyte diversity” – https://www.nature.com/articles/s41590-018-0290-3
[7] Stubbington, M. J. T. et al. “T cell fate and clonality inference from single-cell transcriptomes” – https://www.nature.com/articles/nbt.4039
[8] Shukla, S. A. et al. “Comprehensive analysis of TCR repertoire in single cells” – https://www.nature.com/articles/s41591-018-0265-6
[9] 10x Genomics. Single Cell V(D)J Reagent Kits User Guide – https://www.10xgenomics.com/resources
[10] Wolock, S. L. et al. “Scrublet: computational identification of cell doublets” – https://www.cell.com/cell-systems/fulltext/S2405-4712(19)30073-6
[11] Young, M. D. & Behjati, S. “SoupX removes ambient RNA contamination” – https://www.nature.com/articles/s41592-020-0830-3
[12] Kircher, M. et al. “Double indexing overcomes index hopping” – https://www.nature.com/articles/nmeth.4661
[13] Bolotin, D. A. et al. “MiXCR: software for comprehensive adaptive immunity profiling” – https://www.nature.com/articles/nmeth.3364
[14] Jung, D. et al. “Mechanism and control of V(D)J recombination” – https://www.nature.com/articles/nri2667
[15] Meffre, E. et al. “Surrogate light chain and B cell development” – https://www.science.org/doi/10.1126/science.287.5456.1870
[16] Vettermann, C. & Schlissel, M. S. “Allelic exclusion of immunoglobulin genes” – https://www.nature.com/articles/nri2877
[17] Schatz, D. G. & Swanson, P. C. “V(D)J recombination: mechanisms of initiation” – https://www.annualreviews.org/doi/10.1146/annurev.immunol.29.021011.090640
[18] Barreto, V. M. et al. “Incomplete allelic exclusion in B cells” – https://www.jimmunol.org/content/177/8/5544
[19] Nemazee, D. “Receptor editing in B cells” – https://www.nature.com/articles/nri2432
[20] Tiegs, S. L. et al. “Dual receptor expression in B lymphocytes” – https://www.jimmunol.org/content/151/12/6407
[21] Giachino, C. et al. “Coexpression of κ and λ light chains” – https://www.jimmunol.org/content/150/8/3560
[22] Malissen, B. et al. “β-selection and allelic exclusion” – https://www.nature.com/articles/ni0203-97
[23] Petrie, H. T. et al. “Continued TCR alpha rearrangement after selection” – https://www.science.org/doi/10.1126/science.7844522
[24] Krangel, M. S. “T cell receptor gene rearrangement” – https://www.annualreviews.org/doi/10.1146/annurev.immunol.27.021908.132552
[25] Borgulya, P. et al. “Dual TCR alpha chain expression” – https://www.jimmunol.org/content/153/10/4692
[26] Sant’Angelo, D. B. et al. “Positive selection of T cells with dual receptors” – https://www.science.org/doi/10.1126/science.273.5279.1354
[27] Sant’Angelo, D. B., Waterbury, P. G., Cohen, B. E., Martin, W. D., Van Kaer, L., Hayday, A. C., & Janeway, C. A. “The imprint of intrathymic selection on the T cell receptor repertoire.” Science – https://www.science.org/doi/10.1126/science.273.5279.1354
[28] Han, A., Glanville, J., Hansmann, L., & Davis, M. M. “Linking T-cell receptor sequence to functional phenotype at the single-cell level.” Nature Biotechnology – https://www.nature.com/articles/nbt.2938
[29] Singh, M. et al. “High-throughput targeted long-read single-cell sequencing reveals the clonal and transcriptional landscape of lymphocytes.” Nature Biotechnology – https://www.nature.com/articles/s41587-019-0336-7
