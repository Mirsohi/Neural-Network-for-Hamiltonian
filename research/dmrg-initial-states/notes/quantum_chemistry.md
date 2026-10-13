# Starting state in quantum-chemistry (ab initio) DMRG: initial MPS, orbital basis, orbital ordering, active space — effects on convergence, bond dimension, and wrong-state risk

Scope note: "starting state" here means all of the inputs DMRG is given before sweeping begins: (i) the initial MPS / warm-up ("environment guess"), (ii) the one-particle orbital basis (canonical / localized / natural / DMRG-SCF optimized), (iii) the 1D ordering of orbitals on the MPS chain, (iv) the active space, plus the symmetry sector (S, S_z, irrep) and state-targeting (ground state / state-averaged / excited). Each claim lists the year. "Time" = sweeps/cost to converge; "Result" = the converged energy/state at a given bond dimension M (also written m or D).

Reliability note: Many numbers below come from fetched paper text, but a few full texts (Olivares-Amaya 2015 JCP; Moritz–Hess–Reiher 2005 JCP; Lee 2023 Nat. Commun. final version; Sharma 2014 SI) could not be read in full during this session. Where only the abstract or a secondary description was available, that is stated.

Correction to the assignment brief: Li, Guo, Sun & Chan, "Electronic landscape of the P-cluster of nitrogenase as revealed through many-electron quantum wavefunctions", appeared in **Nature Chemistry** (Nov 2019), not Science — [x-mol record (Nat. Chem.)](https://www.x-mol.com/paper/5875666); [Caltech record, published Nov 2019](https://authors.library.caltech.edu/91401/); [arXiv:1810.10196](https://arxiv.org/abs/1810.10196).

---

## 1. Initial-guess (warm-up) methods for the MPS, which codes use which, and measured effects

### Takeaway
Initial-guess quality mainly changes **how many sweeps** you need, especially the first one or two. For example, CI-DEAS recovers 90–99% of the correlation energy in the first half-sweep (2003). Its effect on the **final converged energy** at fixed M is usually small, but it is not zero: F2 at m = 1024 still differed by about 0.15 mEh between HF and CI-DEAS starts after 20 sweeps (2014). For strongly correlated multi-metal systems, the initial guess decides **which basin** (spin coupling or broken-symmetry pattern) DMRG ends up in, so there it becomes a question of the result and not just the running time (2019, 2026).

### Cited Findings
**Foundational warm-up / environment-guess methods**
- (2003) Legeza & Sólyom introduced the dynamically extended active space (DEAS) warm-up procedure (later called CI-DEAS). It builds an "active-space vector" of the most important orbitals, ranked by single-site entropies from a quick preliminary calculation. At each growth step of the first half-sweep, the environment block is filled with active-space orbitals first and HF-occupied orbitals afterwards, keeping only configurations whose quantum numbers are compatible. If the environment has fewer than M_min states, all of them are kept. Because many sites start empty, the effective chain is short during the first half-sweep. — [Legeza & Sólyom, "Optimizing the density-matrix renormalization group method using quantum information entropy", Phys. Rev. B 68, 195116 (2003), arXiv:cond-mat/0305336](https://arxiv.org/abs/cond-mat/0305336) (journal reference as cited by [Golub et al. 2025](https://arxiv.org/abs/2412.07607))
- (2003) Measured DEAS effects: **90–99% of the correlation energy within the first half-sweep** for CH2, H2O, N2 and F2. CH2 (6e/13o) reached the accuracy of a Cuthill–McKee-ordered run in **13 iteration steps**, and F2 (18/18) reached the accuracy of the optimized-ordering run in **23 iteration steps**. With M_min = 4, F2 reached 5-digit accuracy using M = 120 block states (superblock dimension 220, against an FCI space of 9.08×10^9). For Hubbard chains up to 30 sites, a truncation error of about 1e-5 was reached in 1.5–2 sweeps. Most comparisons with other warm-ups were qualitative. — [Legeza & Sólyom 2003](https://arxiv.org/abs/cond-mat/0305336)
- (2014) Head-to-head HF vs CI-DEAS start for F2, CAS(14,32), m = 1024, CASSCF(14,8) natural orbitals, bond length 141 pm:
  - After sweep 1: HF start −198.886421 Eh; CI-DEAS start −198.962112 Eh (a gap of about 76 mEh).
  - After sweep 20: −198.970559 Eh vs −198.970711 Eh (a gap of about 0.15 mEh).
  - The authors state that "the converged energies still depend on the initial guess" at m = 1024.
  - HF guesses work well with energy-based orderings, while CI-DEAS works best with orderings that place strongly interacting orbital pairs together.
  - Adding white noise to the reduced density matrix (RDM) during warm-up avoids losing important basis states.
  — [Keller & Reiher, "Determining factors for the accuracy of DMRG in chemistry", CHIMIA 2014, arXiv:1401.5497](https://arxiv.org/abs/1401.5497)
- (2006, as summarized 2014) Better environment-state approximations should speed up convergence (Moritz & Reiher, JCP 124, 034103 (2006)). The first sweep needs a guess for the environment, and the two standard options are CI-DEAS or noise/perturbation added to the RDM. — [Reiher, "Three lectures on DMRG in quantum chemistry" (2014 slides)](https://ethz.ch/content/dam/ethz/special-interest/chab/imps/reiher-dam/documents/Diverse/reiher_mariapfarr2014.pdf)
- (2014 review) Catalogue of starting strategies and their reported effects:
  - Random/noise start: distribute D equally over the symmetry sectors and fill the MPS with noise. This reaches energies below HF within the first macro-iteration and is the approach used in CheMPS2 (ref. [121] of the review).
  - Decomposing a cheap CISD wavefunction into an MPS.
  - Starting at small D and enlarging stepwise.
  - Starting from a small active space and adding the frozen orbitals stepwise.
  - The review cites an estimate that "the effect of the starting guess is an order of magnitude smaller than the effect of orbital choice and ordering" (its ref. [80]).
  - The starting guess can still lead to a different converged energy by trapping DMRG in a local minimum (its refs. [69, 73, 80]).
  - DMRG "can get stuck in a local minimum or a limit cycle if D is insufficiently large".
  — [Wouters & Van Neck, "The density matrix renormalization group for ab initio quantum chemistry", Eur. Phys. J. D (2014), arXiv:1407.2040](https://arxiv.org/abs/1407.2040)
- (2014 review) Noise and related fixes: noise can be added to the RDM before diagonalization, or to the two-site tensor before the SVD, to reintroduce lost symmetry sectors. Alternatives are reserving a fraction of D for all sectors, or White's perturbative RDM correction. Two-site DMRG is "less likely to get stuck" than one-site DMRG. — [Wouters & Van Neck 2014](https://arxiv.org/abs/1407.2040). Keller & Reiher (2014) likewise say one-site DMRG "gets trapped in local energy minima for even the simplest systems" and that two-site DMRG is much more robust. — [Keller & Reiher 2014](https://arxiv.org/abs/1401.5497)
- (2007) MPS↔CI conversion: Moritz & Reiher, "Decomposition of DMRG states into a Slater determinant basis", JCP 126, 244109 (2007), was used to reconstruct CI coefficients (ozone example). Boguslawski, Marti & Reiher, JCP 134, 224101 (2011), "SR-CAS", built CASCI-type wavefunctions from DMRG. These underlie "MPS from CI expansion" style conversions in both directions. — cited in [Reiher 2014 slides](https://ethz.ch/content/dam/ethz/special-interest/chab/imps/reiher-dam/documents/Diverse/reiher_mariapfarr2014.pdf)

**Which codes use which initial guess (as documented)**
- **block2** (Chan group; Zhai et al., 2023). Initial-MPS options:
  - (a) a random MPS at the target bond dimension;
  - (b) site occupancies from a cheaper method (e.g., CCSD), used to set the initial quantum-number distribution under an independent-site assumption;
  - (c) fitting from a more approximate MPS (e.g., one optimized in the singles-and-doubles space);
  - (d) building the MPS from a linear combination of determinants or CSFs.
  
  Perturbative noise is used "to escape poor initial guesses". — [Zhai et al., "Block2: a comprehensive open source framework…", arXiv:2310.03920 (Nov 2023)](https://arxiv.org/abs/2310.03920)
- **ORCA (BLOCK backend), 2025 manual (ORCA 6.1)**:
  - `hf_occ` sets the initial occupation pattern: 1 = from one-electron integrals (the default), 2 = canonical-orbital energy ordering, 0 = user-defined.
  - `warmup` selects a Wilson-type warm-up (types 1–4). The default, type 3, uses the full configuration space of n neighbouring sites as the environment and HF occupations for the remaining sites.
  - `startM` = 25 (CASSCF) or 250 (CASCI).
  - Default CASCI schedule: M = 250 for 8 sweeps, then 1000 for 8 sweeps, then +1000 every 4 sweeps, with a two-dot→one-dot switch 2 sweeps after reaching maxM.
  - Advice for local minima: "increase startM (e.g., 500 to 1000) or raise the noise (×10)".
  - Locking quantum numbers too early in DMRG-SCF can trap the orbitals in a local minimum.
  — [ORCA 6.1 manual, DMRG section](https://www.faccts.de/docs/orca/6.1/manual/contents/modelchemistries/dmrg.html)
- **Budapest DMRG (Legeza) / Veis group**: CI-DEAS is the production warm-up. A 2025 ML-DMRG study states "all DMRG calculations start from the CI-DEAS procedure", combined with Fiedler ordering and split-localized orbitals. — [Golub, Yang, Vlček, Veis, J. Phys. Chem. Lett. 2025, DOI 10.1021/acs.jpclett.5c00207; arXiv:2412.07607](https://arxiv.org/abs/2412.07607)
- **CheMPS2** (Wouters): noise-filled MPS with D spread equally over symmetry sectors (as described in the review co-authored by the code's author). — [Wouters & Van Neck 2014](https://arxiv.org/abs/1407.2040)
- **QCMaquis** (Reiher group): Reiher-group material lists CI-DEAS or RDM noise as the warm-up choices. — [Reiher 2014 slides](https://ethz.ch/content/dam/ethz/special-interest/chab/imps/reiher-dam/documents/Diverse/reiher_mariapfarr2014.pdf). The exact current QCMaquis option names were not verified in this session (see Gaps).

**Physically motivated, problem-specific guesses (strong correlation)**
- (2019) P-cluster of nitrogenase: initial guesses were **broken-symmetry product states (D = 1 MPS)** built by distributing local Fe spin states over the 8 Fe centres. These were spin-projected and then grown to larger D. The numbers of basins explored were 20 (synthetic model, S = 0), 35 (P^N, S = 0), 70 (P^1+, S = 1/2 and 5/2) and 152 (P^OX, S = 3 and 4). The authors state: "the non-linear optimization of the wavefunction in the DMRG algorithm is easily trapped in local minima". — [Li, Guo, Sun, Chan, Nat. Chem. 2019, arXiv:1810.10196](https://arxiv.org/abs/1810.10196)
- (2026) FeMoco model (LLDUC, 113e/76o), the most extensive enumeration of starting states found:
  - Under collinear-spin, S_z = 3/2 assumptions there are 35 spin isomers in 10 broken-symmetry families, and 78,750 electronic configurations.
  - 78,750 UHF initial guesses were sampled, keeping 24 low-energy broken-symmetry (BS) solutions per isomer (840 references).
  - The references were ranked by UCCSD, the top 12–24 per isomer were passed to UCCSDT, and finally UCCSDTQ and UDMRG were run.
  - The best filtered BS determinant has an **overlap of 0.4468** with the D = 18,000 UDMRG state.
  
  — [Zhai, Li, Zhang, Li, Lee, Chan, "Classical computational simulation of the FeMo-cofactor model to chemical accuracy and its implications", arXiv:2601.04621 (Jan 2026)](https://arxiv.org/abs/2601.04621)

### Inferences
- Across sources, CI-DEAS and entropy-informed warm-ups mostly save the first one or two sweeps, roughly tens of mEh in the first sweep for small molecules. With adequate M, noise and two-site sweeps, the converged answer is nearly guess-independent (sub-mEh for F2). The guess therefore matters most when (a) M is small relative to the entanglement, (b) the spectrum has many near-degenerate basins (multi-metal clusters), or (c) one-site DMRG without noise is used.
- In the hardest systems, practitioners stopped relying on generic guesses. They instead enumerate many physically motivated product states (BS determinants or spin-coupling patterns) and run DMRG from each. That is an expensive search over initial states that a learned model could plausibly prune.

### Gaps
- No systematic, multi-molecule benchmark was found comparing CI-DEAS vs random+noise vs HF vs CCSD-occupancy vs SCI-derived MPS in sweeps-to-convergence or wall-time. Most numbers are single-molecule (F2, CH2) or qualitative.
- No published measured speedups for CCSD-based or SCI-based MPS initializations in block2 were found. The options are documented but not benchmarked in the text read.
- Current QCMaquis initial-state options (e.g., "default/const/hf/ci-deas"-style keywords) were not verified from primary documentation in this session.

---

## 2. Orbital ordering: Fiedler, genetic algorithms, mutual information, newer and ML-based methods — quantitative effects

### Takeaway
Ordering changes the entanglement each MPS bond must carry. It therefore controls the **accuracy at fixed M** (the result at finite M) and the **risk of local minima**, especially at small M without noise. The standard practice since about 2011–2015 is Fiedler-vector ordering of an exchange-integral or mutual-information "graph Laplacian", optionally refined by a genetic algorithm (GA) (2011, 2015, 2023, 2025). A 2021 theory paper justifies mutual-information-based ordering through strong subadditivity. In quantum chemistry, ML/RL ordering is in its infancy: one ML model predicts mutual information to drive ordering (2023), and the newest ordering work (2025) is tested only on spin chains.

### Cited Findings
- (2002–2006, via 2014 review) Early ordering metrics:
  - Chan & Head-Gordon: minimize the bandwidth of the one-electron integral matrix t_ij.
  - Fock-matrix bandwidth.
  - An MP2-like G_ij = v_ii;jj² / |ε_i − ε_j|.
  - Legeza & Sólyom: high single-orbital-entropy orbitals placed in the chain centre.
  - Rissler, Noack & White (2006): minimize Σ I_kl |k − l|^η using the two-orbital mutual information I_kl.
  - A genetic algorithm (Moritz, Hess, Reiher, JCP 122, 024107 (2005)) was used to find near-optimal orderings, but "was expensive, limiting it to small test systems". It favoured exchange-matrix (K_ij) bandwidth minimization without definite conclusions.
  - For small molecules, grouping orbitals by irrep with bonding and antibonding blocks adjacent (N2/cc-pVDZ, D2h ordering [Ag B1u B3u B2g B2u B3g B1g Au]) gives faster convergence.
  — [Wouters & Van Neck 2014](https://arxiv.org/abs/1407.2040)
- (2003) In the DEAS paper, placing high-entropy orbitals at one end of the chain led to "vanishing mutual entropy and failed convergence". Placing them at the ends, or relying on Cuthill–McKee alone, was often slow or failed. Placing them in the centre worked best, though "not necessarily optimal". — [Legeza & Sólyom 2003](https://arxiv.org/abs/cond-mat/0305336)
- (2005, as summarized 2014) Because DMRG is linear, orbital ordering matters and convergence to local minima is possible. For small m, ordering is "crucial to avoid convergence to local energy minima" when no noise or perturbative correction is used (Moritz, Hess, Reiher, JCP 122, 024107 (2005)). — [Reiher 2014 slides](https://ethz.ch/content/dam/ethz/special-interest/chab/imps/reiher-dam/documents/Diverse/reiher_mariapfarr2014.pdf). Keller & Reiher (2014) note there is "no obvious or simple relation" between ordering and convergence. — [Keller & Reiher 2014](https://arxiv.org/abs/1401.5497)
- (2011) Fiedler-vector ordering (the second eigenvector of the graph Laplacian of the mutual-information or exchange matrix) was introduced for QC-DMRG by Barcza, Legeza, Marti & Reiher, Phys. Rev. A 83, 012508 (2011). — [arXiv:1008.4607](https://arxiv.org/abs/1008.4607); journal reference as cited in [Golub et al. 2025](https://arxiv.org/abs/2412.07607)
- (2015) Olivares-Amaya, Hu, Nakatani, Sharma, Yang & Chan, "The ab-initio density matrix renormalization group in practice", J. Chem. Phys. 142, 034102. This is a user-oriented benchmark covering π-systems, main-group and transition-metal dimers, Mn-oxo-salen and Fe-porphine, addressing what problems suit DMRG, achievable size and accuracy, and how to judge difficulty. Later work cites it for exchange-integral-based ordering and for the statement that DMRG works best in a local basis. — [HKU record / abstract, DOI 10.1063/1.4905329](https://hub.hku.hk/handle/10722/231094); usage as cited by [Golub et al. 2025](https://arxiv.org/abs/2412.07607). Its specific numerical comparisons of orderings could not be retrieved (paywalled; see Gaps).
- (2023) block2 implements:
  - grouping by irrep;
  - Fiedler ordering of a metric matrix (absolute exchange integrals, or two-orbital mutual information for non-spin-adapted MPS), described as "very inexpensive";
  - a GA refinement of the Fiedler ordering, reimplemented to be "much more efficient" than in StackBlock and parallelized over multi-start populations.
  
  No quantitative comparison is given in the paper. — [Zhai et al. 2023, arXiv:2310.03920](https://arxiv.org/abs/2310.03920)
- (2025) ORCA's defaults are Fiedler ordering, with `GAOPT` (a GA minimizing a weighted exchange matrix) as an option that "usually gives better ordering but can be slow for many orbitals". The recommended action when convergence with maxM is slow is to enable GAOPT. — [ORCA 6.1 manual](https://www.faccts.de/docs/orca/6.1/manual/contents/modelchemistries/dmrg.html)
- (2026) Production state of the art (FeMoco, 76 spatial orbitals, unrestricted DMRG): orbitals are ordered in αβ pairs, with pairs formed by maximizing overlap and **a genetic algorithm setting the pair order**. — [Zhai et al. 2026, arXiv:2601.04621](https://arxiv.org/abs/2601.04621)
- (2021) Theory: Ali et al. connect mutual-information-based ordering heuristics to minimizing MPS entanglement entropy, and hence the truncation error at fixed bond dimension, using strong subadditivity of entropy. They give a rigorous justification and suggest alternative criteria. — ["On the ordering of sites in the DMRG using quantum mutual information", arXiv:2103.01111 (Mar 2021)](https://arxiv.org/abs/2103.01111)
- (2025) Legeza group, global fermionic-mode optimization:
  - Reordering via swap gates using Walecki's construction, so every mode pair becomes adjacent within d/2 macro-iterations.
  - The MPS form is kept, so reordering needs no re-sweeps.
  - Mode transformations U(d) are optimized against a block-entropy-area cost, and "such redefinition of modes can drastically reduce the entanglement of the state".
  - Reordering can transiently raise the cost function, with oscillations near the optimum.
  — [Werner, Menczer, Legeza, "Tensor network state methods and quantum information theory for strongly correlated molecular systems", arXiv:2501.18263 (Jan 2025)](https://arxiv.org/abs/2501.18263)
- (Dec 2025) Newest ordering algorithm found: multi-site rearrangement. A block of N_s adjacent sites is contracted and re-decomposed in every permutation, keeping the order with minimal summed bond entanglement, interleaved with DMRG sweeps; it extends the 2022 two-site swap method of Li et al. On a randomly permuted 1D Heisenberg chain (N = 32, χ_D = 48), the mean relative energy error fell from **0.135 (no optimization) to 0.018 (N_s = 3, χ_opt = 16)**, and going from N_s = 2 to 3 cut the error by 65–94%. It was not tested on molecules, and the authors list quantum chemistry as future work. — [Watanabe, Hikihara, Ueda, arXiv:2512.22021 (Dec 2025)](https://arxiv.org/abs/2512.22021)
- (2024, quantum-computing paper's description) DMRG "requires an orbital ordering along a one-dimensional chain, usually by Hartree-Fock energy". This is a simplified description; production codes default to Fiedler or GA (see above). — [Fomichev et al., arXiv:2310.18410](https://arxiv.org/abs/2310.18410)
- (2023) **ML-predicted mutual information for ordering**: Golub, Antalík, Beran & Brabec trained an ML model to predict two-orbital mutual information, which is harder to predict than one-site entropies, to replace costly preliminary DMRG runs. They tested it on two tasks: identifying correlation structure and **ordering orbitals for accurate DMRG**, benchmarked against mutual information from full DMRG. The abstract gives no numbers. — ["Mutual information prediction for strongly correlated systems", Chem. Phys. Lett. 813, 140297 (2023)](https://asep.lib.cas.cz/arl-cav/en/detail-cav_un_epca-0566845-Mutual-information-prediction-for-strongly-correlated-systems); [OSTI record](https://www.osti.gov/pages/biblio/2424209)
- RL-based orbital ordering for molecular DMRG: searches in this session (2020–2026, "reinforcement learning orbital ordering DMRG", "graph neural network DMRG ordering") returned **no primary publication applying RL to QC-DMRG orbital ordering**. A 2026 preprint on optimized DMRG ordering for complex *lattice* geometries exists but was not read. — [Lattice in Line, arXiv:2609.25384 (2026)](https://arxiv.org/html/2609.25384)

### Inferences
- Ordering mainly affects the **result at finite M**: the energy error, or equivalently the M needed for a target error. It also affects **time** indirectly, through the M needed and the number of sweeps before escaping metastable states. With large M plus noise, the converged energy becomes nearly ordering-independent. In practice, though, M is never "large enough" for Fe-S/FeMoco-scale problems, so ordering remains a first-order cost lever.
- The most common objective, Fiedler on exchange or mutual information, is cheap and good. GA refinement buys further gains at greater cost. Both are heuristics for minimizing bond entanglement, which matches the 2021 theory result. A learned ordering policy would therefore need to beat Fiedler+GA, not just energy ordering.

### Gaps
- Exact numbers from Moritz–Hess–Reiher 2005 (the energy spread across orderings at fixed m) and from Olivares-Amaya 2015 (Fiedler vs GA vs symmetry orderings, M needed per system) could not be retrieved in this session. Both are paywalled and their arXiv text was not found.
- No benchmark directly compares Fiedler, GA, simulated annealing and an ML/RL ordering on the same molecular set in terms of M needed for a fixed error.
- The 2022 two-site on-the-fly swap ordering (Li et al.) was identified only through citation and not read.

---

## 3. Orbital basis choice and active space: canonical vs localized vs split-localized vs natural orbitals vs DMRG-SCF

### Takeaway
Localized orbitals reduce long-range entanglement and therefore the M needed, especially for quasi-1D systems. Split-localized orbitals (occupied and virtual localized separately) are the practical default in Chan-group and ORCA workflows (2015, 2025). Natural orbitals from CASSCF, UCCSD or MP2 are preferred over plain HF canonical orbitals. Spin-unrestricted, split-localized UCCSD natural orbitals are the 2026 FeMoco state of the art. Orbital optimization (DMRG-SCF) changes the **result**, since it is a different variational target, and can itself fall into local minima.

### Cited Findings
- (2014) For the C14H16 π-space (28 orbitals), energies "converge significantly faster" with bond dimension D when ordered localized (Edmiston–Ruedenberg) orbitals are used instead of canonical RHF orbitals. Localization helps most for quasi-1D systems such as hydrogen chains, polyenes and acenes. Biorthogonal bases make the effective Hamiltonian non-Hermitian, so localized orthogonal bases are preferred. — [Wouters & Van Neck 2014](https://arxiv.org/abs/1407.2040)
- (2014) CASSCF natural orbitals "will be better suited" for DMRG than plain HF orbitals. Localized orbitals may allow integral screening and reduce entanglement, lowering the required m (stated qualitatively, without numbers). — [Keller & Reiher 2014](https://arxiv.org/abs/1401.5497)
- (2025) ORCA recommends localized orbitals "unless high molecular symmetry offers compensating benefits", specifically split-localized orbitals. Suggested workflow: run DMRG-SCF at small maxM (default 25), then a single point at large maxM. — [ORCA 6.1 manual](https://www.faccts.de/docs/orca/6.1/manual/contents/modelchemistries/dmrg.html)
- (2025) Production π-system workflow: split-localization (Pipek–Mezey) of B3LYP/cc-pVDZ orbitals, citing Olivares-Amaya 2015 for "DMRG performs best in a local basis", plus Fiedler ordering on the exchange matrix and a CI-DEAS start. — [Golub, Yang, Vlček, Veis 2025](https://arxiv.org/abs/2412.07607)
- (2026) FeMoco: each broken-symmetry reference gets its own **split-localized UCCSD natural orbitals** with Pipek–Mezey localization. The orbitals are chosen per starting reference, not once globally. A 404-orbital extension truncated a 994-orbital space by MP2 natural-orbital occupation. — [Zhai et al. 2026](https://arxiv.org/abs/2601.04621)
- (2023) For quantum-computing ansatz analysis, the Fe–S overlap study used split-localized orbitals, and natural orbitals were also shown for [2Fe-2S]. — [Lee et al. arXiv:2208.02199 (published Nat. Commun. 2023)](https://arxiv.org/abs/2208.02199)
- (2015) Hu & Chan used **canonical HF orbitals without localization** for polyene excited-state geometry optimizations (π active space identified by Löwdin population). This shows canonical orbitals remain usable for modest quasi-1D π spaces at M ≤ 1000. — [Hu & Chan, J. Chem. Theory Comput. 2015, DOI 10.1021/acs.jctc.5b00174; arXiv:1502.07731](https://arxiv.org/abs/1502.07731)
- (2025) Global mode (orbital) optimization in the tensor-network framework can "drastically reduce the entanglement of the state", with spin-independent or spin-dependent rotations. — [Werner, Menczer, Legeza 2025](https://arxiv.org/abs/2501.18263). A related paper accelerates orbital optimization of large active spaces on AI accelerators (GPU tensor cores). — [arXiv:2503.20700; J. Chem. Theory Comput. 21, 6545 (2025)](https://arxiv.org/abs/2503.20700) (title and venue only; content not read)
- (2025) In ORCA DMRG-SCF, `switch_rst` (default 1e-3 orbital gradient) switches to one-dot, locks quantum numbers and restarts without noise. "Locking too early may trap orbitals in a local minimum", and at very small M it adds arbitrariness to the final energy. — [ORCA 6.1 manual](https://www.faccts.de/docs/orca/6.1/manual/contents/modelchemistries/dmrg.html)
- (2014) Active-space size effects: for small active spaces, mutual information and single-orbital entropies are overestimated, i.e., they artificially absorb missing dynamic correlation. CASSCF spin densities oscillate with active-space size. — [Reiher 2014 slides](https://ethz.ch/content/dam/ethz/special-interest/chab/imps/reiher-dam/documents/Diverse/reiher_mariapfarr2014.pdf)
- (2016) Automated active-space selection (autoCAS) uses DMRG orbital entropies to pick active orbitals. — [Stein & Reiher, "Automated selection of active orbital spaces", arXiv:1602.03835 (JCTC 2016)](https://arxiv.org/abs/1602.03835) (title and approach only, not re-read here)

### Inferences
- Orbital basis acts on both axes. For a fixed active space and an exact solve, the orbital rotation within the space does not change the CASCI energy, but it changes the M needed and the risk of local minima, which is time and finite-M accuracy. Changing *which* orbitals are active (natural-orbital truncation, autoCAS) or optimizing them (DMRG-SCF) changes the **converged result** itself.
- The 2026 FeMoco protocol shows a pattern: the "best starting state" is a *coupled* choice of (reference determinant → natural orbitals → localization → ordering → DMRG). Each spin or broken-symmetry basin gets its own orbitals. A NN-produced starting state should probably predict these jointly rather than independently.

### Gaps
- No modern quantitative table (M needed for 1 mEh error) comparing canonical vs split-localized vs natural vs DMRG-SCF orbitals across a transition-metal benchmark set was retrieved. Olivares-Amaya 2015 likely contains some of this but was not accessible.

---

## 4. Hard real examples: Fe–S clusters, P-cluster, FeMoco, Cr2, Cu2O2, polyenes/PAHs — where the starting state is critical

### Takeaway
In multi-metal clusters, the low-energy spectrum is dense: many spin couplings and broken-symmetry basins lie within about 1–5 kcal/mol. DMRG is a non-linear optimizer that "is easily trapped in local minima", so the initial state (spin sector, broken-symmetry pattern, orbitals) effectively selects the answer. The state of the art is exhaustive enumeration of starting references (20–152 basins for the P-cluster in 2019; 78,750 UHF guesses reduced to 840 references for FeMoco in 2026), followed by DMRG with D in the thousands to tens of thousands.

### Cited Findings
**[2Fe-2S] / [4Fe-4S] (2014)**
- [4Fe-4S]: minimal complete active space of all Fe 3d plus S 3p, i.e., 54e in 36o (about 10^16 determinants). For [2Fe-2S] ([Fe2S2(SCH3)4]2−/3−), the DMRG levels form a spin ladder S = 0–5 with fitted J ≈ 236 cm⁻¹, against experiment 148 ± 16 cm⁻¹ and BS-DFT ≈ 310 cm⁻¹. Same-spin levels are dense on the scale of vibrational fluctuations, and the Heisenberg–double-exchange model underestimates the number of states by 1–2 orders of magnitude. — [Sharma, Sivalingam, Neese, Chan, Nat. Chem. 6, 927 (2014), DOI 10.1038/nchem.2041; arXiv:1408.5080](https://arxiv.org/abs/1408.5080). (Bond dimensions and orbital and ordering details are in the Methods/SI, which were not retrieved.)

**P-cluster of nitrogenase (Nat. Chem. 2019)**
- Active spaces: CAS(108e,71o) for the synthetic model, (114e,73o) for P^N, (117e,75o) for P^1+ and (120e,77o) for P^OX, corresponding to Hilbert spaces of about 10^31–10^33. The calculations started from BS product states (D = 1) built by distributing Fe spin states, followed by spin projection and growth of D, with 20/35/70/152 basins per system. State-averaged D = 3000 was used for excited-state energies.
- Results: P^N has a single S = 0 spin-coupling pattern within 5 kcal/mol, with the S = 1 recoupling at 0.6 kcal/mol. P^1+ has two patterns, with S = 5/2 lying 2.7 kcal/mol below S = 1/2. P^OX has four patterns, with S = 4 lying 1.4 kcal/mol below S = 3.
- DMRG convergence error was below 0.8 kcal/mol, except about 2.8 kcal/mol for the P^OX S = 3 vs S = 4 gap.
- Quote: "the non-linear optimization of the wavefunction in the DMRG algorithm is easily trapped in local minima".
- — [Li, Guo, Sun, Chan 2019, arXiv:1810.10196](https://arxiv.org/abs/1810.10196)

**FeMoco (Jan 2026)**
- LLDUC model: 113e/76o. UDMRG in block2 used D = 5000 for ranking, D = 8000 for checks and D up to **18,000** in the main calculation. Extrapolation used 12 energies from D = 5000 to 16,000 with ΔE ~ exp[−κ(log D)²].
- Cost: D = 18,000 required **317,440 core-hours per sweep** (2 sweeps), about 2.77 M core-hours in total. Reaching 1 kcal/mol by UDMRG alone would need D ≈ 393,000, about 4.1×10^9 core-hours.
- Consensus ground-state energy: −22140.4106 ± 0.0005 Eh. Two BS isomers (BS7-235 and BS8-237) are degenerate within uncertainty.
- The authors argue that the spin gap within one isomer's tower of states is below 1 kcal/mol, so ranking many largely single-reference BS states is the right framing.
- — [Zhai et al. 2026, arXiv:2601.04621](https://arxiv.org/abs/2601.04621)

**Cr2 (2022)**
- Setup: 28e in 76o, cc-pVDZ-DK with X2C, DMRG with **SU(2) symmetry and bond dimension up to 28,000** (block2). The PDZ curve is the average of DMRG and SHCI, with uncertainty taken as half the DMRG–SHCI difference (below 0.01 eV). Dynamic correlation was added by REPT on a 12e/12o CAS, with CBS extrapolation up to cc-pV5Z-DK.
- CASSCF and CCSD(T) fail to give a reasonable bond length or shelf region.
- — [Larsson, Zhai, Umrigar, Chan, "The chromium dimer: closing a chapter of quantum chemistry", J. Am. Chem. Soc. 144, 15932 (2022); arXiv:2206.10738](https://arxiv.org/abs/2206.10738)
- Earlier Cr2 DMRG (Kurashige & Yanai 2011; Olivares-Amaya 2015) is part of this history, but its ordering and initial-guess details were not retrieved here.

**Cu2O2 (small-m failure example; 2014 slides)**
- CAS(26,44) isomer energy difference: 99.6 kJ/mol at m = 32, 98.2 at m = 44, 103.6 at m = 64 and 109.3 at m = 128, against 149 kJ/mol from large-scale DMRG (Kurashige & Yanai 2009). Results at small m are non-monotonic and far from converged. — [Reiher 2014 slides](https://ethz.ch/content/dam/ethz/special-interest/chab/imps/reiher-dam/documents/Diverse/reiher_mariapfarr2014.pdf)

**Benign cases**
- CoH CAS(10,10): m = 64 gives −1381.952054 Eh against full CAS −1381.952074 Eh, and a singlet–triplet gap of 113.03 vs 112.99 kJ/mol. — [Reiher 2014 slides](https://ethz.ch/content/dam/ethz/special-interest/chab/imps/reiher-dam/documents/Diverse/reiher_mariapfarr2014.pdf)

**Iron nitrosyl spin densities (DMRG(13,29))**
- The deviation from the m = 2048 reference fell from 0.0323 at m = 128 to 0.0034 at m = 1024. — [Reiher 2014 slides](https://ethz.ch/content/dam/ethz/special-interest/chab/imps/reiher-dam/documents/Diverse/reiher_mariapfarr2014.pdf)

**Polycyclic aromatic hydrocarbons / open-shell graphene fragments (2025)**
- Systems: [3]triangulene (22e,22o), ovalene (32e,32o), C40H20 (40e,40o), peripentacene (44e,44o) and an aza-[4]triangulene analogue (36e,33o). References used M = 3000–4000 (truncation error ≤ 1e-7).
- **Standard DMRG predicts the wrong ground-state spin ordering for peripentacene at low M.** The reference singlet–triplet gap is 4.78 mEh. A Δ-ML correction fixes the ordering from M = 500 (truncation error about 1e-4).
- — [Golub, Yang, Vlček, Veis 2025](https://arxiv.org/abs/2412.07607)

**Polyenes (2015)**
- C20H22: M = 100 gives bond-length errors up to 0.006 Å (ground state) and about 0.025 Å (dark state near the solitons), while M = 500 gives about 0.0003–0.0006 Å relative to M = 1000. — [Hu & Chan 2015](https://arxiv.org/abs/1502.07731)

**Spin symmetry (SU(2)) and excited-state targeting**
- block2 supports SU(2) spin-adapted MPS (with singlet embedding for S ≠ 0) and S_z-only MPS. Conversion from SU(2) to non-spin-adapted form is exact, but the bond dimension grows.
- State-averaged DMRG is "robust for tens of roots", but accuracy at fixed M drops as the number of roots grows.
- Alternatives are projected orthogonalization and level-shift state-by-state approaches. Harmonic Davidson for interior states is less stable for dense spectra.
- — [Zhai et al. 2023](https://arxiv.org/abs/2310.03920)
- (2015) Root flipping: state-specific DMRG is susceptible to root flipping, e.g., near conical intersections, because tensors optimized for one state are suboptimal for another. The mitigation is to choose, at every Davidson block step, the eigenvector with maximum overlap to the previous solution. State-averaged DMRG at the first geometry provides the initial guesses, and back-sweeps from large M give accurate small-M guesses. For C20H22 an S2–S3 gap of 0.019 eV (a near crossing) occurred during optimization. — [Hu & Chan 2015](https://arxiv.org/abs/1502.07731)

### Inferences
- In these hard systems, "fast convergence" and "correct state" separate. A good generic MPS (CI-DEAS or random+noise) converges *quickly* to *some* basin. Choosing the starting basin (spin sector, BS pattern, spin-coupling pattern) determines the *answer*. The decisive step is the combinatorial choice of reference, with 20–152 basins (2019) and 840 references (2026). Today that is brute-forced.
- Unrestricted (S_z-only) DMRG from broken-symmetry references (2026) and SU(2)-adapted DMRG (2022 Cr2, 2019 P-cluster via spin projection) represent two different "starting-state" philosophies, with different bond-dimension costs.

### Gaps
- Bond dimensions and ordering/orbital details for Sharma et al. 2014 ([2Fe-2S], [4Fe-4S]), Kurashige & Yanai 2011 (Cr2) and Guo et al. 2018 (Cr2) were not retrieved.
- N2 dissociation as a DMRG initial-state case study (e.g., the DMRG-TCC N2 paper, JCTC 2018) was identified but not read.
- No quantitative study was found of how often root flipping occurs, or how often DMRG converges to the wrong spin state, as a function of the initial guess.

---

## 5. Warm starts across geometries and basis sets, and DMRG as an initial-state generator for quantum algorithms

### Takeaway
Reusing the converged MPS (and quantum-number structure) from a neighbouring geometry is established practice. It requires orbital tracking by maximum overlap and phase alignment, plus root tracking for excited states (2015). For quantum phase estimation (QPE), DMRG/MPS states are now the leading initial-state candidates: about 0.9 squared overlap at D = 4000 for a candidate FeMoco state (2024), and a BS determinant with overlap 0.45 to a D = 18,000 state (2026). However, the overlaps of single determinants or CSFs decay exponentially with the number of metal centres, to about 1e-7 for FeMoco (2023).

### Cited Findings
**Geometry warm starts (2015)**
- At each new geometry, the DMRG sweep restarts from the previous geometry's solution at the same M, using one-site, state-specific sweeps **with noise turned off**. Davidson guesses come from wavefunction prediction. Quantum numbers and block sparsity are fixed at the initial geometry. Orbitals are matched between steps by maximum molecular-orbital overlap, which also aligns phases.
- Looser convergence (fewer sweeps) was used far from equilibrium, where gradients are large. No sweep-count savings were quantified.
- — [Hu & Chan, JCTC 2015](https://arxiv.org/abs/1502.07731)
- (2022) The Cr2 potential curve was computed pointwise with DMRG (D up to 28,000) and SHCI. Whether neighbouring-geometry MPSs were reused is not stated in the text read. — [Larsson et al. 2022](https://arxiv.org/abs/2206.10738)

**Quantum-algorithm initial states**
- (2023) Lee et al. (Nature Communications 14, 2023, DOI 10.1038/s41467-023-37587-6):
  - The largest-weight Slater determinant *and* the best CSF both decay exponentially with the number of metal centres in Fe–S clusters, with weights of about **1e-7 for FeMoco**. This is analysed in split-localized orbitals.
  - For a 24-qubit [2Fe-2S] model, adiabatic state-preparation time varies by about **8 orders of magnitude** depending on the initial Hamiltonian and tracks the inverse initial weight. Mean-field starts were worse than QPE itself, and interacting starts needed about 20 of 24 qubits treated correlatedly.
  - The orthogonality catastrophe was discussed: global overlap is a product of local overlaps for product-like subsystems.
  - For classical DMRG, the bond dimension needed for constant error per metal centre grows more slowly beyond 4 metal centres (area-law-like).
  - Conclusion: no evidence for generic exponential quantum advantage, because good initial states are needed and classical heuristics do not show exponential scaling.
  - — [arXiv:2208.02199](https://arxiv.org/abs/2208.02199); [venue/DOI record](https://ideas.repec.org/a/nat/natcom/v14y2023i1d10.1038_s41467-023-37587-6.html)
- (2023 preprint; PRX Quantum Dec 2024) Fomichev et al.:
  - Pipeline: classical candidate generation (HF, CISD/CCSD, CASCI, SHCI, DMRG), conversion to a sum-of-Slater-determinants or MPS form, quality assessment by **energy distribution** rather than overlap (since the ground state is unknown), quantum implementation and QPE.
  - DMRG and SHCI are judged "the leading contenders" for strongly correlated cases.
  - Encoding classical states usually costs less than energy estimation.
  - For select cases, better states reduce the total cost "by several orders of magnitude" compared with the best single product state (abstract claim; underlying data not retrieved).
  - Test systems include Cr2, [Fe4S4] and H16.
  - — [arXiv:2310.18410](https://arxiv.org/abs/2310.18410); [PRX Quantum record](https://doaj.org/article/35c9de77548240b88849eb6a4efcdbbd)
- (2024) Berry et al. (Google/Caltech et al.):
  - Approach: MPS initial states for QPE with a faster unitary synthesis (about 7× Toffoli reduction over prior work for MPS preparation).
  - For FeMoco, a **D = 4000 MPS gives an estimated squared overlap of about 0.9** with a candidate ground state, using an extrapolation protocol validated on Fe2S2 and Fe4S4. The candidates come from Li–Chan-style spin-coupling enumeration.
  - Only 2–3 QPE repetitions are needed, for a total of about 7.3×10^10 Toffolis to refine the FeMoco energy.
  - — [Berry et al., "Rapid initial state preparation for the quantum simulation of strongly correlated molecules", arXiv:2409.11748 (Sep 2024)](https://arxiv.org/abs/2409.11748)
- (2026) The FeMoco classical study compares its cost with a quantum estimate of about 8.6 h that assumes O(1) overlap. The filtered BS determinant has overlap 0.4468 with the D = 18,000 UDMRG state (described as overlap with the manifold of eigenstates within 1 kcal/mol). The authors suggest quantum methods could reuse the same "rank BS references" strategy for initial states. — [Zhai et al. 2026](https://arxiv.org/abs/2601.04621)

### Inferences
- Warm starts across geometries are effectively a "neighbouring-Hamiltonian" initial-state method. They require consistent orbitals (maximum overlap and phase tracking) and a fixed quantum-number structure. A learned initial state that is smooth in geometry is plausible, but its gains over the previous-geometry MPS would need to be demonstrated.
- No source found quantifies sweeps saved by geometry warm starts, or warm starts across basis sets (e.g., projecting a cc-pVDZ MPS into cc-pVTZ). This remains a gap.

### Gaps
- No quantitative data on sweeps or time saved by reusing an MPS from a neighbouring geometry.
- No literature found on transferring an MPS across basis sets or active-space enlargements beyond the general "small space first, then augment" strategy (2014 review).
- Fomichev et al.'s overlap numbers for Cr2/[Fe4S4]/H16, and Lee et al.'s Table S3 DMRG overlaps, were not extracted.

---

## 6. Machine-learning approaches in quantum-chemistry DMRG

### Takeaway
ML in QC-DMRG so far targets *inputs derived from entanglement*: predicted single-orbital entropies for active-space selection (2020) and predicted mutual information for ordering (2023). Other targets are post-hoc energy corrections from cheap low-M runs (Δ-ML, 2025) and DMRG datasets (2025). No published work was found that uses a neural network to generate the initial MPS itself, or that uses RL for QC-DMRG orbital ordering.

### Cited Findings
- (2020 preprint) ML active-space selection, "Automatic selection of active spaces for strongly correlated systems using machine learning algorithms":
  - Model: feed-forward networks (e.g., 5 hidden layers × 896 ReLU neurons, dropout 0.1) predicting **DMRG single-orbital entropies** (Box-Cox transformed; labels from M = 1024/2048 DMRG).
  - Inputs: 29 HF-level per-orbital features, including one- and two-electron integrals, orbital energy, spatial extent, labels, AO-type vector and the 10 largest exchange integrals.
  - Training: 5,796 artificial transition-metal complexes (Cr–Zn), i.e., 208,656 orbitals. Thresholds: S > 0.1 important; 0.05–0.1 less important.
  - Out-of-sample matches (selected/reference orbitals): CrCl2O2 18/18, [Cr2O7]2− 31/31, Fe(II)-porphyrin 20/22, ferrocene 16/20, Ni(CO)4 17/20, CuOH 12/14. Misses were concentrated in ferrocene and the porphyrin.
  - — [Golub, Antalík, Veis, Brabec, arXiv:2011.14715](https://arxiv.org/abs/2011.14715) (later journal version not verified here)
- (2023) ML-predicted mutual information used to order orbitals for accurate DMRG and to identify correlation structure, replacing costly DMRG pre-runs. — [Golub, Antalík, Beran, Brabec, Chem. Phys. Lett. 813, 140297 (2023)](https://asep.lib.cas.cz/arl-cav/en/detail-cav_un_epca-0566845-Mutual-information-prediction-for-strongly-correlated-systems)
- (2025) Δ-ML-boosted DMRG:
  - Model: a message-passing GNN with orbitals as nodes (feature: single-orbital entropy) and edges where mutual information exceeds 0.004 (features: mutual information and occupancy one-hot), combined with the truncation error. It predicts the zero-truncation-error energy from cheap low-M runs.
  - Training: 100 PAHs (COMPAS-1D). Testing on peri-fused PAHs up to (44e,44o).
  - Results: within 1 mEh of the reference for M = 750–1250, with correct singlet–triplet ordering for peripentacene from M = 500 where plain DMRG fails.
  - Scope: it does **not** predict orderings or initial guesses (these were fixed to Fiedler and CI-DEAS).
  - — [Golub, Yang, Vlček, Veis, J. Phys. Chem. Lett. 2025, DOI 10.1021/acs.jpclett.5c00207](https://pubs.acs.org/doi/10.1021/acs.jpclett.5c00207); [arXiv:2412.07607](https://arxiv.org/abs/2412.07607)
- (2020) ML active-space selection from bond dissociation: Jeong, Stoneburner, King, Gagliardi et al., "Automation of active space selection for multireference methods via machine learning on chemical bond dissociation", JCTC 2020 (SI file ct9b01297). — [Gagliardi group announcement](https://gagliardigroup.uchicago.edu/2020/03/01/several-gagliardi-group-members-have-collaborated-on-a-recent-jctc-publication-automation-of-active-space-selection-for-multireference-methods-via-machine-learning-on-chemical-bond-dissociation/); [ChemRxiv](https://chemrxiv.org/engage/chemrxiv/article-details/60c746babb8c1a4c033da901) (details not read in this session)
- (2025) Dataset: "DMRG Quantum Chemistry Dataset for Multi-Reference Machine Learning" proposes a **50,000-point** DMRG-SCF dataset (pySCF + block2; transition-metal diatomics, organic radicals, metal–ligand complexes). It stores ground- and excited-state energies, spin densities, RDMs and "entanglement metrics", at a cost of about 1 M CPU-hours. Released as a NeurIPS 2025 AI-for-Science workshop poster. — [Gugler & Glaser, NeurIPS 2025 workshop](https://neurips.cc/virtual/2025/126043)
- (2025, 2026) Other ML-adjacent items: DMRG and orbital optimization on AI accelerators (GPU tensor cores), which is hardware rather than learned models. — [Werner, Menczer, Legeza 2025](https://arxiv.org/abs/2501.18263); [arXiv:2503.20700](https://arxiv.org/abs/2503.20700)

### Inferences
- Entanglement descriptors (single-orbital entropy, mutual information) are the shared currency. They determine active space (autoCAS, Golub 2020), ordering (Fiedler on mutual information, Golub 2023) and warm-up (CI-DEAS uses entropies), and they are the features of the 2025 Δ-ML GNN. A network that predicts the mutual-information graph from HF/integral features would therefore feed all three "starting-state" components at once.
- Predicting the MPS tensors themselves, or a determinant/CSF/low-D MPS seed, from a network has not been reported for molecular DMRG. This is an open niche.

### Gaps
- No RL- or GNN-based orbital-ordering method for molecular DMRG with reported M-reduction numbers was found (searched 2020–2026).
- No neural-network-generated initial MPS for QC-DMRG was found.
- Accuracy numbers from the 2023 CPL mutual-information-prediction paper (e.g., energy error under ML vs DMRG-derived ordering) were not retrieved; only the abstract was available.

---

## Open questions and gaps

1. **No standardized benchmark of initial guesses.** No multi-molecule study was found that reports sweeps-to-convergence and wall time for HF, CI-DEAS, random+noise, CCSD-occupancy, SCI-to-MPS and low-D-MPS seeds under fixed orbitals, ordering and M schedule. The best available datum is a single F2 comparison (Keller & Reiher 2014): a 76 mEh first-sweep gap shrinking to 0.15 mEh after 20 sweeps.
2. **Time vs result is under-reported.** Papers rarely separate "converged faster" from "converged to a lower or different state". The 2014 review states the starting-guess effect is about 10× smaller than orbital choice and ordering, but this is a qualitative estimate citing older work.
3. **Ordering benchmarks with numbers are dated or not accessible.** These include Moritz–Hess–Reiher 2005 (GA) and Olivares-Amaya 2015 (Fiedler/GA on transition-metal systems). Modern methods (multi-site rearrangement 2025, swap-gate global optimization 2025) are tested on spin chains or lack published molecular M-reduction numbers.
4. **RL/ML ordering for molecules** is essentially unexplored beyond the 2023 mutual-information prediction. No RL ordering for QC-DMRG was found.
5. **Wrong-state risk is not quantified.** P-cluster (2019) and FeMoco (2026) show that the basin found depends on the starting BS pattern, but no paper gives statistics such as "fraction of random or generic starts landing in the true ground basin".
6. **Warm starts across geometries and basis sets** lack measured savings. Cross-basis MPS transfer is undocumented.
7. **Overlap vs bond dimension for quantum-algorithm state preparation.** Known data points: D = 4000 gives about 0.9 squared overlap for a FeMoco candidate (2024); a single BS determinant gives 0.45 overlap with D = 18,000 (2026); single determinants and CSFs reach about 1e-7 (2023). These involve different Hamiltonians and orbital bases and are not directly comparable.
8. Details from Sharma 2014, Kurashige–Yanai 2011 and Guo 2018 (Cr2), and the N2 DMRG-TCC study (bond dimensions, orderings, guesses) were not retrieved in this session.

## Implications for a neural-network-generated initial state

- **Targets with the most leverage.** Based on the evidence, orbital choice and ordering affect the finite-M result more than the MPS initial guess does (estimate cited in the 2014 review). A network could therefore best predict (a) the mutual-information / single-orbital-entropy graph, which drives active-space selection, Fiedler/GA ordering and the CI-DEAS active-space vector, and (b) the orbital rotation (localization or natural-orbital mixing). An MPS seed comes on top of these. Prior art for (a) exists (Golub et al. 2020, 2023), which provides baselines and possibly training-data recipes.
- **Baselines to beat** (all documented in production codes as of 2023–2025):
  - Ordering: Fiedler on the exchange or mutual-information matrix (cheap), and Fiedler+GA refinement (block2, ORCA GAOPT; GA-ordered αβ pairs in the 2026 FeMoco work).
  - Initial MPS: CI-DEAS (Budapest/Veis), random+noise (CheMPS2/block2), CCSD-occupancy or determinant/CSF-based MPS (block2).
  - Orbitals: split-localized natural orbitals (ORCA, block2/PySCF workflows, FeMoco 2026).
  
  Gains should be reported as sweeps saved and wall time to reach a fixed energy (time), *and* as energy or extrapolated error at fixed M and correct-basin rate (result).
- **Expected magnitude of gains from a better MPS seed alone.** For small or medium molecules, mainly in the first one or two sweeps: tens of mEh in sweep 1 and sub-mEh after convergence (F2, 2014). Warm-up methods like CI-DEAS already capture 90–99% of the correlation energy in the first half-sweep (2003). Overall speedups are probably bounded by the share of total time spent in early sweeps, unless the seed also lets one skip the low-M ramp in ORCA-style schedules (e.g., 250→1000→… for 8+8 sweeps).
- **Where an NN seed could change the result rather than just the time.** In multi-metal clusters, DMRG is "easily trapped in local minima" (2019), and the field currently enumerates 20–152 BS basins (P-cluster) or samples 78,750 UHF guesses (FeMoco 2026). A model that ranks or proposes BS patterns or spin-coupling seeds (D = 1 or low-D MPS) could cut this search. The 2026 FeMoco authors explicitly propose "ranking low-energy broken-symmetry references" as an initial-state strategy for quantum algorithms too.
- **Representation constraints.** The seed must respect the symmetry sector:
  - SU(2)-adapted vs S_z-only (conversion to S_z is exact but raises D);
  - point-group irreps;
  - for excited states, root identity (maximum-overlap tracking to avoid root flipping).
  
  A low-D MPS or a short CSF/determinant expansion is the natural output format. block2 can already build an MPS from a linear combination of determinants or CSFs, or fit from an approximate MPS.
- **Noise and two-site sweeps interact with the seed.** Two-site DMRG with perturbative noise largely erases memory of a poor seed (the stated purpose of noise). A good seed is most valuable when using cheaper one-site sweeps or low noise, as in geometry warm starts with noise off (Hu & Chan 2015). It is risky if it locks in wrong quantum-number sectors; ORCA warns that early locking can trap DMRG-SCF.
- **Quantum-computing tie-in.** If the seed is used for QPE state preparation, overlap matters more than energy. Single determinants and CSFs decay to about 1e-7 overlap for FeMoco (2023), whereas D = 4000 MPSs reach about 0.9 squared overlap for a candidate state (2024). The energy distribution of the candidate state, rather than overlap, is the recommended practical quality metric (Fomichev et al.).
- **Data availability.** A 50k-point DMRG-SCF dataset (pySCF/block2, with entanglement metrics and RDMs) was announced at NeurIPS 2025 (Gugler & Glaser). The PAH sets with CI-DEAS/Fiedler DMRG (Golub et al. 2025) and the 5,796-complex orbital-entropy set (Golub et al. 2020) are other potential training or benchmark sources. Their public availability was not verified.
