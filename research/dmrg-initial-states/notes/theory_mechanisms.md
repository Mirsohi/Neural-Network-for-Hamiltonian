# Why and when the starting MPS matters for DMRG: mechanisms, mitigations, theory

Scope: ground-state and low-lying-state DMRG, both finite and infinite. The notes cover why the initial MPS affects convergence and run time, which algorithmic ingredients amplify or reduce that dependence, what theory says about the optimization landscape, and what a "better" initial state would actually buy. This feeds a project that aims to produce DMRG starting states with neural networks.

Evidence labels used throughout:
- **[measured]**: numerical results reported in a primary paper.
- **[theorem]**: a proved result.
- **[docs]**: official software documentation. This is practitioner guidance, not a controlled study.
- **[forum]**: Q&A posts on ITensor or TeNPy forums. Anecdotal folklore.
- **[memory]**: a citation detail I am confident of but did not re-verify in this session.

Each claim carries its year.

Access note: the SIAM/Crossref record for Rohwedder & Uschmajew (2013) could not be read. The WebFetch proxy rate-limited it (HTTP 429), the Crossref API was blocked by the egress proxy, and SIAM disallows robots. The statements about that paper's content are therefore flagged [memory].

---

## Q1. Documented failure modes caused or worsened by the starting state

### Takeaway
DMRG is a local, alternating optimizer. The documented failures are:
- metastable "sticking" at an energy well above the reachable minimum
- a frozen bond basis or quantum-number (QN) sector structure in single-site DMRG, so missing sectors can never re-enter
- slow build-up of long-range or large-scale correlations
- a bias toward low-entanglement states, which selects symmetry-broken or minimally entangled (MES) members of degenerate manifolds
- convergence to the wrong member of a near-degenerate or first-order-competing manifold, or to excited states
- limit cycles and non-monotonic energies

Each is documented in primary papers from 2005–2023 and in code documentation. The initial state matters most when it lacks QN sectors, structure, or long-range entanglement that the local update cannot create on its own.

### Cited Findings

