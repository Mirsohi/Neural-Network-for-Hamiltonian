# ML / Neural-Network Approaches to Generating, Converting, or Predicting Initial States (and Initial Parameters) for DMRG/MPS and Analogous Variational Many-Body Solvers

Scope note (read first): research done 2026-10-13. Direct arXiv API access was blocked by the egress proxy. Several publisher pages could not be read: MDPI (HTTP 429 rate limit), ACS (fetch error), PMC (reCAPTCHA), OSTI (robots.txt). For those papers, claims come from arXiv abstract pages, indexing records, or search-result metadata. Each such case is flagged. Web search returned titles and URLs only, so most numbers below come from fetched arXiv abstract or HTML pages. Items marked "(metadata not fetched this session)" cite canonical, widely known bibliographic data that I did not re-verify here.

Novelty verdict in one line: **I found no paper (2017–2026) that trains a neural network to generate a DMRG/MPS initial state and then reports sweep-count or wall-clock reductions for DMRG.** The closest items are:
- (a) a 2019 APS March Meeting abstract (Marks, Jiang, Devereaux) claiming ML "improve[s] convergence time" of DMRG, with no mechanism stated and no follow-up paper found;
- (b) a 2026 LLM-agent "autoresearch" study that tunes DMRG protocols, including the choice of product initial state, under a fixed 20 s budget;
- (c) many works in the *reverse* direction (DMRG/MPS → initialize or pretrain an NQS or a quantum circuit);
- (d) ML used elsewhere in the DMRG workflow: energy correction, mutual-information prediction for orbital ordering.

---

## Q1. NQS ↔ tensor-network mappings: has anyone converted a trained NQS (RBM/CNN/transformer) into an MPS and used it to initialize DMRG?

### Takeaway
The exact and approximate mappings between NQS and tensor networks are well established (2017–2018 theory, 2022–2025 algorithms). Every *practical* conversion I found runs MPS → NN: MPS → RBM via CP decomposition (2025), and MPS → RNN exactly (2023). I found **no published pipeline that compresses a trained NQS into an MPS and hands it to DMRG as a starting state**, and so no reported DMRG speedups from one. This appears to be an open gap.

