# Condensed-matter cases where the DMRG starting state matters: a catalogue

Scope: lattice models (frustrated spin systems, Hubbard/t-J, bosons and fractional quantum Hall, long-range and disordered models) where the initial MPS, pinning fields, boundary seeding or continuation path strongly affects DMRG convergence, running time, or which state DMRG converges to. Notes compiled 2026-10-13.

Tags used on every finding:
- **[FINAL]**: the initial state, pinning or path changed the *converged* result (a different local minimum, symmetry-broken pattern, topological sector or eigenstate), at least at the accessible bond dimension.
- **[RUNTIME]**: the initial state or pinning changed only the time to convergence; the final state was the same.
- **[SECTOR-BY-DESIGN]**: the initial state is used on purpose to pick a quantum-number or topological sector that conserved symmetries then keep fixed.

Citation format: Authors, *Title*, Venue (Year), arXiv link. Venue and volume numbers are from my own knowledge of these well-known papers. I verified the content of each one against the arXiv text, but I did not re-check every DOI or volume number; any that I could not confirm are marked "unverified".

---

## Q1. Frustrated magnets on 2D cylinders (kagome, J1-J2 square, triangular, chiral spin liquids): how did initial states, topological sectors or metastability affect results?

### Takeaway
In wide frustrated-magnet cylinders, the initial state (together with the site ordering, edge trimming and real-versus-complex arithmetic) can and does change the converged state at finite bond dimension:
- A pinned valence-bond-crystal start on kagome survived as a metastable state up to m ≈ 2400.
- Real-valued starts cannot find time-reversal-breaking chiral spin liquids, while complex random starts find them "automatically".
- Even/odd topological sectors are chosen by edge sites and the starting state, and a run can sit in the wrong sector for several sweeps before falling into the right one (YC6 at m ≈ 3000).

Competing energies are tiny: 10^-3 to 10^-7 J per site.

