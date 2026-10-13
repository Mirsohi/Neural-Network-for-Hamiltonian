# Novelty check: has a neural network or ML model already been used to generate or predict the DMRG/MPS initial state? (2017–2026)

Scope and access notes (read first). Research date: 2026-10-13. This pass closes gaps left by `ml_neural_network_approaches.md` in this folder.

What worked:
- WebSearch, which returns titles and URLs only.
- WebFetch on arXiv `abs/` and `html/` pages.
- The INSPIRE-HEP REST API, including its full-text search. INSPIRE indexes a hep/quant-ph-heavy subset of arXiv, so its coverage of cond-mat.str-el and physics.chem-ph is partial.
- The MDPI PDF mirror (mdpi-res.com).
- eScholarship PDFs.
- The APS meeting archive.
- The Czech Academy (ASEP) repository record.

What failed:
- Direct curl to arxiv.org, export.arxiv.org, api.semanticscholar.org, api.openalex.org and Google: proxy 403.
- The arXiv search page: robots-disallowed.
- The Semantic Scholar API and web page, and the OpenAlex API: fetch errors.
- Crossref: it ignored the query and returned unrelated records.
- Europe PMC REST and PubMed: HTTP 429 rate limit or reCAPTCHA.
- Every pubs.acs.org URL variant, ResearchGate, and pubs.aip.org: fetch errors.
- The Kobe DMRG preprint list: robots-disallowed.

So nothing on the ACS JCTC pages could be read directly. JCTC content below comes from citing papers and bibliographic records, and each such case is flagged.

## Item 1: "Bridging the Gap between Transformer-Based Neural Networks and Tensor Networks for Quantum Chemistry" (JCTC 2025)

### Takeaway
This paper runs in the **reverse direction (MPS/DMRG → neural network)**. An independent 2025 paper cites it as an example of *pretraining an NQS from matrix product states*. No evidence was found that it uses a neural network to initialize DMRG. The abstract and numbers could not be read because ACS, PubMed, Semantic Scholar and ResearchGate were all blocked. **Classification: closely related, mirror-image direction (not "done exactly").**