**Metastable sticking (2005, 2011, 2012)**
- [measured, 2005] On a 100-site S=1 Heisenberg chain with m=50, plain single-site DMRG "gets stuck significantly above the two-site energy." With periodic boundaries, both the uncorrected single-site and the standard two-site methods stuck "two or three times in higher energy states" during the early sweeps. The density-matrix-corrected single-site method "never gets stuck." — [White, "Density matrix renormalization group algorithms with a single center site," PRB 72, 180403(R) (2005), arXiv:cond-mat/0508709](https://arxiv.org/abs/cond-mat/0508709)
- [review, 2012] DMRG fails for one of two reasons: too few states kept, or getting stuck. The review says DMRG "is globally a variational method and can therefore get stuck in a metastable state." It adds that "a key way to avoid metastability is to begin with a wavefunction that is already close to the true ground state." — [Stoudenmire & White, "Studying two-dimensional systems with the density matrix renormalization group," Annu. Rev. Condens. Matter Phys. 3, 111 (2012), arXiv:1105.1374](https://arxiv.org/abs/1105.1374)
- [review, 2023] In the infinite-system warm-up, "a metastable state can be favored by edge effects in the early DMRG steps." This can lead to poor convergence of the variational problem "or even to incorrect results." — [Catarina & Murta, "Density-matrix renormalization group: a pedagogical introduction," Eur. Phys. J. B 96, 111 (2023)](https://link.springer.com/article/10.1140/epjb/s10051-023-00575-2)
- [review, 2014] Wouters & Van Neck write that "The DMRG algorithm can get stuck in a local minimum or a limit cycle, if D is insufficiently large." The risk is higher with poor orbital choices and orderings. They also note that "the starting wavefunction has an influence on the converged energy" and on convergence rate. — [Wouters & Van Neck, "The density matrix renormalization group for ab initio quantum chemistry," Eur. Phys. J. D 68, 272 (2014) (journal ref [memory]), arXiv:1407.2040](https://arxiv.org/abs/1407.2040)
- [review/measured, 2014] Keller & Reiher write that "in Quantum Chemistry this single-site DMRG gets trapped in local energy minima for even the simplest systems." — [Keller & Reiher, "Determining factors for the accuracy of DMRG in chemistry," Chimia (2014), arXiv:1401.5497](https://arxiv.org/abs/1401.5497)

**Frozen basis and lost QN sectors in single-site DMRG (2005, 2014, 2015, 2023)**
- [mechanism, 2005] White explains the mechanism for single-site DMRG:
  - "any limitation on the quantum numbers present in the environment translates into a restriction on the states appearing in the renormalized system block."
  - An environment with m states supports at most m nonzero density-matrix eigenvalues, so the basis cannot grow unless states are added artificially.
  - Missing system–environment fluctuations propagate back and forth when the blocks swap roles.
  - In wide ladders and long-range systems, the missing fluctuations can lie far from the center site and "never get built in."
  - Adding random extra states with more QNs helps but does not fix poor convergence.
  
  Source: [White 2005](https://arxiv.org/pdf/cond-mat/0508709)
- [measured, 2015] A 20-site S=1/2 chain (S^z_tot=0) was started from an artificial state built from 20 linearly independent states. Without enrichment (α=0), DMRG "converges" to E=-6.35479. The QN distribution stays asymmetric, and states are removed but never added. With enrichment, it reaches E=-8.6824724. Under U(1) symmetry, a local change cannot add a state whose QN has no partner across the bond, because that state's "norm will be zero identically." — [Hubig, McCulloch, Schollwöck & Wolf, "A strictly single-site DMRG algorithm with subspace expansion," PRB 91, 155115 (2015), arXiv:1501.05504](https://arxiv.org/abs/1501.05504)
- [docs, current] The TeNPy source docstring says "the one-site algorithm cannot increase the MPS bond dimension by itself." From a product state, the single-site engine "depends critically on the use of a Mixer." — [TeNPy `tenpy/algorithms/dmrg.py`](https://raw.githubusercontent.com/tenpy/tenpy/main/tenpy/algorithms/dmrg.py)
- [paper, 2023] Gleis, Li & von Delft note that symmetric DMRG ground-state searches must sometimes add or change symmetry sectors on virtual bonds when that lowers the energy. Single-site DMRG cannot do this; two-site DMRG can, at much higher cost. — [Gleis, Li & von Delft, "Controlled bond expansion for DMRG ground state search at single-site costs," PRL 130, 246402 (2023), arXiv:2207.14712](https://arxiv.org/abs/2207.14712)
- [review, 2014] "The corrections or noise help to reintroduce lost symmetry sectors." The one-site method also does not distribute the virtual dimension over symmetry sectors automatically, while the two-site method does. — [Wouters & Van Neck 2014, arXiv:1407.2040](https://arxiv.org/pdf/1407.2040)
- [applied math, 2014] For a single eigenvector, plain ALS (the math analogue of single-site DMRG) "is unable to adapt the ranks." DMRG (two-site, MALS) "is rank adaptive." — [Kressner, Steinlechner & Uschmajew, "Low-rank tensor methods with subspace correction for symmetric eigenvalue problems," EPFL MATHICSE report 40.2013; SIAM J. Sci. Comput. 36, A2346 (2014) [memory]](https://www.epfl.ch/labs/mathicse/wp-content/uploads/2018/10/40.2014NEW_DK-MS-AU.pdf)
- [docs/forum] QN conservation makes sticking worse: "This problem is exacerbated for quantum number conserving DMRG where the search space is more constrained." — [ITensor DMRG FAQ](https://itensor.github.io/ITensors.jl/stable/faq/DMRG.html)

**Slow build-up of long-range and large-scale correlations (2012)**
- [review, 2012] In 2D strips, hopping "may connect sites which are the transverse width apart in the MPS path." These correlations "may have trouble getting started," which is why noise helps. DMRG "is better able to capture entanglement on Hamiltonian bonds that remain nearest-neighbor" along the path. — [Stoudenmire & White 2012](https://arxiv.org/pdf/1105.1374)
- [paper, 2012] Dolfi et al. report that DMRG "often fails to converge" for systems with several length scales, such as lattice discretizations of continuum models and dilute or weakly doped lattice models. The cause is that local optimization "is ineffective in updating large-scale features." — [Dolfi, Bauer, Troyer & Ristivojevic, "Multigrid algorithms for tensor network states," PRL 109, 020604 (2012), arXiv:1203.6363](https://arxiv.org/abs/1203.6363)
- [docs] Starting electrons all on one side can make convergence very slow, because ground states usually have spread-out density. — [ITensor DMRG FAQ](https://itensor.github.io/ITensors.jl/stable/faq/DMRG.html)

**Low-entanglement bias: MES selection and cat-state collapse (2012, 2013)**
- [review, 2012] DMRG has "a bias toward states having low entanglement." Pinning can "select one order parameter direction, reducing the complexity and entanglement of the state." — [Stoudenmire & White 2012](https://arxiv.org/pdf/1105.1374)
- [measured, 2012] Toric-code-type topological order on cylinders:
  - At small m, DMRG returns a minimally entangled state with ⟨G⟩≈0 (a superposition of parity sectors).
  - At larger m on small systems, it converges to the higher-entanglement G=+1 eigenstate.
  - The authors attribute this to DMRG preferring low-entanglement states and to non-convergence of entanglement between the far ends of the snake path.
  
  Source: [Jiang, Wang & Balents, "Identifying topological order by entanglement entropy," Nature Phys. 8, 902 (2012), arXiv:1205.4289](https://arxiv.org/pdf/1205.4289)
- [paper, 2013] Jiang & Balents add a decoherence-like "quench" step that removes non-locally entangled (cat-like) states and favors minimum-entropy states in systems with asymptotic degeneracy, from either topological order or discrete symmetry breaking. — [Jiang & Balents, "Collapsing Schrödinger cats in the density matrix renormalization group," arXiv:1309.7438 (2013)](https://arxiv.org/abs/1309.7438)

**Wrong member of a degenerate or first-order manifold, and convergence to excited states (2021)**
- [measured, 2021] Block et al. (N=32, from random product states):
  - Mixed-field Ising model: DMRG can get stuck in the wrong polarization near the first-order transition and sometimes skips low-lying states entirely.
  - Tricritical Ising model: DMRG overshoots the ground-state energy just below the transition, converging to a paramagnetic state.
  - Anisotropic XXZ model: DMRG often fails to find both degenerate ferromagnetic ground states.
  - ZXZ+XX model (fourfold edge degeneracy): DMRG from a random start often finds excited states before all four ground states. They explain that "DMRG introduces a bulk excitation as it orthogonalizes the trial state against existing lower-energy states," and that this excitation is never removed.
  - "Results depend strongly on initialization," and seeding is hard without knowing where the transition is.
  
  Source: [Block, Motruk, Gazit, Zaletel, Landau, Vazirani & Yao, "Performance of the rigorous renormalization group for first-order phase transitions and topological phases," PRB 103, 195122 (2021)](https://quantumoptics.physics.berkeley.edu/s/2021-Performance-of-the-rigorous-renormalization-group-for-first-order-phase-transitions-and-topolog.pdf)
- [docs] A small energy variance shows only that ψ is close to *an* eigenstate: "this check does not ensure that psi is the ground state, but only one of the eigenstates." — [ITensor DMRG FAQ](https://itensor.github.io/ITensors.jl/stable/faq/DMRG.html)

**Competing orders in 2D: metastability that depends on the initial state (2011, 2017)**
- [measured, 2011] Kagome Heisenberg model:
  - "DMRG can get stuck in metastable states" on wider cylinders.
  - When the initial state and boundaries favored a honeycomb valence-bond crystal (HVBC), the HVBC stayed "metastable out to about m = 2400" before turning into the spin liquid.
  - With standard site ordering, the prepared HVBC "disappears within the first few sweeps with m < 200."
  - In a 400-site YC12 comparison, a random start found the spin liquid and became lower in energy near m≈2000.
  
  Source: [Yan, Huse & White, "Spin-liquid ground state of the S=1/2 kagome Heisenberg antiferromagnet," Science 332, 1173 (2011) [journal ref memory], arXiv:1011.6114](https://arxiv.org/pdf/1011.6114)
- [measured, 2017] In the stripe study of the 2D Hubbard model, DMRG used edge pinning fields (|h|=0.5t) to target stripe patterns. Some pinned stripe states are labeled metastable (e.g., the 6×16 FM-pinned 3-node state). Competing wavelengths differ by about 0.001t in DMRG energy for 6×32. — [Zheng et al., "Stripe order in the underdoped region of the two-dimensional Hubbard model," Science 358, 1155 (2017), supplement](https://authors.library.caltech.edu/records/45z9g-a3558/preview/aan7127_Zheng_SM.pdf)

**Other documented symptoms (docs, current)**
- [docs] TeNPy warning signs: an energy increase or entropy decrease between sweeps is "particularly suspicious"; the run hits max sweeps instead of a convergence criterion; results vary wildly under small parameter changes. TeNPy also warns that an "artificially enforced translational invariance" (wrong iDMRG unit cell) can block the true ground state. — [TeNPy "Protocol for using (i)DMRG"](https://raw.githubusercontent.com/tenpy/tenpy/main/doc/intro/dmrg-protocol.rst)
- [forum, 2026] An N=48 spin-1 chain (QN conserving, Néel-like start) needed about 150 sweeps for the entanglement entropy to converge, versus about 30 typically. Raising `eigsolve_krylovdim` to 5 made convergence "much faster." The user's edge-state explanation is a hypothesis only. — [ITensor Discourse, "Slow convergence of spin 1 AF Heisenberg chain" (Feb 2026)](https://itensor.discourse.group/t/slow-convergence-of-spin-1-af-heisenberg-chain/2579)

### Inferences
- The failure modes split into two groups:
  - **Representational:** the start lacks QN sectors, bond-basis directions, or long-range entanglement that local moves cannot create. This is mainly single-site DMRG without enrichment.
  - **Landscape:** two basins of comparable energy, e.g., first-order competition, competing 2D orders, or degenerate and topological manifolds. Even two-site DMRG with noise can stay in the wrong basin for many sweeps and large m (HVBC to m≈2400).
- A good initial state removes the first group almost entirely: right sectors, right bond-QN distribution, seeded long-range correlations. For the second group, it decides which basin DMRG lands in. This is a benefit only if the predictor is right; if it is wrong, it actively harms the result.
- The low-entanglement bias means DMRG's "attractor" in degenerate manifolds is the MES or symmetry-broken state. An initial state that is a symmetric cat superposition may be pulled toward a broken state anyway. This matters if the NN is trained to output symmetric states.

### Gaps
- I found no paper that systematically counts how often random starts get stuck as a function of model, size, and algorithm (a "success probability vs seed" study). Most evidence is case studies.
- I found no specific source naming "non-ergodic sweeps" as a term. The closest are the frozen-basis and QN arguments of White (2005) and Hubig (2015), and Dolfi's (2012) statement that local updates cannot change large-scale features.

---

## Q2. How single- vs two-site DMRG, density-matrix perturbation, subspace expansion (DMRG3S) and CBE change sensitivity to the starting state

### Takeaway
Two-site DMRG and all bond-enrichment schemes exist to make the result independent of the starting bond basis and QN structure:
- White's (2005) density-matrix perturbation
- DMRG3S/AMEn subspace expansion (2015)
- CBE (2023)

They remove the representational failure modes (frozen sectors and frozen rank) and cut run time by factors of about 2–4. None of them is a global optimizer, so basin-selection effects from the start survive. Noise also partly erases the information in a good initial state, a trade-off that matters for a learned initializer.

### Cited Findings

**White 2005: density-matrix correction ("noise")**
- [paper, 2005] The correction is Δρ = Σ_α a_α A^α ρ A^α†, built from operators acting at the block boundary. For Heisenberg: Δρ = a(S⁺ρS⁻ + S⁻ρS⁺ + S^zρS^z).
  - Typical prefactor: "a_α = a ∼ 10^-3 – 10^-4".
  - Larger a puts more "noise" into the basis, which speeds convergence but limits final accuracy.
  - Example schedule: a=1e-4 for sweeps 1–8, then 1e-6.
  - The derivation is a power-method or perturbation argument that needs only a starting state not orthogonal to the ground state.
  - Cost is about m³ times the number of connecting terms, which is usually small.
  - Speed-up from going to one site: about 2–4× overall; "the two site method is roughly a factor of three slower."
  
  Source: [White 2005](https://arxiv.org/pdf/cond-mat/0508709)
- [paper, 2012] Noise helps long-range correlations get started and is "particularly important" for periodic boundaries. It is "generally... turned off in later sweeps." — [Stoudenmire & White 2012](https://arxiv.org/pdf/1105.1374)

**DMRG3S, Hubig et al. 2015: subspace expansion**
- [measured, 2015]
  - **Expansion term.** The local tensor is enlarged by P_i = α L_{i-1} M_i W_i, a partial projection of H|ψ⟩, with zero padding on the neighbor and then truncation. This costs O(d w² m³), compared with O(w d³ m³) for White's perturbation.
  - **Choosing α.** α is adapted so the truncation energy change is about −0.3 × the optimization energy gain, which gives the fastest convergence. α "has to be taken to zero eventually" if m is too small, and must be fixed for extrapolation.
  - **Speed-ups.** Up to 3.9× over two-site DMRG (Fermi–Hubbard, m=1200) and about 2–2.7× over White's correction method. Over two-site DMRG for free fermions, it reaches more than 6×.
  - **Convergence tail.** The correction method shows "a long tail of slow convergence."
  
  Source: [Hubig et al. 2015, arXiv:1501.05504](https://arxiv.org/pdf/1501.05504)
- [applied math, 2014] AMEn (alternating minimal energy) enlarges the subspace each step with steepest-descent-like (residual) directions, which makes it rank-adaptive. Its geometric convergence rate is tied to that of steepest descent, and its convergence is "comparable to that of DMRG-type algorithms." — [Dolgov & Savostyanov, "Alternating minimal energy methods for linear systems in higher dimensions," SIAM J. Sci. Comput. 36, A2248 (2014) [journal ref memory], arXiv:1301.6068](https://arxiv.org/abs/1301.6068)
- [applied math, 2014] EVAMEn is the eigenvalue version: enrichment with a preconditioned block residual. Without preconditioning it "converges much worse." With preconditioning, EVAMEn beat ALS in iterations and time for multiple eigenvectors (p=3, 11) in one setting and matched it in another. — [Kressner, Steinlechner & Uschmajew 2014](https://www.epfl.ch/labs/mathicse/wp-content/uploads/2018/10/40.2014NEW_DK-MS-AU.pdf)

**CBE, Gleis–Li–von Delft 2023**
- [paper, 2023] CBE finds the significant part of the orthogonal complement in HΨ and expands bonds only by that part. It "yields two-site accuracy and convergence per sweep, at single-site costs," "uses no mixing parameters and is fully variational." — [Gleis, Li & von Delft 2023, arXiv:2207.14712](https://arxiv.org/abs/2207.14712)

**Two-site DMRG**
- [review, 2014] "It is better to use the two-site DMRG algorithm than the one-site version": it has more variational freedom, is less likely to get stuck, and distributes D over symmetry sectors automatically. — [Wouters & Van Neck 2014](https://arxiv.org/pdf/1407.2040)
- [measured, 2005] Two-site DMRG can still stick, as in the periodic S=1 chain. — [White 2005](https://arxiv.org/pdf/cond-mat/0508709)
- [docs] TeNPy notes the two-site engine "has occasionally displayed some convergence issues" from product states and advises "Just try both of them." — [TeNPy dmrg.py](https://raw.githubusercontent.com/tenpy/tenpy/main/tenpy/algorithms/dmrg.py)

**Typical production pattern (docs)**
- [docs] block2's default schedule: two-site sweeps with noise 1e-3 and Davidson threshold 1e-4 early, then noise 0 and threshold 1e-6. After `twodot_to_onedot`, it switches to final one-site sweeps. — [block2 docs, "Input File: Basic Usage"](https://block2.readthedocs.io/en/stable/user/basic.html)
- [docs] TeNPy mixer defaults: amplitude 1e-5, decay 2.0, disabled after 15 sweeps (finite). The default class is `SubspaceExpansion` for the single-site engine (on by default) and `DensityMatrixMixer` for the two-site engine (off by default). — [TeNPy dmrg.py](https://raw.githubusercontent.com/tenpy/tenpy/main/tenpy/algorithms/dmrg.py)
- [docs] ITensor calls noise "the most important and useful technique" for failing convergence. Example: `setnoise!(sweeps, 1e-6, 1e-7, 1e-8, 0.0)`, ending near 1e-11 or 0. — [ITensor DMRG FAQ](https://itensor.github.io/ITensors.jl/stable/faq/DMRG.html)

### Inferences
- With enrichment (noise, subspace expansion, CBE, or two-site), the representational effect of the start (which sectors and directions exist on each bond) is largely washed out within the first few sweeps. The start then matters mainly through:
  1. the basin it sits in
  2. how much converged structure it already carries, i.e., how many sweeps and how much bond-dimension growth are saved
- **Noise trade-off for a good initial state.** Noise of 1e-3 (block2 default) or White's a ≈ 1e-3–1e-4 deliberately perturbs the reduced density matrices and can degrade a high-quality start. A NN initializer should therefore be benchmarked with a reduced or zero noise schedule as well as the default.
- CBE and DMRG3S give a cleaner comparison than White's noise: CBE has no mixing parameter, and DMRG3S adapts α, so the start's information is less likely to be scrambled.
- A start with correct QN sectors is what makes pure single-site DMRG (with no enrichment) viable. Single-site is about 2–4× cheaper per sweep, so the payoff is concrete.

### Gaps
- No paper found that measures sensitivity to the initial state (e.g., variance of outcome over random seeds) for 2DMRG vs DMRG3S vs CBE head-to-head. Hubig (2015) always uses the same initial state for all methods.

---

## Q3. Standard initialization strategies and what the codes recommend

### Takeaway
Common starting points are:
- random MPS of modest bond dimension (ITensor example: linkdims=10)
- QN-correct product states (Néel, or Hartree–Fock occupations)
- infinite-system warm-up (White 1992/93) or its quantum-chemistry descendants (DEAS / CI-DEAS)
- states pinned toward a candidate order
- free-fermion (Gaussian) MPS
- warm starts from a simpler or neighboring Hamiltonian
- coarse-grid (multigrid) solutions
- imaginary-time evolution

These are combined with bond-dimension ramps, decreasing noise, and loose-to-tight eigensolver tolerances. Code documentation gives heuristics, not measurements. The few measured comparisons are in Q7.

### Cited Findings

**Random MPS**
- [docs] ITensor tutorial: `psi0 = random_mps(sites; linkdims=10)` is "made by a random quantum circuit that is reshaped into an MPS." It "can help prevent the DMRG calculation from getting stuck in a local minimum." — [ITensorMPS.jl DMRG tutorial](https://github.com/ITensor/ITensorMPS.jl/blob/main/docs/src/tutorials/DMRG.md)
- [docs] ITensor FAQ: use "a random MPS with a modestly large bond dimension," since random states have "properties which are 'typical' of most ground states." — [ITensor DMRG FAQ](https://itensor.github.io/ITensors.jl/stable/faq/DMRG.html)
- [review, 2014] Quantum chemistry option: "distribute D equally over the symmetry sectors, and... fill the MPS with noise." This reportedly gives energies below Hartree–Fock in the first macro-iteration. — [Wouters & Van Neck 2014](https://arxiv.org/pdf/1407.2040)
- [theorem, 2023/2025] For Haar-random isometric MPS with extensive nearest-neighbor Hamiltonians, energy-gradient variance converges to a system-size-independent value of about 1/m². Randomly initialized isometric tensor networks therefore have no barren plateaus (see Q4). — [Barthel & Miao, "Absence of barren plateaus and scaling of gradients in the energy optimization of isometric tensor network states," Commun. Math. Phys. (2025), DOI 10.1007/s00220-024-05217-x, arXiv:2304.00161](https://arxiv.org/abs/2304.00161)

**Product and physically motivated states**
- [review, 2012] For antiferromagnets, "a Néel state may be a sufficiently good starting point." For subtler order, add pinning fields and remove them gradually. Smaller or lower-m runs can guide initial states. — [Stoudenmire & White 2012](https://arxiv.org/pdf/1105.1374)
- [review, 2014] Quantum chemistry: the "simplest option is to encode the Hartree-Fock determinant and to add white noise," or a perturbative correction, so important basis states are not lost during warm-up. — [Keller & Reiher 2014](https://arxiv.org/pdf/1401.5497)

**Free-fermion / Gaussian MPS**
- [forum, 2023] In one 2D Hubbard case, a Gaussian (Slater-determinant) MPS start did worse than a random product start, and the energy sometimes rose. Stoudenmire replied that "Gaussian MPS is mainly applicable to quasi-1D systems," that its parameters (`eigval_cutoff`, `maxblocksize`≈Ly) need tuning, and that one should check `inner(psi',H,psi)` before using it. — [ITensor Discourse, "Initial state calculation on 2D DMRG with Gaussian MPS" (Apr 2023)](https://itensor.discourse.group/t/initial-state-calculation-on-2d-dmrg-with-gaussian-mps/755)
- [memory] The underlying method is Fishman & White, "Compression of correlation matrices and an efficient method for forming matrix product states of fermionic Gaussian states," PRB 92, 075132 (2015), [arXiv:1504.07701](https://arxiv.org/abs/1504.07701).

**Infinite-system warm-up and DEAS / CI-DEAS**
- [history] In MPS-era practice, infinite-system DMRG "was seen as just a warm-up procedure" for finite sweeps. — [Schollwöck, "The density-matrix renormalization group in the age of matrix product states," Ann. Phys. 326, 96 (2011), arXiv:1008.3477](https://homepages.physik.uni-muenchen.de/~Schollwoeck/annals.pdf)
- [memory] Original algorithms: White, PRL 69, 2863 (1992), [doi:10.1103/PhysRevLett.69.2863](https://doi.org/10.1103/PhysRevLett.69.2863); White, PRB 48, 10345 (1993), [doi:10.1103/PhysRevB.48.10345](https://doi.org/10.1103/PhysRevB.48.10345).
- [measured, 2003] DEAS (dynamically extended active space) grows the active space during the first half-sweep by maximizing an entropy criterion. It "substantially" speeds convergence for momentum-space and quantum-chemistry DMRG; the abstract gives no sweep counts. — [Legeza & Sólyom, arXiv:cond-mat/0305336 (2003); published PRB 68, 195116 (2003) [memory]](https://arxiv.org/abs/cond-mat/0305336)
- [review, 2014] CI-DEAS "may achieve the fastest convergence, i.e. requires the smallest number of sweeps." Its best ordering places strongly entangled orbitals together. — [Keller & Reiher 2014](https://arxiv.org/pdf/1401.5497)

**Warm starts from a simpler or nearby problem**
- [docs] ITensor: run DMRG on a simplified Hamiltonian (interactions removed or local patches) and use its output as the start. For stubborn cases, use imaginary-time evolution first. — [ITensor DMRG FAQ](https://itensor.github.io/ITensors.jl/stable/faq/DMRG.html)
- [forum, 2024] Stoudenmire: converge a related Hamiltonian with a larger gap and use it as the start. Also run many sweeps at small `maxdim` (e.g., 40 sweeps at 10, then 40 at 20) before increasing, and use an Observer to watch for metastability. — [ITensor Discourse, "Ground state energy not always decreasing at each sweep" (Aug 2024)](https://itensor.discourse.group/t/ground-state-energy-not-always-decreasing-at-each-sweep/1950)
- [paper, 2012] Multigrid: optimize at several spatial resolutions so that large-scale features are updated. — [Dolfi et al. 2012](https://arxiv.org/abs/1203.6363)
- [measured, 2021] Seeding DMRG with rigorous-RG (RRG) states removed the "energy-ordering instability" in topological models. — [Block et al. 2021](https://quantumoptics.physics.berkeley.edu/s/2021-Performance-of-the-rigorous-renormalization-group-for-first-order-phase-transitions-and-topolog.pdf)

**Imaginary-time evolution**
- [docs] ITensor recommends imaginary-time evolution before DMRG for stubborn cases. This is folklore with no measurement cited. — [ITensor DMRG FAQ](https://itensor.github.io/ITensors.jl/stable/faq/DMRG.html)
- [theory, 2016] DMRG "is obtained as a special case of imaginary time evolution with infinite time step" in the TDVP framework. — [Haegeman, Lubich, Oseledets, Vandereycken & Verstraete, "Unifying time evolution and optimization with matrix product states," PRB 94, 165116 (2016), arXiv:1408.5056](https://arxiv.org/abs/1408.5056)
- [paper, 2018] VUMPS shows "substantial gains in convergence speed and precision" over iDMRG and iTEBD (imaginary time) for infinite systems. — [Zauner-Stauber, Vanderstraeten, Fishman, Verstraete & Haegeman, PRB 97, 045145 (2018), arXiv:1701.07035](https://arxiv.org/abs/1701.07035)

**Bond-dimension ramps**
- [docs] ITensor examples: `maxdim=[10,20,100,100,200]` (tutorial) and `100,200,400,800,1600` (FAQ). If "maxlinkdim" quickly reaches the cap, raise `maxdim`; if truncation error is consistently above 1e-5, allow larger bond dimension. — [ITensor tutorial](https://github.com/ITensor/ITensorMPS.jl/blob/main/docs/src/tutorials/DMRG.md); [ITensor FAQ](https://itensor.github.io/ITensors.jl/stable/faq/DMRG.html)
- [docs] TeNPy: "Ramp up the maximum bond dimension during simulation, rather than starting at the highest value." `chi_list(chi_max, dchi=20, nsweeps=20)` adds dchi every nsweeps. — [TeNPy protocol](https://raw.githubusercontent.com/tenpy/tenpy/main/doc/intro/dmrg-protocol.rst); [TeNPy dmrg.py](https://raw.githubusercontent.com/tenpy/tenpy/main/tenpy/algorithms/dmrg.py)
- [review, 2014] "To achieve a very accurate MPS quickly, it is also best to start from calculations with relatively small virtual dimension D," then enlarge stepwise. — [Wouters & Van Neck 2014](https://arxiv.org/pdf/1407.2040)
- [review, 2012] With adaptive truncation, "A minimum m is important because the reported truncation error early on in the calculation could be very inaccurate." — [Stoudenmire & White 2012](https://arxiv.org/pdf/1105.1374)

**Eigensolver tolerance and initial-guess schedules**
- [docs] ITensor defaults: `eigsolve_krylovdim=3`, `eigsolve_maxiter=1`, `eigsolve_tol=1e-14`. So each local problem is solved only approximately per visit, and the docs suggest raising krylovdim when convergence is slow or near a critical point. — [ITensorMPS DMRG docs](https://itensor.github.io/ITensorMPS.jl/stable/DMRG.html)
- [docs] block2: Davidson threshold 1e-4 in early sweeps, tightening to 1e-6. — [block2 docs](https://block2.readthedocs.io/en/stable/user/basic.html)
- [docs] TeNPy ties the Lanczos tolerance to truncation: `P_tol_to_trunc=0.05`, `P_tol_max=1e-4`. Convergence defaults are `max_E_err=1e-8` and `max_S_err=1e-5`. — [TeNPy dmrg.py](https://raw.githubusercontent.com/tenpy/tenpy/main/tenpy/algorithms/dmrg.py)
- [review, 2011] Because the eigensolver dominates cost, "it is highly desirable to have a good prediction for a starting vector." The previous result is transformed to the shifted block configuration ("state prediction," White 1996, PRL 77, 3633 [memory]). — [Schollwöck 2011](https://homepages.physik.uni-muenchen.de/~Schollwoeck/annals.pdf)
- [paper, 2008] McCulloch's improved wavefunction transformation for iDMRG is "much more effective than previous versions" and gives "much faster convergence" than iTEBD. — [McCulloch, "Infinite size density matrix renormalization group, revisited," arXiv:0804.2509 (2008)](https://arxiv.org/abs/0804.2509)

**Code-by-code summary**

| Code | Recommended start | Mixer / noise | Ramp and schedule | Source |
|---|---|---|---|---|
| ITensor | random_mps with modest linkdims (10 in tutorial), or a physically motivated state; warm start from simpler H; imaginary-time evolution for hard cases | Noise is "most important" fix; decrease to ~0 | maxdim ramp; Krylov dim 3 / 1 restart default | [FAQ](https://itensor.github.io/ITensors.jl/stable/faq/DMRG.html), [tutorial](https://github.com/ITensor/ITensorMPS.jl/blob/main/docs/src/tutorials/DMRG.md) |
| TeNPy | Usually a product state (the docstrings discuss product-state starts) | Mixer needed initially; SubspaceExpansion default for single-site; amplitude 1e-5, decay 2, off after 15 sweeps | chi_list ramp; min_sweeps; check E and S errors | [dmrg.py](https://raw.githubusercontent.com/tenpy/tenpy/main/tenpy/algorithms/dmrg.py), [protocol](https://raw.githubusercontent.com/tenpy/tenpy/main/doc/intro/dmrg-protocol.rst) |
| block2 | Not described on the basic page | Noise 1e-3 → 0 in default schedule | Two-site then one-site; Davidson tolerance 1e-4 → 1e-6; reverse schedule to check for local minima | [block2 docs](https://block2.readthedocs.io/en/stable/user/basic.html) |
| CheMPS2 / QC-DMRG | HF-based plus noise, D spread equally over sectors plus noise, or CI-DEAS | Noise or perturbation reintroduces lost sectors | Small D first, then enlarge | [Wouters & Van Neck 2014](https://arxiv.org/pdf/1407.2040), [Keller & Reiher 2014](https://arxiv.org/pdf/1401.5497) |
| SyTen, Block | Not verified in this session (see Gaps) | DMRG3S is by Hubig (SyTen author) | — | [Hubig 2015](https://arxiv.org/abs/1501.05504) |

### Inferences
- **Two philosophies in the codes.** "Unbiased random" starts aim to avoid preferring any candidate order. "Physically informed" starts (Néel, HF, pinned, Gaussian, CI-DEAS) save sweeps but risk bias. A NN initializer is the physically-informed philosophy taken to its limit, so it inherits the bias risk. Stoudenmire & White's test is the countermeasure: if DMRG restores a symmetry the start broke, that ordering scenario is disfavored.
- **Loose eigensolver tolerances early** (ITensor: Krylov dim 3, 1 restart; block2: 1e-4) only make sense because the environment is poor in early sweeps. A good initial state makes environments accurate from sweep 1, so tight tolerances can start sooner. This hidden saving is not captured by "number of sweeps."

### Gaps
- I did not retrieve SyTen, Block (StackBlock) or CheMPS2 documentation on initialization. The CheMPS2 view comes from Wouters & Van Neck's review. The TeNPy rendered docs and the "Why you need the Mixer" notebook could not be fetched; the TeNPy facts come from source docstrings and the raw protocol .rst.
- I found no measured comparison of random MPS bond dimensions (e.g., linkdims 1 vs 10 vs 100) as starting points.
- I found no measured study of imaginary-time-evolution pre-conditioning versus direct DMRG.

---

## Q4. Theory: optimization landscape, hardness, and convergence guarantees

### Takeaway
1. **Worst case is hard.** Global optimization over several sites, and finding MPS ground states even when an exact MPS ground state with a polynomial gap exists, are NP-hard or factoring-hard (2006, 2008). No initializer can remove worst-case difficulty.
2. **Gapped 1D is efficient.** It admits provably polynomial algorithms that do not depend on an initial state (LVV 2015; Arad et al. 2017). These are non-variational and much slower in practice than DMRG.
3. **Local convergence only.** ALS/DMRG theory gives local (linear-rate) convergence near a non-degenerate solution of fixed rank. Global convergence of DMRG is "not well understood" (2014).
4. **No barren plateaus.** Energy landscapes of isometric MPS, TTNS and MERA have no exponentially vanishing gradients (2023–2025). Gradient-based MPS optimization from random starts is trainable, unlike deep circuits or global-loss tensor-network ML (2022).

So initial-state quality matters through local basins and constant factors, not through flat landscapes.

### Cited Findings

**Hardness**
- [theorem, 2006] Optimizing an MPS globally over several sites, instead of DMRG's local updates, is NP-hard in the worst case and "hard even in approximation" (reduction from binary quadratic programming). DMRG's local optimization comes with no proof of reaching the global optimum. — [Eisert, "Computational difficulty of global variations in the density matrix renormalization group," PRL 97, 260501 (2006), arXiv:quant-ph/0609051](https://arxiv.org/abs/quant-ph/0609051)
- [theorem, 2008] Schuch, Cirac & Verstraete:
  - There are 1D frustration-free Hamiltonians with a unique MPS ground state and a polynomial gap for which "finding the ground state is at least as hard as factoring."
  - Without uniqueness, finding a ground state solves an NP-complete problem, and even verifying one is not possible.
  - Proving convergence of variational MPS methods (DMRG) needs more than an MPS ground state and a polynomial gap.
  
  Source: [Schuch, Cirac & Verstraete, "The computational difficulty of finding MPS ground states," PRL 100, 250501 (2008), arXiv:0802.3351](https://arxiv.org/abs/0802.3351)
- [memory] The prompt's "Computational complexity of PEPS" is a different paper about PEPS contraction (#P-hardness), not the 2008 MPS ground-state result: Schuch, Wolf, Verstraete & Cirac, PRL 98, 140506 (2007), [arXiv:quant-ph/0611050](https://arxiv.org/abs/quant-ph/0611050). Also, 1D local Hamiltonian problems with 1/poly gaps are QMA-complete: Aharonov, Gottesman, Irani & Kempe, CMP 287, 41 (2009), [arXiv:0705.4077](https://arxiv.org/abs/0705.4077).

**Provably efficient algorithms (gapped 1D)**
- [theorem, 2013/2015] LVV give "the first randomized polynomial-time algorithm for finding ground states of gapped one-dimensional Hamiltonians." The output is an MPS of polynomial bond dimension. — [Landau, Vazirani & Vidick, arXiv:1307.5143; Nature Phys. 11, 566 (2015) [journal ref memory]](https://arxiv.org/abs/1307.5143)
- [theorem, 2017] Arad, Landau, Vazirani & Vidick:
  - polynomial-time algorithm for poly(n)-degenerate gapped ground spaces
  - n^{O(log n)} algorithm for the poly(n) lowest-energy states, under a density condition
  - O(n M(n)) time for frustration-free unique ground states
  
  Source: [Arad et al., ITCS 2017, LIPIcs 67:46, DOI 10.4230/LIPIcs.ITCS.2017.46; arXiv:1602.08828; CMP 356, 65 (2017) [memory]](https://drops.dagstuhl.de/opus/volltexte/2017/8192)
- [measured, 2017] The RRG implementation performs similarly to DMRG for gapped, non-degenerate systems. For criticality, large degeneracy and long-range entanglement, it still finds candidate states with large overlap with low-energy eigenstates and outperforms DMRG in some cases. It is non-variational. — [Roberts, Vidick & Motrunich, PRB 96, 214203 (2017), arXiv:1703.01994](https://arxiv.org/abs/1703.01994)
- [measured, 2021] RRG costs far more than DMRG: 13.5×10³ s vs 24 s (tricritical Ising, N=32, D=8). RRG variances are 10⁻⁶–10⁻² vs about 10⁻¹⁰ for DMRG. — [Block et al. 2021](https://quantumoptics.physics.berkeley.edu/s/2021-Performance-of-the-rigorous-renormalization-group-for-first-order-phase-transitions-and-topolog.pdf)

**ALS / tensor-train convergence theory**
- [paper, 2012] Holtz, Rohwedder & Schneider generalize ALS to the TT format and introduce MALS (modified ALS), which adapts ranks dynamically. MALS corresponds to two-site DMRG [memory: equivalence is stated in the paper body]. Structural properties carry over to micro-iterations through retractions. Numerical experiments show that high TT ranks are sometimes needed even for low-rank targets. — [Holtz, Rohwedder & Schneider, "The alternating linear scheme for tensor optimization in the tensor train format," SIAM J. Sci. Comput. 34(2), A683–A713 (2012), DOI 10.1137/100818893](https://epubs.siam.org/doi/10.1137/100818893)
- [theorem, 2013; content from memory, abstract not fetched] Rohwedder & Uschmajew prove *local* linear convergence of ALS (and, under conditions, of MALS/DMRG) for strongly convex problems in TT format. This includes the Rayleigh-quotient eigenproblem near a non-degenerate solution of full TT rank. The method is viewed as nonlinear block Gauss–Seidel on a quotient manifold. Global convergence is not established. — [Rohwedder & Uschmajew, "On local convergence of alternating schemes for optimization of convex problems in the tensor train format," SIAM J. Numer. Anal. 51(2), 1134–1162 (2013), DOI 10.1137/110857520](https://opus.bibliothek.uni-augsburg.de/opus4/frontdoor/index/index/docId/103361)
- [paper, 2017–2019] Oseledets, Rakhuba & Uschmajew recast ALS as sequential optimization on moving subspaces. Local convergence conditions reduce to contractivity of multiplicative Schwarz methods and to the curvature of low-rank manifolds. Verifying these conditions in concrete scenarios is "open in most cases." — [Oseledets, Rakhuba & Uschmajew, "Alternating least squares as moving subspace correction," arXiv:1709.07286; SIAM J. Numer. Anal. 56, 3459 (2018) [memory]](https://arxiv.org/abs/1709.07286)
- [paper, 2021/22] The same authors analyze the local convergence of overrelaxed (SOR-type) alternating low-rank optimization. — [Oseledets, Rakhuba & Uschmajew, arXiv:2111.14758](https://arxiv.org/abs/2111.14758)
- [paper, 2014] Kressner et al. write: "The global and local convergence properties of the DMRG algorithm are not well understood." — [Kressner, Steinlechner & Uschmajew 2014](https://www.epfl.ch/labs/mathicse/wp-content/uploads/2018/10/40.2014NEW_DK-MS-AU.pdf)
- [paper, 2025] A parallel DMRG variant pairs independent local minimizations with a global coarse-space correction (additive Schwarz). It shows "competitive convergence rates" on molecular systems, which points to domain-decomposition theory as a new analysis route. — [Grigori & Hassan, "An additive two-level parallel variant of the DMRG algorithm with coarse-space correction," arXiv:2505.23429 (2025)](https://arxiv.org/abs/2505.23429)

**Landscape and barren plateaus**
- [theorem, 2023/2025] Barthel & Miao, for Haar-random isometric tensor networks:
  - **MPS, single-site terms:** gradient variance decays with distance |i−j| as η^{|i−j|}, with η=(1−1/m²)/(d−1/(m²d)).
  - **MPS, extensive nearest-neighbor Hamiltonians:** the variance converges to a size-independent value that scales as 1/(m²d⁴) for large m (exact prefactor in their Theorem 4, which involves Tr h² and partial traces of h). So it scales as 1/m² and does not decay with L.
  - **MERA:** variance falls with layer depth τ, not with L.
  - **Conclusion:** "free of barren plateaus." The results "motivate certain initialization schemes"; the only concrete one is ramping MERA bond dimension in early layers.
  
  Sources: [Barthel & Miao, CMP (2025), arXiv:2304.00161](https://arxiv.org/pdf/2304.00161v4); companion: [Miao & Barthel, "Isometric tensor network optimization for extensive Hamiltonians is free of barren plateaus," PRA 109, L050402 (2024), arXiv:2304.14320](https://arxiv.org/abs/2304.14320)
- [theorem, 2021/2022] In MPS-based machine learning, barren plateaus "prevail" for global loss functions but are absent for local losses. — [Liu, Yu, Duan & Deng, "Presence and absence of barren plateaus in tensor-network based machine learning," PRL 129, 270501 (2022), arXiv:2108.08312](https://arxiv.org/abs/2108.08312)
- [theorem, 2023] For quantum-circuit versions of tensor networks with local Hamiltonians:
  - Gradient variance decays exponentially with the distance of a Hamiltonian term from the canonical center.
  - For qMPS, most gradient variances decay exponentially in qubit number; for qTTN and qMERA they decay polynomially.
  - Computing these gradients classically is exponentially more efficient than on a quantum device.
  
  Source: [Cervero Martín, Plekhanov & Lubasch, "Barren plateaus in quantum tensor network optimization," Quantum 7, 974 (2023), arXiv:2209.00292](https://arxiv.org/abs/2209.00292)
- [paper, 2023] The "Garcia, Zhao, … Jaffe" work the prompt mentions is about learning scramblers with quantum neural networks under local costs, not classical MPS/DMRG. — [Garcia, Zhao, Bu & Jaffe, "Barren plateaus from learning scramblers with local cost functions," JHEP 01 (2023) 090, arXiv:2205.06679](https://arxiv.org/abs/2205.06679)

**DMRG as an optimizer**
- [theory, 2016] DMRG is imaginary-time TDVP with infinite time step. In that sense it is a projected (Riemannian) flow on the MPS manifold, so its fixed points are stationary points of the energy on that manifold. — [Haegeman et al. 2016](https://arxiv.org/abs/1408.5056)

### Inferences
- **Hardness bounds the promise.** A NN cannot guarantee better-than-DMRG outcomes on worst-case instances: the instances are NP- or factoring-hard, and for the non-unique case even verification fails. Claims should be framed for physically natural families.
- **For gapped 1D, the payoff is a constant factor.** Polynomial-time algorithms exist and DMRG works well in practice. The benefit is fewer sweeps and lower intermediate bond dimension, not changed outcomes.
- **Local theory rewards starting in the basin.** Local-convergence theory (linear rate near a non-degenerate, full-rank solution) means a start inside the right basin gives asymptotically linear convergence. The number of sweeps then scales like log(initial error / tolerance) divided by the contraction rate. Cutting initial error by a factor ε saves roughly log(1/ε)/|log ρ| sweeps, where ρ is the local rate. This is my extrapolation from the general theory, not a published DMRG-specific bound.
- **Basins, not plateaus.** The no-barren-plateau results suggest that random starts fail because of discrete basin structure (orders, sectors, degeneracies), not vanishing gradients. NN initialization is therefore most valuable where basins compete, as in Q1's second group.
- **Loss choice for training.** For a NN that outputs MPS tensors and is trained end-to-end, Liu et al. (2022) suggest preferring local losses (energy of local terms) over global fidelity losses, to avoid barren plateaus in training. This is an inference from the ML setting.

### Gaps
- There is no proved global convergence theorem for DMRG, and no landscape result counting or characterizing local minima of the fixed-bond-dimension MPS energy for physical Hamiltonians.
- I found no paper on "entanglement and tensor network barren plateaus" authored by Eisert. Eisert's relevant contribution is the 2006 NP-hardness result.
- The Rohwedder & Uschmajew abstract could not be read in this session (rate limit, proxy block, robots).

---

## Q5. How gap, entanglement, correlation length and long-range couplings affect sweeps and sensitivity

### Takeaway
The required bond dimension grows with entanglement:
- an area law for gapped 1D
- logarithmic growth plus finite-entanglement scaling at criticality
- exponential growth with cylinder width in 2D

Convergence slows when:
- the gap or correlation length makes the local eigenproblems and large-scale features hard to resolve
- Hamiltonian bonds are long-range along the MPS path (2D snakes, quantum-chemistry orbitals)
- there are several length scales

I found no published closed-form "sweeps vs gap" law. The evidence is qualitative and from case studies.

### Cited Findings

**Width, path and boundaries in 2D**
- [review, 2012] "The number of states kept must be increased exponentially with the width of the system" to hold accuracy constant. Fully periodic boundaries "require m² states" for the same accuracy as open or cylindrical boundaries. — [Stoudenmire & White 2012](https://arxiv.org/pdf/1105.1374)
- [review, 2012] Long-range bonds along the 1D path (about width W apart) have "trouble getting started." The choice of path matters, and reproducing "the same ground state with different DMRG paths" is evidence against metastability. — [Stoudenmire & White 2012](https://arxiv.org/pdf/1105.1374)
- [measured, 2005] Periodic chains (long-range bond along the path) stick more than open chains, for both uncorrected methods. — [White 2005](https://arxiv.org/pdf/cond-mat/0508709)

**Criticality and gaplessness**
- [theory, 2009] Finite-entanglement scaling: at 1D critical points, finite bond dimension acts like a finite length scale governed by the central charge. [memory] The known form is ξ_χ ∝ χ^κ with κ = 6/[c(√(12/c)+1)]. — [Pollmann, Mukerjee, Turner & Moore, "Theory of finite-entanglement scaling at one-dimensional quantum critical points," PRL 102, 255701 (2009), arXiv:0812.2903](https://arxiv.org/abs/0812.2903)
- [docs] ITensor suggests a larger Krylov dimension "if convergence is slow or the Hamiltonian is near a critical point." — [ITensorMPS DMRG docs](https://itensor.github.io/ITensorMPS.jl/stable/DMRG.html)
- [forum, 2024–2026] Stoudenmire (Aug 2024): if the system is gapless with many low-lying excitations, DMRG may converge slowly. Fishman (Feb 2026): "gapless systems will generally converge slower." — [ITensor Discourse 2024](https://itensor.discourse.group/t/ground-state-energy-not-always-decreasing-at-each-sweep/1950); [ITensor Discourse 2026](https://itensor.discourse.group/t/slow-convergence-of-spin-1-af-heisenberg-chain/2579)
- [docs] TeNPy: critical states can cause convergence problems, and low-effort tests should "target a non-critical region of phase space." — [TeNPy protocol](https://raw.githubusercontent.com/tenpy/tenpy/main/doc/intro/dmrg-protocol.rst)

**Multiple length scales and first-order or degenerate regimes**
- [paper, 2012] DMRG fails to converge with multiple length scales (continuum discretizations, dilute or weakly doped systems). — [Dolfi et al. 2012](https://arxiv.org/abs/1203.6363)
- [measured, 2021] Near first-order transitions and in degenerate topological phases, DMRG outcomes depend strongly on initialization (see Q1). — [Block et al. 2021](https://quantumoptics.physics.berkeley.edu/s/2021-Performance-of-the-rigorous-renormalization-group-for-first-order-phase-transitions-and-topolog.pdf)

**Quantum chemistry (long-range orbital couplings)**
- [review, 2014] "The orbital choice and their ordering ... also influence the convergence rate with D." The starting guess is estimated to matter about an order of magnitude less than orbital choice and ordering. — [Wouters & Van Neck 2014](https://arxiv.org/pdf/1407.2040)
- [review, 2014] There is "no obvious or simple relation" between ordering and convergence. Guess and ordering are interdependent: HF guesses suit energetic ordering, while CI-DEAS suits mutual-information ordering. — [Keller & Reiher 2014](https://arxiv.org/pdf/1401.5497)

**Area law, background (memory)**
- Gapped 1D ground states obey an area law and are efficiently approximable by MPS: Hastings, J. Stat. Mech. P08024 (2007), [arXiv:0705.2024](https://arxiv.org/abs/0705.2024); Verstraete & Cirac, PRB 73, 094423 (2006), [arXiv:cond-mat/0505140](https://arxiv.org/abs/cond-mat/0505140).

### Inferences
- **Mechanistically**, one sweep propagates information across the system once. A start lacking correlations at length scale ξ needs several sweeps, roughly proportional to how many "relaxation passes" the local updates need to build those correlations. Long-range path bonds (width W in 2D) and critical correlations are exactly where local updates are weakest (Dolfi; Stoudenmire–White). This is where a pre-correlated start should save the most sweeps. This is an inference; no paper quantifies sweeps vs ξ.
- **Ordering inside the NN.** In quantum chemistry, ordering and orbital choice matter more than the starting guess (Wouters & Van Neck). Any NN initializer for molecules should be evaluated at a fixed, good ordering, or should predict ordering too.
- **Critical systems.** A start at too small χ cannot hold the critical correlations, so the start's value is bounded by finite-entanglement scaling. The useful target is a start at moderate χ with the right short-distance structure plus a ramp.

### Gaps
- No quantitative formula or systematic study was found linking the number of sweeps to gap, correlation length or cylinder width at fixed initial-state quality.
- No study was found that directly compares sensitivity to the start for 2D snakes vs alternative paths beyond qualitative remarks.

---

## Q6. Convergence diagnostics used to detect a bad start or a stuck run

### Takeaway
Practitioners combine several checks; there is "no automatic or bulletproof check":
- energy variance (necessary for an eigenstate, but not sufficient for the ground state)
- extrapolation in truncation error (linear behavior; plateaus followed by sudden drops indicate sticking)
- reproducibility across different starts, seeds, paths, pinnings and reverse schedules
- non-monotonic energy or entropy
- symmetry restoration
- comparison with exact diagonalization on small systems
- entanglement-entropy saturation, which lags the energy

### Cited Findings

**Energy variance**
- [docs] Compute `var = H2 - E^2`. A low variance indicates an eigenstate, but "does not ensure that psi is the ground state." "there is no automatic or bulletproof check for DMRG convergence"; check many observables and symmetries (e.g., reflection), and compare with exact diagonalization on small systems. — [ITensor DMRG FAQ](https://itensor.github.io/ITensors.jl/stable/faq/DMRG.html)
- [paper, 2018] A cheap approximation of the full variance (about two ⟨H⟩ evaluations plus a parallel part like one two-site operator application) extrapolates "on-par" with two-site truncation error or full variance. — [Hubig, Haegeman & Schollwöck, "Error estimates for extrapolations with matrix-product states," PRB 97, 045125 (2018), arXiv:1711.01104](https://arxiv.org/abs/1711.01104)
- [paper, 2008] MPOs can compute the exact energy variance in iDMRG. — [McCulloch 2008](https://arxiv.org/abs/0804.2509)

**Truncation-error extrapolation**
- [docs] "A strong deviation from a linear function" (for example, a plateau followed by a sudden energy drop) "indicates that the DMRG was stuck in a local minimum." Use two-site DMRG for extrapolation, and a reverse schedule to make sure energies at each bond dimension are "not representing any local minima." — [block2 docs](https://block2.readthedocs.io/en/stable/user/basic.html)
- [paper, 2005] With very small noise, the apparent truncation error "goes to zero and is unrelated to the exact truncation error." Use larger noise (a=1e-2) for extrapolation runs. Extrapolation typically gives about an order-of-magnitude improvement, and linearity must be checked. — [White 2005](https://arxiv.org/pdf/cond-mat/0508709)
- [review, 2014] Energy-based criteria can mislead because energy error is quadratic in wavefunction error. Energies do not decrease monotonically within micro-iterations. — [Wouters & Van Neck 2014](https://arxiv.org/pdf/1407.2040)

**Comparing different starts**
- [measured, 2011] Energies from different prepared starts were compared, e.g., HVBC-pinned vs random, and the lower one taken; leftover "localized defects" were noted. — [Yan, Huse & White 2011](https://arxiv.org/pdf/1011.6114)
- [review, 2012] "If DMRG restores a symmetry explicitly broken by the initial state, one has strong evidence against that particular ordering scenario." Agreement across different DMRG paths is also evidence. — [Stoudenmire & White 2012](https://arxiv.org/pdf/1105.1374)

**Run-time symptoms**
- [docs] Watch for non-monotonic energy or entropy, stopping at max sweeps, and wild sensitivity to small parameter or bond-dimension changes. `min_sweeps` guards against "premature convergence." — [TeNPy protocol](https://raw.githubusercontent.com/tenpy/tenpy/main/doc/intro/dmrg-protocol.rst)
- [forum, 2026] Entanglement entropy "converges much more slowly than the ground-state energy." — [ITensor Discourse 2026](https://itensor.discourse.group/t/slow-convergence-of-spin-1-af-heisenberg-chain/2579)

**Entanglement-based checks**
- [measured, 2012] Topological entanglement entropy and its dependence on m distinguish MES from definite-parity eigenstates. This is an entanglement-based check of which sector DMRG landed in. — [Jiang, Wang & Balents 2012](https://arxiv.org/pdf/1205.4289)

### Inferences
- **Benchmark protocol for a NN initializer:**
  - report variance and truncation-extrapolated energy, not just energy after k sweeps
  - verify that NN-initialized and random-initialized runs extrapolate to the same value, or explain why not
  - test symmetry restoration when the NN start breaks a symmetry
- **"Converged" by energy is not enough**, because entropy and long-range correlators lag. Time-to-solution should be defined with an observable-aware criterion, such as energy plus entropy plus the target correlator.

### Gaps
- No primary source was found that formalizes entanglement-spectrum degeneracy checks (e.g., for SPT phases) as a convergence diagnostic for DMRG specifically. The idea is common in practice but undocumented in what I retrieved.
- No formal guidance was found on how many random seeds to run.

---

## Q7. Quantitative studies of time-to-solution or sweeps vs initial-state quality

### Takeaway
Direct, controlled studies of sweeps or time versus initial-state overlap or energy are essentially absent. The measured evidence consists of:
- head-to-head algorithm benchmarks from a fixed start (White 2005; Hubig 2015)
- initial-guess comparisons in quantum chemistry (HF vs CI-DEAS, Keller & Reiher 2014; DEAS, Legeza 2003)
- seeding experiments (RRG seeds into DMRG, Block 2021)
- metastability case studies (Yan, Huse & White 2011)
- forum anecdotes

### Cited Findings
- [measured, 2014] **F2 molecule**, CAS(14,32), m=1024:

  | | HF-based guess | CI-DEAS |
  |---|---|---|
  | After sweep 1 | −198.886421 Eh | −198.962112 Eh |
  | After sweep 20 | −198.970559 Eh | −198.970711 Eh |

  The roughly 0.15 mEh difference persists: "for the moderate choice of m=1024, the converged energies still depend on the initial guess." — [Keller & Reiher 2014](https://arxiv.org/pdf/1401.5497)
- [measured, 2003] DEAS initialization "substantially" speeds convergence; the abstract gives no sweep numbers. — [Legeza & Sólyom 2003](https://arxiv.org/abs/cond-mat/0305336)
- [measured, 2021] **RRG seeds into DMRG.** RRG seeds (D=4, s=8) at N=64 had variances around 0.1. DMRG refinement reduced these to about 10⁻⁴ and removed the energy-ordering instability (missed or excited states) in topological models. — [Block et al. 2021](https://quantumoptics.physics.berkeley.edu/s/2021-Performance-of-the-rigorous-renormalization-group-for-first-order-phase-transitions-and-topolog.pdf)
- [measured, 2015] **Algorithm runtimes from a common start**, as wall times to a fixed energy-change criterion:

  | Method | Heisenberg S=1, PBC, m=200 / 400 / 800 |
  |---|---|
  | DMRG3S | 583 / 1935 / 3990 s |
  | White's correction (CWF) | 1519 / 2695 / 11133 s |
  | Two-site DMRG | 762 / 3181 / 21963 s (higher final energies) |

  Fermi–Hubbard: DMRG3S 3955 s vs two-site DMRG 15596 s at the largest m. — [Hubig et al. 2015](https://arxiv.org/pdf/1501.05504)
- [measured, 2005] On the periodic S=1 chain, uncorrected runs "stall for several sweeps before the missing link enters the basis." The corrected run never stalls. — [White 2005](https://arxiv.org/pdf/cond-mat/0508709)
- [measured, 2011] **Kagome:**
  - The HVBC start remained metastable to m≈2400 with biased ordering, versus melting within a few sweeps at m<200 with standard ordering.
  - The random start overtook it in energy near m≈2000 on YC12.
  
  So a wrong-but-plausible start can cost a large part of the total compute budget. — [Yan, Huse & White 2011](https://arxiv.org/pdf/1011.6114)
- [forum, 2023] 2D Hubbard from a random QN product state: ">300 sweeps and still not close to convergence." The Gaussian-MPS start was worse. — [ITensor Discourse 2023](https://itensor.discourse.group/t/initial-state-calculation-on-2d-dmrg-with-gaussian-mps/755)
- [forum, 2026] Spin-1 chain, N=48: entropy convergence took about 150 sweeps vs about 30 typical. The fix was eigensolver Krylov dimension 3→5 (an eigensolver issue, not the initial state). — [ITensor Discourse 2026](https://itensor.discourse.group/t/slow-convergence-of-spin-1-af-heisenberg-chain/2579)
- [forum, 2023] A TeNPy user workflow restarts DMRG with χ multiplied by 1.5–2 each run, using the previous MPS as the start. For finite DMRG, a non-canonical start "doesn't really matter, as it effectively brings the MPS to canonical form in the first sweep." For iDMRG, a badly prepared start "might never be able to recover." — [TeNPy Forum, "Non-canonical MPS as an initial guess for DMRG" (May 2023)](https://forum.tenpy.org/viewtopic.php?p=1135)
- [related ML, 2025] **Not an initializer.** A graph-NN predicts the correction from low-bond-dimension quantum-chemistry DMRG energies to the high-bond-dimension limit. Features are orbital entropies, mutual information, DFT occupancies and truncation error. Results are within 1 mHa at M=750–1250, with correct state ordering for peripentacene at M=500, where plain DMRG fails at low M. — [Golub, Yang, Vlček & Veis, "Quantum chemical DMRG method boosted by machine learning," J. Phys. Chem. Lett. (2025), DOI 10.1021/acs.jpclett.5c00207, arXiv:2412.07607](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973911)

### Inferences
- Across the available data, a better start mostly helps in three ways:
  1. a lower first-sweep energy (HF vs CI-DEAS differ by about 76 mEh after sweep 1)
  2. a lower final energy at *fixed moderate* bond dimension (about 0.15 mEh), meaning the final MPS at fixed m depends on the start
  3. avoiding very long metastable episodes (kagome, first-order and topological cases)
  
  Runtime ratios between enrichment algorithms (2–6×) are comparable to or larger than the documented initial-guess gains. A NN initializer should therefore be benchmarked on top of the best algorithm (CBE or DMRG3S), not against plain two-site DMRG.
- The ML literature I found around DMRG targets energy correction and extrapolation, not initialization. Initialization appears to be an open niche.

### Gaps
- No study was found that plots sweeps-to-tolerance or wall time against initial-state fidelity or initial energy across many initial states for one Hamiltonian. This is the key missing experiment for the project.
- The DEAS and multigrid papers report gains qualitatively in their abstracts; I did not retrieve their quantitative tables.

---

## Open questions and gaps

1. **Dose-response curve.** No published curve of DMRG sweeps or time-to-tolerance vs initial-state fidelity |⟨ψ₀|ψ_GS⟩|² or energy error. It is unknown whether the dependence is logarithmic (as the local linear-convergence theory suggests) or has thresholds (basin boundaries).
2. **Global landscape.** No theorem characterizes local minima of the fixed-m MPS energy for physical Hamiltonians. Existing results are worst-case hardness (2006, 2008), local convergence (2013–2019) and gradient-variance scaling (2023–2025).
3. **Enrichment vs a good start.** Unmeasured: how much noise, subspace expansion or CBE degrades or preserves a high-quality start, and the optimal noise schedule given a good start.
4. **Sensitivity by algorithm.** No head-to-head study of seed-to-seed variance of outcomes for two-site DMRG, DMRG3S, CBE and VUMPS.
5. **Sweeps vs physics.** No quantitative law relating sweeps to gap, correlation length, cylinder width or interaction range.
6. **Degenerate manifolds.** Open how DMRG's low-entanglement bias (MES and cat collapse) interacts with a supplied symmetric or superposed start. Which ground state DMRG ends in may depend on both the start and m (Jiang–Wang–Balents 2012).
7. **Code documentation not retrieved:** SyTen, StackBlock/Block and CheMPS2 docs, and the TeNPy mixer notebook (fetch failures). The CheMPS2 view comes from the Wouters–Van Neck review.
8. **Not found as stated in the prompt:** an Eisert-authored "tensor-network barren plateaus" paper. Also, the "Garcia, Zhao, Jaffe" paper concerns scramblers and quantum neural networks, not MPS energy landscapes.
9. **Imaginary-time evolution as preconditioner:** only documentation folklore; no measured benefit found.

---

## Implications for a neural-network-generated initial state

What a better start can buy, by mechanism, and how to test it:

| Mechanism (source) | What a better start buys | Conditions and caveats | Suggested metric |
|---|---|---|---|
| Frozen QN sectors and bond basis in single-site DMRG ([White 2005](https://arxiv.org/abs/cond-mat/0508709); [Hubig 2015](https://arxiv.org/abs/1501.05504); [CBE 2023](https://arxiv.org/abs/2207.14712)) | Correct total QN and a correct bond-QN distribution let pure single-site DMRG (about 2–4× cheaper per sweep) work without noise | Must output a symmetric MPS with the right sector content on *every* bond, not just total charge | Final energy and variance of noise-free single-site DMRG vs two-site DMRG with noise |
| Slow long-range and large-scale correlation build-up ([Stoudenmire & White 2012](https://arxiv.org/abs/1105.1374); [Dolfi 2012](https://arxiv.org/abs/1203.6363)) | Fewer sweeps, especially for 2D cylinders, periodic boundaries, dilute or doped systems, continuum limits | Gains concentrate where local updates are weakest; little gain for short-ξ gapped chains | Sweeps-to-tolerance for energy, entropy and the longest-range correlator |
| Metastable competing orders, first-order transitions, degenerate or topological manifolds ([Yan, Huse & White 2011](https://arxiv.org/abs/1011.6114); [Block 2021](https://quantumoptics.physics.berkeley.edu/s/2021-Performance-of-the-rigorous-renormalization-group-for-first-order-phase-transitions-and-topolog.pdf); [Zheng 2017](https://authors.library.caltech.edu/records/45z9g-a3558/preview/aan7127_Zheng_SM.pdf)) | Lands in the correct basin and avoids metastable episodes that can last to m≈2000+ | Largest upside and largest risk: a confidently wrong NN start biases the result, and DMRG may never leave it | Success probability over Hamiltonian instances; compare with ≥ several random seeds; symmetry-restoration test ([Stoudenmire & White 2012](https://arxiv.org/abs/1105.1374)) |
| Excited-state and multi-root searches ([Block 2021](https://quantumoptics.physics.berkeley.edu/s/2021-Performance-of-the-rigorous-renormalization-group-for-first-order-phase-transitions-and-topolog.pdf)) | Supplying the full low-energy manifold (as RRG seeds do) removes energy-ordering failures from orthogonalization | Requires generating several mutually near-orthogonal states | Fraction of the true low-lying spectrum recovered in order |
| Bond-dimension ramp and eigensolver schedule ([ITensor](https://itensor.github.io/ITensorMPS.jl/stable/DMRG.html); [TeNPy](https://raw.githubusercontent.com/tenpy/tenpy/main/tenpy/algorithms/dmrg.py); [block2](https://block2.readthedocs.io/en/stable/user/basic.html)) | Shorter low-m warm-up phase, earlier tight Davidson/Lanczos tolerances, fewer wasted sweeps at small m | Savings capped by the cost of the final high-m sweeps, which dominate; also count the NN inference and MPS compression time | Wall time to fixed variance, including NN cost |
| Final energy at fixed moderate m depends on the start ([Keller & Reiher 2014](https://arxiv.org/abs/1401.5497)) | Better energy at a given m, i.e., a smaller m needed for target accuracy | Quantum-chemistry evidence; orbital ordering matters more than the guess ([Wouters & Van Neck 2014](https://arxiv.org/abs/1407.2040)) | Energy vs m curves for NN vs CI-DEAS/HF vs random starts at a fixed ordering |

**Design and benchmark recommendations** (inferences drawn from the cited findings):
1. **Baselines.** At minimum: random MPS (e.g., linkdims ≈ 10, QN-correct), a physically motivated product state (Néel or HF), and a warm start from a neighboring Hamiltonian (ITensor and Stoudenmire advice). Where relevant, also CI-DEAS (quantum chemistry), Gaussian MPS (quasi-1D fermions), pinned states (2D order) and RRG or multigrid seeds.
2. **Algorithms.** Benchmark on top of CBE or DMRG3S as well as two-site DMRG with noise. Enrichment reduces the representational benefit of a good start, and algorithm choice alone gives 2–6× ([Hubig 2015](https://arxiv.org/abs/1501.05504)).
3. **Noise schedule.** Report results with the default noise or mixer schedule *and* with reduced or zero noise. Default noise (1e-3 in block2) may scramble a good start.
4. **Convergence criteria.** Define convergence by variance plus extrapolated energy plus entropy or long-range correlator, not energy alone ([ITensor FAQ](https://itensor.github.io/ITensors.jl/stable/faq/DMRG.html); [block2](https://block2.readthedocs.io/en/stable/user/basic.html); [Wouters & Van Neck 2014](https://arxiv.org/abs/1407.2040)). Check that NN-started and random-started runs agree after extrapolation.
5. **Training loss.** If the NN outputs MPS tensors trained through an energy loss, prefer local (sum-of-local-terms) objectives. Global fidelity losses on MPS can show barren plateaus ([Liu et al. 2022](https://arxiv.org/abs/2108.08312)). Isometric MPS energy landscapes have gradient variance about 1/m², independent of L ([Barthel & Miao 2025](https://arxiv.org/abs/2304.00161)), so moderate starting m keeps gradients healthy.
6. **Expectations by regime.** In gapped 1D, expect constant-factor savings only: provably polynomial algorithms exist, and DMRG already converges quickly ([LVV 2015](https://arxiv.org/abs/1307.5143)). Expect the largest payoffs in 2D, frustrated, first-order, degenerate and topological, multi-scale, and long-range quantum-chemistry regimes. These are the same regimes where a wrong start is most costly, so calibrated uncertainty, or offering several candidate starts, may be worth building in.
7. **No worst-case guarantees.** Do not claim them: finding MPS ground states is NP-hard or factoring-hard in the worst case, even with a polynomial gap ([Schuch, Cirac & Verstraete 2008](https://arxiv.org/abs/0802.3351); [Eisert 2006](https://arxiv.org/abs/quant-ph/0609051)).
