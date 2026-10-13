# Physics-informed (non-ML) DMRG initial states and warm starts: methods and measured gains

Scope: every non-neural "smart" way to start DMRG (or its infinite/variational variants), with quantitative evidence where it exists. Research date: 2026-10-13. Each claim carries the year of its source. A "†" after a journal reference means the arXiv record was checked during this research but the journal volume/page comes from memory and was not re-checked. Treat those references accordingly.

---

## 1. Gaussian / mean-field states (Slater determinants, BCS/Bogoliubov, HFB) converted to MPS and used as DMRG starting points

### Takeaway
Exact or near-exact algorithms for turning fermionic Gaussian states into MPS have existed since 2015 (Fishman-White GMPS), and the construction is cheap: O(N) gates, about 90 s on a laptop for a gapless N≈1000 chain. However, the foundational papers propose DMRG initialization without benchmarking it. The only head-to-head numbers I found for *unprojected* Gaussian starts are toy-scale (1D, ~6 sweeps → 1 sweep). There is also a documented case where a GMPS start was *worse* than random for a 2D Hubbard model. The large measured gains come from Gutzwiller-*projected* Gaussian states (Section 2).

### Cited Findings
- **Fishman & White (2015), "Compression of correlation matrices and an efficient method for forming matrix product states of fermionic Gaussian states," Phys. Rev. B 92, 075132.** The correlation matrix is compressed into O(B·N) local Givens-rotation gates with block size B. Bond dimension χ = 2^(B−1) before truncation. A "GDMRG" variant finds the gates directly from a hopping Hamiltonian at O(B³N) cost versus O(N³) for full diagonalization. — [arXiv:1504.07701](https://arxiv.org/abs/1504.07701); [PRB DOI](https://link.aps.org/doi/10.1103/PhysRevB.92.075132)
- Fishman & White (2015), accuracy and cost numbers on the SSH chain:
  - Gapped case (δ=0.1, Δ≈0.2t): B=8 and χ=55, independent of N.
  - Gapless case: B ~ log N. N=2¹⁶ needs B=22 for 10⁻¹⁰ energy accuracy.
  - Gapless N=1025: B=11 gives relative energy error <10⁻⁶. Untruncated χ=1024 compresses to χ=364 at SVD cutoff 10⁻¹¹.
  - Run time scales ≈N^2.03 (gapless) and N^1.02 (gapped). A gapless N=1025 MPS forms "on a laptop in only ~90 seconds."
  — [arXiv:1504.07701](https://arxiv.org/pdf/1504.07701)
- Fishman & White (2015) **do not benchmark DMRG warm starts.** They state only that the method could be used "either by creating starting states to aid DMRG calculations or preparing a particular ansatz as an MPS," and that "One might also begin a DMRG simulation with such a variational state." — [arXiv:1504.07701](https://arxiv.org/pdf/1504.07701)
- **ITensorGaussianMPS.jl (ITensor package; README example, accessed 2026).** The example is a spinless chain with N=20, Nf=10, t=1, plus interaction U=1. The free-fermion MPS from `slater_determinant_to_mps(s, Φ; maxblocksize=4)` starts at ⟨H⟩ = −2.38128 (random start: +10.0). Converged energy is −2.381489999595.
  - Free-fermion start: −2.381489929965 after sweep 1; converged at sweep 4.
  - Random start: converged only by sweep ~6–10.
  - Per-sweep times are ~0.14–0.17 s.
  - This amounts to roughly a 6× reduction in sweeps on a weakly interacting 1D toy problem.
  — [ITensorGaussianMPS.jl GitHub](https://github.com/ITensor/ITensorGaussianMPS.jl)
- **Negative practitioner report (ITensor Discourse, April 2023).** A user's 2D Hubbard run from a random QN product state needed ">300 sweeps" without converging. A GMPS built from the hopping-matrix eigenvectors started *worse* than the random guess, and the energy sometimes rose during sweeps. Miles Stoudenmire replied:
  - Gaussian MPS is "mainly applicable to quasi-1D systems" but "may work fine for quasi-1D i.e. small 2D systems if one tunes the parameters well."
  - Tune `eigval_cutoff` (default 1e-8) and `maxblocksize`, starting with `maxblocksize` ≈ L_y.
  - Check ⟨ψ|H|ψ⟩ of the GMPS before using it.
  — [ITensor Discourse thread 755](https://itensor.discourse.group/t/initial-state-calculation-on-2d-dmrg-with-gaussian-mps/755)
- **Schuch & Bauer (2019), "Matrix product state algorithms for Gaussian fermionic states," Phys. Rev. B 100, 245121†.** This gives a Gaussian-state counterpart of MPS algorithms and is part of the GMPS toolkit. I did not retrieve any DMRG-initialization benchmarks from it. — [arXiv:1906.10144](https://arxiv.org/pdf/1906.10144)
- **Petrica, Zheng, Chan & Clark (2021), "Finite and infinite matrix product states for Gutzwiller projected mean-field wave functions," Phys. Rev. B (2021; Caltech record: published 15 March 2021).**
  - Builds finite and infinite MPS for Slater determinants, Pfaffians/BdG states (via particle-hole or canonical maps to a Slater determinant) and products of them, then Gutzwiller-projects.
  - Cost per tensor: O(N³) + O(D²N² log₂D). "Highly parallel."
  - Energies match VMC: Heisenberg point −1.3999 (fMPS) vs −1.4001±0.0004 (VMC), with DMRG at −1.4015.
  - DMRG use is only proposed: "It could be used to initialize DMRG with a good initial mean-field guess… both for calculations on discrete lattices as well as DMRG in the continuum." No convergence benchmarks are given.
  — [arXiv:2009.00064](https://arxiv.org/pdf/2009.00064); [Caltech record](https://authors.library.caltech.edu/106297)
- **Hille & Szabó (2025), "TeMFpy: a Python library for converting fermionic mean-field states into tensor networks" (arXiv 2025).**
  - Converts Slater determinants and Pfaffian (BdG/HFB-type) states into finite or infinite MPS on top of TeNPy.
  - Cost: O(N³ + χ² log³χ), versus a stated O(χ²N³) for earlier Slater-determinant constructions.
  - Motivation stated: "DMRG and VUMPS are typically initialised with a random MPS," which risks local minima. Mean-field states are "a much closer starting point, stabilising and reducing the computational cost of MPS optimisation." No sweep or time benchmarks appear in the portion I read.
  — [arXiv:2510.05227](https://arxiv.org/html/2510.05227)
- **Fermi-sea starts used in production 2D work (2025).** Blatz, Paeckel, Schollwöck, Grusdt & Bohrdt, "Large Isolated Stripes on Short 18-leg t-J Cylinders," start DMRG "from a Fermi-sea initial state." They combine this with global subspace expansion early on and reach bond dimension m up to 6144 (m_eff≈18000 with SU(2)). They report no ablation against other starts. — [arXiv:2512.15714](https://arxiv.org/html/2512.15714v1)

### Inferences
- Unprojected Gaussian starts help most when the interacting ground state is adiabatically close to the free-fermion state: 1D, weak U, and the quasi-1D ordering problem solved by tuning `maxblocksize`. For strongly correlated 2D lattices, the doubly occupied weight of a Slater determinant is far from the Mott/spin physics, so a random or product start can be competitive. This is consistent with the 2023 negative report.
- The cost of building a GMPS is negligible compared with a production DMRG run: seconds versus hours, with O(N) gates. A neural initializer therefore has to match this "almost free" baseline on preparation cost.

### Gaps
- I found **no peer-reviewed systematic benchmark** of unprojected Slater-determinant, BCS or HFB MPS starts versus random starts in interacting lattice models (sweeps or wall-clock). The available numbers are the ITensor toy example and anecdotes.
- I found no quantitative report of HFB-MPS warm starts in nuclear-structure DMRG or of BCS-MPS warm starts for attractive-U Hubbard models.
- The specific numbers from Fishman & White's Hubbard demonstrations, if any exist beyond the SSH tests, were not in the arXiv text I retrieved.

---

## 2. Gutzwiller-projected / parton wavefunctions as MPS initial states ("Gutzwiller-boosted" or "Gutzwiller-guided" DMRG)

### Takeaway
This is the best-quantified physics-informed warm start in the literature. On the Kitaev honeycomb model, a 6×6 cylinder, Gutzwiller-projected Majorana-parton MPS starts did the following:
- reached δE≈10⁻⁸ in 7–16 sweeps, versus δE≈1.5×10⁻⁷ after 26 sweeps from random;
- reached that accuracy with about 20% smaller final bond dimension (6500 vs 8000);
- landed in the correct flux sector, where random starts always converged to the wrong one.

The gains are not universal. There was no advantage for critical SO(5)/SO(6) chains, none in the intermediate-field Kitaev regime, and energies equal to random-start energies on the kagome lattice, though there the start still gave control of sectors and chirality.

### Cited Findings
- **Wu, Wang & Tu (2020), "Tensor network representations of parton wave functions," Phys. Rev. Lett. 124, 246401†** (the "MPO-MPS" method).
  - Each parton orbital becomes a D=2 MPO applied to the vacuum, followed by the Gutzwiller projector, with SVD compression. Maximally localized Wannier orbitals plus "left-meet-right" ordering reduce intermediate entanglement.
  - Haldane-Shastry chain, N=100 (exact −41.14391334): energy deviation 3.7×10⁻⁴ at D=1000, 3.4×10⁻⁵ at D=2000, 7.2×10⁻⁶ at D=3000, 8.6×10⁻⁷ at D=5000.
  - Chiral spin liquid on a 16×10 cylinder with entanglement spectra.
  - The paper itself contains no DMRG-initialization benchmark.
  — [arXiv:1910.11011](https://ar5iv.labs.arxiv.org/html/1910.11011)
- **Jin, Tu & Zhou (2021), "Density matrix renormalization group boosted by Gutzwiller projected wave functions," Phys. Rev. B 104, L020409.** Kitaev honeycomb model, L_x×L_y = 6×6 cylinder, J_x=J_y=J_z=1, gapless. Exact E_g(Φ_y=+1) = −54.469847490329 and E_g(Φ_y=−1) = −54.385529432483, so the sector gap is ≈0.084. The GWF MPS used initial bond dimension D̃=200. DMRG truncation error was <10⁻⁹. Table S1:

  | Start | Sweeps | δE_g | D |
  |---|---|---|---|
  | GWF, Φ_y=+1 | 7 | 6.4×10⁻⁸ | 3875 |
  | GWF, Φ_y=+1 | 16 | 5.2×10⁻⁹ | 5846 |
  | GWF, Φ_y=−1 | 7 | 1.2×10⁻⁷ | 4216 |
  | GWF, Φ_y=−1 | 16 | 6.2×10⁻⁹ | 6500 |
  | random | 17 | 2.3×10⁻⁴ | 4230 |
  | random | 20 | 1.1×10⁻⁶ | 5488 |
  | random | 26 | 1.5×10⁻⁷ | 8000 |

  In words: δE is reduced "by two orders of magnitude." Random-start runs stalled from sweep 24 to 36, with the energy changing by only ~3×10⁻⁸; the authors read this as a local minimum. Random starts **always converged to the Φ_y=−1 sector even though Φ_y=+1 is lower**, while GWF starts stayed in their prescribed sector.
  — [arXiv:2009.04129](https://arxiv.org/pdf/2009.04129); [PRB DOI](https://link.aps.org/doi/10.1103/PhysRevB.104.L020409)
- Jin, Tu & Zhou (2021): **the initial state can be crude.** "A GWF MPS with D̃=200 can have ε_trunc ∼ 0.25 and still work well for initializing DMRG." In other words, the compressed starting MPS had lost about a quarter of its norm weight to truncation and still gave the speedups above. Lattice-labeling choice matters: ε_trunc≈0.09 vs 0.24 at D̃=100 for two orderings. The method is said to add "no extra computational costs," but no timings are given. — [arXiv:2009.04129](https://arxiv.org/pdf/2009.04129)
- Jin, Tu & Zhou (2021): **failure regime.** In the Kitaev model with a magnetic field h (10×4 cylinder), the four candidate Gutzwiller ansätze give the following:
  - Non-Abelian Kitaev state: matches the DMRG ground state for 0<h<0.35.
  - Fully polarized and partially polarized states: match for h>1.25.
  - U(1) spin liquid: negligible fidelity at all h.
  - For 0.35<h<1, "the DMRG cannot be boosted by any of the four Gutzwiller ansatzes."
  - A {W_y, W_p}-flux-fixed (symmetry-sector-fixed but otherwise random) MPS gave δE "almost the same" as random, so **sector fixing alone is not sufficient; the correlation structure of the ansatz matters**.
  — [arXiv:2009.04129](https://arxiv.org/pdf/2009.04129)
- **Jin, Sun, Tu & Zhou (2025), "A promising method for strongly correlated electrons in two dimensions: Gutzwiller-guided density matrix renormalization group," AAPPS Bulletin (2025) (review).**
  - Summarizes the Kitaev 6×6 result as "roughly half" the sweeps of random MPS, two orders of magnitude smaller δE, and optimum reached at D=6500 vs D=8000.
  - Applications listed: SU(4) Kugel-Khomskii on the triangular lattice (Sci. Bull. 67, 918 (2022)); SU(4) on the honeycomb lattice (PRB 107, L180401 (2023)); kagome Heisenberg (npj Quantum Mater. 9, 16 (2024)).
  - Stated limitations:
    - MPO-MPS conversion is "somewhat brute-force."
    - Gutzwiller projection is restricted to U→∞ and half filling; finite U and doping are open.
    - Conversion to PEPS is an open problem.
    - Finite cylinders can gap out gapless states.
  — [arXiv:2503.18374](https://arxiv.org/html/2503.18374v2); [AAPPS Bulletin](https://link.springer.com/article/10.1007/s43673-025-00156-8)
- **Sun, Jin, Tu & Zhou (2024), "Possible chiral spin liquid state in the S=1/2 kagome Heisenberg model," npj Quantum Mater. 9, 16.**
  - **Energies are the same as from random starts**: relative difference between random- and boosted-DMRG energies is ~10⁻⁷–10⁻⁹ on 224-site YC8 (e.g., 6.45×10⁻⁸ at J'=0). E/site = −0.4383(6).
  - **Starting energy does not predict time-to-solution.** Three starts were compared at J'=0 on 156-site YC8 with D=5000. The Dirac-spin-liquid [0,π] ansatz starts *lowest* in energy, yet CSL-initialized runs "decay faster and offset the higher initial energy drawback." All converge to the same state.
  - **Control of degenerate subspaces.** Random-DMRG converged to an uncontrolled superposition of the two chiral states, so fidelity between neighboring J' "fluctuates strongly without any regular pattern." Adiabatic boosted continuation from J'=0.1 down to −0.03 gives fidelity "a plateau close to 1."
  - Semion-sector minimally entangled states were reached only via the parton start, with energy variance σ²/N≈10⁻⁴ and overlaps between sectors ≈10⁻⁹–10⁻¹¹. Bond dimensions reached up to D=18000.
  — [arXiv:2203.07321](https://arxiv.org/pdf/2203.07321)
- **Aghaei, Bauer, Shtengel & Mishmash (2020), "Efficient matrix-product-state preparation of highly entangled trial states: Weak Mott insulators on the triangular lattice revisited," arXiv:2009.12435.** Correction to the brief: the fourth author is Ryan V. **Mishmash** (not Mong), and the v2 title concerns weak Mott insulators. I found no Weyl-semimetal content.
  - **Method ("Gutzwiller zipper").** Spin-↑ and ↓ parton MPS are built with Fishman-White Givens rotations at bond dimension m. They are then multiplied, projected and truncated to bond dimension M in one sweep at cost O(N M² m²), which is "computationally cheaper than the subsequent DMRG sweeps."
  - **Scale.** m up to 1200 and M up to 6000 on 6-leg ladders. Estimated c≈9 trial states would need m≳2000 and M≳10000.
  - **2-leg ladder.** The Gutzwiller-projected Fermi sea (GPFS) seed "converges drastically quicker" than random (figure only, no numbers).
  - **4-leg, K/J=0.6.** Starting from the c≈5 spinon-Fermi-surface state, "after only two DMRG sweeps, the entanglement entropy… rapidly decreases and almost immediately saturates to very clear c = 0 behavior." This is evidence against the spin Bose metal. Random starts on 4×24 give "the same final S₁ values after many sweeps."
  — [arXiv:2009.12435](https://arxiv.org/pdf/2009.12435v2)
- **Cai, Jin & Zhou (2025), "Symmetry-protected topological order identified via Gutzwiller-guided DMRG: SO(n) spin chains," Phys. Rev. B (2025).**
  - PBC and APBC parton states, followed by the Gutzwiller projector, give two independent DMRG runs that target the two Z₂-parity (SPT) sectors. D=2000–6000, truncation <10⁻⁹.
  - Claimed "notably efficient in targeting specific topological sectors," with no numbers.
  - **Negative result:** for critical SO(5) and SO(6) chains, "MPO-MPS initialization provides no clear advantage over random initialization," so random starts were used.
  — [arXiv:2504.10919](https://arxiv.org/html/2504.10919); [PRB](https://journals.aps.org/prb/abstract/10.1103/tdgz-ky5v)
- **Jin, Tu & Zhang (2024/2025), "Dirac and chiral spin liquids on spin-1/2 square-lattice Heisenberg antiferromagnet," Phys. Rev. B (2025).** Uses Gutzwiller-guided DMRG to argue for a Z₂ Dirac spin liquid in the J₁-J₂ model. The abstract page contains no random-vs-guided numbers. — [arXiv:2411.14114](https://arxiv.org/abs/2411.14114); [PRB](https://journals.aps.org/prb/abstract/10.1103/4yrt-nsth)
- **Jin, Natori, Pollmann & Knolle (2022), "Unveiling the S=3/2 Kitaev honeycomb spin liquids," Nat. Commun. 13, 3813†.** Parton mean-field theory is compared with DMRG on a 3×4 torus at χ=4000. In the text I retrieved, the DMRG was *not* described as initialized from parton states, so this paper should not be cited as a Gutzwiller-boost benchmark. — [arXiv:2107.13364](https://ar5iv.labs.arxiv.org/html/2107.13364); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9250503/)

### Inferences
- The gain comes mainly from **choosing the right basin or sector**, not from high initial fidelity. A start with ε_trunc≈0.25 still produced ~2× fewer sweeps and ~100× lower δE. A sector-fixed random state gave nothing, and a lower-energy but wrong ansatz (DSL on kagome) converged more slowly. The figure of merit for any initializer, neural ones included, should therefore be "time to correct basin," not ⟨H⟩ of the start.
- Gains concentrate in gapped topological phases with a known parton description (Kitaev, chiral spin liquids, SPT chains). They vanish for critical chains and for phases without a good mean-field ansatz (intermediate-field Kitaev). These are the regimes where a learned initializer could add value beyond mean-field theory.

### Gaps
- No wall-clock timings were found in any Gutzwiller-boost paper. The data are in sweeps, δE and D, so true time-to-solution savings including construction cost are not quantified.
- I found no study that scans initial-state fidelity or truncation level against DMRG sweeps to locate a threshold, beyond the single ε_trunc≈0.25 anecdote.
- I did not retrieve quantitative random-vs-GWF data from the SU(4) triangular (Sci. Bull. 2022) or SU(4) honeycomb (PRB 2023) papers.

---

## 3. Continuation and transfer strategies (parameter continuation, system-size growth, bond-dimension ramps, multigrid, basis-set/geometry transfer, iDMRG/VUMPS → finite)

### Takeaway
Continuation is ubiquitous but rarely quantified. The best numbers come from three places:
- **White's 1996 within-sweep wavefunction prediction**: Davidson time cut by 20–50×, and up to two orders of magnitude overall.
- **Bond-dimension and precision schedules** (2026 software benchmark): ~2–5× in wall-clock for 1D Hubbard.
- **Multigrid DMRG**: converges where random and standard warm-up starts fail outright on fine continuum grids.

Adiabatic parameter continuation is mostly reported as improving *reliability*: tracking a degenerate state or sector, or avoiding hops between metastable states.

### Cited Findings
- **Within-sweep warm start (state prediction).** White (1996), "Spin gaps in a frustrated Heisenberg model for CaV₄O₉," Phys. Rev. Lett. 77, 3633†.
  - Transforming the previous step's wavefunction into the new superblock basis "can reduce the number of Davidson steps by one half, typically." Used at low accuracy, only 2–3 Davidson steps are needed, saving "a factor of 20-50 in the time required by the Davidson procedure."
  - Without a good guess, Davidson needs 40–100 steps.
  - Overall speedup versus constant-m without the transformation "can be over two orders of magnitude."
  - This is now standard in all DMRG codes and is the baseline any global initial state builds on.
  — [arXiv:cond-mat/9604129](https://arxiv.org/abs/cond-mat/9604129)
- **iDMRG wavefunction prediction.** McCulloch (2008), "Infinite size density matrix renormalization group, revisited," arXiv:0804.2509. Introduces a more versatile transformation for predicting the wavefunction as the lattice grows. It "allows much faster convergence" than iTEBD, but the abstract gives no numbers. — [arXiv:0804.2509](https://arxiv.org/abs/0804.2509)
- **Size growth (warm-up) alternatives.** Tezuka (2007), "An improved initialization procedure for the density-matrix renormalization group," arXiv:cond-mat/0702242.
  - The "recursive sweep method" adds N_c sites per side, does finite sweeps at each size, and reuses the previous target state as the initial vector. Random vectors are needed "only once."
  - Faster warm-up is shown for the 84-site Hubbard model at U/t=2 with m=30–80, in a figure only.
  — [arXiv:cond-mat/0702242](https://ar5iv.labs.arxiv.org/html/cond-mat/0702242)
- **iDMRG as finite-DMRG initializer can trap.** Pfeifer (2015), "Symmetry-protected local minima in infinite DMRG," Phys. Rev. B 92, 205127. iDMRG is "widely used… for initializing finite DMRG" but can get stuck in physically irrelevant local minima protected by symmetry. A modified iDMRG avoids them. — [arXiv:1505.06266](https://arxiv.org/abs/1505.06266v2)
- **Multigrid (coarse-to-fine) DMRG.** Dolfi, Bauer, Troyer & Ristivojevic (2012), "Multigrid algorithms for tensor network states," Phys. Rev. Lett. 109, 020604†.
  - Optimize on a coarse grid, then prolongate (interpolate) the MPS to the next finer grid as its initial state, with local DMRG updates during prolongation.
  - Test: 1D bosons in an optical lattice, L=32 unit cells, up to N=128 grid points per cell, M=200, 12 single-site sweeps per level.
  - Standard DMRG from random *and* from the ALPS infinite-size warm-up gave non-converged, inhomogeneous densities after 12 sweeps. MG-DMRG gave the correct symmetric profile.
  - "For modest discretizations, standard approaches yield energies comparable to MG-DMRG," but "encounter severe convergence problems for smaller values of Δx."
  - No CPU-time ratios are given.
  — [arXiv:1203.6363](https://ar5iv.arxiv.org/html/1203.6363)
- **Multigrid renormalization for MPS.** Lubasch, Moinier & Jaksch (2018), "Multigrid renormalization," J. Comput. Phys.† The coarse-grid MPS solution approximates the finer one. Claims an exponential speedup over standard multigrid (O(log N) vs O(N)), not over DMRG from scratch. — [arXiv:1802.07259](https://ar5iv.labs.arxiv.org/html/1802.07259)
- **Bond-dimension and precision schedules as "initialization."** Sehlstedt, Bientinesi & Karlsson (2026), "Performance benchmarking: software for the density matrix renormalization group," arXiv:2607.28369 (8 packages, Fermi-Hubbard L=100, target 10⁻¹¹).
  - YASTN: a gradual bond-dimension increase alone gives "nearly a 2-fold speedup" over a ~3100 s baseline. Hybrid 1-site/2-site with a ramp reaches the target in ~1000 s vs ~1800 s for pure 2-site.
  - TeNPy: 2-site with a gradual ramp reaches 10⁻¹¹ in ~270 s vs ~1400 s in the baseline figure, about 5×.
  - ITensorMPS.jl: single precision for early sweeps then double gives 2600→2100 s (1.24×).
  - All runs start from a random MPS with fixed bond dimension. Caveat: the ramp comparisons use separate baseline runs, not matched controls.
  — [arXiv:2607.28369](https://arxiv.org/html/2607.28369)
- **The ramp is not always better.** Zauner-Stauber, Vanderstraeten, Fishman, Verstraete & Haegeman (2018), "Variational optimization algorithms for uniform matrix product states," Phys. Rev. B 97, 045145†.
  - For VUMPS, starting directly at the final D is usually more efficient than growing D. Growing D helps for hard problems "such as the Hubbard model."
  - Preconditioning with imaginary-time evolution "has proven to be even slower in all cases tried."
  - The early, irregular convergence regime "strongly depends on the chosen initial state."
  — [arXiv:1701.07035](https://arxiv.org/pdf/1701.07035)
- **Adiabatic parameter continuation (spin liquids).** Sun et al. (2024): recursive "Boosted-DMRG" from J'=0.1 to −0.03 turns erratic neighbor fidelities from random starts into a plateau ≈1. The semion-sector state on 296-site YC8 was continued from J'=0.2 down to J'=0. — [arXiv:2203.07321](https://arxiv.org/pdf/2203.07321)
- **Adiabatic flux insertion.** He, Sheng & Chen (2014), "Obtaining topological degenerate ground states by the density matrix renormalization group," Phys. Rev. B 89, 075110†. A twist θ is raised from 0 to 2π in steps, "each step's converged state used as the initial wavefunction for the next," to move between topological sectors without domain walls. — [arXiv:1309.5669](https://ar5iv.arxiv.org/html/1309.5669)
- **Parameter-scan warm starts outside condensed matter.** Zima, Nicholson & Gingrich (2025/2026), "Chemical master equation parameter exploration using DMRG," arXiv:2501.09692.
  - Converge in an easy corner of parameter space; from a uniform seed this took up to 10⁴ sweeps.
  - Then pass each converged MPS to the neighboring point, using 200 sub-steps of δc=5×10⁻⁵ between grid points.
  - Smaller steps need fewer sweeps per point. As a problem gets harder, "the cost to converge brute-force Gillespie histograms varies over three orders of magnitude, the number of DMRG sweeps varies over only one."
  - Trade-off: small steps mean many reconvergences, while large steps make each reconvergence more expensive.
  - No random-start control at each point. One sweep took ≈0.4 s.
  — [arXiv:2501.09692](https://arxiv.org/pdf/2501.09692)
- **Developer guidance (ITensor).** "Lots of initial sweeps at a low maximum bond dimension" (e.g., χ=20) is "the simplest strategy." Warm-starting from neighboring parameters "could be good," but simpler approaches may work "as well or even better." — [ITensor Discourse thread 990](https://itensor.discourse.group/t/initial-mps-choice/990)
- **ITensor FAQ (2024–2026 docs).**
  - Starting "from a simpler, related Hamiltonian" and feeding its output into the full calculation is recommended.
  - Bunching all particles on one side "can take DMRG a very long time to converge."
  - Local minima are "exacerbated for quantum number conserving DMRG."
  — [ITensorMPS DMRG FAQ](https://docs.itensor.org/ITensorMPS/dev/faq/DMRG.html)
- **Chemistry ramps.** ORCA's DMRG documentation states that "it is often advantageous to perform DMRG calculations at small M, then increase M." The default starting M is 250 for CASCI (8 sweeps) and 25 for CASSCF. If the sweeps look stuck in a local minimum, "the simplest thing to do is to increase the starting number of states." Noise ×10 is also suggested. — [ORCA 6.1 manual, DMRG](https://orca-manual.mpi-muelheim.mpg.de/contents/modelchemistries/dmrg.html)

### Inferences
- The strongest *measured* general-purpose speedups are not physics-informed initial states. They are schedules: the ramp, noise or subspace expansion, precision, and within-sweep state prediction. These give 2–5× in wall-clock on standard 1D benchmarks (2026). A neural initializer must therefore be compared against a **tuned-schedule random start**, not against a naive one.
- Continuation pays off most for phase-diagram scans and degenerate or topological manifolds, where the value is *consistency*: staying in one branch. Fewer sweeps per point is secondary.

### Gaps
- **Thin-to-wide cylinder transfer** (embedding a width-L_y MPS as the initial state for width L_y+2): I found no quantitative study.
- **VUMPS/iDMRG unit cell → finite DMRG**: common practice, and Pfeifer (2015) shows it can trap, but I found no sweep or time comparison against random finite starts.
- **Smaller basis set → larger basis set (chemistry) and geometry-to-geometry restarts**: I found no quantitative paper in this search. The Molcas/ORCA documentation and forums describe restart options without benchmarks. DMRG-SCF converges "within two to four cycles" ([Ma, Knecht, Keller & Reiher, arXiv:1611.05972](https://ar5iv.arxiv.org/html/1611.05972)), but the MPS-reuse savings were not reported in the text I saw.
- Multigrid DMRG for lattice models (doped ladders via CORE) was proposed in 2012 without results. I found no follow-up numbers.

---

## 4. Other tensor networks and methods as warm starts: imaginary time, ED/infinite-system growth, perturbative/CI-based guesses (chemistry), pinning fields and symmetry-breaking seeds, PEPS/TTN/MERA, QMC

### Takeaway
In quantum chemistry, the **CI-DEAS** entanglement-based warm-up is the established physics-informed start. It captures 90–99% of the correlation energy in the first half-sweep. In F₂ it is 76 mEh better than a Hartree-Fock start after sweep 1, and it can even change the converged energy at moderate M. In lattice 2D work, **pinning fields and symmetry-broken product states** are the standard way to choose among competing orders, with metastable stripe energies differing by only ~10⁻³ t/site. Imaginary-time pre-evolution is recommended by ITensor for stuck cases but was found slower than direct VUMPS in all cases tried. I found **no quantitative literature** on PEPS→MPS, MERA→MPS or QMC→MPS warm starts for DMRG.

### Cited Findings
- **CI-DEAS / DEAS (chemistry and momentum-space DMRG).** Legeza & Sólyom (2003), "Optimizing the density-matrix renormalization group method using quantum information entropy," Phys. Rev. B 68, 195116† (arXiv title: "Optimizing momentum space DMRG using quantum information entropy").
  - The DEAS warm-up maximizes the Kullback-Leibler entropy and extends the active space dynamically. It "reduces significantly the effective system size during the first half sweep" and "accelerates the speed of convergence… to a great extent."
  - Molecules (CH₂, H₂O, N₂, F₂): "usually 90-99 percent of the correlation energy was obtained within the first one half sweep."
  - CH₂ reaches the reference accuracy in 13 iteration steps; F₂ in 23.
  - Momentum-space Hubbard L=18: "the desired accuracy was obtained within two sweeps."
  - No CPU-time comparison is given.
  — [arXiv:cond-mat/0305336](https://arxiv.org/pdf/cond-mat/0305336v2)
- **CI-DEAS vs Hartree-Fock guess.** Keller & Reiher (2014), "Determining factors for the accuracy of DMRG in chemistry," Chimia 68, 200†.
  - F₂, CAS(14,32), m=1024: after sweep 1, HF guess −198.886421 Eh vs CI-DEAS −198.962112 Eh (76 mEh lower).
  - After 20 sweeps: −198.970559 vs −198.970711 (CI-DEAS 0.15 mEh lower). "For the moderate choice of m=1024, the converged energies still depend on the initial guess."
  - "The speed at which a converged solution is obtained strongly depends on the initial guess." CI-DEAS "may achieve the fastest convergence."
  - Guess and orbital ordering are "intertwined": HF goes with energy ordering, CI-DEAS with mutual-information ordering.
  - Other guess options listed: an HF determinant plus white noise (Chan & Head-Gordon 2002), or a perturbative correction (White 2005).
  — [arXiv:1401.5497](https://arxiv.org/pdf/1401.5497)
- **ED/infinite-system growth.** The conventional infinite-system warm-up uses "a random vector" at each growth step. Recursive-sweep reuse of the previous target state is faster, as noted above (Tezuka 2007). — [arXiv:cond-mat/0702242](https://ar5iv.labs.arxiv.org/html/cond-mat/0702242)
- **Imaginary-time evolution as pre-conditioner: conflicting guidance.**
  - ITensor FAQ: imaginary time "always reaches the ground state if (a) performed accurately on (b) a state which is not orthogonal to the ground state," and the result can seed DMRG. — [ITensorMPS DMRG FAQ](https://docs.itensor.org/ITensorMPS/dev/faq/DMRG.html)
  - Zauner-Stauber et al. (2018) found imaginary-time preconditioning "even slower in all cases tried" compared with running VUMPS throughout. — [arXiv:1701.07035](https://arxiv.org/pdf/1701.07035)
- **Pinning fields and symmetry-breaking seeds (2D).** Stoudenmire & White (2012), "Studying two-dimensional systems with the density matrix renormalization group," Annu. Rev. Condens. Matter Phys. 3, 111†.
  - "A key way to avoid metastability is to begin with a wavefunction that is already close to the true ground state."
  - A Néel state can be a sufficient start for bipartite antiferromagnets.
  - For VBS order, add pinning terms λS_i·S_j, and "after a few sweeps λ can be gradually tuned to zero."
  - Edge pinning fields of strength J/2 are used, and pinning "may" reduce entanglement.
  - Hypothesis testing: "If DMRG restores a symmetry explicitly broken by the initial state, one has strong evidence against that" order. This was used against checkerboard order in t-J and a VBS in the kagome model.
  - Verification: energy variance, plus "the same ground state with different DMRG paths."
  — [arXiv:1105.1374](https://arxiv.org/pdf/1105.1374)
- White & Chernyshev (2007), "Néel order in square and triangular lattice Heisenberg models," Phys. Rev. Lett. 99, 127004: an early systematic use of pinning fields to extract order parameters. — [PRL abstract](https://link.aps.org/abstract/PRL/v99/e127004)
- **Pinning-selected metastable stripes.** Zheng et al. (2017), "Stripe order in the underdoped region of the two-dimensional Hubbard model," Science 358, 1155†, supplementary Table S5.
  - DMRG with different pinning-field patterns converges to different stripe states. On 6×32, the 6-node (metastable) state gives −0.7648(3) t/site and the 4-node (λ=8) state gives −0.7658(7): "The energy difference between the two states is 0.001 in DMRG."
  - On 6×16: an FM-pinned 3-node state gives −0.7682(3) vs an AFM-pinned λ=8 state at −0.7691(5).
  — [Zheng et al. SM (Caltech)](https://authors.library.caltech.edu/records/45z9g-a3558/preview/aan7127_Zheng_SM.pdf); [arXiv:1701.00054](https://arxiv.org/pdf/1701.00054)
- **Subspace expansion and noise (algorithmic alternatives to a good start).**
  - Hubig, McCulloch, Schollwöck & Wolf (2015), "Strictly single-site DMRG algorithm with subspace expansion," Phys. Rev. B 91, 155115. Subspace expansion is "sufficient to avoid local minima during the optimisation." Runtime to convergence improves by up to 3.9× vs two-site DMRG and 2.5× vs the earlier single-site method on Fermi-Hubbard. — [arXiv:1501.05504](https://arxiv.org/abs/1501.05504)
  - ITensor calls noise "the most important and useful technique" for getting unstuck, e.g., `noise=[1e-6,1e-7,1e-8,0]`. — [ITensorMPS DMRG FAQ](https://docs.itensor.org/ITensorMPS/dev/faq/DMRG.html)
- **MPO-based projected states and exact MPS ansätze (AKLT-like, RVB, parton).** The MPO-MPS construction (D=2 MPO per orbital, D=1 Gutzwiller projector MPO) is the working realization of "MPO-projected" warm starts (see Section 2). — [arXiv:1910.11011](https://ar5iv.labs.arxiv.org/html/1910.11011); [arXiv:2503.18374](https://arxiv.org/html/2503.18374v2)

### Inferences
- In chemistry, physics-informed warm-ups (CI-DEAS) mostly buy **early-sweep accuracy and fewer total sweeps**. At finite M they can also change the final answer, which means the energy landscape is not benign even in "1D-ordered" orbital chains.
- In 2D lattice models, initial states and pinning are used as **selectors and hypothesis tests among near-degenerate competing orders** (ΔE~10⁻³ t/site), not as accelerators. A neural initializer that biases toward one order could silently bias the physics. Multi-start protocols remain necessary.

### Gaps
- **PEPS/iPEPS → MPS, TTN → MPS, MERA → MPS warm starts**: I found no paper reporting DMRG speedups from these. The searches returned only iMPS-vs-iPEPS comparisons ([arXiv:1705.03222](https://arxiv.org/pdf/1705.03222)) and DMRG-style PEPS optimizers ([arXiv:1908.08833](https://arxiv.org/pdf/1908.08833)).
- **QMC-derived or perturbation-theory-derived MPS starts** (e.g., Schrieffer-Wolff strong-coupling states): I found no quantitative reports. White's 2005 perturbative density-matrix correction is a convergence aid, not an initial state.
- The CI-DEAS speedup in wall-clock time (versus HF+noise) is not quantified in the sources retrieved. Section-level details in the Szalay et al. (2015) review ([arXiv:1412.5829](https://arxiv.org/pdf/1412.5829)) were not accessible in the excerpt fetched.

---

## 5. Excited-state and symmetry-sector targeting through initial states

### Takeaway
Initial states are the main lever for selecting **topological sectors** (parton states, edge spinons, flux insertion) and for **highly excited MBL eigenstates** (DMRG-X from a product state, with maximum-overlap selection). In both cases the initial state determines *which* state is found, not just how fast. Quantum-number-conserving DMRG fixes the symmetry sector through the initial state, but also makes local minima worse.

### Cited Findings
- **Topological sectors via parton initial states.**
  - Kitaev 6×6: GWF starts stay in Φ_y=±1 as prescribed, while random starts always land in Φ_y=−1, the higher-energy sector. — [Jin, Tu & Zhou 2021, arXiv:2009.04129](https://arxiv.org/pdf/2009.04129)
  - Kagome: identity- and semion-sector minimally entangled states come from the two parton states Ψ₁ and Ψ₂, with overlaps between sectors ≈10⁻⁹–10⁻¹¹. — [Sun et al. 2024, arXiv:2203.07321](https://arxiv.org/pdf/2203.07321)
  - SO(n): PBC and APBC parton states give the two Z₂ parity sectors. — [Cai, Jin & Zhou 2025, arXiv:2504.10919](https://arxiv.org/html/2504.10919)
- **Edge-spinon initial conditions and flux insertion in iDMRG.** He, Sheng & Chen (2014).
  - Inserting sites with or without an anyon line at iDMRG initialization costs either 2E_q (two domain walls) or only ΔE. When 2E_q≫ΔE the run collapses into the sector containing the anyon line.
  - Flux insertion then moves between sectors adiabatically.
  - For the easy-axis kagome model, all 4 sectors were found. For the nearest-neighbor kagome Heisenberg model, only 2 of 4 were found accurately.
  — [arXiv:1309.5669](https://ar5iv.arxiv.org/html/1309.5669)
- **Complete set of minimally entangled ground states on infinite cylinders.** Cincio & Vidal (2013), "Characterizing topological order by studying the ground states of an infinite cylinder," Phys. Rev. Lett. 110, 067208†. iDMRG yields "a complete, orthonormal set of ground states on a cylinder of infinite length," each with a different anyonic flux. The excerpt I read did not include the initialization details. — [arXiv:1208.2623](https://ar5iv.arxiv.org/html/1208.2623)
- **Highly excited states (MBL).** Khemani, Pollmann & Sondhi (2016), "Obtaining highly excited eigenstates of many-body localized Hamiltonians by the density matrix renormalization group," Phys. Rev. Lett. 116, 247204.
  - DMRG-X starts from a σᶻ product state with finite overlap on an l-bit configuration. At each local update it keeps the eigenstate "that has maximum overlap with the current MPS."
  - L=12, W=8, χ=16: overlaps with exact eigenstates are 1 to machine precision, and variances are below 10⁻¹².
  - χ≈40 reaches machine precision at W=8. Accuracy degrades around W≈5.
  - Compared with energy-targeting (L=24, W=12), the overlap rule converged quickly after each χ increase, while energy-targeting showed "poor convergence and large variances."
  — [arXiv:1509.00483](https://arxiv.org/pdf/1509.00483); [PRL](https://link.aps.org/accepted/10.1103/PhysRevLett.116.247204)
- **Low-lying excited states.** ITensor documents excited-state DMRG by "constraining them to be orthogonal to the ground state" (penalty / orthogonal projection). It also notes that QN-conserving DMRG, where the initial state fixes the sector, has a "more constrained" search space and worse local-minimum problems. — [ITensorMPS DMRG FAQ](https://docs.itensor.org/ITensorMPS/dev/faq/DMRG.html)

### Inferences
- For sector or excited-state targeting, the relevant metric is **success probability of landing in the requested state**: overlap with that sector's eigenstate, or the variance. Speed is secondary. A neural initializer competing here must be evaluated on sector purity, for example via flux or Wilson-loop expectation values or entanglement spectra. Parton constructions provide that purity by design.

### Gaps
- **Momentum-sector targeting** through initial states in hybrid real/momentum-space DMRG ([Ehlers, White & Noack 2017, PRB 95, 125125](https://link.aps.org/doi/10.1103/PhysRevB.95.125125); [arXiv:1701.03690](https://arxiv.org/pdf/1701.03690)) was not examined in detail. No numbers were gathered.
- I found no quantitative comparison of penalty-method excited-state DMRG convergence as a function of initial-state choice. A FEAST-based excited-state DMRG exists ([arXiv:2110.00092](https://arxiv.org/pdf/2110.00092)) but was not reviewed.

---

## 6. Systematic benchmarks of time-to-solution vs initial-state quality

### Takeaway
**No systematic, cross-strategy benchmark exists** that measures time-to-solution against initial-state quality (energy, fidelity, entanglement) across several warm-start families. The closest items are:
- the 2026 DMRG software benchmark, which covers schedules only and uses random starts;
- per-paper random-vs-X comparisons for single models: Kitaev, kagome, F₂, MBL, and continuum bosons.

### Cited Findings
- Sehlstedt et al. (2026) benchmark eight DMRG packages (block2, ITensorMPS.jl, MPSKit.jl, PyTeNet, quimb, Renormalizer, TeNPy, YASTN). All runs use "a random state with a fixed bond dimension," averaged over 10 runs, with MPS initialization time excluded.
  - Initial-state strategies are not compared.
  - Schedule changes alone give ~1.24× (precision), ~2× (YASTN ramp) and ~5× (TeNPy ramp, 1400→270 s).
  - Conclusion: "the optimization strategy can matter more than the choice of package."
  — [arXiv:2607.28369](https://arxiv.org/html/2607.28369)
- The best initial-state-quality data point is the **kagome three-ansatz comparison** (2024): the lowest-energy start (DSL) converged more slowly than higher-energy CSL starts. — [arXiv:2203.07321](https://arxiv.org/pdf/2203.07321)
- The best fidelity-tolerance data point is **Kitaev 6×6** (2021): a start with truncation error ~0.25 still gave ~2× fewer sweeps and ~100× lower δE. — [arXiv:2009.04129](https://arxiv.org/pdf/2009.04129)
- **Chemistry** (F₂, 2014): CI-DEAS starts 76 mEh closer after sweep 1 and ends 0.15 mEh lower at m=1024. — [arXiv:1401.5497](https://arxiv.org/pdf/1401.5497)

### Inferences
- The literature supports two observations. First, ⟨H⟩ of the initial state is a weak predictor of DMRG time-to-solution. Second, sector and basin correctness plus correlation structure (entanglement pattern) matter more. A benchmark designed around "time to δE<ε at fixed final D, and probability of the correct sector across seeds," including preparation cost, would fill a real gap.

### Gaps
- No study reports wall-clock time-to-solution for GMPS, Gutzwiller, CI-DEAS, continuation or multigrid against a tuned random-start baseline on the same hardware and schedule.
- No study correlates initial-state fidelity or entanglement with the sweep count needed across models.

---

## Comparison table of strategies

| Strategy (key source, year) | What it needs | When it works | Measured gains (year) | Limitations |
|---|---|---|---|---|
| Within-sweep state prediction (White 1996) | Previous step's wavefunction plus basis transforms | Always (finite DMRG). Now standard | Davidson steps ~½. Davidson time 20–50× less. Up to ~100× overall vs constant-m without it (1996) | Local to each sweep; not a global initializer |
| Bond-dimension ramp / precision schedule (Sehlstedt et al. 2026; ORCA; ITensor) | Schedule tuning only | Most 1D/quasi-1D; hard problems such as Hubbard | ~2× (YASTN), ~5× (TeNPy), 1.24× (FP32→FP64) to 10⁻¹¹ on Hubbard L=100 (2026) | Not matched controls. For VUMPS, starting at final D is often faster (2018) |
| Noise / subspace expansion (White 2005; Hubig et al. 2015) | Algorithm option | Escaping local minima; single-site DMRG | Up to 3.9× vs 2-site and 2.5× vs older 1-site on Hubbard (2015) | Not an initial state; noise schedule needs tuning |
| Unprojected Gaussian / Slater MPS, GMPS (Fishman & White 2015; ITensorGaussianMPS) | Quadratic mean-field H, Givens-gate compression; O(BN) gates, seconds | Weak-coupling, (quasi-)1D | ~6 → 1 sweep on an N=20 spinless chain at U=1 (toy, README) | Can be *worse* than random for 2D Hubbard (2023 report). Needs `maxblocksize` tuning. No peer-reviewed benchmark |
| Gutzwiller-projected parton MPS, MPO-MPS or zipper (Jin, Tu & Zhou 2021; Aghaei et al. 2020; Sun et al. 2024) | A parton mean-field ansatz (PSG choice) and MPO-MPS or Givens-plus-zipper compression | Gapped topological spin liquids, Kitaev, CSL, SPT chains | Kitaev 6×6: δE 10⁻⁸ in 7–16 sweeps vs 1.5×10⁻⁷ after 26 random. D 6500 vs 8000. Correct flux sector (random always wrong) (2021). Kagome: same energy as random, but controlled chirality and sector; fidelity plateau ≈1 (2024). 2-leg triangular: "drastically quicker" (2020) | No gain in critical SO(5)/SO(6) chains (2025), intermediate-field Kitaev (2021) or wrong ansätze. Half-filling, U→∞ only. Projection compression is costly (m~1000, M~6000). No wall-clock data |
| Adiabatic parameter continuation (Sun et al. 2024; He et al. 2014; Zima et al. 2025) | Converged neighbor MPS; step-size choice | Phase-diagram scans, degenerate manifolds, flux threading | Fidelity plateau ≈1 vs erratic for random (2024). Sweeps per point vary over only ~1 decade while the problem cost varies over ~3 (2025) | Can stay in a metastable branch past a transition (hysteresis). Step-size trade-off |
| Size growth: infinite-system warm-up, recursive sweeps, iDMRG→finite (White 1992; Tezuka 2007; McCulloch 2008) | Smaller converged system or iDMRG unit cell | 1D, translation-invariant | Qualitatively faster warm-up (Hubbard 84 sites). iDMRG "much faster" than iTEBD (2008) | Symmetry-protected local minima in iDMRG (Pfeifer 2015). No sweep counts |
| Multigrid DMRG, coarse → fine (Dolfi et al. 2012) | Restriction/prolongation maps; coarse model | Continuum or multi-scale; dilute fine grids | Converges (correct homogeneous density) where random and ALPS warm-up fail in 12 sweeps for N≥32 points per cell (2012) | No CPU-time numbers. Lattice restriction (CORE) untested |
| CI-DEAS / DEAS entanglement-based warm-up (Legeza & Sólyom 2003; Keller & Reiher 2014) | Orbital entropies / mutual information; CI on small active spaces | Ab initio chemistry; momentum-space Hubbard | 90–99% of correlation energy in the first half-sweep. F₂: 76 mEh better after sweep 1 and 0.15 mEh lower final at m=1024 (2014) | Coupled to orbital ordering. More complex to implement. No CPU-time data |
| HF determinant + noise (Chan & Head-Gordon 2002, via Keller & Reiher 2014; ORCA `hf_occ`) | HF occupations | Weakly multireference chemistry | Baseline (worse than CI-DEAS in F₂) | Slower early convergence; can bias the final energy at finite M |
| Pinning fields / symmetry-broken product states (Stoudenmire & White 2012; Zheng et al. 2017) | A hypothesis about the order | 2D competing orders (Néel, VBS, stripes) | Selects among metastable stripes differing by ~0.001 t/site (2017) | Biases the outcome; must be turned off or tested across multiple starts |
| Imaginary-time pre-evolution (ITensor FAQ vs Zauner-Stauber 2018) | TEBD/TDVP in imaginary time | Stubborn local minima (ITensor) | None measured. "Even slower in all cases tried" for VUMPS (2018) | Trotter error, cost |
| DMRG-X product-state targeting (Khemani et al. 2016) | l-bit product state; max-overlap selection | MBL highly excited states | Machine-precision eigenstates at χ≈40 (W=8). Energy targeting fails (2016) | Requires strong localization (fails for W≲5) |
| PEPS/TTN/MERA/QMC → MPS | — | — | **No quantitative reports found** | — |

---

## Open questions and gaps

- **No fair, cross-strategy, wall-clock benchmark.** Every warm-start paper compares against a random start under its own schedule. None compares against a *tuned* random start (ramp plus noise or subspace expansion), which by itself yields 2–5× (2015, 2026). Construction time for the initial state is never included in time-to-solution, except as qualitative remarks ("no extra cost," "cheaper than subsequent DMRG sweeps").
- **What property of the start matters?** The evidence says it is not starting energy (kagome 2024) and not high fidelity (Kitaev ε_trunc≈0.25 works, 2021). Sector or basin and entanglement structure seem to matter, but no study systematically varies fidelity, energy or entanglement and measures sweeps.
- **Regimes where physics-informed starts fail.** Critical chains (SO(5)/SO(6), 2025), intermediate-field Kitaev (2021), 2D Hubbard with unprojected GMPS (2023 forum report), and doped or finite-U systems where Gutzwiller projection does not apply (2025 review). No good physics baseline exists there beyond random plus schedule.
- **Untested transfer strategies.** Thin→wide cylinder embedding, VUMPS/iDMRG→finite with measured savings, PEPS→MPS, basis-set→basis-set and geometry→geometry MPS transfer in chemistry, and QMC-informed MPS all lack quantitative reports.
- **Reproducibility and statistics.** Results are single-run anecdotes, e.g., Kitaev Table S1. There are no distributions over random seeds, and no "success probability of reaching the true ground state or correct sector."
- **Venue and author check.** The brief's "Aghaei, Bauer, Shtengel, Mong 2020 … Weyl semimetals and beyond" does not match the arXiv record. Verified: Aghaei, Bauer, Shtengel, **Mishmash**, arXiv:2009.12435, "…Weak Mott insulators on the triangular lattice revisited." I found no Weyl-semimetal content. The S=3/2 Kitaev Nat. Commun. paper (2022) did not document parton-initialized DMRG in the text I read.

---

## Implications for a neural-network-generated initial state

- **Baselines to beat, in order of strength:**
  1. a random MPS with a tuned bond-dimension ramp plus noise or subspace expansion (2–5× from schedule alone; 2015, 2026);
  2. model-specific physics starts: Gutzwiller/parton MPS for spin liquids and Kitaev-type models (≈2× fewer sweeps, ~100× lower δE, ~20% smaller final D, correct sector; 2021), CI-DEAS for chemistry (90–99% correlation energy in the first half-sweep; 2003/2014), and continuation from neighboring parameters for scans (2024–2025).

  The NN must be compared with **the same DMRG schedule**, and its inference cost must be counted, because GMPS construction is seconds (2015) and parton zipper construction is "cheaper than the subsequent DMRG sweeps" (2020).
- **Optimize for the right target.** The evidence says ⟨H⟩ of the initial state is a poor proxy (2024 kagome: lowest-energy start converged slowest). High fidelity is also unnecessary (2021 Kitaev: ε_trunc≈0.25 sufficed). Training or evaluation objectives should therefore target (i) sweeps or wall-clock to a fixed δE at fixed final D, (ii) the probability across seeds of reaching the true ground state or requested sector, and (iii) the final bond dimension needed. Initial energy or overlap alone is not enough.
- **Output format.** Physics baselines emit an MPS at moderate D (D̃≈200 for Kitaev; M up to ~6000 for triangular ladders) with the correct quantum numbers. A neural initializer should emit a QN-conserving MPS in the code's native format (ITensor/TeNPy/block2), so QN-DMRG can run directly. ITensor notes that QN-conserving runs are *more* prone to local minima, so the initial-state quality matters most there.
- **Where a NN can plausibly add value:**
  - Regimes with no good mean-field or parton ansatz: critical systems (2025), intermediate-field Kitaev (2021), doped and finite-U Hubbard (2025 review), and 2D Hubbard, where GMPS can be worse than random (2023).
  - Amortizing continuation: predicting the MPS at a new parameter point without sequential sweeps (2025 chemical-master-equation work shows the sequential cost trade-off).
  - Chemistry, by learning CI-DEAS-like environment guesses jointly with orbital ordering (2014 shows the guess and ordering are coupled).
- **Risks inherited from physics-informed starts.** A strong initializer can bias DMRG into a metastable competing order, e.g., stripes differing by 10⁻³ t/site (2017), or into a wrong sector that random starts would also miss (Kitaev 2021). The NN pipeline should keep the multi-start or variance verification protocol (Stoudenmire & White 2012) and report sector diagnostics.
- **A hybrid is natural.** The best-documented physics pipelines are already hybrids: mean field → MPS → DMRG. A NN could replace or augment the mean-field step (for example, predicting parton/PSG parameters or Gaussian-gate parameters, which keeps the cheap Fishman-White/MPO-MPS conversion). This is a lower-risk path than predicting raw MPS tensors, and it is directly comparable with the 2021–2025 Gutzwiller-guided results.