### Cited Findings
- Full citation: Kan, B.; Tian, Y.; Wu, Y.; Zhang, Y.; Shang, H. "Bridging the Gap between Transformer-Based Neural Networks and Tensor Networks for Quantum Chemistry," *J. Chem. Theory Comput.* **21**, 3426–3439 (2025), DOI 10.1021/acs.jctc.4c01703 — bibliography entry [24] in [Wu, Zhang, Fang, Li, arXiv:2507.19276](https://arxiv.org/html/2507.19276); [ACS landing page (not readable)](https://pubs.acs.org/doi/10.1021/acs.jctc.4c01703); [PubMed record 40196992 (not readable, 429)](https://pubmed.ncbi.nlm.nih.gov/40196992/). The ACS URL path gives issue 7 ([ACS](https://pubs.acs.org/jctcce/article-abstract/21/7/3426/3693086/Bridging-the-Gap-between-Transformer-Based-Neural?redirectedFrom=fulltext)).
- How a citing paper describes it: Wu et al. (2025) say NQS results can be sensitive to parameter initialization, and that recent work addressed this through pretraining strategies. They cite Liu & Clark [23] for pretraining from a CISD wavefunction and **Kan et al. [24] for pretraining from matrix product states (MPS)** — [arXiv:2507.19276 HTML](https://arxiv.org/html/2507.19276).
- A second citing paper from the same group lineage, "Transformer-Based Neural Networks Backflow for Strongly Correlated Electronic Structure," cites Kan et al. only inside a range of second-quantized NQS works (refs 15–23), with no description. That paper itself uses no DMRG/MPS initialization in either direction; DMRG appears only as a benchmark — [arXiv:2509.25720](https://arxiv.org/html/2509.25720v1).
- Group context: the same corresponding author (H. Shang) had already published DMRG→NNQS pretraining in 2024 (Item 4) — [Mathematics 12, 433](https://doi.org/10.3390/math12030433).

### Inferences
- The likeliest reading is that the JCTC 2025 paper extends the 2024 *Mathematics* DMRG-pretraining idea to transformer NNQS, i.e. MPS → transformer. This is an inference from the citing description and the shared authors, not from the abstract.
- Even if it also discusses an exact MPS↔transformer correspondence, no source describes an NN → MPS → DMRG pipeline.

### Gaps
- Abstract, systems, bond dimensions and any convergence numbers were not retrieved: every ACS URL, PubMed (429), Europe PMC (429), Semantic Scholar and ResearchGate failed. A reader with ACS access should check whether the paper includes an NN → MPS conversion experiment. It is unlikely but not excluded.

## Item 2: "Symmetry-Blocked Matrix Product States as a Neural-Network Quantum-State Ansatz for Quantum Chemistry" (JCTC 2026)

### Takeaway
The paper is confirmed to exist only as a title and citation: *J. Chem. Theory Comput.* **22**(16), 8350 (2026). Authors, abstract and arXiv version could not be retrieved. The title says the MPS **is** the NQS ansatz (an MPS optimized as a neural-network-style VMC wavefunction). That is neither "NN initializes DMRG" nor clearly the reverse. **Classification (provisional): only analogous; unverified.**

### Cited Findings
- Title, journal, volume, issue and first page: "Symmetry-Blocked Matrix Product States as a Neural-Network Quantum-State Ansatz for Quantum Chemistry," *J. Chem. Theory Comput.* 22(16), 8350 (2026) — [ACS article-abstract URL (title from search index; page not readable)](https://pubs.acs.org/jctcce/article-abstract/22/16/8350/5253629/Symmetry-Blocked-Matrix-Product-States-as-a-Neural?redirectedFrom=fulltext); issue TOC [JCTC 22(16)](https://pubs.acs.org/jctcce/issue/22/16) (not readable).
- The closest open, related work found is Wu, Zhang, Fang, Li (2025), "Hybrid tensor network and neural network quantum states for quantum chemistry." It does not cite any symmetry-blocked MPS NQS paper.
  - Its BDG-RNN ansatz is **initialized from an MPS** ("initialized by using MPS generated from the Focus package"). The direction is MPS → NN only.
  - It contains no direct comparison of MPS-initialized versus random-initialized optimization.
  - Numbers:
    - H50 (STO-6G): BDG(1)-RNN at χ = 30 gives 0.6 mHa error, while a plain MPS needs χ > 50.
    - [Fe2S2(SCH3)4]2− CAS(30e,20o): chemical accuracy at χ = 200 versus χ = 400 for MPS.
    - H18 (3×3×2): ≈1.1 mHa at χ = 250 (χ = 150 with an RBM correlator), versus χ > 500 for MPS.
  - Semi-stochastic local energy gives ~2000× (H50) and ~80× (H18) cost reductions.
  - Source: [arXiv:2507.19276](https://arxiv.org/html/2507.19276).
- The 2026 APS Global Physics Summit NQS session (G42) has no talk title mentioning MPS, DMRG or initialization. Its 10 talks include "Foundation Neural-Networks Quantum States as a Unified Ansatz for Multiple Hamiltonians" (Rende) and "Data-Driven Pretraining of Time-Dependent NQS" (Wilke) — [APS GPS 2026 G42](https://meetings-archive.aps.org/smt/2026/mar-g42/).

### Inferences
- A "symmetry-blocked MPS as NQS ansatz" most plausibly treats a block-sparse (U(1)/SU(2)) MPS as an autoregressive, sampleable VMC ansatz, possibly started from DMRG. Initialization would then again run MPS → NQS. This is an inference from the title only.

### Gaps
- Authors, abstract, arXiv ID and results are unknown. Searches for a preprint under variant titles found nothing. Someone with ACS access must verify it.

## Item 3: Marks, Jiang, Devereaux — APS March Meeting 2019, C18.7 (and follow-ups)

### Takeaway
The talk title, "Accelerating Density Matrix Renormalization Group Computations with Machine Learning," and the abstract claim **ML-improved DMRG convergence time** for several classes of strongly correlated systems. The abstract does not say what the model predicts (initial state, Davidson guess, or other) and gives no numbers. **No follow-up paper or thesis was found.** INSPIRE lists Jacob Marks's later publications (2017–2021), and none is on ML-for-DMRG. **Classification: closely related, possibly "done exactly" but unverifiable.** It is the only prior claim found of ML that directly speeds up DMRG convergence.

### Cited Findings
- Title: "Accelerating Density Matrix Renormalization Group Computations with Machine Learning."
  - Authors: Jacob Marks (Physics, Stanford), Hong-Chen Jiang (SIMES, SLAC & Stanford), Thomas Devereaux (SIMES, SLAC & Stanford).
  - Oral talk in Session C18, "Machine Learning Quantum Many-body Models" (chair Yi Zhang). Monday, March 4, 2019, 4:06–4:18 PM, BCEC Room 156B, Boston. Bull. Am. Phys. Soc. 64(2).
  - Sources: [APS Bulletin MAR19 C18.7](https://meetings.aps.org/Meeting/MAR19/Session/C18.7); [APS meeting archive](https://meetings-archive.aps.org/mar/2019/c18/7).
- Abstract content (paraphrased from the archive page): DMRG works well for 1D and quasi-2D systems. The variational ground-state search is a major bottleneck. The authors apply ML to that step and report improved convergence time for several classes of strongly correlated systems. **No method details or numbers are on the page** — [APS archive](https://meetings-archive.aps.org/mar/2019/c18/7).
- Jacob Marks's INSPIRE record lists five works, none on ML-accelerated DMRG:
  - Correlation-assisted quantized charge pumping (with Schüler, Budich, Devereaux), PRB 103, 035112 (2021), arXiv:2001.01696.
  - Gauge invariance of light–matter interactions in first-principles tight-binding models, PRB 103, 155409 (2021), arXiv:2101.01143.
  - Dynamical signatures of SPT following symmetry breaking, PRR 3, 023137 (2021), arXiv:2101.12405.
  - Verdon, Marks et al., "Quantum Hamiltonian-Based Models and the Variational Quantum Thermalizer Algorithm," arXiv:1910.02071.
  - A 2017 NJP paper on qudit memory thresholds.
  - Source: [INSPIRE API query](https://inspirehep.net/api/literature?q=a%20J.Marks.1%20or%20a%20%22Marks%2C%20Jacob%22&size=25&fields=titles,authors.full_name,arxiv_eprints,dois,publication_info,document_type). The same-name matches may include different people.
- A DeepAI profile describes Jacob Marks as a "Stanford Physics PhD candidate conducting research in Condensed Matter Theory and Quantum Information" and a former Wolfram Research fellow — [DeepAI profile](https://cdnjs.deepai.org/profile/jacob-marks). Web results show a Jacob Marks later working as an ML developer advocate ([Zilliz](https://zilliz.com/authors/Jacob_Marks); [Embedded Vision Summit 2024](https://embeddedvisionsummit.com/2024/speaker/jacob-marks/)). This suggests he left academic physics, but it is not confirmed to be the same person.
- An INSPIRE query for author "Marks, Jacob" with "DMRG" in the title returned 0 hits — [INSPIRE](https://inspirehep.net/api/literature?q=a%20Marks%2C%20Jacob%20and%20t%20DMRG&size=10&fields=titles,authors.full_name,arxiv_eprints,abstracts,dois,publication_info).

### Inferences
- The 2019 work seems never to have been written up as a paper. Whatever the method was (possibly an ML-predicted initial MPS or Davidson guess), it left no citable, reproducible record. It shows the idea has been floated before, so a new paper should cite it. But it does not pre-empt a published, quantified method.

### Gaps
- No Stanford dissertation by Jacob Marks was found. SearchWorks and the Stanford Digital Repository could not be queried directly. If a thesis exists (c. 2021–2022), it may contain a chapter with the method and numbers. Checking `searchworks.stanford.edu` or emailing the authors is the remaining route.
- H.-C. Jiang's later DMRG papers were not systematically checked for an ML-initialization method. Spot searches found none.

## Item 4: Kan et al., *Mathematics* 12, 433 (2024) — tensor-network pretraining of NQS

### Takeaway
The direction is **DMRG → NNQS (reverse)**. A DMRG MPS is turned into CI-type {configuration, amplitude} data via a genetic algorithm (EDGA), and the NNQS is fitted to that data before VMC. **Measured gains are on the NNQS side:**
- Steps to chemical precision for H10/STO-6G fall from 2732 to as few as 347 (≈7.9×). For H2O they fall from 7376 to as few as 2358 (≈3.1×).
- Elapsed time improves only up to ≈1.6×, and some checkpoints are slower than no pretraining.
**Classification: closely related (mirror image of the project's idea).**

### Cited Findings
- Citation: Kan, B.; Tian, Y.; Xie, D.; Wu, Y.; Fan, Y.; Shang, H. "Solving the Electronic Schrödinger Equation by Pairing Tensor-Network State with Neural Network Quantum State," *Mathematics* **12**(3), 433 (2024), DOI 10.3390/math12030433 — [MDPI](https://www.mdpi.com/2227-7390/12/3/433); [PDF](https://mdpi-res.com/d_attachment/mathematics/mathematics-12-00433/article_deploy/mathematics-12-00433-v2.pdf?version=1706588699).
- Pipeline:
  1. DMRG produces an MPS. The bond dimension m is "manually assigned to make the computational cost acceptable", and no value is reported.
  2. An entanglement-driven genetic algorithm (EDGA), with mutual-information-guided mutations, extracts the important configurations and CI coefficients.
  3. The NNQS is pretrained by supervised regression against the DMRG ψ values, using AdamW with 4000 warmup steps.
  4. VMC follows.
  - Source: [MDPI HTML](https://www.mdpi.com/2227-7390/12/3/433/htm).
- The paper states "We employ DMRG for pre-training NNQS". Nothing describes an NN → MPS direction — [MDPI HTML](https://www.mdpi.com/2227-7390/12/3/433/htm).
- Systems: LiH (12 qubits), H2O (14), H10/STO-6G (20), N2 (20), NH3 (16), H2S (22), Li2O (30), C2H4O (38), and ferrocene (30 spin-orbitals, cc-pVTZ-DK) — [PDF](https://mdpi-res.com/d_attachment/mathematics/mathematics-12-00433/article_deploy/mathematics-12-00433-v2.pdf?version=1706588699).
- Steps to reach chemical precision (Table 4; checkpoint = number of pretraining steps):

  | Checkpoint | H10 | H2O |
  |---|---|---|
  | None | 2732 | 7376 |
  | 1000 | 890 | 6925 |
  | 2000 | 347 | 2871 |
  | 3000 | 507 | 2358 |

  — [PDF](https://mdpi-res.com/d_attachment/mathematics/mathematics-12-00433/article_deploy/mathematics-12-00433-v2.pdf?version=1706588699)
- Elapsed time (Table 3; units not stated):

  | Checkpoint | H10 | H2O |
  |---|---|---|
  | None | 103.79 | 1524.39 |
  | 1000 | 65.65 | 1580.02 |
  | 2000 | 76.34 | 944.51 |
  | 3000 | 113.55 | 1032.19 |

  So the best wall-clock gain is ≈1.6× for both molecules, and H2O@1000 and H10@3000 are *slower* than no pretraining. The authors attribute an abnormal H10 1000-step curve to overfitting — [PDF](https://mdpi-res.com/d_attachment/mathematics/mathematics-12-00433/article_deploy/mathematics-12-00433-v2.pdf?version=1706588699).
- C2H4O (38 qubits):
  - The initial VMC energy is −134.756 without pretraining, versus −149.321, −149.337 and −149.345 after 20k, 40k and 80k pretraining steps. The DMRG reference is ≈ −151.12; the figure label is garbled in extraction.
  - Without pretraining, the error is still > 0.02 at step 29,000.
  - Source: [PDF](https://mdpi-res.com/d_attachment/mathematics/mathematics-12-00433/article_deploy/mathematics-12-00433-v2.pdf?version=1706588699).

### Inferences
- This is the closest *quantified* evidence that a good tensor-network-derived starting point speeds up a *neural* variational solver: 3–8× fewer iterations, ≤1.6× wall-clock. The project's idea is the exact mirror (NN-derived start → DMRG), and no paper reporting that direction was found.
- The modest wall-clock gain, compared with the large iteration gain, is a caution for the project. Pretraining overhead can eat the convergence savings, so benchmarks should count generator cost.

### Gaps
- The DMRG bond dimensions used for pretraining were not reported. Energy units in Tables 2–3 are not stated (Hartree assumed for energies, seconds for time — unverified).

## Item 5: Golub et al., *Chem. Phys. Lett.* 813, 140297 (2023) — ML-predicted mutual information for DMRG orbital ordering

### Takeaway
**Authorship correction:** CPL 813, 140297 (2023) is by **Golub, Antalík, Beran, Brabec**, not "Golub, Yang, Vlček, Veis". The latter authors wrote a different paper, *J. Phys. Chem. Lett.* 16, 3295 (2025), on Δ-ML energy corrections. The CPL paper trains ML to predict orbital mutual information. It uses the predictions to set **orbital ordering** for DMRG, a pre-processing input and not the initial MPS. **No quantitative effect on DMRG energies or convergence could be retrieved**, and the abstract contains no numbers. **Classification: only analogous** (ML-predicted DMRG *input*, not initial state).

### Cited Findings
- Citation: Golub, P.; Antalík, A.; Beran, P.; Brabec, J. "Mutual information prediction for strongly correlated systems," *Chem. Phys. Lett.* **813**, 140297 (Feb 2023), DOI 10.1016/j.cplett.2023.140297.
  - Keywords: DMRG, quantum chemistry, mutual information, strong correlation, machine learning. Funded by GA ČR GJ19-13126Y.
  - Abstract content: a new ML model predicts mutual information, replacing expensive DMRG runs. It is tested on (i) determining correlation structure and (ii) **orbital ordering for accurate DMRG calculations**, and compared with accurate DMRG MI. The abstract gives no numbers.
  - Sources: [ASEP (CAS) record](https://asep.lib.cas.cz/arl-cav/en/detail-cav_un_epca-0566845-Mutual-information-prediction-for-strongly-correlated-systems); [Loughborough Primo/OSTI record with DOI](https://vufind.lboro.ac.uk/PrimoRecord/cdi_osti_scitechconnect_1960562); [Charles University record](https://nomos.is.cuni.cz/publication/643438?query=DMRG).
- The DOI resolves to Elsevier pii S0009261423000027. The linkinghub page returned no content — [doi.org](https://doi.org/10.1016/j.cplett.2023.140297).
- The related paper by the requested authors: Golub, P.; Yang, C.; Vlček, V.; Veis, L. "Quantum Chemical Density Matrix Renormalization Group Method Boosted by Machine Learning," *J. Phys. Chem. Lett.* **16**, 3295–3301 (2025).
  - A one-layer message-passing GNN (orbitals as nodes, MI edge feature, edge threshold 0.004) predicts the correction from low-M DMRG to reference energies.
  - Training set: 100 PAHs from COMPAS-1D. Tests: [3]triangulene, ovalene, C40H20, peripentacene, aza-[4]triangulene.
  - Error is **< 1 mHa for M = 750–1250**. The peripentacene state ordering is correct from M = 500 (gap 4.5–4.7 × 10⁻³ Ha versus reference 4.78 × 10⁻³ Ha).
  - **No wall-time numbers.** The paper does not cite Golub 2023 or any ML-for-DMRG-initialization work.
  - Source: [eScholarship PDF](https://escholarship.org/content/qt2r8757gr/qt2r8757gr.pdf).

### Inferences
- Neither Golub paper touches the initial MPS. One learns a DMRG input (ordering); the other post-processes the DMRG output (energy correction). Both show that orbital-graph GNN features (entropies, MI) work as inputs, which suits a chemistry-side initial-state generator.

### Gaps
- Effect sizes for ML-predicted versus DMRG-derived orderings in Golub 2023 were not retrieved. The ScienceDirect full text was unreadable and OSTI is robots-blocked.

## Additional searches via alternative routes (arXiv abs pages, INSPIRE full text, web search)

### Takeaway
Across ~25 query variants and two INSPIRE full-text queries, **no paper was found that uses a NN/ML model to generate or predict the initial MPS for DMRG and reports sweep or wall-clock savings.** Every NN↔MPS initialization found runs MPS → NN, or the NN replaces DMRG instead of warm-starting it.

### Cited Findings
- INSPIRE full-text query `"initial MPS" AND "machine learning"`: 29 hits (2017–2026). None is about ML-generated DMRG starts. They include SeeMPS (arXiv:2601.16734), TensorRL-QAS (arXiv:2505.09371), QCMaquis 4.0 (arXiv:2505.01405) and MPS preparation-circuit papers — [INSPIRE query](https://inspirehep.net/api/literature?q=fulltext%3A%22initial%20MPS%22%20and%20fulltext%3A%22machine%20learning%22&size=40&sort=mostrecent&fields=titles,arxiv_eprints).
- INSPIRE full-text query `"initialize DMRG"`: 10 hits. The relevant non-ML ones are "DMRG boosted by Gutzwiller projected wave functions" (arXiv:2009.04129), "Finite and infinite MPS for Gutzwiller projected mean-field wave functions" (arXiv:2009.00064) and controlled bond expansion (arXiv:2207.14712). None is ML — [INSPIRE query](https://inspirehep.net/api/literature?q=fulltext%3A%22initialize%20DMRG%22&size=40&sort=mostrecent&fields=titles,arxiv_eprints).
- Web-search variants returned no direct hit. These were: "warm start DMRG machine learning", "neural quantum state converted to MPS initial state DMRG", "RBM convert MPS initial state DMRG fewer sweeps", "hypernetwork outputs MPS tensors conditioned on Hamiltonian", "transfer learning DMRG", "amortized DMRG/MPS", "graph neural network predicts MPS tensors", "ML initial guess DMRG quantum chemistry", "NN predicts MPS from Hamiltonian parameters", "foundation model TN initial state DMRG", and "neural network initial state DMRG fewer sweeps / faster convergence". Results were generic DMRG references or the analogous items below — e.g., [ITensor DMRG FAQ](https://docs.itensor.org/ITensorMPS/stable/faq/DMRG.html), [Schollwöck review](https://homepages.physik.uni-muenchen.de/~Schollwoeck/annals.pdf).
- NN → MPS *conversion* (without DMRG) exists in theory. Howard (2019) gives conditions and an algorithm to map an RBM to an MPS, with an Ising proof, and mentions no DMRG — ["Deep learning of matrix product states," EasyChair Preprint 1239 (2019)](https://easychair.org/publications/preprint/FS1c). A 2018 APS abstract, "Efficient Representation of Matrix Product State with Restricted Boltzmann Machine," runs MPS → RBM — [APS MAR18 R34.3](https://meetings-archive.aps.org/mar/2018/r34/3).
- Supervised "ML MPS ansatz" (ChemRxiv 2022, later *J. Chem. Phys.* 158, 064108 (2023)): an MPS is fitted by supervised learning to CI coefficients (from ED/FCI or MCCI) for Heisenberg chains and ladders, as a cheaper alternative to variational optimization. It does not involve DMRG initialization — [ChemRxiv](https://chemrxiv.org/engage/chemrxiv/article-details/629f35def85b5916850040af); [JCP abstract page (not readable)](https://pubs.aip.org/aip/jcp/article-abstract/158/6/064108/2874971/Machine-learning-matrix-product-state-ansatz-for). Authors not retrieved.
- Reduced-basis surrogates (non-NN):
  - Greedy-selected MPS ground-state "snapshots" span a subspace that gives observables at any parameter value, applied to spin-1 chains.
  - The surrogate *replaces* new DMRG solves and is not used as a warm start. No speedup numbers in the abstract.
  - Source: [Brehmer, Herbst, Wessel, Rizzi, Stamm, PRE 108, 025306 (2023), arXiv:2304.13587](https://arxiv.org/abs/2304.13587).

### Inferences
- The "NN → MPS → DMRG warm start" pipeline has all its ingredients in the literature: NN↔MPS mappings, MPS-pretrained NQS, and Hamiltonian-conditioned networks. The assembled pipeline, benchmarked on DMRG sweeps or wall-clock, was not found.

### Gaps
- No arXiv full-text search was possible. arXiv search is robots-blocked, and the Google Scholar, Semantic Scholar and OpenAlex APIs were unreachable. INSPIRE full text covers only its indexed subset. Unindexed workshop papers (NeurIPS ML4PS, ICML AI4Science) and theses could still contain an attempt.

## 2025–2026 frontier: Hamiltonian-conditioned generators, operator learning for TT eigenproblems, LLM/agent DMRG tuning

### Takeaway
2026 has **Hamiltonian- or geometry-conditioned foundation models** that output wavefunctions, including one built on a neural tree tensor network. They are used as *replacements* for variational solves, with large reported amortization gains, and **not as DMRG warm starts**. No applied-math work was found that trains a model to initialize TT-ALS/DMRG eigen-solvers. LLM-agent work beyond Mantilla Calderón et al. runs tensor-network or CAS codes but does not learn initial states.

### Cited Findings
- **Hamilton-Zero (2026).** Heightman, Orlova, Mantrov, Ustimenko (ICFO; Simulacra Research), "Hamilton-Zero: A Neural Tensor-Network Foundation Model for Ground States of Arbitrary Quadratic Qubit Hamiltonians," [arXiv:2608.11911](https://arxiv.org/html/2608.11911).
  - About 0.5B parameters. The Hamiltonian (J, h) conditions the network, which outputs log ψ through a balanced binary merge tree with a shared rank-4 tensor ("a neural augmentation of tree tensor networks").
  - Trained on ≤ 64 qubits, fine-tuned to 1024 and evaluated up to 8100.
  - Zero-shot median gaps to ED: 4.02%, 4.21% and 12.63%. Fine-tuned: 3.1×10⁻⁴%, 1.2×10⁻³% and 6.0×10⁻³%.
  - It does **not** output an MPS for DMRG and reports no DMRG warm start. DMRG is mentioned only as inapplicable to its non-local topologies, and no prior NN-initialized-DMRG work is cited.
  - **Classification: closely related** (a Hamiltonian-conditioned TN-like generator; the missing step is MPS export plus DMRG refinement).
- **Foundation NQS for molecular PES (2026).** Fu, Wei, Wang, Shang, "Foundation Neural-Network Quantum States for Molecular Potential Energy Surfaces in Second Quantization," [arXiv:2609.37733](https://arxiv.org/abs/2609.37733).
  - A geometry-conditioned autoregressive NQS gives wavefunctions at unseen geometries for N2, CO and H4.
  - Orbital alignment lowers the MAE from 34–37 mHa to 0.049–0.085 mHa.
  - At ~1 mHa, frozen evaluation is **986× cheaper per geometry** than independent optimization, and **25.8×** cheaper end-to-end on a 161-point N2 grid.
  - No DMRG/MPS involvement stated. **Classification: only analogous** (amortization of NQS, not DMRG).
- **Rende et al.** "Foundation Neural-Networks Quantum States as a Unified Ansatz for Multiple Hamiltonians," APS GPS 2026 talk — [APS G42](https://meetings-archive.aps.org/smt/2026/mar-g42/). Analogous; no DMRG.
- **Applied math, TT eigenproblems.** Searches for learned initialization of TT-ALS/AMEn/DMRG eigen-solvers or "neural operator → tensor train" found only classical work: TT black-box approximation initialized by an ANOVA decomposition ([SIAM, DOI 10.1137/22M1514088](https://doi.org/10.1137/22M1514088)), the alternating linear scheme ([Holtz, Rohwedder, Schneider, SIAM J. Sci. Comput.](https://epubs.siam.org/doi/10.1137/100818893)), and deep-learning-aided ALS for **CP** (not TT) decomposition in MIMO channel estimation ([arXiv:2305.13947](https://arxiv.org/html/2305.13947v2)). **No learned TT eigen-solver initializer was found.** The CP-ALS paper is the nearest "learned ALS initialization" analog, outside physics.
- **LLM/agent work beyond Mantilla Calderón et al. (arXiv:2604.25610):**
  - Li, Ren, Cheng, Gong, "Autonomous Quantum Simulation through Large Language Model Agents." Multi-agent LLMs (DeepSeek-V3.2, Gemini 2.5 Pro, Claude Opus 4.5) perform tensor-network simulations with ~90% success on benchmark tasks: quantum phase transitions, open-system dynamics, photochemistry. Initial-state choice is not addressed and there are no speedup numbers — [arXiv:2601.10194](https://arxiv.org/abs/2601.10194).
  - Lee & Rondinelli, "Can Autonomous LLM Agents Execute Multireference Quantum Chemistry Calculations?" (Sept 2026). A Claude Opus 5 agent runs CASSCF/SC-NEVPT2 in ORCA. Coverage of 558 QUESTDB transitions rises from 24.9% to 44.1% with a decision ladder (MAE 0.373 → 0.339 eV), and replication MAE is 23 meV. **No DMRG runs** — [arXiv:2609.13357](https://arxiv.org/html/2609.13357v1).
  - Mantilla Calderón et al. (2026), already covered in `ml_neural_network_approaches.md`: an LLM "autoresearch" agent picks among *discrete* product initial states and sweep schedules under a 20 s budget for L = 64 Heisenberg/XXZ/XX chains, ΔE ≈ −0.0096 to −0.013 — [arXiv:2604.25610](https://arxiv.org/abs/2604.25610) (numbers from the earlier notes' fetch of the [HTML v2](https://arxiv.org/html/2604.25610v2); not re-fetched here). **Classification: closely related** (an AI system chooses the DMRG start, but by selecting among product states, not generating one).
- **Other 2025–2026 items surfaced but irrelevant to initialization:**
  - Excited local quantum annealing (ExcLQA), which beats an MPS-based method on Ising excited states, with no DMRG initialization — [arXiv:2507.12394](https://arxiv.org/abs/2507.12394).
  - "Quantum Tensor Network Learning with DMRG" (ESANN 2025), which uses DMRG to train ML models: [arXiv:2608.18901](https://arxiv.org/abs/2608.18901).
  - An iterative dual-channel NQS for selected CI, which uses no DMRG/MPS initialization — [arXiv:2606.26760](https://arxiv.org/html/2606.26760v1).
  - Transformer NQS on Fugaku, which also uses no DMRG/MPS initialization — [arXiv:2506.23809](https://arxiv.org/html/2506.23809).

### Inferences
- The 2026 trend is toward amortized, Hamiltonian-conditioned generators that *replace* per-instance optimization. Examples: Hamilton-Zero's zero-shot ground states, and the 986× per-geometry savings for foundation NQS. "Generator + DMRG refinement" is the natural, apparently unpublished combination. It could be framed as fixing the accuracy floor of zero-shot generators (Hamilton-Zero's 4–13% zero-shot gaps) with a few DMRG sweeps.

### Gaps
- Hamilton-Zero's full text was not checked for supplementary DMRG comparisons. The summary of the main text found none.
- No systematic check of NeurIPS/ICML 2025–2026 workshop proceedings was possible.

## Classification table and novelty verdict

### Takeaway
**No item was found that does the project's idea exactly:** a NN/ML model generating or predicting the starting MPS for DMRG, with measured sweep or wall-clock gains. Confidence is moderate-to-high, about 75–85%.

### Cited Findings
| Item | Direction | Classification | Key numbers |
|---|---|---|---|
| Marks, Jiang, Devereaux, APS MAR19 C18.7 ([link](https://meetings-archive.aps.org/mar/2019/c18/7)) | ML → speeds DMRG's variational step; mechanism unstated | Closely related (possibly exact, unverifiable) | None published; no paper/thesis found |
| Mantilla Calderón et al. 2026 ([arXiv:2604.25610](https://arxiv.org/abs/2604.25610)) | LLM agent *selects* product start + schedule | Closely related | ΔE ≈ −0.0096 to −0.013 at 20 s, L = 64 (from earlier notes) |
| Hamilton-Zero 2026 ([arXiv:2608.11911](https://arxiv.org/html/2608.11911)) | Hamiltonian-conditioned neural TTN; replaces solver | Closely related | Zero-shot 4–13% gaps; up to 8100 qubits; no DMRG |
| Kan et al., Mathematics 2024 ([DOI](https://doi.org/10.3390/math12030433)) | DMRG → NNQS pretraining (reverse) | Closely related (mirror) | Steps 2732→347 (H10), 7376→2358 (H2O); time ≤1.6× |
| Kan et al., JCTC 2025 "Bridging the Gap" ([cited in 2507.19276](https://arxiv.org/html/2507.19276)) | MPS → transformer NQS pretraining (reverse; per citing paper) | Closely related (mirror) | Not retrieved |
| Wu, Zhang, Fang, Li 2025 ([arXiv:2507.19276](https://arxiv.org/abs/2507.19276)) | MPS → BDG-RNN initialization (reverse) | Only analogous | Same accuracy at about half the χ of a plain MPS |
| Symmetry-blocked MPS as NQS ansatz, JCTC 22, 8350 (2026) ([ACS](https://pubs.acs.org/jctcce/article-abstract/22/16/8350/5253629/Symmetry-Blocked-Matrix-Product-States-as-a-Neural?redirectedFrom=fulltext)) | MPS *as* NQS ansatz (title only) | Only analogous (provisional) | Not retrieved |
| Golub, Antalík, Beran, Brabec, CPL 2023 ([record](https://asep.lib.cas.cz/arl-cav/en/detail-cav_un_epca-0566845-Mutual-information-prediction-for-strongly-correlated-systems)) | ML-predicted MI → DMRG orbital ordering | Only analogous | Not retrieved |
| Golub, Yang, Vlček, Veis, JPCL 2025 ([PDF](https://escholarship.org/content/qt2r8757gr/qt2r8757gr.pdf)) | GNN corrects low-M DMRG energies (post-hoc) | Only analogous | < 1 mHa at M = 750–1250; no timings |
| Fu, Wei, Wang, Shang 2026 ([arXiv:2609.37733](https://arxiv.org/abs/2609.37733)) | Geometry-conditioned foundation NQS | Only analogous | 986× per-geometry, 25.8× end-to-end |
| Brehmer et al., PRE 2023 ([arXiv:2304.13587](https://arxiv.org/abs/2304.13587)) | MPS-snapshot reduced basis (non-NN surrogate) | Only analogous | No speedups in abstract |
| ML MPS ansatz, JCP 158, 064108 (2023) ([ChemRxiv](https://chemrxiv.org/engage/chemrxiv/article-details/629f35def85b5916850040af)) | Supervised fit of MPS to CI data | Only analogous | Not retrieved |
| Howard 2019 RBM→MPS mapping ([EasyChair](https://easychair.org/publications/preprint/FS1c)) | NN → MPS conversion, no DMRG | Only analogous | None |
| Li, Ren, Cheng, Gong 2026 ([arXiv:2601.10194](https://arxiv.org/abs/2601.10194)); Lee & Rondinelli 2026 ([arXiv:2609.13357](https://arxiv.org/html/2609.13357v1)) | LLM agents run TN/CAS codes | Only analogous | ~90% task success; 24.9→44.1% coverage |

### Inferences
- **Novelty verdict.** Across direct reads of arXiv abstract/HTML pages, INSPIRE full-text queries, ~25 web-search variants, and targeted checks of all five named items, I found **no published or preprint work (2017–2026) that uses a neural network or other ML model to generate or predict the initial MPS for DMRG and reports measured speedups.** Every NN↔TN initialization link found runs the other way: DMRG/MPS pretrains or initializes an NQS. Kan et al. 2024 quantify that reverse direction at 3–8× fewer VMC steps but ≤1.6× wall-clock. The 2026 Hamiltonian-conditioned foundation models replace solvers rather than warm-start DMRG.
- The closest precedents are:
  - the never-published 2019 Marks–Jiang–Devereaux claim that ML accelerates DMRG convergence, which should be cited;
  - Mantilla Calderón et al. 2026, where an AI agent selects among product starts;
  - Hamilton-Zero 2026, a TN-structured, Hamiltonian-conditioned generator without DMRG refinement.
- I rate confidence that the exact idea is unpublished at about 75–85%.

### Gaps
- Two JCTC papers could not be read: Kan et al. 2025, and the 2026 symmetry-blocked MPS NQS paper, whose authors are unknown.
- No arXiv/Google Scholar full-text search was possible.
- No Stanford thesis by Marks was found.
- Golub 2023 effect sizes were not retrieved.
- Workshop papers (NeurIPS ML4PS, ICML) and non-English venues were not covered.
- Rate limits blocked pages: Europe PMC REST and PubMed returned HTTP 429, and the PubMed search page showed reCAPTCHA. Those routes were abandoned for this session.