### Cited Findings
- **Carleo & Troyer (2017).** Introduced NQS (RBM wavefunction plus variational Monte Carlo) — G. Carleo, M. Troyer, "Solving the quantum many-body problem with artificial neural networks," *Science* 355, 602 (2017), [arXiv:1606.02318](https://arxiv.org/abs/1606.02318) (metadata not fetched this session).
- **Deng, Li, Das Sarma (2017).** "The entanglement of all short-range RBM states satisfies an area law for arbitrary dimensions and bipartition geometry," while long-range RBM states "could exhibit volume-law entanglement." Random-weight RBMs have volume-law average entanglement that differs from the Page value, and their entanglement spectra show Poisson-type level statistics — [Deng, Li, Das Sarma, "Quantum Entanglement in Neural Network States," PRX 7, 021021 (2017), arXiv:1701.04844](https://arxiv.org/abs/1701.04844).
- **Chen, Cheng, Xie, Wang, Xiang (2018).**
  - "We devise efficient algorithms to translate an RBM into the commonly used TNS."
  - They give "sufficient and necessary conditions to determine whether a TNS can be transformed into an RBM."
  - They note that "RBM can represent quantum many-body states with fewer parameters compared to TNS."
  - The abstract page gives no explicit bond-dimension bounds.
  - Source: [Chen et al., "Equivalence of restricted Boltzmann machines and tensor network states," PRB 97, 085104 (2018), arXiv:1701.04831](https://arxiv.org/abs/1701.04831).
- **Glasser, Pancotti, August, Rodriguez, Cirac (2018).**
  - "Short-range Restricted Boltzmann Machines are Entangled Plaquette States."
  - "Fully connected Restricted Boltzmann Machines are String-Bond States with a nonlocal geometry and low bond dimension."
  - They propose a way to combine TN and NN, show that NQS and the SBS extension describe a lattice FQH state exactly, and approximate a chiral spin liquid "with better accuracy than Entangled Plaquette States."
  - Source: [Glasser et al., PRX 8, 011006 (2018), arXiv:1710.04045](https://arxiv.org/abs/1710.04045).
- **Wu, Rossi, Vicentini, Carleo (2023).** "Any matrix product state (MPS) can be exactly represented by a recurrent neural network (RNN)" with linear memory update. A multilinear 2D extension encodes wavefunctions "using a bond dimension lower by orders of magnitude when compared to MPS" — [Wu et al., "From Tensor Network Quantum States to Tensorial Recurrent Neural Networks," PRR 5, L032001 (2023), arXiv:2206.12363](https://arxiv.org/abs/2206.12363).
- **Kaneko & Goto (2025), MPS → RBM.**
  - Method: approximately convert MPS into RBMs with a multinomial hidden unit via canonical polyadic (CP) decomposition, to seed NQS ground-state calculations.
  - Main test: open-boundary TFIM, n = 16, MPS D_max = 8, DMRG converged to better than 10⁻⁹ J.
  - CP rank R scanned 8–64. For h/J = 0.5, "when R ≥ 24, the energy error becomes less than 10⁻⁴."
  - Infidelity and energy error scale roughly as R⁻².
  - In the periodic h/J = 1 size study with R = n/2, the VMC energy error is "always less than 2%."
  - There is no random-initialization baseline, so VMC iteration savings are not quantified.
  - The paper does not propose the reverse NQS → MPS → DMRG route.
  - Source: [Kaneko & Goto, "Seeding neural network quantum states with tensor network states," arXiv:2506.23550 (2025)](https://arxiv.org/abs/2506.23550); details from [HTML](https://arxiv.org/html/2506.23550).
- **Pastori, Kaubruegger, Budich (2019).** "Generalized transfer matrix states from artificial neural networks": a neural network produces configuration-dependent matrices whose product gives the amplitude. This is the closest early example of "an NN that outputs MPS-like matrices," but it is a variational ansatz, not an MPS handed to DMRG — [arXiv:1808.02069](https://arxiv.org/pdf/1808.02069) (abstract not fetched this session; description from prior knowledge, treat as unverified).
- **Practical conversion tool (not ML-specific).** Tensor cross interpolation (TCI) learns an MPS/tensor train from black-box function evaluations. It is therefore a candidate route for NQS → MPS (amplitude oracle → TT) — [Fernández et al., "Learning tensor networks with tensor cross interpolation: New algorithms and libraries," SciPost Phys. 18, 104 (2025), arXiv:2407.02454](https://scipost.org/SciPostPhys.18.3.104). I found no paper that applies TCI to a trained NQS in order to initialize DMRG.
- **2018 APS March Meeting abstract.** "Efficient Representation of Matrix Product State with Restricted Boltzmann Machine" (MPS → RBM direction; I could not view the abstract text) — [APS MAR18 R34.3](https://meetings-archive.aps.org/mar/2018/r34/3).

### Inferences
- **NQS → MPS is sound in principle.** The area-law result for short-range RBMs (Deng 2017) and the efficient RBM → TNS algorithms (Chen 2018) mean that NQS trained on gapped 1D ground states should compress to modest-χ MPS. NQS with long-range or volume-law structure (fully connected RBMs, transformers) may need impractically large χ unless compressed variationally (fit to the NQS by sampling or TCI) rather than converted exactly.
- **The community has optimized the other direction.** MPS → NQS seeding (Kaneko & Goto 2025) and exact MPS ⊂ RNN embeddings (Wu 2023) are mature, which suggests the practical bottleneck is NQS optimization, not DMRG warm-up. The NQS → DMRG direction needs an explicit argument for why it beats cheap DMRG warm-up sweeps.

### Gaps
- No paper found reporting fidelity, sweeps, or wall-clock for "trained NQS → MPS (exact, sampled, or TCI) → DMRG." Search coverage limits (blocked arXiv API, title-only search results) mean I cannot fully exclude workshop papers or theses.
- I could not retrieve the explicit RBM → MPS bond-dimension bounds from Chen et al. (abstract page only).

---

## Q2. The reverse direction and hybrids: DMRG/MPS used to pretrain or initialize NQS; MPS–NQS hybrids; what they show about convergence

### Takeaway
Using DMRG/MPS to initialize or pretrain neural ansätze is common and documented (2022–2025): ANTN, backflow-MPS, TN-pretrained NQS for chemistry, MPS → RBM seeding. One careful ablation (ANTN) finds that the **MPS structure (inductive bias) matters more than the DMRG initialization itself**. This cautions anyone expecting large gains from initialization alone.

### Cited Findings
- **ANTN (Chen, Newhouse, Chen, Luo, Soljačić; NeurIPS 2023).**
  - "In practice, we can initialize the TN component with the optimized DMRG results of the same bond dimension," which the authors describe as "a pretraining of the ANTN."
  - Their ablation: "the improvement from ANTN mainly comes from the effective inductive bias of MPS structure," and TN initialization matters less than the structure itself.
  - 10×10 J1–J2 energies per site (lower is better):

    | J2 | DMRG χ=1024 | PixelCNN | ANTN elementwise χ=8 |
    |---|---|---|---|
    | 0.5 | −1.938770 | −1.74098 | −1.94001 |
    | 0.2 | −2.255633 | — | −2.26034 |

  - At 10×10, J2 = 0.8, DMRG (−2.062730) beats both ANTN variants.
  - Source: [Chen et al., "ANTN: Bridging Autoregressive Neural Networks and Tensor Networks for Quantum Many-Body Simulation," arXiv:2304.01996](https://arxiv.org/abs/2304.01996); numbers from [HTML v3](https://arxiv.org/html/2304.01996v3); venue [NeurIPS 2023](https://neurips.cc/virtual/2023/poster/70347).
- **MPS with backflow correlations (Lami, Carleo, Collura 2022).** The MPS ansatz is extended with backflow-style configuration dependence and optimized with a TN + VMC scheme. It is "competitive" with state-of-the-art 2D methods on S=1/2 J1–J2. The abstract does not say whether the MPS part is DMRG-initialized — [PRB 106, L081111 (2022), arXiv:2201.00810](https://arxiv.org/abs/2201.00810). (Note: the brief's "Lami, Carleo, Collura, 'MPS-based NQS'" is this paper.)
- **Kan, Tian, Xie, Wu, Fan, Shang (2024).** The authors "develop a novel approach through incorporating the density-matrix renormalization group (DMRG) method" with NQS. "When tensor-network pre-training is introduced into the neural network," high efficiency is achieved for strongly correlated systems. The abstract gives no numbers, and the full text could not be fetched (MDPI 429) — ["Solving the Electronic Schrödinger Equation by Pairing Tensor-Network State with Neural Network Quantum State," *Mathematics* 12(3), 433 (2024)](https://ideas.repec.org/a/gam/jmathe/v12y2024i3p433-d1329006.html), [DOI](https://doi.org/10.3390/math12030433).
- **Wu, Zhang, Fang, Li (2025).** Hybrid TN + NN ansätze for chemistry: a bounded-degree graph RNN and RBM-inspired correlators. They are meant to address "initialization challenges" and TN expressivity. Chemical accuracy is reported on H50, [Fe2S2(SCH3)4]²⁻ and 3D H18 (code: PyNQS); the abstract gives no numbers — [arXiv:2507.19276 (2025)](https://arxiv.org/abs/2507.19276).
- **Kaneko & Goto (2025).** MPS → RBM seeding via CP decomposition; numbers under Q1 — [arXiv:2506.23550](https://arxiv.org/abs/2506.23550).
- **Wu, Rossi, Vicentini, Carleo (2023).** Exact MPS → tensorial RNN embedding, which allows an RNN-NQS to start exactly at a DMRG MPS — [PRR 5, L032001](https://arxiv.org/abs/2206.12363).
- **Data-pretrained NQS (Lange et al. 2025).** A patched transformer NQS is pretrained on numerical or Rydberg-experiment snapshots and then optimized on the Hamiltonian. Pretraining gives access to the sign structure, "speeding convergence." Systems: 2D TFIM and dipolar XY on 6×6 and 10×10. A second measurement basis "substantially improves performance." No MPS/DMRG involvement — [Lange, Bornet, Emperauger, Chen, Lahaye, Kienle, Browaeys, Bohrdt, Quantum 9, 1675 (2025), arXiv:2406.00091](https://arxiv.org/abs/2406.00091).
- **Entanglement of autoregressive NQS (Jreissaty et al. 2025/26).** "The standard softmax normalization of the wavefunction suppresses entanglement and fluctuations." A square-modulus normalization restores them, and the authors link this to initialization strategies for VMC ground-state searches (no MPS comparison in the abstract) — [Jreissaty, Zhang, Quijano, Carrasquilla, Wiersema, arXiv:2509.12365, DOI 10.1103/t2cg-kr7y (PRR)](https://arxiv.org/abs/2509.12365).
- **Supervised NQS training.** One paper trains NQS on reference data for the next-nearest-neighbor Ising model — ["Supervised training of neural-network quantum states for the next-nearest neighbor Ising model," Comput. Phys. Commun. (2024), arXiv:2305.03394](https://arxiv.org/html/2305.03394) (not fetched; title and venue from search metadata).

### Inferences
- The literature consistently treats DMRG/MPS as the *cheap, reliable* first stage and NQS as the *expensive refinement*. The proposal reverses this, so it must show that NN inference plus conversion costs less than the DMRG warm-up it replaces, or that it avoids local minima DMRG falls into (e.g., wrong stripe pattern or wrong symmetry sector on 2D cylinders).
- ANTN's ablation (structure > initialization) suggests that initialization gains may be modest when the optimizer is strong. DMRG's local eigen-solver plus subspace expansion is a strong optimizer, so any claimed gain needs careful, budget-matched baselines.

### Gaps
- No quantitative numbers retrieved for Kan et al. 2024 (MDPI page blocked) or Wu–Zhang–Fang–Li 2025 (abstract only).
- I did not find a paper explicitly titled "MPS-pretrained NQS" that measures VMC iterations saved versus random initialization. Kaneko & Goto lack a random baseline.
- No "transformer + MPS" paper with a DMRG-initialized MPS component was verified beyond ANTN. A JCTC 2025 title, "Bridging the Gap between Transformer-Based Neural Networks and Tensor Networks for Quantum Chemistry" ([ACS](https://pubs.acs.org/doi/10.1021/acs.jctc.4c01703)), appeared in search but could not be read. Likewise "Symmetry-Blocked Matrix Product States as a Neural-Network Quantum-State Ansatz for Quantum Chemistry," JCTC 22(16), 8350 (2026) ([ACS](https://pubs.acs.org/jctcce/article-abstract/22/16/8350/5253629/Symmetry-Blocked-Matrix-Product-States-as-a-Neural?redirectedFrom=fulltext)) appeared only as a title. Both are likely relevant hybrids and need checking.

---

## Q3. Learned warm starts across a family of Hamiltonians: supervised H → ground-state learning, Hamiltonian-conditioned generative models, foundation NQS, hypernetworks/GNNs that output MPS. Were any fed into DMRG?

### Takeaway
Hamiltonian-conditioned and amortized models now exist: TQS 2023, foundation NQS 2025, HyperRBM 2026, conditional generative models 2022–24, GNN ansätze 2021, and provable property predictors 2022/2024. MPS-based reduced-basis surrogates span parameter domains (2023). **None of these was used to produce an initial MPS for DMRG, and I found no network that outputs MPS tensors directly from a Hamiltonian description.** The "amortized DMRG" idea is unexplored in the literature I could access.

### Cited Findings
- **Provable property prediction (Huang, Kueng, Torlai, Albert, Preskill 2022).** Classical ML on classical-shadow data efficiently predicts ground-state *properties* (not the state) of gapped Hamiltonians in the same phase. Experiments cover Rydberg atoms, 2D random Heisenberg, and SPT/topological phases — ["Provably efficient machine learning for quantum many-body problems," *Science* (2022), DOI 10.1126/science.abk3333, arXiv:2106.12627](https://arxiv.org/abs/2106.12627).
- **Improved algorithm (Lewis, Huang, Tran, Lehner, Kueng, Preskill 2024).** O(log n) training data for an n-qubit gapped local Hamiltonian, versus O(n^c) previously; O(n log n) training and prediction time; numerics up to 45 qubits — ["Improved machine learning algorithm for predicting ground state properties," *Nat. Commun.* (2024), DOI 10.1038/s41467-024-45014-7, arXiv:2301.13169](https://arxiv.org/abs/2301.13169).
- **Conditional generative models (Wang, Weber, Izaac, Lin; v3 2024).** A conditional generative model represents a family of ground states and predicts arbitrary local properties for unseen states. Tested on 2D random Heisenberg up to 45 qubits and on 13×13 Rydberg arrays (hardware) — [arXiv:2211.16943](https://arxiv.org/abs/2211.16943); [code](https://github.com/PennyLaneAI/generative-quantum-states).
- **Transformer Quantum State (Zhang & Di Ventra 2023).** One model "can generate the entire phase diagram," transfers "to new systems it has never been trained on," and "fine-tuning the TQS produces accurate results with small computational cost" — [PRB 107, 075147 (2023), arXiv:2208.01758](https://arxiv.org/abs/2208.01758v4).
- **Foundation NQS (Rende, Viteritti, Becca, Scardicchio, Laio, Carleo 2025).** The model takes spin configurations *and Hamiltonian couplings* as input, generalizes to unseen Hamiltonians, and "can be efficiently fine-tuned for specific quantum systems." Uses: disorder averages, fidelity susceptibility; models are on Hugging Face. Note: Goldt is not an author of this paper; he is a co-author of the 2024 fine-tuning paper below — [arXiv:2502.09488; *Nat. Commun.* (2025), DOI 10.1038/s41467-025-62098-x](https://arxiv.org/abs/2502.09488).
- **Fine-tuning NQS (Rende, Goldt, Becca, Viteritti 2024).** Pretrain once near a phase transition, then fine-tune only the output layer at other points. "The computational cost of the fine-tuning step is very low compared to the pretraining stage" (no numbers in the abstract) — [PRR 6, 043280 (2024), arXiv:2403.07795](https://arxiv.org/abs/2403.07795).
- **HyperRBM (Tonner, Tran, Kueng 2026).** A hypernetwork conditions an RBM on Hamiltonian control parameters, so one model covers a family of TFIM ground states (1D and 2D). It reproduces fidelity susceptibility and locates the transition. This is tomography from Pauli data, not energy minimization, and has no DMRG link — [arXiv:2601.20950](https://arxiv.org/abs/2601.20950).
- **GNN ansatz (Kochkov, Pfaff, Sanchez-Gonzalez, Battaglia, Clark 2021).** A GNN variational manifold for "a diverse set of Heisenberg Hamiltonians," which "generalize[s] to problems of larger size"; no MPS/DMRG link — [arXiv:2110.06390](https://arxiv.org/abs/2110.06390).
- **Reduced-basis surrogates from MPS snapshots (Brehmer, Herbst, Wessel, Rizzi, Stamm 2023).** A greedy algorithm picks parameter points. DMRG/MPS ground states at those points form a reduced basis, after which observables anywhere in the parameter domain cost nothing that scales with Hilbert-space size. Tested on 1D spin-1 models with anisotropy and biquadratic exchange. This is non-neural amortization across a Hamiltonian family, and the abstract does not mention warm-starting DMRG — [PRE 108, 025306 (2023), arXiv:2304.13587](https://arxiv.org/abs/2304.13587). Precursor: Herbst et al., "Surrogate models for quantum spin systems based on reduced order modeling" — [arXiv:2110.15665](https://arxiv.org/abs/2110.15665v2) (not fetched).
- **Meta-learning.** I did not locate a paper titled "Meta-learning NQS." Meta-learning hits were all for VQE/QAOA initializers (see Q5).

### Inferences
- All the ingredients for "amortized DMRG initialization" exist separately:
  - Hamiltonian-conditioned NQS (FNQS, TQS, HyperRBM) that produce a state for an unseen H;
  - NQS → MPS compression tools (TCI, sampling-based fitting);
  - evidence that fine-tuning from a pretrained model is much cheaper than training from scratch (Rende 2024; Scherbela 2023/24 in Q5).
  
  Composing them into "Hamiltonian → NN → MPS → DMRG" has not, as far as I can find, been done or benchmarked.
- The reduced-basis method (Brehmer 2023) is the strongest *non-neural* competitor for "warm start across a parameter family." Interpolating or projecting stored MPS snapshots could supply initial MPS at new parameters without any NN, so any NN proposal should benchmark against it.

### Gaps
- No paper found where a GNN or hypernetwork outputs MPS tensors (with gauge/canonical form) directly from a Hamiltonian graph. Queries such as "hypernetwork generates MPS tensors" returned only generic TN tutorials.
- I could not verify whether Huang 2022 or Lewis 2024 generated training data with DMRG. Abstract pages do not say.

---

## Q4. ML for the DMRG workflow itself: orbital/site ordering, bond-dimension/entanglement prediction, sweep schedules, hyperparameter tuning, 2D → 1D path

### Takeaway
ML is used *around* DMRG:
- predicting mutual information for orbital ordering (2023);
- correcting low-χ DMRG energies with a GNN (2025, 2026);
- predicting entanglement entropy (2025);
- an LLM coding agent tuning whole DMRG protocols, including the choice of initial product state, under fixed wall-clock budgets (2026).

State-of-the-art 2D-lattice and site ordering (2025–2026) uses combinatorial optimization, not ML. No work found uses ML to output the initial MPS itself.

### Cited Findings
- **ML correction of DMRG energies (Golub, Yang, Vlček, Veis 2025).**
  - Model: a one-layer message-passing GNN. Each orbital is a node (feature: single-orbital entropy). Edges exist where mutual information > 0.004 (features: MI and DFT occupancy). Pooled output plus the truncation error feeds an MLP that predicts the normalized gap between low-χ and reference energies.
  - Data: trained on 100 PAHs (COMPAS-1D); tested on 5 PAHs with active spaces from (22e,22o) to (44e,44o).
  - Accuracy: for χ = 750–1250, corrected energies are within 1 mHa of reference. The [3]triangulene singlet–triplet gap is correct at M = 750; the peripentacene state ordering is correct at M = 500.
  - The model needs a single low-χ run, whereas extrapolation needs several. No timing or speedup numbers are given, and **the DMRG initial state is not touched.**
  - Source: [Golub et al., J. Phys. Chem. Lett. 16(13), 3295 (2025), arXiv:2412.07607](https://arxiv.org/abs/2412.07607); details from [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973911).
- **Excited-state follow-up (Golub & Veis, Sept 2026).** The same ML + DMRG-as-CAS-solver idea applied to excitation energies of PAHs with up to 34 π-electrons — [arXiv:2609.12616](https://arxiv.org/abs/2609.12616).
- **ML-predicted mutual information for orbital ordering (Golub, Antalík, Beran, Brabec 2023).** An ML model "replaces expensive DMRG" mutual-information calculations, used to determine correlation structure and "orbital ordering for accurate DMRG calculations." Numbers were not retrievable: the OSTI page is robots-blocked and the CAS repository record has the abstract only — [Chem. Phys. Lett. 813, 140297 (2023)](https://asep.lib.cas.cz/arl-cav/en/detail-cav_un_epca-0566845-Mutual-information-prediction-for-strongly-correlated-systems). Training database: [SC1MC-2022, arXiv:2101.06090](https://arxiv.org/abs/2101.06090), with one- and two-site entropies and MI at DMRG level for transition-metal complexes.
- **Earliest "ML accelerates DMRG convergence" claim (Marks, Jiang, Devereaux; APS March Meeting 2019).** They "investigate the application of machine learning methods" to the variational ground-state step and "improve convergence time for various classes of strongly correlated systems." The mechanism is unspecified, and I found no follow-up paper — [APS MAR19 C18.7](https://meetings-archive.aps.org/mar/2019/c18/7).
- **LLM-agent DMRG protocol tuning (Mantilla Calderón, Gonthier, Gustin, Bernales, Aspuru-Guzik 2026).**
  - Setup: a GPT-based coding agent evolves VQE, DMRG and AFQMC protocols. Each DMRG candidate is scored under a "fixed 20 s budget" (Apple M4 Pro, 10 cores) on four L = 64 open chains.
  - Baseline: DMRG1, random initial state, χ schedule 4-6-8, 6 sweeps.
  - Best protocols switched to DMRG2 or staged DMRG1↔DMRG2, **changed the initial state (random → Néel, or plus/minus product state)**, and raised χ and sweep counts. Energies at fixed budget:

    | Chain | Baseline | Best | ΔE |
    |---|---|---|---|
    | XXX | −28.165820 | −28.175425 | ≈ −0.0096 |
    | XXZ | — | — | ≈ −0.0119 |
    | XX | — | — | ≈ −0.0130 |
    | critical TFIM | — | — | ≈ −2×10⁻⁵ |

  - No time-to-solution metric is given, and **no ML-generated initial MPS** is used.
  - Source: ["Optimizing ground state preparation protocols with autoresearch," arXiv:2604.25610 (2026)](https://arxiv.org/abs/2604.25610); numbers from [HTML v2](https://arxiv.org/html/2604.25610v2).
- **GNN entanglement predictor (Saleh 2025).** Predicts von Neumann entropy from measured bitstrings (Rydberg ladder). In-range MAE is 3.6×10⁻³ (MAPE 1.44%), and it beats MI-based bounds. This could in principle inform χ choice, but the paper does not do so — [arXiv:2503.23635](https://arxiv.org/abs/2503.23635).
- **Site-order optimization (non-ML; Watanabe, Hikihara, Ueda 2025).** Multi-site local rearrangement of the MPS site order. Going from 2-site to 3-site rearrangement "reduces the average relative error in the ground-state energy by 65% to 94%" for randomly permuted Heisenberg chains — [arXiv:2512.22021](https://arxiv.org/abs/2512.22021).
- **2D/3D lattice → 1D path (non-ML; Rausch, Sept 2026).** "Lattice compilation" with cutwidth (which sets peak MPO bond dimension) and average range (which sets average bond dimension) as proxies. Reverse Cuthill–McKee is "unreliable," and QUBO gives only marginal gains. Staged SAT / CP-SAT (OR-Tools) gives the best orderings with rigorous bounds. No numbers in the abstract — [arXiv:2609.25384](https://arxiv.org/abs/2609.25384).
- **Non-neural prior art for orderings.** Fiedler-vector / mutual-information ordering heuristics are covered in [Szalay et al., "Tensor product methods and entanglement optimization for ab initio quantum chemistry," IJQC (2015)](https://onlinelibrary.wiley.com/doi/full/10.1002/qua.24898) and ["On the Ordering of Sites in the Density Matrix Renormalization Group using Quantum Mutual Information," arXiv:2103.01111](https://arxiv.org/abs/2103.01111). Neither page was fetched this session; titles come from search metadata and authors were not verified.
- **Bayesian optimization of DMRG hyperparameters.** Not found. A targeted search returned only library docs on χ schedules and energy extrapolation, e.g. [block2 energy extrapolation docs](https://block2.readthedocs.io/en/latest/tutorial/energy-extrapolation.html).

### Inferences
- The only paper that optimizes DMRG time-to-quality with an AI system (Mantilla Calderón 2026) picks the initial state from a tiny discrete menu. This is evidence that initial state matters at fixed compute budgets, and a natural baseline/upper envelope for a learned continuous initial MPS.
- Golub-style GNN features (orbital entropies, MI graphs) are a natural input representation for a chemistry-oriented initial-state generator. The same graph could output orbital ordering, an initial occupation pattern (a CI-DEAS-like guess), and low-χ MPS tensors.

### Gaps
- No quantitative results retrieved for Golub 2023 (CPL) on how ML-predicted orderings affect DMRG energy or convergence.
- No paper found on ML-predicted sweep schedules, ML-chosen χ schedules (other than the LLM agent), RL for orbital ordering, or GNN-learned 2D paths for DMRG.
- The 2019 Marks/Jiang/Devereaux work is unverifiable beyond the abstract.

---

## Q5. Analogous initialization problems in other variational solvers (VQE/PQC, NQS-VMC, quantum-chemistry VMC, SCF) that a DMRG version could borrow from

### Takeaway
Learned or transferred initialization is mature for parametrized quantum circuits:
- meta-learned RNN initializers (2019);
- size-flexible FLIP (2021);
- identity-block initialization (2019);
- Bayesian "fast-and-slow" (2022);
- MPS/TN pretraining of circuits (2022–2023);
- LSTM / quantum-sequence meta-initializers (2025–2026).

The same holds for NQS (transfer across sizes, 2020; fine-tuning, 2024) and deep-learning VMC for molecules (pretrained transferable wavefunctions, 2023–2024). An SCF analog (NN-predicted density matrix as initial guess, 2024) is the cleanest template: "learned initial guess → fewer self-consistent iterations." DMRG lacks this.

### Cited Findings
- **Meta-learned PQC initialization (Verdon et al. 2019).** "Learning to learn with quantum neural networks via classical neural networks": a classical RNN learns to initialize and optimize QAOA/VQE parameters across problem families — [arXiv:1907.05415](https://ar5iv.labs.arxiv.org/html/1907.05415) (abstract not fetched; description from prior knowledge).
- **FLIP (Sauvage, Sim, Kunitsa, Simon, Mauri, Perdomo-Ortiz 2021).** A meta-learned initializer that can "predict initial parameters for circuits with more parameters than those seen in training." Tested on barren-plateau families, max-cut, and 1D Fermi–Hubbard ground-state energies; no numbers in the abstract — [arXiv:2103.08572](https://arxiv.org/abs/2103.08572).
- **Identity-block initialization (Grant, Wossnig, Ostaszewski, Benedetti 2019).** "An initialization strategy for addressing barren plateaus in parametrized quantum circuits," *Quantum* 3, 214 (2019) — [arXiv:1903.05076](https://arxiv.org/abs/1903.05076) (metadata not fetched this session).
- **Bayesian-learning initialization (Rad, Seif, Linke 2022).** Correct title: "Surviving The Barren Plateau in Variational Quantum Circuits with Bayesian Learning Initialization." It is a "fast-and-slow" scheme: Bayesian learning finds a promising region, then a fast local optimizer finishes. It is demonstrated on the Bars-and-Stripes quantum generative model, **not on VQE**, contrary to the brief's phrasing — [arXiv:2203.02464](https://arxiv.org/abs/2203.02464).
- **MPS pretraining of PQCs (Dborin, Barratt, Wimalaweera, Wright, Green 2022).** "Accelerates training of PQCs for both supervised learning, energy minimization, and combinatorial optimization" (no numbers in the abstract) — [arXiv:2106.05742](https://arxiv.org/abs/2106.05742); [Quantum Sci. Technol. (2022), DOI 10.1088/2058-9565/ac7073](https://iopscience.iop.org/article/10.1088/2058-9565/ac7073).
- **TN-pretrained PQCs (Rudolph, Miller, Motlagh, Chen, Acharya, Perdomo-Ortiz 2023).** A TN simulation finds a promising state, which is decomposed into PQC gate parameters. The result "avoids barren plateaus," and more classical resources give better performance and faster training — [arXiv:2208.13673](https://arxiv.org/abs/2208.13673); published as "Synergistic pretraining of parametrized quantum circuits via tensor networks," [*Nat. Commun.* (2023), DOI 10.1038/s41467-023-43908-6](https://pmc.ncbi.nlm.nih.gov/articles/PMC10724286/).
- **DMRG-guided quantum state preparation (Watanabe, Nishi, Kosugi, Tsuneyuki, Matsushita 2026; non-ML).** DMRG MPS → optimization-free matrix-product disentangler circuit, truncated at the inflection layer L*, then probabilistic imaginary-time evolution. The tail of encoding layers scales empirically as O(N⁵ log(N/ε)) — [arXiv:2605.30141](https://arxiv.org/abs/2605.30141).
- **Recent meta-learned VQA initializers (2025–2026).**
  - QK-LSTM meta-learner for QAOA on Max-Cut (n = 10–13) gives "the fastest convergence rate," with 43 versus 56 parameters for a classical LSTM — [Lin, Hsu, Chen, arXiv:2512.05058 (2025)](https://arxiv.org/abs/2512.05058v1).
  - LSTM-FC-VQE meta-initialization on CUDA-Q for molecular Hamiltonians gives "near FCI accuracy" with "O(N²) scaling" (no error numbers) — [Chen, Chang, Huang, Kuo, arXiv:2602.15706 (2026)](https://arxiv.org/abs/2602.15706).
  - Earlier: ["Accelerating Parameter Initialization in Quantum Chemical Simulations via LSTM-FC-VQE," arXiv:2505.10842](https://arxiv.org/html/2505.10842v1) (not fetched).
- **NQS transfer across system sizes (Zen et al. 2020).** Physics-inspired protocols reuse RBM-NQS trained on small systems for larger ones: 1D TFIM and XXZ up to 128 spins, 2D XXZ up to 8×8. Some protocols are "far more effective and efficient than starting from" random initialization (no factor in the abstract) — [Zen, My, Tan, Hébert, Gattobigio, Miniatura, Poletti, Bressan, PRE 101, 053301 (2020), arXiv:1908.09883](https://arxiv.org/abs/1908.09883).
- **Pretrained transferable molecular neural wavefunctions (Scherbela, Gerard, Grohs 2023).** Deep-learning VMC normally "requires a full optimization for every new problem instance, consuming thousands of GPUhs even for small molecules." A pretrained model gives zero-shot energies that beat CCSD(T)-2Z, and "only few fine-tuning steps" are needed for accurate relative energies. Zero-shot accuracy improves by two orders of magnitude over prior state of the art — ["Variational Monte Carlo on a Budget," arXiv:2307.09337 (NeurIPS 2023)](https://arxiv.org/abs/2307.09337).
  - Companion paper: ["Towards a transferable fermionic neural wavefunction for molecules," *Nat. Commun.* (2024)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10762074/). The PMC page was reCAPTCHA-blocked, so no numbers were retrieved.
- **SCF analog (Hazra, Patil, Sanvito 2024).** A neural network maps atomic positions to the Kohn–Sham density matrix, giving an SCF initial guess "far superior to any other recipes available, in particular for molecules with metallic bonds." It enables MD "with little to no self-consistent steps" — [J. Chem. Theory Comput. (2024), DOI 10.1021/acs.jctc.4c00042, arXiv:2401.06533](https://arxiv.org/abs/2401.06533).

### Inferences
- Design patterns that transfer directly to DMRG:
  - (i) **meta-learned initializer across a problem family** (Verdon, FLIP) → Hamiltonian-conditioned MPS generator;
  - (ii) **size-flexible initializer** (FLIP, Zen) → MPS "growing" or translation-invariant tensor generator that works for any L;
  - (iii) **pretrain then fine-tune** (Rende 2024, Scherbela 2023) → generator output plus a few DMRG sweeps;
  - (iv) **classical TN → quantum-circuit init** (Dborin, Rudolph) shows that "initialization from a cheaper related solver" is publishable when it fixes a real pathology (barren plateaus).
- For DMRG the analogous pathology is local minima or metastability (2D cylinders, quantum chemistry with poor orbital guesses), not vanishing gradients. The value proposition should be framed around probability of reaching the correct minimum, not only sweep counts.
- The SCF analog (Hazra 2024) offers a clean benchmark template: report iterations-to-convergence versus standard guesses (superposition of atomic densities ↔ random/product MPS), plus failure rates.

### Gaps
- Quantitative speedup factors for FLIP, Dborin, Rudolph, Zen and Scherbela 2024 were not retrievable from abstract pages. The full texts contain them.
- FermiNet/PauliNet pretraining on HF/CASSCF orbitals was not re-verified this session. Canonical references: Pfau et al., PRR 2, 033429 (2020), [arXiv:1909.02487](https://arxiv.org/abs/1909.02487); Hermann, Schätzle, Noé, *Nat. Chem.* 12, 891 (2020), [arXiv:1909.08423](https://arxiv.org/abs/1909.08423) (metadata not fetched).

---

## Q6. Has any paper (2017–2026) reported wall-clock or sweep-count reductions for DMRG specifically from an ML-generated initial state?

### Takeaway
**No. I found no primary source reporting DMRG sweep or wall-clock reductions attributable to an ML- or NN-generated initial MPS.** This appears to be a genuine gap. My confidence is moderate: arXiv full-text search was unavailable, and several publisher pages were blocked. The closest works fall into three groups.

### Cited Findings
- **"Done exactly": none found.**
- **Closely related (DMRG + ML aimed at convergence/time, or ML choosing the DMRG start):**
  - Marks, Jiang, Devereaux (APS 2019): ML "improve[s] convergence time" of the DMRG variational step for strongly correlated systems. Mechanism and numbers are unknown, and no paper was found — [APS MAR19 C18.7](https://meetings-archive.aps.org/mar/2019/c18/7).
  - Mantilla Calderón et al. (2026): an LLM agent picks among product initial states (random/Néel/±) plus schedules under a 20 s budget. It yields ΔE ≈ −0.0096 to −0.013 on L = 64 Heisenberg/XXZ/XX chains, and the initial state is a discrete choice, not ML-generated — [arXiv:2604.25610](https://arxiv.org/abs/2604.25610).
  - Golub et al. (2025): GNN correction of low-χ DMRG energies (post-hoc, not initialization); within 1 mHa at χ = 750–1250; no timings — [JPCL 2025](https://arxiv.org/abs/2412.07607).
  - Golub et al. (2023): ML-predicted MI for DMRG orbital ordering, a pre-processing input to DMRG — [CPL 813, 140297](https://asep.lib.cas.cz/arl-cav/en/detail-cav_un_epca-0566845-Mutual-information-prediction-for-strongly-correlated-systems).
- **Reverse direction (DMRG/MPS → NN or circuit init):**
  - ANTN 2023: DMRG initializes the MPS part; the ablation says structure > initialization — [arXiv:2304.01996](https://arxiv.org/html/2304.01996v3).
  - Kaneko & Goto 2025: MPS → RBM via CP decomposition — [arXiv:2506.23550](https://arxiv.org/abs/2506.23550).
  - Kan et al. 2024: TN pretraining of NQS for chemistry — [Mathematics 12, 433](https://doi.org/10.3390/math12030433).
  - Dborin 2022 and Rudolph 2023: MPS/TN → PQC initialization — [arXiv:2106.05742](https://arxiv.org/abs/2106.05742), [arXiv:2208.13673](https://arxiv.org/abs/2208.13673).
- **Only analogous:**
  - Hamiltonian-conditioned NQS (TQS 2023, FNQS 2025, HyperRBM 2026), fine-tuning NQS (2024), NQS size transfer (2020);
  - meta-learned VQE/QAOA initializers (2019–2026);
  - SCF density-matrix initial guess (2024);
  - reduced-basis MPS surrogates (2023).

  Citations are under Q3 and Q5.

### Inferences
- The novelty claim "use an NN to generate the best DMRG starting state for fastest convergence" is defensible as **not previously published as a benchmarked method**. It must be positioned carefully against:
  - (a) strong non-ML warm starts: adiabatic/parameter continuation, i.e., reusing the converged MPS from a neighbouring parameter; reduced-basis surrogates; small-system → large-system MPS growing; CI-DEAS-type guesses in chemistry;
  - (b) the 2026 LLM-agent work, which already shows "pick a better initial state + schedule under a budget."
- A reviewer will ask whether the NN start beats "previous-parameter MPS + 2 sweeps." This is the critical baseline, and it is likely hard to beat in smooth regions of a phase diagram. The NN may win mainly near transitions, in disordered ensembles (no neighbouring solution exists), for new geometries or sizes, and in avoiding metastable minima.

### Gaps
- I could not run an arXiv full-text query for phrases like "initial MPS" + "neural network." Theses, workshop papers (e.g., NeurIPS ML4PS) and non-English venues may contain unindexed attempts.
- The JCTC 2025 "transformer ↔ TN" and JCTC 2026 "symmetry-blocked MPS NQS" papers were seen only as titles and might contain MPS ↔ NN initialization experiments.

---

## Gaps and open questions for NN-generated DMRG initial states

### Takeaway
The open space is large: no benchmarked NN → MPS → DMRG pipeline, no Hamiltonian-to-MPS generator, no cost accounting that includes NN training, and no study of whether initialization changes *which* minimum DMRG reaches. Each question below is unaddressed in the sources found.

### Cited Findings (evidence that frames each gap)
- **Expressivity mismatch.** RBMs can carry volume-law entanglement (long-range) while short-range RBMs are area-law ([Deng 2017](https://arxiv.org/abs/1701.04844)), and RBMs can need fewer parameters than TNS ([Chen 2018](https://arxiv.org/abs/1701.04831)). So compressing NN outputs into MPS can lose information or need large χ. *Open:* what χ, fidelity and energy does a compressed NN start need to reduce total DMRG cost?
- **Initialization vs structure.** In ANTN, gains come "mainly" from MPS inductive bias, not DMRG initialization ([ANTN 2023](https://arxiv.org/html/2304.01996v3)). *Open:* is DMRG's convergence actually sensitive to initial-state quality beyond the first few low-χ sweeps, and for which Hamiltonian classes?
- **Discrete initial-state choice already helps under budgets** ([Mantilla Calderón 2026](https://arxiv.org/html/2604.25610v2)). *Open:* does a continuous, learned, Hamiltonian-specific MPS beat the best product state plus an optimized schedule?
- **Fine-tuning is cheap relative to pretraining** ([Rende 2024](https://arxiv.org/abs/2403.07795); [Scherbela 2023](https://arxiv.org/abs/2307.09337)). *Open:* the amortization break-even — how many DMRG instances must share one trained generator before NN training cost is recovered?
- **Reduced-basis MPS surrogates already amortize over parameter domains** ([Brehmer 2023](https://arxiv.org/abs/2304.13587)). *Open:* NN generator versus RB-projected or interpolated MPS as initial states.
- **ML for orbital ordering exists, but its effect on DMRG convergence is unquantified here** ([Golub 2023](https://asep.lib.cas.cz/arl-cav/en/detail-cav_un_epca-0566845-Mutual-information-prediction-for-strongly-correlated-systems)). *Open:* jointly learning ordering + initial MPS in chemistry.

### Inferences (open questions list)
1. **Sector/minimum selection.** Can an NN start raise the probability that DMRG lands in the true ground state? Examples: correct stripe period in Hubbard cylinders, correct dimerization pattern, correct total-spin or momentum sector, avoiding metastable states in frustrated 2D systems. Nobody has reported "probability of correct minimum" as a metric for learned starts.
2. **Gauge and symmetry handling.** How should an NN output U(1)/SU(2)-symmetric block-sparse MPS tensors with consistent quantum-number labels? Exact embeddings (MPS ⊂ RNN, [Wu 2023](https://arxiv.org/abs/2206.12363)) suggest architectures, but the output side (NN → symmetric MPS) is unexplored.
3. **Size extrapolation.** Can a generator trained at L ≤ 32 produce useful starts at L = 128–512 (cf. size transfer for NQS, [Zen 2020](https://arxiv.org/abs/1908.09883); FLIP's size flexibility, [Sauvage 2021](https://arxiv.org/abs/2103.08572))?
4. **Chemistry.** Can a GNN on orbital/MI graphs (features as in [Golub 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973911)) output ordering + initial MPS that beats CI-DEAS/HF-occupation starts in sweeps-to-chemical-accuracy for PAHs, Fe–S clusters, Cr2?
5. **Conversion route choice.** Exact (RBM → MPS), sampled fitting, or TCI ([SciPost 2025](https://scipost.org/SciPostPhys.18.3.104)): which gives the best fidelity per unit cost?
6. **Excited states and time evolution.** Learned starts for excited-state DMRG or for TDVP initial states are untouched; the Golub & Veis 2026 excited-state work corrects energies only ([arXiv:2609.12616](https://arxiv.org/abs/2609.12616)).

### Gaps
- No empirical data exist anywhere (in the sources found) on DMRG sensitivity curves of the form sweeps-to-tolerance versus initial overlap or energy for realistic models. This is basic groundwork the project would need to produce first.

---

## Suggested concrete research directions and benchmark designs

### Takeaway
Run a staged study:
1. Measure DMRG's sensitivity to initial-state quality.
2. Benchmark NN-generated starts against strong non-ML warm starts.
3. Report full cost, including NN training amortized over instances.

Lead with the regimes where warm starts plausibly matter: disorder ensembles, near-critical points, 2D cylinders with competing orders, and quantum chemistry with poor orderings.

### Cited Findings (anchors for design choices)
- Hamiltonians with established DMRG/NQS benchmarks:
  - TFIM, XXZ, XX and Heisenberg chains (used by [Mantilla Calderón 2026](https://arxiv.org/html/2604.25610v2) at L = 64 with a 20 s budget);
  - 2D J1–J2 on 10×10 and 12×12 ([ANTN 2023](https://arxiv.org/html/2304.01996v3));
  - spin-1 bilinear-biquadratic / anisotropic chains ([Brehmer 2023](https://arxiv.org/abs/2304.13587));
  - 2D random Heisenberg ([Huang 2022](https://arxiv.org/abs/2106.12627); [Wang 2022](https://arxiv.org/abs/2211.16943));
  - PAH active spaces up to (44e,44o) ([Golub 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973911));
  - H50, Fe2S2, H18 ([Wu–Zhang–Fang–Li 2025](https://arxiv.org/abs/2507.19276)).
- Pretrained Hamiltonian-conditioned NQS available publicly: FNQS models on Hugging Face/NetKet ([Rende et al. 2025](https://arxiv.org/abs/2502.09488)).
- MPS → NN and NN ↔ MPS tools: CP-decomposition seeding ([Kaneko & Goto 2025](https://arxiv.org/abs/2506.23550)); TCI libraries ([Fernández et al. 2025](https://scipost.org/SciPostPhys.18.3.104)).

### Inferences (proposed designs)

**Direction A — sensitivity study (prerequisite; no NN needed).**
- Prepare initial MPS with controlled overlap or energy error. Generate them by mixing the converged ground state with noise, or by truncating it to χ₀ ∈ {1, 2, 4, 8, 16}.
- Measure DMRG sweeps-to-tolerance and wall-clock.
- This gives the "maximum possible gain" curve for any learned initializer, and tells you which Hamiltonians are worth targeting.

**Direction B — NQS → MPS → DMRG.**
- Take FNQS/TQS-style Hamiltonian-conditioned NQS. Compress to MPS at χ₀ by (i) exact RBM → MPS where applicable, (ii) TCI on the amplitude oracle, or (iii) variational fitting from samples.
- Start DMRG from the result. Report conversion cost separately.

**Direction C — direct Hamiltonian → MPS generator ("amortized DMRG").**
- Architecture: a GNN or transformer over the Hamiltonian's interaction graph that outputs site tensors in left-canonical form, with symmetry blocks.
- Training options: (a) supervised fidelity/overlap to DMRG ground states across a parameter or disorder family; (b) energy minimization with exact MPS contraction (no Monte Carlo needed, since the output is an MPS); (c) hybrid.
- Generalization tests: unseen couplings, larger L, new geometries.

**Direction D — chemistry.**
- A GNN on orbital graphs (entropy/MI features, as in Golub) jointly outputs orbital ordering, occupation pattern, and low-χ initial MPS.
- Baselines: Fiedler/MI ordering + CI-DEAS/HF-occupation start; block2 defaults.

**Baselines (must include):**
1. Random MPS (χ₀ small) with the standard ramped χ schedule and noise or subspace expansion.
2. Best product state (Néel / ferro / ± / stripe) — the agent-found winners in [Mantilla Calderón 2026](https://arxiv.org/html/2604.25610v2).
3. Parameter continuation: the converged MPS from the nearest trained parameter point plus re-optimization (likely the strongest).
4. Reduced-basis surrogate MPS projected or interpolated at the new parameter ([Brehmer 2023](https://arxiv.org/abs/2304.13587)).
5. Smaller-system MPS grown or inserted to the target L (iDMRG-style), and low-χ DMRG pre-run ("χ = 16 for 2 sweeps").
6. For chemistry: CI-DEAS / HF-occupation starts with Fiedler or MI-based ordering.

**Metrics:**
- Sweeps-to-tolerance (ΔE between sweeps < 10⁻⁸ and/or energy variance < threshold, at fixed final χ).
- Wall-clock to target energy error. Report three variants: (i) excluding NN cost, (ii) including NN inference + MPS conversion, (iii) including amortized training cost, giving a break-even instance count N*.
- Initial-state quality: energy error, overlap/fidelity with the reference ground state, and entanglement profile versus the reference.
- **Probability of landing in the correct sector/minimum** over many seeds and instances. Criteria: symmetry quantum numbers, order-parameter pattern (e.g., stripe period), and final energy within δ of the best-known value.
- Anytime curves: energy error versus cumulative wall-clock, comparable to a fixed-budget protocol such as the 20 s budget used by [Mantilla Calderón 2026](https://arxiv.org/html/2604.25610v2).
- Out-of-distribution generalization: unseen parameters, larger L, different geometry or disorder realization.
- Report medians and tails (90th percentile), since warm-start benefits are likely concentrated in hard instances.

**Suggested Hamiltonian suite (ordered by expected payoff):**
1. Disordered chains (random-bond Heisenberg/XXZ, random-field TFIM): no neighbouring solution exists, so amortization over the disorder distribution is the natural NN use case.
2. Near-critical 1D points (TFIM h ≈ 1, XXZ Δ ≈ 1, J1–J2 chain near the Majumdar–Ghosh / dimerization transition).
3. 2D J1–J2 Heisenberg and t-J/Hubbard on 4–6-leg cylinders (metastable stripe or VBS states; test correct-minimum probability).
4. Spin-1 bilinear–biquadratic chain (rich phase diagram; matches the RB-surrogate baseline).
5. Quantum chemistry: PAH active spaces (Golub's dataset), N2/Cr2 dissociation curves, Fe–S clusters (orbital ordering + initial MPS).

**Expected failure modes to check:**
- NN starts biased toward training-distribution minima (wrong phase at OOD parameters).
- Low-χ compressed starts that sit in the wrong symmetry sector.
- Overhead dominating for easy gapped 1D instances, where random-start DMRG converges in a few sweeps anyway.

### Gaps
- Concrete numbers for how many sweeps standard DMRG needs from random starts on these benchmarks are not in the sources above. Direction A must generate them. They may also be covered in other researchers' notes on non-ML DMRG initialization.