### Cited Findings
- **Kagome Heisenberg, Yan, Huse & White (2011)**. [FINAL at finite m]
  - The Fig. 1 run was "prepared in the HVBC state" (the 36-site hexagonal valence-bond crystal), with edges trimmed to pin it. The authors describe favoring the HVBC "both in initial state and boundary conditions" as their way of ruling it out.
  - They state that "on the wider systems, DMRG can get stuck in metastable states."
  - With a special irregular site ordering, a perfect HVBC needs only m = 2 states per block, and it stays metastable "out to about m = 2400" before turning into a spin liquid, with an energy drop of about 0.1%. With standard ordering, "the HVBC is not even metastable; it disappears within the first few sweeps with m < 200." On the largest cylinders the HVBC can be metastable even with standard ordering.
  - On a 400-site YC12 cylinder they compared an HVBC-pinned start with an "essentially random initial state". Just after the pinning is released at m = 600, the HVBC has lower energy. Near m = 2000 the randomly started run finds the spin liquid and becomes lower. The final state "appears to be a spin liquid with several localized defects which the simulation had not yet eliminated."
  - Final schedule: sweep 6 at m = 200, sweep 14 at m = 600, sweep 34 at m = 8000.
  - Energies: spin liquid XC8 −0.43824(2) and YC8 −0.43836(2); HVBC-phase XC8 (at λ = 0.98) −0.43237(4); 2D estimate E0 = −0.4379(3). The XC8 splitting to the higher topological sector is 0.00069(3) per site.
  - Source: Yan, Huse, White, *Spin-Liquid Ground State of the S = 1/2 Kagome Heisenberg Antiferromagnet*, Science 332, 1173 (2011) — [arXiv:1011.6114](https://arxiv.org/abs/1011.6114)
- **Kagome Heisenberg, Depenbrock, McCulloch & Schollwöck (2012)**. [RUNTIME / convergence artifact]
  - SU(2) DMRG kept up to 16,000 states (earlier U(1) calculations used up to 8,000) on YC4–YC12 and XC8–XC20 cylinders, up to about 726 sites.
  - Unconverged wavefunctions showed "frozen" bond-energy patterns that break translation invariance. These disappear with more states and more sweeps, and the authors call them "a distinguishing feature of an insufficiently converged wave function."
  - DMRG's low-entanglement bias means that with too few states it can favour valence-bond crystals over spin liquids.
  - Non-Abelian SU(2) symmetry removes the need for the pinning fields used in U(1) runs, and the S = 1 state is computed directly.
  - E/N = −0.4386(5); topological entanglement entropy γ consistent with log 2.
  - Source: Depenbrock, McCulloch, Schollwöck, *Nature of the Spin-Liquid Ground State of the S = 1/2 Heisenberg Model on the Kagome Lattice*, PRL 109, 067201 (2012) — [arXiv:1205.4858](https://arxiv.org/abs/1205.4858)
- **J1-J2 square lattice, Jiang, Yao & Balents (2012)**. [FINAL: sector and pattern set by boundary]
  - Cylinders with Ly = 3–14, Lx ≥ 2Ly, more than m = 12,000 states and truncation error ≲ 10^-7.
  - Static dimerization appears for odd Ly and is "entirely absent for even Ly".
  - For even Ly they used "modified cylinders" with altered ends that break y-translation, because otherwise they "expect the DMRG to converge to the symmetric linear combination of the two dimer states". The induced dimer order decays into the bulk with ξ ≈ 4.
  - "The DMRG preferentially converges ... to just one of the quasi-degenerate ground states." Increasing m can push it to the global ground state, with "a sharp increase in the entanglement entropy."
  - Source: Jiang, Yao, Balents, *Spin liquid ground state of the spin-1/2 square J1-J2 Heisenberg model*, PRB 86, 024424 (2012) — [arXiv:1112.2241](https://arxiv.org/abs/1112.2241)
- **J1-J2 square lattice, Gong, Zhu, Sheng, Motrunich & Fisher (2014)**. [FINAL: boundary seeding selects the order pattern]
  - Vertical dimer order was induced near the open boundaries by changing every other boundary bond to J_pin ≠ J1. On tilted cylinders, every other boundary site is trimmed "to select a unique PVB order".
  - The S = 1 sector needs "about twice as many states" as S = 0 for the same accuracy. Tori of 8×8 and larger are hard to converge fully.
  - Up to 36,000 U(1)-equivalent states; truncation errors 1×10^-6 (Ly = 10) and 5×10^-6 (Ly = 12).
  - Source: Gong, Zhu, Sheng, Motrunich, Fisher, *Plaquette Ordered Phase and Quantum Phase Diagram in the Spin-1/2 J1-J2 Square Heisenberg Model*, PRL 113, 027201 (2014) — [arXiv:1311.5962](https://arxiv.org/abs/1311.5962)
- **Triangular J1-J2, Zhu & White (2015)**. [FINAL at intermediate sweeps; RUNTIME eventually]
  - On a YC6 cylinder with Lx = 30, a run in the higher-energy *even* topological sector stayed there for "a number of sweeps", then suddenly dropped to the odd sector near m ~ 3000. The authors say this "depends on many details of the simulation".
  - They can prepare the initial DMRG state in the two-spinon sector to control this fall (paraphrased by my fetch; check the original wording).
  - The relaxation works by creating a spinon at each end. Moving one site from one end of the cylinder to the other switches the dimer-parity sector.
  - Energies per site: YC6 odd sector −0.52096(1), even sector −0.5152(2), a difference of 0.0058(2) (about 1.1%). On YC4 the even sector is lower and the odd sector is about 3% higher. On YC8 the odd sector is about 0.6% lower.
  - Pinning fields on the left edge favour 120° order. Up to M = 6400 states.
  - Source: Zhu, White, *Spin liquid phase of the S = 1/2 J1-J2 Heisenberg model on the triangular lattice*, PRB 92, 041105(R) (2015) — [arXiv:1502.04831](https://arxiv.org/abs/1502.04831)
- **Triangular J1-J2, Hu, Gong, Zhu & Sheng (2015)**. [FINAL: depends on real vs complex start]
  - On YC10 in the even sector, a run with a complex wavefunction keeps long-range chiral correlations, so time-reversal symmetry is spontaneously broken.
  - A run with a real wavefunction settles into a state with short-range chiral correlations. Its bulk energy is nearly the same but its edge energy is higher; at 4000 SU(2) states it reaches E = −122.978, still above the complex state.
  - The odd sector is obtained by removing one site at each open end. 2π flux insertion with U(1) DMRG at 5000 states reproduces the same sector.
  - Sector splitting Δe = e_even − e_odd at J2 = 0.1: 0.0055 (YC6), 0.0024 (YC8), −0.0004(2) (YC10). So at YC10 the two sectors are degenerate within error.
  - Source: Hu, Gong, Zhu, Sheng, *Competing spin-liquid states in the spin-1/2 Heisenberg model on the triangular lattice*, PRB 92, 140403(R) (2015) — [arXiv:1504.00654](https://arxiv.org/abs/1504.00654)
- **Kagome chiral spin liquid, Gong, Zhu & Sheng (2014)**. [FINAL]
  - "We used a real number initial wavefunction in DMRG calculations which forbids any spontaneous TRS breaking." By contrast, "if we initiate the DMRG state with a random complex number state, we automatically find such a MES" (a time-reversal-breaking minimally entangled state).
  - In flux insertion "a state with the definite chirality and sign of Chern number will be randomly selected."
  - Sectors are targeted by "pinning sites in the open boundaries or insert[ing] flux".
  - Sector splitting at J′ = 0.5, Ly = 4 shrinks with bond dimension: 0.00008 (2000 SU(2) states) → 0.00002 (4000) → 0.00001 (5000).
  - Source: Gong, Zhu, Sheng, *Emergent Chiral Spin Liquid: Fractional Quantum Hall Effect in a Kagome Heisenberg Model*, Sci. Rep. 4, 6317 (2014) — [arXiv:1312.4519](https://arxiv.org/abs/1312.4519)
- **Kagome chiral spin liquid, He, Sheng & Chen (2014)**. [FINAL]
  - A real-arithmetic code converges to the maximally entangled superposition (ψ ± ψ*)/√2, with a doubly degenerate entanglement spectrum and entropy larger by ln 2. A complex code biases towards the chiral spin liquid.
  - In transition regions the real and complex codes give different states (a time-reversal-symmetric spin liquid versus the chiral spin liquid) whose energies differ by about 10^-5.
  - The spinon sector ψs is made by pinning or removing one edge site, or by adiabatic 2π flux, which "will pump a spinon from one edge to the other". The overlap ⟨ψ1|ψs⟩ is about 0.1.
  - Sector energies: YC8 −0.463771 vs −0.463756; YC12 −0.46356936 vs −0.46356941 (a 10^-7 difference). Up to 8000 states.
  - Source: He, Sheng, Chen, *Chiral Spin Liquid in a Frustrated Anisotropic Kagome Heisenberg Model*, PRL 112, 137202 (2014) — [arXiv:1312.3461](https://arxiv.org/abs/1312.3461)
- **Kagome Dirac spin liquid, He, Zaletel, Oshikawa & Pollmann (2017)**. [FINAL: path-dependent]
  - "We implement the adiabatic twist by using the previous DMRG wavefunction as the initial step for the next θ value." Overlaps between neighbouring twist angles are about 0.99.
  - Type I geometries (YC8-0, YC8-4): adiabaticity fails near θ ≈ 4π/3 and "the simulation collapses to the other topological sector with lower energy". For π < θ ≲ 4π/3 the run follows a higher-energy state.
  - Type II geometries (YC6-2, YC8-2, ...): "for θ = π, we always end up with an ordered state with a sudden jump."
  - m = 4000–6000.
  - Source: He, Zaletel, Oshikawa, Pollmann, *Signatures of Dirac Cones in a DMRG Study of the Kagome Heisenberg Model*, PRX 7, 031020 (2017) — [arXiv:1611.06238](https://arxiv.org/abs/1611.06238)
- **Triangular-lattice Hubbard chiral spin liquid, Szasz, Motruk, Zaletel & Moore (2020)**. [SECTOR-BY-DESIGN + FINAL]
  - iDMRG in a mixed real/momentum basis can be "initialize[d] ... with states in different sectors of momentum around the cylinder". On YC6 they converged to both chiralities in each momentum sector using different product-state initializations.
  - Flux is inserted in steps of π/12, each step starting from the previous state.
  - YC6 at χ ~ 10,000 still has truncation error ~10^-4, and the authors call YC6 "much less converged".
  - Source: Szasz, Motruk, Zaletel, Moore, *Chiral Spin Liquid Phase of the Triangular Lattice Hubbard Model: A Density Matrix Renormalization Group Study*, PRX 10, 021042 (2020) — [arXiv:1808.00463](https://arxiv.org/abs/1808.00463)

### Inferences
- In frustrated magnets, two facts make the starting point decisive: competing states differ by about 10^-3 to 10^-7 J per site, and DMRG at finite m favours low entanglement. A start that is close to a symmetry-broken or low-entanglement product (a valence-bond crystal, an ordered state, a real-valued state) can persist far into the run. Yan et al. are the clearest quantitative case: the biased ordering kept the HVBC metastable up to m ≈ 2400, while the unbiased ordering lost it at m < 200.
- "Real vs complex" is effectively a discrete initial-state choice that decides between a TRS-breaking chiral spin liquid and a TRS-symmetric superposition or spin liquid. A neural-network generator for chiral phases must output complex amplitudes, or it will be locked out of the chiral minimum.
- Sector selection on finite cylinders is mostly controlled by the edges (removing or adding sites, edge pinning), but the bulk of the initial state matters because the higher-energy sector is metastable for many sweeps (Zhu & White, YC6).

### Gaps
- No paper gives wall-clock comparisons of "good" versus "random" initial states for kagome or triangular cylinders. The effect is reported as sweeps and m thresholds, not hours.
- I did not find the exact initial-state recipe in Depenbrock et al. (2012) or Jiang, Yao & Balents (2012); the papers do not state it.
- Recent (2024–2026) kagome and triangular DMRG papers were not systematically surveyed for initial-state protocols.

---

## Q2. Topological degeneracy and sector selection (MES, iDMRG, flux insertion, FQH root states): how is the desired sector targeted through the initial state?

### Takeaway
DMRG converges to a minimally entangled state (MES), not to an arbitrary superposition, and *which* MES it finds is set in three ways:
- By the initial state and random seed. In iDMRG with random starts, the sector came out roughly 50/50 at random.
- By the edges or flux history on finite cylinders.
- By construction, through conserved charge and momentum of an orbital "root configuration" seed in quantum Hall iDMRG.

Metastability between near-degenerate topological states (Pfaffian vs anti-Pfaffian) depends on bond dimension. At χ = 2000, neither state could tunnel into the other.

### Cited Findings
- **Jiang, Wang & Balents (2012)** [FINAL: the MES is chosen, not the true superposition]
  - "The DMRG algorithm naturally produces a minimally entangled state."
  - In the toric code at small m, the global winding parity ⟨G⟩ ≈ 0 and entanglement is reduced. At large m the state jumps to G = 1 with higher entanglement, and the m needed "grows rapidly with Lx".
  - Kagome J1-J2 gave γ = 0.698(8) and 0.694(6) for Ly = 4–12, compared with ln 2 ≈ 0.693.
  - Source: Jiang, Wang, Balents, *Identifying topological order by entanglement entropy*, Nat. Phys. 8, 902 (2012) — [arXiv:1205.4289](https://arxiv.org/abs/1205.4289)
- **Cincio & Vidal (2013)**: the cleanest evidence of random sector selection. [FINAL: stochastic]
  - Model: hard-core boson Haldane model on the honeycomb lattice (φ = 0.4π; t, t′, t″ = 1, 0.6, −0.58) on infinite cylinders with Ly = 4, 6, 8 unit cells.
  - "For each value of Ly, we repeated the optimization of an infinite MPS several times. Each optimization produced one of two states, with each state occurring roughly half of the runs."
  - They found a set of MES this way and computed the modular S and U matrices. The paper gives no χ or iteration counts.
  - Source: Cincio, Vidal, *Characterizing Topological Order by Studying the Ground States on an Infinite Cylinder*, PRL 110, 067208 (2013) — [arXiv:1208.2623](https://arxiv.org/abs/1208.2623)
- **Zaletel, Mong & Pollmann (2013)**: quantum Hall iDMRG with root-configuration seeds. [SECTOR-BY-DESIGN]
  - Procedure: choose an orbital root pattern (such as 010) with momentum K per unit cell, build a χ = 1 MPS from it, run iDMRG, and compare energies across seeds.
  - Because particle number and K are conserved, a seed in a K sector containing an MES converges to that MES; a sector containing no MES ends up at higher energy.
  - For ν = 1/2 the seed 0110 gives four states by translation and 0101 gives two. For ν = 2/5, 01010 gave all five MES.
  - The standard two-site update "can get stuck", because the constraints block some configurations. An n-site update fixes this: a 6-site update for 2/5, and a 10-site update reached the same state. They conjecture q+3 sites is ergodic for filling 1/q.
  - Largest run: χ = 3600, which took under a day; circumference L ≤ 23.5 ℓ_B.
  - Source: Zaletel, Mong, Pollmann, *Topological Characterization of Fractional Quantum Hall Ground States from Microscopic Hamiltonians*, PRL 110, 236801 (2013) — [arXiv:1211.3733](https://arxiv.org/abs/1211.3733)
- **Zaletel, Mong, Pollmann & Rezayi (2015)**: multicomponent quantum Hall. [FINAL at finite χ]
  - Pfaffian and anti-Pfaffian are near-degenerate. Starting separate runs from exact Pfaffian and anti-Pfaffian MPS, the wrong one can "tunnel" into the lower state after several sweeps.
  - At χ = 2000, runs from either seed could not tunnel, so each gave its own variational energy. At larger Landau-level mixing the Pfaffian tunnelled into the anti-Pfaffian.
  - "DMRG is a local optimization algorithm, so for longer-range Hamiltonians it is susceptible to getting stuck." Two-site updates with density-matrix corrections "do[es] avoid sticking".
  - Cost: χ = 15,000 at L = 24 ℓ_B took about 3.5 days and 60 GB on a 16-core node; the three-Landau-level 5/2 run (χ = 6300) took about 2.5 days.
  - Source: Zaletel, Mong, Pollmann, Rezayi, *Infinite density matrix renormalization group for multicomponent quantum Hall systems*, PRB 91, 045115 (2015) — [arXiv:1410.3861](https://arxiv.org/abs/1410.3861)
- **Spinon or vison sector seeding by edge sites and flux, across papers.** [SECTOR-BY-DESIGN]
  - He, Sheng & Chen (2014): the normal sector ψ1 "arises naturally"; the spinon sector ψs comes from pinning or removing one edge site, or 2π flux — [arXiv:1312.3461](https://arxiv.org/abs/1312.3461)
  - Hu et al. (2015): odd sector by removing one site at each end; flux θ = 2π gives edge S^z = ±1/2 and the same sector — [arXiv:1504.00654](https://arxiv.org/abs/1504.00654)
  - Zhu & White (2015): moving one site from one end to the other switches the dimer-parity sector — [arXiv:1502.04831](https://arxiv.org/abs/1502.04831)
- **Rydberg kagome, Samajdar et al. (2021)**: DMRG "preferentially converges to one of the quasidegenerate ground states". The authors say this "accounts for the apparent absence of a topological degeneracy in several numerical studies". On a cylinder a Z2 spin liquid is twofold, not fourfold, degenerate. Source: Samajdar, Ho, Pichler, Lukin, Sachdev, *Quantum phases of Rydberg atoms on a kagome lattice*, PNAS 118, e2015785118 (2021) — [arXiv:2011.12295](https://arxiv.org/abs/2011.12295)
- **Flux insertion as adiabatic continuation of the initial state.** Each θ step uses the previous MPS. This works until a level crossing, then jumps (He et al. 2017; Szasz et al. 2020 in π/12 steps) — [arXiv:1611.06238](https://arxiv.org/abs/1611.06238), [arXiv:1808.00463](https://arxiv.org/abs/1808.00463)

### Inferences
- Topological-sector selection is the clearest case where the initial state decides the **final** answer even at infinite run time on a finite or infinite cylinder. Sectors are exponentially close in energy, and DMRG never tunnels between MES at practical χ. Random starts sample sectors stochastically (Cincio & Vidal: about 50/50).
- For a neural-network initializer this means that a "best" initial state is ill-defined unless the target sector is specified. The network should be conditioned on sector labels (momentum K, spinon parity, chirality sign), or it should output several seeds, one per sector.
- In quantum Hall iDMRG the seed is a χ = 1 product state, and the hard part is ergodicity of the local update, not the seed. A better seed does not remove the need for multi-site or density-matrix-correction updates.

### Gaps
- No quantitative study found of how many sweeps a random versus an MES-proximate seed needs to converge for a given sector.
- Cincio & Vidal (2013) do not report χ or iteration counts, and do not characterise what in the random initial state decides the sector.

---

## Q3. Hubbard and t-J models (stripes vs uniform d-wave, competing orders): how do initial states, pinning fields and bond-dimension schedules bias results, and are there documented cases where different starts gave different converged states?

### Takeaway
This is the class with the most documented cases where the **final** state depends on the start at accessible bond dimension:
- Stripe wavelength and filling (λ = 5.3 vs 8; filled vs 2/3-filled).
- Paired vs unpaired states.
- Néel vs stripe states (electron-doped t-t′-J, width 8).

Energy differences are about 5×10^-4 to 10^-3 t per site. The ranking can invert between fixed-m and extrapolated comparisons, which is why practitioners routinely use temporary pinning (local chemical potentials, staggered fields, pair fields) during early sweeps and compare several seeded states by extrapolated energy. On width-4 cylinders, by contrast, random starts and stripe-pinned starts converged to the same state (runtime-only effect).

### Cited Findings
- **Zheng et al. (2017)**. [FINAL: states were metastable or never appeared]
  - DMRG on cylinders of width up to 7 and length up to 64, using real-space and hybrid-space codes.
  - The λ = 9 state "was not even metastable as boundary conditions and initial states were varied", so it was forced with a static potential.
  - Uniform d-wave states "never appeared spontaneously" in DMRG and lie about 0.01t above the lowest state. Diagonal stripes "did not spontaneously appear" because the boundary conditions frustrate them.
  - The λ = 5 vs λ = 8 energy difference is 0.0005t (DMRG) to 0.0041t (iPEPS) per site. A frustrated diagonal stripe costs about 0.005–0.009t.
  - Earlier width-6 DMRG found 2/3-filled stripes, but filled stripes win after extrapolation to infinite bond dimension.
  - AFQMC used trial wavefunctions of a chosen wavelength, made from a non-interacting Hamiltonian with pinning fields. About 100 combinations of clusters and boundary conditions were explored.
  - Source: Zheng, Chung, Corboz, Ehlers, Qin, Noack, Shi, White, Zhang, Chan, *Stripe order in the underdoped region of the two-dimensional Hubbard model*, Science 358, 1155 (2017) — [arXiv:1701.00054](https://arxiv.org/abs/1701.00054)
- **Ehlers, White & Noack (2017)**: the key quantitative example of the fixed-m vs extrapolated inversion. [FINAL at fixed m]
  - Pinning fields are usually needed only "during the initial sweeps". For width 6 at U/t = 8, however, the λ = 8 pattern needed a persistent field (P = 0.01).
  - The λ = 8 state is lower at any fixed discarded weight, but the λ = 5.3 state is lower at any accessible fixed m. With zero pinning field the λ = 8 state "becomes unstable", because DMRG converges to the lowest state within the fixed-m subspace.
  - Energies: −0.7627(5) for λ = 8 vs −0.76210(5) for λ = 5.3. The difference "can only be resolved by careful extrapolation in truncation error and system length."
  - m ≥ 25,000–30,000.
  - The hybrid momentum/real-space basis is about 12× faster for Ly = 4, 20× for Ly = 6 and 26× for Ly = 8 at fixed m.
  - Source: Ehlers, White, Noack, *Hybrid-space density matrix renormalization group study of the doped two-dimensional Hubbard model*, PRB 95, 125125 (2017) — [arXiv:1701.03690](https://arxiv.org/abs/1701.03690)
- **LeBlanc et al., Simons Collaboration (2015)**. [FINAL: metastable stripes]
  - For metastable cases the DMRG run was repeated with "an initial state favoring the lower energy state". Stripes with the wrong number of holes are "typically metastable", and metastability shows up as nonlinearity in energy versus truncation error.
  - At 1/8 doping (U/t = 8), DMRG on width-4 and width-6 cylinders gave an extrapolated value the authors "consider ... not reliable", so they omitted it.
  - Source: LeBlanc et al., *Solutions of the Two-Dimensional Hubbard Model: Benchmarks and Results from a Wide Range of Numerical Algorithms*, PRX 5, 041041 (2015) — [arXiv:1505.02290](https://arxiv.org/abs/1505.02290)
- **Qin et al. (2020)**. [FINAL ordering depends on m; seeded with temporary potentials]
  - Stripe states were prepared with "temporary local chemical potentials ... applied in the first few sweeps on the expected locations of the stripes". These are switched off after m = 4000 for filled stripes and m = 1400 for 2/3-filled stripes.
  - Filled vs 2/3-filled stripes at width 6: −0.7581(6) vs −0.7574(4), about 0.0007t. The filled stripe is lower "only once the bond dimension is large enough".
  - Width-6 runs used single-site SU(2) DMRG with up to 22,000 SU(2) states. A pairing pinning field h_p = 0.25 on the left edge was used for the pairing study.
  - The authors note that "the variational ground states often break the symmetry due to the finite bond dimensions kept."
  - Source: Qin, Chung, Shi, Vitali, Hubig, Schollwöck, White, Zhang, *Absence of Superconductivity in the Pure Two-Dimensional Hubbard Model*, PRX 10, 031016 (2020) — [arXiv:1910.08931](https://arxiv.org/abs/1910.08931)
- **Jiang & Devereaux (2019)**: a width-4 case where the start did not matter. [RUNTIME]
  - "We typically start our calculation with a random state." A pinning field with the right wavelength was tried as a check, but was needed only in the first sweeps at m = 4096. For m > 4096 the stripes form without pinning and the results match the random starts.
  - About 60 sweeps, m up to 20,000, truncation error about 10^-6.
  - Bond-dimension schedule and extrapolation matter: a quadratic fit using only m ≤ 10,000 misses the long-distance superconducting correlations, which the authors suggest "may explain the absence of long-range superconductivity in previous DMRG studies."
  - Source: Jiang, Devereaux, *Superconductivity in the doped Hubbard model and its interplay with next-nearest hopping t′*, Science 365, 1424 (2019) — [arXiv:1806.01465](https://arxiv.org/abs/1806.01465)
- **Jiang, Scalapino & White (2021)**: t-t′-J on width-8 and width-6 cylinders. [FINAL]
  - Explicit protocol: "a variety of simulations with different starting states and temporary pinning fields". Stripes start from product states with holes near their expected positions; for example, 8 holes as "two 4-hole stripes or four 2-hole stripes", compared by energy.
  - At t′ = 0.2 and x = 0.20, a product-state start "can get stuck" in an unpaired state. A pair field for a few sweeps moves it to the paired state, about 0.001t per site lower. On width 6 the unpaired state is not metastable.
  - The W3 stripe is metastable about 0.001t above the conventional stripe.
  - A weak global pair field can give false positives, and a particle-conserving run with weak pairing may stay trapped.
  - Scans vary doping or t′ slowly along a long cylinder so that phase boundaries can self-adjust.
  - Source: Jiang, Scalapino, White, *Ground-state phase diagram of the t-t′-J model*, PNAS 118, e2109978118 (2021) — [arXiv:2104.10149](https://arxiv.org/abs/2104.10149)
- **Shen, Qian & Qin (2024)**: electron-doped t-t′-J. [FINAL]
  - "We try different states (Neel and stripe) to start the DMRG calculation." On width 8 "the results depend on the starting state in the DMRG sweep".
  - At 1/12 doping only the Néel state can be stabilized; at 1/6 only the stripe; at 1/8 "both stripe and Neel states are stable in the DMRG sweep ... regardless of the boundary conditions."
  - Width 8 at D = 30,000 still has truncation error ~10^-4 ("not well converged"). Antiferromagnetic pinning h_m = 0.5 on the left edge.
  - Source: Shen, Qian, Qin, *The ground state of electron-doped t-t′-J model on cylinders*, arXiv (2024) — [arXiv:2404.01979](https://arxiv.org/abs/2404.01979). A Chin. Phys. B 2025 version appeared in search results but is unverified.
- **Xu, Chung, Qin, Schollwöck, White & Zhang (2024)**. [FINAL: depends on initial condition]
  - DMRG "can hop among low-lying states depending on the initial condition, convergence criterion, etc."; it "may not have reached full convergence in width-6 systems".
  - Edge antiferromagnetic pinning h_m = 0.25 was tried in in-phase and π-phase configurations, and "the one with lower energy is shown".
  - Low-lying branches "are characterized by different numbers of stripes" and are separated by tiny energy differences. "Two entirely different ground states are obtained for the same physical parameters" on width-4 vs width-6 cylinders.
  - Source: Hao Xu, Chia-Min Chung, Mingpu Qin, Ulrich Schollwöck, Steven R. White, Shiwei Zhang, *Coexistence of superconductivity with partially filled stripes in the Hubbard model*, Science (2024), DOI 10.1126/science.adh7691 — [arXiv:2303.08376](https://arxiv.org/abs/2303.08376). The arXiv author list does not include G. K.-L. Chan, despite the brief's "Xu, ... Chan, Zhang".
- **Lu, Chen, Zhu, Sheng & Gong (2024)**: t-J width 6 and 8. [FINAL varies with D]
  - Up to D = 15,000 SU(2) multiplets for width 6 and 28,000 for width 8 (about 45,000 and 84,000 U(1) states). Truncation error < 1.2×10^-6 (width 6) and 2.5×10^-5 (width 8).
  - At t2/t1 = −0.2 the charge profile changes from CDW-like to nearly uniform as D grows. The paper does not state initial states.
  - Source: Lu, Chen, Zhu, Sheng, Gong, *Emergent Superconductivity and Competing Charge Orders in Hole-Doped Square-Lattice t-J Model*, PRL 132, 066002 (2024) — [APS accepted manuscript](https://link.aps.org/accepted/10.1103/PhysRevLett.132.066002)
- **Gong, Zhu & Sheng (2021)**: width-6 t-J with D = 20,000 SU(2) multiplets (about 60,000 U(1)), truncation about 10^-6. No initial-state discussion in the accessible text. Source: Gong, Zhu, Sheng, *Robust d-Wave Superconductivity in the Square-Lattice t-J Model*, PRL 127, 097003 (2021) — [arXiv:2104.03758](https://arxiv.org/abs/2104.03758)

### Inferences
- In the doped Hubbard and t-J models, the converged *pattern* (number of stripes, holes per stripe, paired or not, Néel or stripe) is an initial-condition-dependent local minimum at accessible m on width ≥ 6, and often on width 8. Practitioners treat this as a multi-start problem: seed several patterns, extrapolate each in truncation error, and compare. Ehlers et al. show the trap explicitly: the wrong state wins at every accessible fixed m.
- Pinning fields applied during the first sweeps work as a cheap "initial-state generator". A neural-network initializer competes directly with this (hand-designed product states plus temporary potentials) and should be benchmarked against it, not only against random MPS.
- Width 4 is much more forgiving: Jiang & Devereaux report random and pinned starts agreeing once m > 4096. Any neural-network speed-up claim on width-4 Hubbard would be a runtime-only claim.

### Gaps
- No paper reports wall-clock or sweep-count savings from a good seeded start compared with a random start on Hubbard/t-J cylinders. Savings are described qualitatively ("pinning only needed in initial sweeps").
- The exact DMRG initial-state recipe in Xu et al. (2024) and Lu et al. (2024) was not found in the accessible text.
- Corboz, Rice & Troyer, PRL 113, 046402 (2014), an iPEPS study of uniform d-wave vs stripe in t-J ([arXiv:1402.2859](https://arxiv.org/abs/1402.2859)), was not read in detail.

---

## Q4. Symmetry sectors and quantum numbers: U(1)/SU(2) sectors fixed by the initial MPS, single-site DMRG unable to change sector, targeting excited states and other sectors

### Takeaway
With conserved abelian charges, the initial MPS fixes the global sector exactly. With single-site DMRG it also fixes the *distribution* of quantum numbers on each bond unless a mixer or subspace expansion is used. A bad product state can therefore trap DMRG at a much higher energy, or even at bond dimension 1 with zero energy. Other sectors are reached by changing the initial state (different S^z or N), by penalty or orthogonality terms, or by temporary symmetry-breaking fields with conservation switched off.

### Cited Findings
- **TeNPy v1 paper**: "Note that when using charge conservation, the initial guess determines the charge sector of the target state." With a Z2 symmetry enforced in the ordered phase, DMRG "converges to a cat state"; without it, DMRG converges to a maximally ordered state. Source: Hauschild, Unfried, Anand, ..., Mong, Zaletel, Pollmann (30 authors), *Tensor Network Python (TeNPy) version 1*, SciPost Phys. Codebases 41 (2024), DOI 10.21468/SciPostPhysCodeb.41 — [arXiv:2408.02010](https://arxiv.org/abs/2408.02010)
- **Hubig, McCulloch, Schollwöck & Wolf (2015)**. [FINAL without mixer]
  - In single-site DMRG with U(1) symmetry, "it is impossible for a local change" to add a state in a new quantum-number sector.
  - Test: 20 spin-1/2 sites with an artificial m = 20 start. Without enrichment (α = 0) it converges to E = −6.35479 with an asymmetric quantum-number distribution. With subspace expansion it reaches E = −8.6824724.
  - Subspace expansion is up to 2.5× faster than single-site DMRG with White's correction and up to 3.9× faster than two-site DMRG (Hubbard, 100 sites, m = 1200).
  - Source: Hubig, McCulloch, Schollwöck, Wolf, *Strictly single-site DMRG algorithm with subspace expansion*, PRB 91, 155115 (2015) — [arXiv:1501.05504](https://arxiv.org/abs/1501.05504). This builds on White, *Density matrix renormalization group algorithms with a single center site*, PRB 72, 180403 (2005), cited inside it.
- **Practitioner evidence (ITensor Discourse, 2023)**. [FINAL without fix; RUNTIME with fix]
  - Model: 16×2 Hubbard ladder at quarter filling with conserved quantum numbers. A product state with two adjacent up spins blocked hopping, so every sweep reported maxlinkdim = 1 and energy 0.0. Ryan Levy: "the eigensolver is getting stuck on your zero energy initial state."
  - Fixes: reorder the product state; add noise (10^-4, then 10^-8, then 0); use randomMPS; or use a Gaussian free-fermion MPS. "The free fermion state (U=0) is generally a good starting guess when U is small"; Miles Stoudenmire adds that it helps at larger U too because it "already ... minimiz[es] the hopping part".
  - After the fix it converged to −33.921257572 by sweep 10.
  - Source: ITensor Discourse, [*doping makes maxlinkdim get stuck at 1*](https://itensor.discourse.group/t/doping-makes-maxlinkdim-get-stuck-at-1/983) (June 2023)
- **Zaletel, Mong & Pollmann (2013)**: conserving N and K pins the sector exactly. The two-site update is not ergodic for long-range orbital Hamiltonians, so 6- to 10-site updates are needed — [arXiv:1211.3733](https://arxiv.org/abs/1211.3733)
- **Separate targeting of sectors:**
  - Jiang, Yao & Balents (2012) target S^z = 0 and S^z = 1 separately for triplet gaps, and target the two lowest states in the central half for singlet gaps — [arXiv:1112.2241](https://arxiv.org/abs/1112.2241)
  - Gong et al. (2014): S = 1 needs about 2× the states of S = 0 — [arXiv:1311.5962](https://arxiv.org/abs/1311.5962)
  - Samajdar et al. (2020) target the first excited state with H′ = H + wP0, a projector penalty — [arXiv:1910.09548](https://arxiv.org/abs/1910.09548)
- **Jiang, Scalapino & White (2021)**: SU(2)-conserving codes keep the ground state in the singlet sector and prevent spin-symmetry breaking; ITensor conserves U(1) only. Particle-number conservation can be turned off to allow a definite pairing phase, and real wavefunctions restrict the broken symmetry to a Z2 choice. "A system with weak pairing may stay trapped in a particle-conserving state", and a temporary pair field frees it — [arXiv:2104.10149](https://arxiv.org/abs/2104.10149)
- **Depenbrock et al. (2012)**: SU(2) symmetry removes the need for U(1) pinning fields and gives S = 1 directly — [arXiv:1205.4858](https://arxiv.org/abs/1205.4858)

### Inferences
- Any neural-network-generated initial MPS must carry exact quantum-number labels: a definite N, S^z, or SU(2) multiplet structure, and, for quantum Hall, momentum K. Otherwise the conserving DMRG code either rejects it or is locked into the wrong sector.
- With single-site DMRG, the *bond-level* quantum-number distribution of the seed matters as well as the total. A network that outputs a compressed MPS with a skewed sector distribution could trap single-site DMRG unless a mixer or subspace expansion is enabled.
- Product-state seeds can be pathologically bad (zero hopping matrix elements). This is a minimal sanity bar for a neural-network seed: a non-zero energy gradient on every bond.

### Gaps
- No systematic study found of how the bond-sector distribution of a seed affects the convergence rate of single-site DMRG with a mixer, beyond Hubig et al.'s single toy test.
- I could not fetch the TeNPy forum thread on targeting excited states in other sectors (redirected to [forum.tenpy.org](https://forum.tenpy.org/viewtopic.php?p=629)).

---

## Q5. Gapless and critical systems, long-range interactions (Rydberg arrays, dipolar), disordered systems (random singlet, MBL with DMRG-X and shift-invert MPS): where the initial state drives which eigenstate is found

### Takeaway
- **MBL excited-state methods (DMRG-X, ES-DMRG):** the initial state decides the eigenstate *by design*. A product state picks the eigenstate of maximal overlap, and this breaks down near the MBL transition (W ≲ 4–5).
- **Strongly disordered ground states (random singlet):** standard DMRG gets stuck in metastable states that more states do not fix, and the remedy is continuation in disorder strength, using the previous eigenstate as the initial guess.
- **Rydberg arrays and long-range density waves:** open edges act as seeds, and the main risks are domain walls and even/odd-length effects. Practitioners mitigate with many low-χ sweeps plus noise, about O(10^2) sweeps in total.

### Cited Findings
- **Khemani, Pollmann & Sondhi (2016), DMRG-X**. [FINAL: by design]
  - Starts "with a product state that has a finite overlap with some l-bit state". At each two-site update it chooses the local eigenvector with *maximum overlap* with the current MPS, not the one closest in energy.
  - Random-field Heisenberg chain: at L = 12, W = 8, χ = 16 every state's variance is below about 10^-12 with unit overlaps. χ ≈ 40 suffices at W = 8.
  - Accuracy degrades around W ≈ 5. Griffiths inclusions give superpositions that differ inside the inclusion.
  - Cost is χ^6 L for full diagonalization of the local problem, or about χ^3 if only k eigenstates near the current energy are computed.
  - Source: Khemani, Pollmann, Sondhi, *Obtaining Highly Excited Eigenstates of Many-Body Localized Hamiltonians by the Density Matrix Renormalization Group Approach*, PRL 116, 247204 (2016) — [arXiv:1509.00483](https://arxiv.org/abs/1509.00483)
- **Yu, Pekker & Clark (2017), shift-invert MPS (SIMPS) and ES-DMRG**. [FINAL: seed-dependent]
  - SIMPS starts from a random MPS and repeatedly applies (H − λ)^-1. ES-DMRG starts from an S^z product state at bond dimension 2 and picks the local eigenvalue closest to the current energy, so "there is no clean way to target a particular energy". One test used 6144 random product starts.
  - With two random initial conditions at L = 10, M = 12, SIMPS reached 10 of 12 targeted eigenstates.
  - Failures appear for W ≲ 4–5. Main runs used L = 30–40 and M = 60.
  - Source: Yu, Pekker, Clark, *Finding Matrix Product State Representations of Highly Excited Eigenstates of Many-Body Localized Hamiltonians*, PRL 118, 017201 (2017) — [arXiv:1509.01244](https://arxiv.org/abs/1509.01244)
- **Xavier, Hoyos & Miranda (2018), adaptive DMRG for random spin chains**. [FINAL]
  - Standard DMRG "could easily get stuck in an excited/metastable state" for strong disorder (D ≳ 1) and misses long singlets; "increasing the number of states does not help". The effective excitation energy of a strongly locked singlet "can be smaller than the standard DMRG error."
  - Remedy: start at weak disorder (D0 = 0.4) and step δD = 0.06 up to D = 1, using the previous eigenstate "as the initial guess in the Lanczos or Davidson procedure" with about 4 sweeps per step.
  - Tested on L = 120 random XX and Heisenberg chains and L = 84 spin-1 chains.
  - Source: Xavier, Hoyos, Miranda, *Adaptive density matrix renormalization group for disordered systems*, arXiv (2018) — [arXiv:1809.04029](https://arxiv.org/abs/1809.04029). Published as PRB 98, 195115 (2018), per my recollection; unverified.
- **Square-lattice Rydberg arrays, Samajdar et al. (2020)**. [RUNTIME mitigation; FINAL via geometry]
  - Strategy: "a large number of sweeps at relatively small bond dimensions before ramping d up"; noise added early and then turned off; convergence at truncation error 10^-11 after about O(10^2) sweeps.
  - d = 200–1600; interactions truncated at third neighbours. Open boundaries act as pinning fields. The ground state differs for even and odd Lx, and the staggered phase cannot be defect-free on cylinders with even Ly.
  - Source: Samajdar, Ho, Pichler, Lukin, Sachdev, *Complex Density Wave Orders and Quantum Phase Transitions in a Model of Square-Lattice Rydberg Atom Arrays*, PRL 124, 103601 (2020) — [arXiv:1910.09548](https://arxiv.org/abs/1910.09548)
- **Kagome Rydberg arrays, Samajdar et al. (2021)**. Note: the kagome paper is PNAS 2021, not PRL 2020.
  - d up to 3200 on YC6–YC12. The supplement warns the lattice "may be sensitive to the jagged edges", where edge-seeded configurations can meet and form a domain wall.
  - The authors check they are not "stuck in a metastable state" through convergence in bond dimension and sweep number. On YC12, energies change by less than 0.002% between d = 2400 and 3200.
  - The nematic phase on 8×4 is a superposition of two competing symmetry-broken states "nucleated by the edges".
  - Source: [arXiv:2011.12295](https://arxiv.org/abs/2011.12295)
- **Long-range (orbital-basis) Hamiltonians.** "DMRG is a local optimization algorithm, so for longer-range Hamiltonians it is susceptible to getting stuck" (Zaletel et al. 2015) — [arXiv:1410.3861](https://arxiv.org/abs/1410.3861)
- **Critical chains, practitioner evidence (ITensor Discourse, 2023).** A user with a 12-dimensional local Hilbert space and 512–1024 sites at a critical point, with periodic boundaries, proposed continuing the converged MPS from a nearby non-critical point. Miles Stoudenmire: "Your idea about gradually changing the state could be good", but suggested first trying "lots of initial sweeps at a low maximum bond dimension" (χ ≈ 20). Source: [*Initial MPS choice*](https://itensor.discourse.group/t/initial-mps-choice/990) (2023–2024)

### Inferences
- In disordered systems the initial state matters for a different reason than in frustrated 2D systems: small local gaps (a strongly locked long singlet) are invisible below the DMRG error. Continuation from an easier Hamiltonian is the documented cure. A neural-network seed that already encodes the strong-disorder RG singlet pattern is the natural analogue, but I found no paper testing this.
- In MBL excited-state DMRG the "initial state = target selector" relation is exact, so a learned initializer would act as an eigenstate *selector* (for example, predicting l-bit configurations), not as an accelerator.

### Gaps
- No primary source found on initial-state effects for the Haldane–Shastry chain or for dipolar or other long-range spin chains specifically.
- No wall-clock comparisons for random-singlet DMRG with and without continuation (the paper gives no CPU timings).
- Not covered: Lim & Sheng's energy-targeted DMRG for MBL, and later shift-invert or "DMRG-X+" variants.

---

## Q6. Magnetization plateaus, first-order transitions, hysteresis, and adiabatic continuation of an MPS along a parameter path

### Takeaway
Near level crossings, DMRG started from (or continued from) one phase follows that metastable branch past the true crossing, producing hysteresis. This has been used deliberately to locate first-order transitions (kagome HVBC↔spin liquid at λc = 0.984). Continuation (flux insertion, disorder ramps, parameter scans) is the standard way to carry an MPS into a target state. Recent plateau work (2026) reports that random starts "frequently converge to metastable low-energy configurations" and uses weak, quickly released pinning fields plus several symmetry-related seeds.

### Cited Findings
- **Yan, Huse & White (2011)**: hysteresis used to locate a first-order transition. The bond-strength parameter λ was changed "between each DMRG sweep" at fixed m, and the hysteresis placed the HVBC/spin-liquid transition at λc = 0.984 on a 194-site XC8 cylinder. [FINAL: path-dependent] — [arXiv:1011.6114](https://arxiv.org/abs/1011.6114)
- **He, Zaletel, Oshikawa & Pollmann (2017)**: during flux continuation the MPS follows a higher-energy branch (π < θ ≲ 4π/3) before "tunneling" to the lower sector or jumping to an ordered state. The trajectory is not symmetric about θ = π. [FINAL: path-dependent] — [arXiv:1611.06238](https://arxiv.org/abs/1611.06238)
- **Zaletel et al. (2015)**: Pfaffian/anti-Pfaffian metastability. Neither tunnels at χ = 2000; energy splittings measured in early sweeps are "qualitative". [FINAL at finite χ] — [arXiv:1410.3861](https://arxiv.org/abs/1410.3861)
- **Hagymási (2026), spin-1 and spin-3/2 pyrochlore plateaus**. [FINAL]
  - "Starting from random initial states frequently converge[s] to metastable low-energy configurations". Weak pinning fields "can already be switched off at very small bond dimensions", and the resulting states are "intrinsic variational solutions".
  - Several symmetry-related starts are run per pattern. Comparisons are made "only after extrapolation and not at fixed bond dimension", because symmetry-related partners "are not represented with identical numerical accuracy" on the snake path.
  - Spin-1, 64-site energies: −0.3386(6) (S state) vs −0.3361(6) (R) vs −0.3360(5) (q = 0) J per site. For spin-3/2 the ordering of S and R reverses between 32 and 64 sites.
  - Up to χ = 20,000 on periodic clusters of up to 128 sites.
  - Source: Hagymási, *A Tale of Two Plateaus: Competing Orders in Spin-1 and Spin-3/2 Pyrochlore Magnets*, arXiv (Feb 2026) — [arXiv:2602.16661](https://arxiv.org/abs/2602.16661)
- **Xavier, Hoyos & Miranda (2018)**: continuation in disorder strength avoids metastable traps "if energy levels change smoothly" — [arXiv:1809.04029](https://arxiv.org/abs/1809.04029)
- **Jiang, Scalapino & White (2021)**: spatial "scans" slowly vary doping or t′ along one long cylinder so that phase boundaries self-position, with regions deep inside each phase stabilizing the calculation — [arXiv:2104.10149](https://arxiv.org/abs/2104.10149)
- **Capponi, Derzhko, Honecker, Läuchli & Richter (2013)**: kagome magnetization plateaux at m = 1/3, 5/9 and 7/9 studied with exact diagonalization. The paper cites a parallel DMRG plateau study (Nishimoto, Shibata, Hotta) that I could not read. Plateau widths are about 0.5J, 0.3J and 0.1J. Source: *Numerical study of magnetization plateaux in the spin-1/2 kagome Heisenberg antiferromagnet*, PRB 88, 144416 (2013) — [arXiv:1307.0975](https://arxiv.org/abs/1307.0975) (venue from memory, unverified)

### Inferences
- Hysteresis in DMRG is both a hazard (a wrong branch persists) and a tool (bracketing first-order transitions). A learned initializer that is "too good" at reproducing one phase could bias results near a first-order line. Protocols should keep running from both sides of a transition.
- Adiabatic continuation is effectively a hand-built "initial state predictor" from a nearby Hamiltonian. A neural network that maps H → MPS is a generalisation of it, and continuation is the natural baseline.

### Gaps
- Nishimoto, Shibata & Hotta's DMRG study of kagome plateaus (Nat. Commun. 2013) was not read. I have no first-hand details on DMRG hysteresis at plateau edges.
- No sources quantify how many sweeps continuation saves compared with a cold start at each parameter point.

---

## Q7. What do Stoudenmire & White (2012) and other practitioner guides say about initial states, pinning fields and cylinder geometries?

### Takeaway
The practitioner consensus (2012–2024):
- DMRG is "locally exact but globally variational" and can get stuck.
- Start from a physically motivated or pinned state, then relax the pinning.
- Use noise or mixers early.
- Run many cheap low-χ sweeps before ramping m, with a minimum m.
- Prefer cylinders over tori, since a torus needs about m² states.
- Validate by energy variance and by reproducing the same state from different "paths".

Biased initial states are also a deliberate test: if DMRG restores a symmetry the start broke, that ordering is disfavoured.

### Cited Findings
- **Stoudenmire & White (2012)**:
  - A good starting wavefunction helps avoid metastability; smaller systems and smaller m are a guide. "A Néel state may be a sufficiently good starting point" for bipartite antiferromagnets. For subtler valence-bond-solid order, start from a pinned Hamiltonian (λ S_i·S_j on chosen bonds) and tune λ → 0 after a few sweeps.
  - "If DMRG restores a symmetry explicitly broken by the initial state", that is strong evidence against the ordering. This was used to rule out checkerboard order in t-J and a valence-bond solid in kagome.
  - Validation: check the variance ⟨H²⟩ − E², and reproduce the ground state along different DMRG paths.
  - Noise added to the density matrix lets long-range correlations "get started"; it is turned off later.
  - Fully periodic boundaries need m² states. Optimal aspect ratios Lx/Ly are about 1.9 for cylinders and about 7 for periodic boundaries.
  - Use both a maximum and a *minimum* m, because early truncation estimates are inaccurate. Repeat each m for two full sweeps before extrapolating.
  - Source: Stoudenmire, White, *Studying Two-Dimensional Systems with the Density Matrix Renormalization Group*, Annu. Rev. Condens. Matter Phys. 3, 111 (2012) — [arXiv:1105.1374](https://arxiv.org/abs/1105.1374)
- **LeBlanc et al. (2015), DMRG methods section**: each basis size is kept for two sweeps, energies are extrapolated in truncation error, and metastability is detected as nonlinearity of E versus truncation error and fixed by rerunning from a state favouring the lower one — [arXiv:1505.02290](https://arxiv.org/abs/1505.02290)
- **ITensor Discourse (2022)**, practitioner evidence: for a Hubbard–Hofstadter model, "different initial states gave different ground states". Miles Stoudenmire: "It is a kind of variational method, so it can become 'stuck' in a local optimum"; use a start closer to the ground state, or "the 'noise term' which can greatly help with DMRG convergence". Adding noise solved it. Source: [*How to make DMRG independent of initial state?*](https://itensor.discourse.group/t/how-to-make-dmrg-independent-of-initial-state/86) (Apr 2022)
- **ITensor Discourse (2023)**, practitioner evidence: Miles Stoudenmire recommends "a DMRG calculation initially start with a smaller bond/link dimension": many sweeps at χ ≈ 20, then a few final sweeps at the target χ. A Gaussian (free-fermion) MPS is a good Hubbard seed. Source: [*doping makes maxlinkdim get stuck at 1*](https://itensor.discourse.group/t/doping-makes-maxlinkdim-get-stuck-at-1/983)
- **Samajdar et al. (2020, 2021)**: the same recipe in production use (many small-d sweeps, early noise, O(10^2) sweeps, truncation threshold 10^-11) — [arXiv:1910.09548](https://arxiv.org/abs/1910.09548), [arXiv:2011.12295](https://arxiv.org/abs/2011.12295)
- **Hubbard/t-J production protocols**: temporary local chemical potentials (Qin et al. 2020), temporary pair fields and product states with holes at stripe positions (Jiang, Scalapino & White 2021), edge antiferromagnetic pinning at 0.25–0.5 (Xu et al. 2024; Shen et al. 2024) — see Q3.

### Inferences
- Current best practice is in effect a *manual* initial-state pipeline: physically designed product state → temporary pinning → low-χ sweeps with noise → ramp χ → multi-start comparison by extrapolated energy. An ML initializer should be evaluated against this pipeline, not only against random MPS, and could plausibly replace its first two stages.

### Gaps
- The guides give no quantitative "sweeps saved" numbers for good starting states.

---

## Q8 (Summary). Where the initial state matters most: ranked by model class, dimension and geometry

### Takeaway
The initial state matters most, in the sense of changing the **final** answer, in 2D-like cylinders of width ≥ 6 with near-degenerate competing orders or topological sectors. It matters least (runtime only) in 1D gapped or uniform chains and in narrow width-4 cylinders at large m.

### Cited Findings
Ranked list. "Final?" means whether the converged answer changed (F) or only runtime (R); ΔE is the typical gap between competing states, per site.

| Rank | Model class / geometry | What goes wrong / what the start controls | Final? | Typical ΔE | Key sources |
|---|---|---|---|---|---|
| 1 | Doped Hubbard / t-J, width 6–8 cylinders (1/8–1/5 doping) | Stripe wavelength and filling, paired vs unpaired, Néel vs stripe all depend on the seed and pinning; the wrong state can win at every accessible fixed m | F (at accessible m) | 5×10^-4 – 10^-3 t | [Ehlers 2017](https://arxiv.org/abs/1701.03690), [Zheng 2017](https://arxiv.org/abs/1701.00054), [Qin 2020](https://arxiv.org/abs/1910.08931), [JSW 2021](https://arxiv.org/abs/2104.10149), [Xu 2024](https://arxiv.org/abs/2303.08376), [Shen 2024](https://arxiv.org/abs/2404.01979) |
| 2 | Topologically ordered or chiral spin liquids on cylinders (kagome, triangular, Haldane-boson; YC8–YC12; iDMRG) | Sector (spinon/vison, momentum) and chirality sign set by edges, real vs complex arithmetic and random seed; random seeds give about 50/50 sectors | F (by sector) | 10^-7 – 5×10^-3 J | [Cincio–Vidal 2013](https://arxiv.org/abs/1208.2623), [He–Sheng–Chen 2014](https://arxiv.org/abs/1312.3461), [Gong 2014](https://arxiv.org/abs/1312.4519), [Hu 2015](https://arxiv.org/abs/1504.00654), [Zhu–White 2015](https://arxiv.org/abs/1502.04831) |
| 3 | Frustrated magnets with crystal vs liquid competition on wide cylinders (kagome YC12, J1-J2) | Valence-bond-crystal seeds metastable to m ≈ 2400 (with biased ordering); frozen bond patterns at low m | F at finite m; R at large m | ~10^-3 J (≈0.1–1%) | [Yan 2011](https://arxiv.org/abs/1011.6114), [Depenbrock 2012](https://arxiv.org/abs/1205.4858) |
| 4 | FQH / long-range orbital iDMRG | Seed root pattern fixes K sector (by design); Pfaffian vs anti-Pfaffian metastable at χ = 2000; two-site update non-ergodic | F | small (unquantified) | [ZMP 2013](https://arxiv.org/abs/1211.3733), [ZMPR 2015](https://arxiv.org/abs/1410.3861) |
| 5 | Plateau and first-order regimes (pyrochlore, kagome) | Random starts land in metastable plateau patterns; hysteresis across transitions | F | 3×10^-4 – 3×10^-3 J | [Hagymási 2026](https://arxiv.org/abs/2602.16661), [Yan 2011](https://arxiv.org/abs/1011.6114) |
| 6 | Strongly disordered chains (random singlet, D ≳ 1) | Stuck in excited/metastable states; more states do not help; continuation required | F | below the DMRG error locally | [Xavier 2018](https://arxiv.org/abs/1809.04029) |
| 7 | MBL excited states (DMRG-X, SIMPS) | Seed *defines* the eigenstate; fails near W ≈ 4–5 | F (by design) | — | [Khemani 2016](https://arxiv.org/abs/1509.00483), [Yu 2017](https://arxiv.org/abs/1509.01244) |
| 8 | Rydberg / long-range density-wave crystals on cylinders | Edge-seeded domains and domain walls, even/odd Lx; handled by many low-χ sweeps plus noise | Mostly R; F via geometry | — | [Samajdar 2020](https://arxiv.org/abs/1910.09548), [Samajdar 2021](https://arxiv.org/abs/2011.12295) |
| 9 | Width-4 Hubbard at large m; 1D uniform chains | Random and pinned starts agree; bad product states can still stall (QN blocking) | R | — | [Jiang–Devereaux 2019](https://arxiv.org/abs/1806.01465), [ITensor 983](https://itensor.discourse.group/t/doping-makes-maxlinkdim-get-stuck-at-1/983) |

### Inferences
- Dimension and geometry: the effect grows with cylinder width. Width ≥ 6 for Hubbard/t-J and ≥ 8–12 for frustrated spins is where the bond dimension needed to "tunnel" out of a wrong minimum exceeds what is affordable. Odd vs even widths and edge terminations change which sector is natural.
- Energy scale: in every rank-1 to rank-5 case, competing states differ by ≲ 10^-3 per site, comparable to or smaller than the finite-m energy error. This is why the seed, rather than the optimizer, decides the outcome.

### Gaps
- No paper gives a controlled, cross-model benchmark (same code, same schedule) of random vs designed seeds. The ranking above is a synthesis of separate reports.

---

## Q9. Open questions and gaps

### Takeaway
The literature documents *that* initial states change outcomes, but almost never quantifies *by how much* (sweeps or wall-clock), and there is no standard benchmark for seed quality.

### Cited Findings
- Practitioners routinely use multi-start plus extrapolated-energy comparison, but report results only for the winning state ("the one with lower energy is shown", [Xu 2024](https://arxiv.org/abs/2303.08376); "a variety of simulations with different starting states", [JSW 2021](https://arxiv.org/abs/2104.10149)).
- Energy ranking at fixed m can invert compared with the extrapolated ranking ([Ehlers 2017](https://arxiv.org/abs/1701.03690); [Hagymási 2026](https://arxiv.org/abs/2602.16661)), so "which seed converges fastest" and "which seed gives the true ground state" can be different questions.
- ML for DMRG so far targets other parts of the pipeline:
  - Marks, Jiang & Devereaux (APS March Meeting 2019) claimed "improved convergence time" using ML on the variational step, with no published numbers in the abstract — [APS abstract](https://meetings-archive.aps.org/mar/2019/c18/7)
  - Golub, Yang, Vlček & Veis (2024) use a graph neural network to predict the zero-truncation DMRG energy from low-bond-dimension runs in quantum chemistry, not initial states; their DMRG used the non-ML CI-DEAS initialization — [arXiv:2412.07607](https://arxiv.org/abs/2412.07607)

### Inferences
Open questions:
- (i) A metric for seed quality that predicts sweeps-to-convergence: overlap with the target, energy, entanglement profile, or bond-sector distribution.
- (ii) Whether a seed can escape the low-entanglement (MES) bias, or whether it is always re-projected.
- (iii) How seeds interact with single-site vs two-site updates and mixers.
- (iv) Whether learned seeds introduce systematic bias near first-order lines.
- (v) Transfer of seeds across width (Ly = 4 → 6 → 8), where physics changes qualitatively (half-filled stripes "special to width-4", [Xu 2024](https://arxiv.org/abs/2303.08376)).

### Gaps
- I found no condensed-matter paper (through Oct 2026) that uses a neural network to generate the DMRG initial MPS for lattice models and reports convergence speed-ups. Search results surfaced the reverse direction, seeding neural quantum states with tensor networks ([arXiv:2506.23550](https://arxiv.org/abs/2506.23550)). This was a quick search, not a systematic survey; adjacent researchers may cover it.

---

## Q10. Implications for a neural-network-generated initial state

### Takeaway
A neural-network initializer is most valuable where the literature shows the seed decides the **final** state: doped Hubbard/t-J at width ≥ 6, topological or chiral sectors, crystal-vs-liquid competition, and plateaus. There it would replace today's hand-designed product states, temporary pinning and multi-start searches. To be useful it must:
- respect exact quantum numbers and the target sector,
- support complex amplitudes,
- produce several distinct candidate seeds rather than one,
- be judged against designed or continuation seeds, with extrapolated energies, not fixed-m energies.

### Cited Findings
- Seeds must carry conserved charges: "the initial guess determines the charge sector" ([TeNPy 2024](https://arxiv.org/abs/2408.02010)). Single-site DMRG cannot add sectors without enrichment: a 20-site test was stuck at E = −6.355 vs the true −8.682 ([Hubig 2015](https://arxiv.org/abs/1501.05504)).
- Real-valued seeds forbid TRS-breaking chiral states; complex random seeds find them "automatically" ([Gong 2014](https://arxiv.org/abs/1312.4519); [He 2014](https://arxiv.org/abs/1312.3461); [Hu 2015](https://arxiv.org/abs/1504.00654)).
- Sector choice from random seeds is stochastic, about 50/50 ([Cincio–Vidal 2013](https://arxiv.org/abs/1208.2623)). Quantum Hall seeds are chosen per sector by root pattern ([ZMP 2013](https://arxiv.org/abs/1211.3733)).
- Strong pinning or biased seeds can lock in the wrong state up to large m: the HVBC survived to m ≈ 2400 with biased ordering ([Yan 2011](https://arxiv.org/abs/1011.6114)). The λ = 5.3 stripe wins at every accessible fixed m ([Ehlers 2017](https://arxiv.org/abs/1701.03690)).
- Baselines a learned seed should beat:
  - Gaussian / free-fermion MPS for Hubbard ([ITensor 983](https://itensor.discourse.group/t/doping-makes-maxlinkdim-get-stuck-at-1/983))
  - hole-positioned product states plus temporary potentials ([Qin 2020](https://arxiv.org/abs/1910.08931); [JSW 2021](https://arxiv.org/abs/2104.10149))
  - continuation from a nearby Hamiltonian ([Xavier 2018](https://arxiv.org/abs/1809.04029); [He 2017](https://arxiv.org/abs/1611.06238))
  - many low-χ sweeps plus noise ([Samajdar 2020](https://arxiv.org/abs/1910.09548); [Stoudenmire–White 2012](https://arxiv.org/abs/1105.1374))
- Where seeds matter only for runtime (width-4 Hubbard at m > 4096 converged identically from random starts, [Jiang–Devereaux 2019](https://arxiv.org/abs/1806.01465)), the realistic gain is fewer early sweeps. Note that the early low-χ sweeps are already cheap in standard practice.

### Inferences
Design recommendations, synthesized from the above:
1. Condition the network on the target sector (N, S^z or SU(2) label, momentum, edge termination or spinon parity, chirality sign), and output the MPS with exact block-sparse quantum-number structure.
2. Output a *diverse set* of candidate seeds, for example different stripe counts or fillings, Néel vs stripe, or both chiralities. The documented practice is multi-start, and the hard cases are near-degenerate local minima.
3. Evaluate by (a) sweeps and wall-clock to reach a target variance or truncation-extrapolated energy, and (b) the probability of reaching the lowest *extrapolated* state. Fixed-m energies can mislead.
4. Keep noise or a mixer on early, so a learned seed that is slightly off in its sector distribution can be corrected (Hubig 2015).
5. Test near first-order lines from both sides to detect bias, since hysteresis is documented.
6. The best testbeds for showing a final-state benefit are width-6 or width-8 doped Hubbard/t-J at 1/8–1/5 doping, kagome or triangular YC8–YC12 in both sectors, and Rydberg kagome YC8–YC12. Width-4 Hubbard and 1D chains are suitable only for runtime claims.

### Gaps
- No direct evidence yet that a learned seed can escape DMRG's minimally entangled bias or reduce the m at which tunnelling between competing minima occurs. This is a hypothesis to test, not an established result.
