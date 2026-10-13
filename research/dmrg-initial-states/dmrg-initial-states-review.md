# Starting states steer which minimum DMRG finds

**The starting MPS affects DMRG in two different ways, and only the second one justifies a neural network.** In the first, the start lacks quantum-number sectors, bond-basis directions or long-range correlations that local updates cannot create. Two-site updates, density-matrix noise, subspace expansion and controlled bond expansion repair this within a few sweeps. In gapped one-dimensional problems a better start therefore buys only a constant factor, and schedule and algorithm tuning already deliver 2–6×. In the second, nearly degenerate states compete and the start decides which basin DMRG ends in. This happens in doped Hubbard and t-J cylinders of width six or more, frustrated magnets on YC8–YC12 cylinders, topological and chiral sectors, first-order lines, strongly disordered chains and iron–sulfur clusters. Wrong basins survive to bond dimension ≈2400 on kagome, and the wrong stripe wins at every affordable bond dimension on width-6 Hubbard cylinders. The best-measured physics warm start, Gutzwiller-projected partons on a Kitaev cylinder, roughly halved the sweeps, cut the energy error about 100× and needed about 20% less bond dimension. It also found the flux sector random starts always missed, even though the start had lost a quarter of its weight to truncation. On kagome, by contrast, the lowest-energy starting ansatz converged slowest, so the energy of a start is a poor training target. No published work was found in which a neural network generates the DMRG starting MPS and reports measured savings; the researchers rate this absence at about 75–85% confidence. The project is therefore open, and its first deliverable should be the unpublished curve of sweeps versus start quality.

## Local updates leave DMRG blind to what the start omits

DMRG is a local, alternating optimizer. Each step solves an eigenproblem for one or two site tensors inside an environment built from the rest of the MPS. Stoudenmire and White state the consequence plainly. Because DMRG is globally variational, it "can get stuck in a metastable state," and "a key way to avoid metastability is to begin with a wavefunction that is already close to the true ground state" ([Stoudenmire & White 2012](https://arxiv.org/abs/1105.1374)). The documented failures fall into two groups. That split determines what any learned initializer can and cannot do.

### Representational failures: the start lacks what local moves cannot create

In single-site DMRG, "any limitation on the quantum numbers present in the environment translates into a restriction on the states appearing in the renormalized system block." An environment with m states supports at most m nonzero density-matrix eigenvalues. In wide ladders and long-range systems, the missing fluctuations therefore "never get built in" ([White 2005](https://arxiv.org/abs/cond-mat/0508709)).

Hubig and co-workers made this concrete. They started a 20-site spin-1/2 chain from an artificial state, and without enrichment it converged to **E = −6.35479 instead of −8.6824724**. Under U(1) symmetry, a state whose quantum number has no partner across a bond has a norm that is "zero identically" ([Hubig et al. 2015](https://arxiv.org/abs/1501.05504)).

The same pathology appears in practice. In one forum report, a 16×2 Hubbard ladder at quarter filling was started from a product state with adjacent up spins. It sat at **bond dimension 1 and energy 0.0 on every sweep**. It escaped only after the product state was reordered, noise was added, or a free-fermion MPS was used instead ([ITensor Discourse 2023](https://itensor.discourse.group/t/doping-makes-maxlinkdim-get-stuck-at-1/983)).

Long-range bonds along the MPS path, such as the width-W hops of a 2D snake or the bond that closes a periodic chain, "may have trouble getting started" ([Stoudenmire & White 2012](https://arxiv.org/abs/1105.1374)). Systems with several length scales, such as continuum discretizations and dilute or weakly doped lattices, "often fail to converge." Local optimization "is ineffective in updating large-scale features" ([Dolfi et al. 2012](https://arxiv.org/abs/1203.6363)). Conserving quantum numbers makes all of this worse: getting stuck "is exacerbated for quantum number conserving DMRG where the search space is more constrained" ([ITensor DMRG FAQ](https://itensor.github.io/ITensors.jl/stable/faq/DMRG.html)).

### Landscape failures: the start sits in the wrong basin

Landscape failures happen when two or more basins of nearly equal energy compete. Even two-site DMRG with noise can then stay in the wrong basin for many sweeps and very large bond dimension. Block and co-authors ran 32-site chains from random product states and saw four distinct failures. Near the first-order line of the mixed-field Ising model, DMRG stuck in the wrong polarization. In the tricritical Ising model it overshot into a paramagnet. In an anisotropic XXZ model it missed degenerate ferromagnetic ground states. In a ZXZ+XX model with fourfold edge degeneracy it found excited states before all four ground states, because orthogonalizing against earlier states introduces a bulk excitation that is never removed. Their summary: "results depend strongly on initialization" ([Block et al. 2021](https://quantumoptics.physics.berkeley.edu/s/2021-Performance-of-the-rigorous-renormalization-group-for-first-order-phase-transitions-and-topolog.pdf)).

### A low-entanglement bias overlays both groups

At finite bond dimension DMRG prefers low-entanglement states. In degenerate manifolds it converges to a minimally entangled state (MES) or a symmetry-broken member, not to a symmetric cat superposition ([Jiang, Wang & Balents 2012](https://arxiv.org/abs/1205.4289); [Jiang & Balents 2013](https://arxiv.org/abs/1309.7438)). A network trained to output symmetric superpositions will see DMRG pull them toward a broken or minimally entangled state anyway.

### Enrichment erases representational dependence and part of any good start

Three algorithmic devices exist partly to make results independent of the starting bond basis. White's density-matrix correction adds Δρ = Σ a A ρ A† with a ≈ 10⁻³–10⁻⁴; it makes single-site DMRG workable and about **2–4× faster** than two-site DMRG ([White 2005](https://arxiv.org/abs/cond-mat/0508709)). Subspace expansion (DMRG3S) enriches each bond with a partial projection of H|ψ⟩, at lower cost ([Hubig et al. 2015](https://arxiv.org/abs/1501.05504)). Controlled bond expansion (CBE) "yields two-site accuracy and convergence per sweep, at single-site costs" and "uses no mixing parameters" ([Gleis, Li & von Delft 2023](https://arxiv.org/abs/2207.14712)).

Gains from the choice of algorithm alone, measured from one common start, are as large as any documented initial-state gain:

| Method | S=1 Heisenberg (PBC), wall time to criterion at m = 200 / 400 / 800 | Fermi–Hubbard, largest m |
|---|---|---|
| DMRG3S (subspace expansion) | 583 / 1935 / 3990 s | 3955 s |
| Single site with White's correction | 1519 / 2695 / 11133 s | — |
| Two-site DMRG | 762 / 3181 / 21963 s (and higher final energies) | 15596 s |

Data from [Hubig et al. 2015](https://arxiv.org/pdf/1501.05504). Against two-site DMRG, the speed-up reaches 3.9× on Hubbard and more than 6× on free fermions.

Two consequences follow for a learned initializer.

First, enrichment removes representational failures within a few sweeps. With two-site DMRG, DMRG3S or CBE, the start then matters mainly through the basin it sits in and how much converged structure it already carries.

Second, noise deliberately perturbs the reduced density matrices, so it partly scrambles a high-quality start. block2's default schedule, for example, uses noise of 10⁻³ in early sweeps ([block2 docs](https://block2.readthedocs.io/en/stable/user/basic.html)).

The flip side is a concrete payoff. Suppose a start carries the correct quantum-number distribution on every bond, not just the right total charge. Then pure single-site DMRG without noise becomes viable, and that is the cheapest algorithm per sweep. Quantum chemists already do this when restarting from a neighbouring geometry, using "one-site, state-specific sweeps with noise turned off" ([Hu & Chan 2015](https://arxiv.org/abs/1502.07731)).

### The eigensolver hides a saving that sweep counts miss

Within each local update, the iterative eigensolver dominates the cost, and its speed depends on its starting vector. White's 1996 wavefunction prediction carries the previous step's state over into the new basis. It halved the number of Davidson steps and cut Davidson time by **20–50×**, for overall gains "over two orders of magnitude" compared with constant-m runs without it ([White 1996](https://arxiv.org/abs/cond-mat/9604129)). Every code now does this.

Codes also solve early local problems loosely on purpose, because early environments are poor. ITensor defaults to Krylov dimension 3 with one restart ([ITensorMPS docs](https://itensor.github.io/ITensorMPS.jl/stable/DMRG.html)). block2 starts at a Davidson threshold of 10⁻⁴ ([block2 docs](https://block2.readthedocs.io/en/stable/user/basic.html)). A good global start makes environments accurate from sweep 1, so tight tolerances can begin earlier. Sweep counts do not capture this saving.

Not every slow run is an initial-state problem. In one 2026 forum case, an N=48 spin-1 chain needed about 150 sweeps for its entanglement entropy to converge, against about 30 typically. Raising the Krylov dimension from 3 to 5 fixed it ([ITensor Discourse 2026](https://itensor.discourse.group/t/slow-convergence-of-spin-1-af-heisenberg-chain/2579)).

## Theory caps the payoff at basins and constant factors

Worst-case theory rules out any universal fix. Optimizing an MPS globally over several sites is NP-hard and "hard even in approximation" ([Eisert 2006](https://arxiv.org/abs/quant-ph/0609051)). Some 1D frustration-free Hamiltonians have a unique MPS ground state and a polynomial gap, yet finding that state "is at least as hard as factoring." Without uniqueness the problem is NP-complete, and even verifying a candidate is not possible ([Schuch, Cirac & Verstraete 2008](https://arxiv.org/abs/0802.3351)). More generally, 1D local Hamiltonians with 1/poly gaps are QMA-complete ([Aharonov et al. 2009](https://arxiv.org/abs/0705.4077)). No initializer, learned or otherwise, can claim worst-case guarantees.

Gapped 1D is the opposite case. Randomized polynomial-time algorithms exist there that need no initial state ([Landau, Vazirani & Vidick 2015](https://arxiv.org/abs/1307.5143); [Arad et al. 2017](https://drops.dagstuhl.de/opus/volltexte/2017/8192)). Their implementation, the rigorous renormalization group (RRG), is non-variational and far slower than DMRG: **13.5×10³ s versus 24 s** on a 32-site tricritical Ising chain, with energy variances of 10⁻⁶–10⁻² versus about 10⁻¹⁰. As seeds, though, RRG states proved useful. Refining them with DMRG removed the energy-ordering failures in the topological models ([Block et al. 2021](https://quantumoptics.physics.berkeley.edu/s/2021-Performance-of-the-rigorous-renormalization-group-for-first-order-phase-transitions-and-topolog.pdf)). That is the template for a learned seed: cheap, approximate and globally informed, then polished by DMRG.

Convergence theory for the DMRG iteration itself is only local. The single-site analogue in applied mathematics, alternating least squares in tensor-train format, cannot adapt its ranks. Its two-site version (MALS) can ([Holtz, Rohwedder & Schneider 2012](https://epubs.siam.org/doi/10.1137/100818893); [Kressner, Steinlechner & Uschmajew 2014](https://www.epfl.ch/labs/mathicse/wp-content/uploads/2018/10/40.2014NEW_DK-MS-AU.pdf)). Rohwedder and Uschmajew prove local linear convergence near a non-degenerate solution of fixed rank, with no global result ([Rohwedder & Uschmajew 2013](https://opus.bibliothek.uni-augsburg.de/opus4/frontdoor/index/index/docId/103361)); the content is cited from memory because the abstract could not be retrieved. Kressner and co-authors write that "the global and local convergence properties of the DMRG algorithm are not well understood." Later analysis finds that verifying the local conditions is "open in most cases" ([Oseledets, Rakhuba & Uschmajew 2018](https://arxiv.org/abs/1709.07286)).

One inference follows from geometric convergence inside the right basin. Cutting the initial error by a factor ε saves only about log(1/ε)/|log ρ| sweeps, where ρ is the local contraction rate. A start ten times better in the right basin therefore buys a handful of sweeps, not an order of magnitude. This is an extrapolation from general theory, not a published DMRG bound.

The landscape is not flat. For Haar-random isometric MPS with extensive nearest-neighbour Hamiltonians, the variance of the energy gradient converges to a **system-size-independent value scaling as 1/m²**, so isometric tensor networks are "free of barren plateaus" ([Barthel & Miao 2025](https://arxiv.org/abs/2304.00161); [Miao & Barthel 2024](https://arxiv.org/abs/2304.14320)). Random starts fail because of discrete basin structure, not vanishing gradients, and those basins are exactly where a predicted start can help.

The same literature carries a design warning. In MPS-based machine learning, barren plateaus "prevail" for global loss functions but are absent for local ones ([Liu et al. 2022](https://arxiv.org/abs/2108.08312)). A network trained through MPS tensors should therefore minimize sums of local energy terms rather than a global fidelity. This is an inference carried over from that setting.

Physics adds qualitative scaling but no law. Bond dimension must grow exponentially with cylinder width at fixed accuracy, and fully periodic boundaries need roughly m² states ([Stoudenmire & White 2012](https://arxiv.org/abs/1105.1374)). At 1D critical points, finite bond dimension acts as a length scale set by the central charge ([Pollmann et al. 2009](https://arxiv.org/abs/0812.2903)). ITensor developers report that "gapless systems will generally converge slower" ([ITensor Discourse 2026](https://itensor.discourse.group/t/slow-convergence-of-spin-1-af-heisenberg-chain/2579)). No paper quantifies how the number of sweeps depends on gap, correlation length, cylinder width or interaction range at fixed initial-state quality.

## Wide cylinders, degenerate sectors and stripes are where starts decide answers

The condensed-matter record is a catalogue of cases in which the seed changed the converged state, at least at affordable bond dimension. One number unites them. **Competing states differ by about 10⁻³ to 10⁻⁷ per site**, which is comparable to or smaller than the finite-m energy error. The optimizer cannot tell such states apart, so the start decides. The ranking below synthesizes separate reports; no study compares these models with a common code and schedule.

| Rank | Model class and geometry | What the start controls | Changes final answer? | Typical ΔE per site | Key sources |
|---|---|---|---|---|---|
| 1 | Doped Hubbard and t-J, width 6–8 cylinders | Stripe wavelength and filling, paired vs unpaired, Néel vs stripe | Yes, at accessible m | 5×10⁻⁴–10⁻³ t | [Ehlers 2017](https://arxiv.org/abs/1701.03690), [Zheng 2017](https://arxiv.org/abs/1701.00054), [JSW 2021](https://arxiv.org/abs/2104.10149) |
| 2 | Topological and chiral spin liquids (kagome, triangular, Haldane bosons; YC8–YC12; iDMRG) | Anyon sector, chirality sign; random seeds split ≈50/50 | Yes, by sector | 10⁻⁷–5×10⁻³ J | [Cincio & Vidal 2013](https://arxiv.org/abs/1208.2623), [He, Sheng & Chen 2014](https://arxiv.org/abs/1312.3461) |
| 3 | Crystal vs liquid competition on wide frustrated cylinders | Valence-bond-crystal seeds metastable to m≈2400 | Yes, at finite m | ~10⁻³ J | [Yan, Huse & White 2011](https://arxiv.org/abs/1011.6114) |
| 4 | Fractional quantum Hall and long-range orbital iDMRG | Momentum sector (by design); Pfaffian vs anti-Pfaffian | Yes | Small (unquantified) | [Zaletel, Mong & Pollmann 2013](https://arxiv.org/abs/1211.3733), [Zaletel et al. 2015](https://arxiv.org/abs/1410.3861) |
| 5 | Magnetization plateaus and first-order lines | Metastable plateau patterns; hysteresis | Yes | 3×10⁻⁴–3×10⁻³ J | [Hagymási 2026](https://arxiv.org/abs/2602.16661), [Block 2021](https://quantumoptics.physics.berkeley.edu/s/2021-Performance-of-the-rigorous-renormalization-group-for-first-order-phase-transitions-and-topolog.pdf) |
| 6 | Strongly disordered chains (random singlet) | Stuck in excited or metastable states; more states do not help | Yes | Below the DMRG error | [Xavier, Hoyos & Miranda 2018](https://arxiv.org/abs/1809.04029) |
| 7 | Many-body-localized excited states (DMRG-X, shift-invert MPS) | The seed defines which eigenstate is found | Yes, by design | — | [Khemani, Pollmann & Sondhi 2016](https://arxiv.org/abs/1509.00483) |
| 8 | Rydberg density waves on cylinders | Edge-seeded domains; even vs odd lengths | Mostly runtime | — | [Samajdar et al. 2020](https://arxiv.org/abs/1910.09548) |
| 9 | Width-4 Hubbard at large m; gapped 1D chains | Sweep count; pathological product states | Runtime only | — | [Jiang & Devereaux 2019](https://arxiv.org/abs/1806.01465) |

### Doped Hubbard and t-J cylinders flip with the seed above width four

Ehlers, White and Noack give the sharpest example of a start-dependent trap. On width-6 cylinders at U/t=8, the λ=8 stripe is lower at any fixed discarded weight. Yet the λ=5.3 stripe is lower **at every accessible fixed bond dimension**, even with m ≥ 25,000–30,000. With no pinning field, the λ=8 state "becomes unstable," because DMRG converges to the lowest state within the fixed-m subspace. The two energies, −0.7627(5) and −0.76210(5), can be separated only "by careful extrapolation in truncation error and system length" ([Ehlers, White & Noack 2017](https://arxiv.org/abs/1701.03690)).

The multi-method stripe study found that the λ=9 state "was not even metastable as boundary conditions and initial states were varied." Uniform d-wave states "never appeared spontaneously." On 6×32 cylinders, DMRG stripes with different pinning patterns differed by 0.001 t/site ([Zheng et al. 2017](https://arxiv.org/abs/1701.00054); [supplement](https://authors.library.caltech.edu/records/45z9g-a3558/preview/aan7127_Zheng_SM.pdf)).

Qin and co-workers seeded stripes with temporary local chemical potentials, which stayed on until m=4000 for filled stripes. Filled stripes beat 2/3-filled ones by about 0.0007 t, but "only once the bond dimension is large enough" ([Qin et al. 2020](https://arxiv.org/abs/1910.08931)).

In the t-t′-J model at t′=0.2 and x=0.20, a product-state start "can get stuck" in an unpaired state about 0.001 t/site above the paired one. It escapes only under a temporary pair field ([Jiang, Scalapino & White 2021](https://arxiv.org/abs/2104.10149)).

On width-8 electron-doped cylinders, "the results depend on the starting state." At 1/8 doping, Néel and stripe states are both stable, and the truncation error is still about 10⁻⁴ at D=30,000 ([Shen, Qian & Qin 2024](https://arxiv.org/abs/2404.01979); a Chinese Physics B version is unverified).

A 2024 Science study reports that DMRG "can hop among low-lying states depending on the initial condition" and shows "the one with lower energy" ([Xu et al. 2024](https://arxiv.org/abs/2303.08376)).

Width 4 is the control case. Jiang and Devereaux start from random states and use pinning only in the first sweeps up to m=4096. They recover identical stripes either way ([Jiang & Devereaux 2019](https://arxiv.org/abs/1806.01465)). Current Hubbard practice is therefore a hand-run multi-start search: seed several stripe patterns with product states and temporary fields, extrapolate each one, and keep the lowest.

### Frustrated magnets keep crystals and wrong sectors alive for thousands of states

On the kagome Heisenberg model, one run was "prepared in the HVBC state" (a hexagonal valence-bond crystal) with a special site ordering. It stayed metastable "out to about m = 2400" before melting into the spin liquid. With standard ordering the crystal "disappears within the first few sweeps with m < 200." On a 400-site YC12 cylinder, an essentially random start overtook the pinned run only near m≈2000. Even then the result carried "several localized defects which the simulation had not yet eliminated" ([Yan, Huse & White 2011](https://arxiv.org/abs/1011.6114)). The same authors turned the effect into a tool: they varied a bond strength between sweeps and used the resulting hysteresis to place a first-order transition at λc = 0.984.

SU(2) runs with up to 16,000 multiplets later showed that frozen bond patterns breaking translation symmetry are "a distinguishing feature of an insufficiently converged wave function" ([Depenbrock, McCulloch & Schollwöck 2012](https://arxiv.org/abs/1205.4858)).

On the triangular J1-J2 YC6 cylinder, a run in the higher even sector stayed there for "a number of sweeps." It dropped to the odd sector near m~3000; the two sectors differ by about 1.1% in energy ([Zhu & White 2015](https://arxiv.org/abs/1502.04831)). The notes also say the initial state can be prepared in the two-spinon sector to control this drop. That wording is a fetch-tool paraphrase and was not checked against the original.

Real versus complex arithmetic is itself a discrete initial-state decision. "A real number initial wavefunction … forbids any spontaneous TRS breaking," whereas "if we initiate the DMRG state with a random complex number state, we automatically find" the chiral minimally entangled state ([Gong, Zhu & Sheng 2014](https://arxiv.org/abs/1312.4519)). A real code converges to the superposition (ψ±ψ*)/√2, whose entropy is larger by ln 2 ([He, Sheng & Chen 2014](https://arxiv.org/abs/1312.3461)). On triangular YC10, real and complex runs reach nearly equal bulk energies but different chiral correlations ([Hu et al. 2015](https://arxiv.org/abs/1504.00654)). A generator restricted to real amplitudes is locked out of every phase that breaks time-reversal symmetry.

Geometry compounds the problem. Edge terminations and odd versus even widths change which sector is natural, and the 2D-to-1D path is its own optimization problem. A September 2026 preprint calls reverse Cuthill–McKee ordering "unreliable" and finds that staged SAT/CP-SAT solvers give the best orderings ([Rausch 2026, arXiv:2609.25384](https://arxiv.org/abs/2609.25384); seen only as an abstract). For infinite systems, TeNPy warns that an artificially enforced translational invariance, such as a wrong iDMRG unit cell, can block the true ground state ([TeNPy protocol](https://raw.githubusercontent.com/tenpy/tenpy/main/doc/intro/dmrg-protocol.rst)).

### Topological sectors are selected, not discovered

Cincio and Vidal repeated iDMRG optimizations on the hard-core-boson Haldane model and found "each state occurring roughly half of the runs" ([Cincio & Vidal 2013](https://arxiv.org/abs/1208.2623)).

Quantum Hall iDMRG picks sectors by design. A χ=1 root-configuration seed has conserved charge and momentum that fix the sector. Ergodicity is the hard part instead: the two-site update "can get stuck," and 6- to 10-site updates were needed ([Zaletel, Mong & Pollmann 2013](https://arxiv.org/abs/1211.3733)). Pfaffian and anti-Pfaffian seeds could not tunnel into each other at χ=2000, and one χ=15,000 run took about 3.5 days on a 16-core node ([Zaletel et al. 2015](https://arxiv.org/abs/1410.3861)).

On finite cylinders, edges and flux history pick the sector. Removing or pinning an edge site creates the spinon sector. Adiabatic flux insertion carries the MPS between sectors until a level crossing makes it collapse "to the other topological sector" ([He et al. 2017](https://arxiv.org/abs/1611.06238)). In the triangular-lattice Hubbard model, iDMRG product-state starts in different momentum sectors reached both chiralities ([Szasz et al. 2020](https://arxiv.org/abs/1808.00463)).

DMRG "preferentially converges to one of the quasidegenerate ground states." That, according to one Rydberg study, "accounts for the apparent absence of a topological degeneracy in several numerical studies" ([Samajdar et al. 2021](https://arxiv.org/abs/2011.12295)). For a learned initializer, a single "best" start is undefined unless the target sector is specified.

### Disorder, first-order lines and plateaus reward continuation

In random-singlet chains, standard DMRG "could easily get stuck in an excited/metastable state," and "increasing the number of states does not help." The reason is that a strongly locked long singlet has an excitation energy that "can be smaller than the standard DMRG error." The cure was continuation: start at weak disorder (D₀=0.4) and step up by 0.06, with about four sweeps per step ([Xavier, Hoyos & Miranda 2018](https://arxiv.org/abs/1809.04029); the PRB 98, 195115 venue is unverified).

For excited states of many-body-localized chains, the initial product state defines the target. DMRG-X keeps the local eigenvector with maximum overlap to the current MPS. It reaches machine-precision eigenstates at χ≈40 for disorder W=8 and fails near W≈5 ([Khemani, Pollmann & Sondhi 2016](https://arxiv.org/abs/1509.00483)).

A 2026 pyrochlore plateau study reports that random starts "frequently converge to metastable low-energy configurations." It runs several symmetry-related seeds per pattern and compares them "only after extrapolation and not at fixed bond dimension" ([Hagymási 2026](https://arxiv.org/abs/2602.16661)).

### Narrow and gapped systems forgive almost any sensible start

The forgiving cases matter equally for project design. Width-4 Hubbard at large m and gapped uniform chains converge to the same state from random or designed starts. So do Rydberg arrays run with many cheap low-χ sweeps plus noise, which take about O(10²) sweeps to reach a 10⁻¹¹ truncation threshold ([Samajdar et al. 2020](https://arxiv.org/abs/1910.09548)). Any speed-up claimed on these systems is runtime-only. Standard practice already makes the early sweeps cheap by running many of them at χ≈20 before ramping up ([ITensor Discourse 2023](https://itensor.discourse.group/t/initial-mps-choice/990)).

## Chemistry trades the MPS guess for orbitals, ordering and spin basins

In ab initio DMRG, the "starting state" bundles five choices: the initial MPS or warm-up, the orbital basis, the order of orbitals along the chain, the active space, and the spin and symmetry sector. The MPS guess is the weakest lever on the converged answer.

The canonical head-to-head is F₂ in a (14 electron, 32 orbital) active space at m=1024. After sweep 1, a Hartree–Fock start gave −198.886421 Eh, while the entanglement-based CI-DEAS warm-up gave −198.962112 Eh. That **76 mEh gap shrank to 0.15 mEh after 20 sweeps**. Still, "for the moderate choice of m=1024, the converged energies still depend on the initial guess" ([Keller & Reiher 2014](https://arxiv.org/abs/1401.5497)).

DEAS recovered **90–99% of the correlation energy within the first half-sweep** for CH₂, H₂O, N₂ and F₂ ([Legeza & Sólyom 2003](https://arxiv.org/abs/cond-mat/0305336)). A review cites an estimate that "the effect of the starting guess is an order of magnitude smaller than the effect of orbital choice and ordering" ([Wouters & Van Neck 2014](https://arxiv.org/abs/1407.2040)). That is a qualitative estimate based on older work, not a modern benchmark.

Guess and ordering are coupled. Hartree–Fock guesses suit energy-based orderings, and CI-DEAS suits mutual-information orderings. There is "no obvious or simple relation" between ordering and convergence. Single-site DMRG in chemistry also "gets trapped in local energy minima for even the simplest systems," which is why production codes use two-site sweeps with noise ([Keller & Reiher 2014](https://arxiv.org/abs/1401.5497)).

Production defaults define the chemistry baselines. block2 offers four ways to build the initial MPS: random, from CCSD occupations, by fitting an approximate MPS, or from determinants or configuration state functions. It adds perturbative noise "to escape poor initial guesses" ([Zhai et al. 2023](https://arxiv.org/abs/2310.03920)).

ORCA 6.1 defaults to Hartree–Fock-type occupations, a Wilson-type warm-up, Fiedler ordering with optional genetic-algorithm refinement (GAOPT), split-localized orbitals, and an M schedule of 250 for 8 sweeps then 1000 for 8. Its advice for local minima is to "increase startM … or raise the noise (×10)" ([ORCA 6.1 manual](https://www.faccts.de/docs/orca/6.1/manual/contents/modelchemistries/dmrg.html)). The Budapest/Veis workflow begins "all DMRG calculations from the CI-DEAS procedure," with Fiedler ordering and split-localized orbitals ([Golub et al. 2025](https://arxiv.org/abs/2412.07607)).

Fiedler ordering uses the second eigenvector of the graph Laplacian of the exchange or mutual-information matrix. It dates to 2011 ([Barcza et al. 2011](https://arxiv.org/abs/1008.4607)), and a 2021 paper justifies mutual-information ordering through strong subadditivity ([arXiv:2103.01111](https://arxiv.org/abs/2103.01111)). Localized orbitals make energies "converge significantly faster" with bond dimension in quasi-1D π systems ([Wouters & Van Neck 2014](https://arxiv.org/abs/1407.2040)). The newest ordering method, multi-site rearrangement, cut the mean relative energy error on a randomly permuted 32-site Heisenberg chain from 0.135 to 0.018, but it is untested on molecules ([Watanabe, Hikihara & Ueda 2025](https://arxiv.org/abs/2512.22021)).

### Multi-metal clusters turn initialization into a combinatorial search

In iron–sulfur and molybdenum clusters, the start stops being a convenience. For the nitrogenase P-cluster, active spaces reached 120 electrons in 77 orbitals. Calculations began from broken-symmetry product states with bond dimension 1, built by distributing Fe spin states. The authors explored **20, 35, 70 and 152 basins** across four systems, and warned that "the non-linear optimization of the wavefunction in the DMRG algorithm is easily trapped in local minima" ([Li, Guo, Sun & Chan, Nat. Chem. 2019](https://arxiv.org/abs/1810.10196)).

The 2026 FeMoco study (113 electrons in 76 orbitals) went further. It sampled **78,750 unrestricted Hartree–Fock initial guesses** and kept 840 broken-symmetry references across 35 spin isomers, which it ranked with coupled cluster. It then ran unrestricted DMRG up to D=18,000 at **317,440 core-hours per sweep**, about 2.77 million core-hours in total. Each reference got its own split-localized UCCSD natural orbitals and a genetic-algorithm ordering of αβ orbital pairs. The best filtered determinant had overlap 0.4468 with the D=18,000 state ([Zhai et al. 2026](https://arxiv.org/abs/2601.04621)).

In these systems, fast convergence and the correct state come apart. A generic start converges quickly to *some* basin. The combinatorial choice of reference decides *which* one, and today that choice is brute-forced.

Smaller molecules show the same weak points. Standard DMRG predicts the wrong singlet–triplet ordering for peripentacene (44 electrons, 44 orbitals) at low M ([Golub et al. 2025](https://arxiv.org/abs/2412.07607)). Cu₂O₂ isomer energies at m=32–128 were non-monotonic and 40–50 kJ/mol off the large-m value ([Reiher 2014 lectures](https://ethz.ch/content/dam/ethz/special-interest/chab/imps/reiher-dam/documents/Diverse/reiher_mariapfarr2014.pdf)). State-specific DMRG suffers root flipping near conical intersections, which maximum-overlap root tracking and state-averaged initial guesses control ([Hu & Chan 2015](https://arxiv.org/abs/1502.07731)). Cr₂ required SU(2) DMRG at bond dimension up to 28,000 ([Larsson et al. 2022](https://arxiv.org/abs/2206.10738)).

### The same states seed quantum algorithms

Initial-state quality is also the bottleneck for quantum phase estimation, which gives a learned DMRG seed a second market. The largest single determinant or configuration-state-function weight decays exponentially with the number of metal centres, to about **10⁻⁷ for FeMoco**. Adiabatic state-preparation time in a 24-qubit [2Fe-2S] model varied by about eight orders of magnitude with the choice of initial Hamiltonian ([Lee et al., Nat. Commun. 2023](https://arxiv.org/abs/2208.02199)). A D=4000 MPS reaches an estimated squared overlap of about 0.9 with a FeMoco candidate state ([Berry et al. 2024](https://arxiv.org/abs/2409.11748)). Because the true ground state is unknown, practical quality assessment uses the energy distribution rather than the overlap ([Fomichev et al. 2024](https://arxiv.org/abs/2310.18410)).

## Physics-informed warm starts set a demanding but under-measured bar

Non-neural warm starts are diverse and cheap. Most have been benchmarked only against naive random starts, each under its own paper's schedule. The table collects every measured gain the researchers found.

| Strategy | Works when | Measured gain | Limits | Source |
|---|---|---|---|---|
| Within-sweep wavefunction prediction | Always; now standard | Davidson time 20–50× lower; up to ~100× overall | Local, not a global start | [White 1996](https://arxiv.org/abs/cond-mat/9604129) |
| Bond-dimension ramp or precision schedule | 1D Hubbard | ~2× (YASTN), ~5× (TeNPy, ~1400 s → ~270 s), 1.24× (FP32 then FP64), to 10⁻¹¹ at L=100 | Separate baselines rather than matched controls; random starts only | [Sehlstedt et al. 2026](https://arxiv.org/html/2607.28369) |
| Subspace expansion or noise | Escaping minima | Up to 3.9× vs two-site | Needs noise-schedule tuning | [Hubig 2015](https://arxiv.org/abs/1501.05504) |
| Gaussian (Slater-determinant) MPS | Weak coupling, quasi-1D | N=20 toy chain: within 7×10⁻⁸ after sweep 1, converged by sweep 4 vs 6–10 from random | Worse than random in a 2D Hubbard report | [ITensorGaussianMPS](https://github.com/ITensor/ITensorGaussianMPS.jl), [Discourse 755](https://itensor.discourse.group/t/initial-state-calculation-on-2d-dmrg-with-gaussian-mps/755) |
| Gutzwiller-projected parton MPS | Gapped spin liquids, Kitaev, SPT chains | Kitaev 6×6: ~2× fewer sweeps, ~100× lower δE, D 6500 vs 8000, correct flux sector | No gain at criticality or intermediate-field Kitaev; U→∞, half filling only | [Jin, Tu & Zhou 2021](https://arxiv.org/abs/2009.04129) |
| Adiabatic parameter continuation | Phase scans, degenerate manifolds | Neighbour fidelity ≈1, vs erratic from random | Hysteresis past transitions | [Sun et al. 2024](https://arxiv.org/abs/2203.07321) |
| Multigrid, coarse to fine | Continuum and multi-scale problems | Converges where random and standard warm-up fail within 12 sweeps | No CPU times | [Dolfi et al. 2012](https://arxiv.org/abs/1203.6363) |
| CI-DEAS entanglement warm-up | Ab initio chemistry | 90–99% of correlation in first half-sweep; F₂ 76 mEh better after sweep 1 | Coupled to ordering; no timings | [Legeza & Sólyom 2003](https://arxiv.org/abs/cond-mat/0305336), [Keller & Reiher 2014](https://arxiv.org/abs/1401.5497) |
| Pinning fields, symmetry-broken product states | 2D competing orders | Selects among stripes 10⁻³ t/site apart | Biases the outcome; needs multi-start | [Stoudenmire & White 2012](https://arxiv.org/abs/1105.1374) |
| Imaginary-time pre-evolution | Stubborn minima (folklore) | None measured; "even slower in all cases tried" for VUMPS | Cost | [Zauner-Stauber et al. 2018](https://arxiv.org/abs/1701.07035) |
| PEPS, TTN, MERA or QMC converted to MPS | — | No quantitative reports found | — | — |

### Gutzwiller-guided DMRG is the best-quantified and most instructive case

On a gapless 6×6 Kitaev cylinder, starts from Gutzwiller-projected Majorana partons reached δE≈6×10⁻⁹ in 16 sweeps at D=5846–6500. Random starts reached only 1.5×10⁻⁷ after 26 sweeps at D=8000, stalled from sweep 24 to 36, and "always" converged to the higher-energy Φ_y=−1 flux sector ([Jin, Tu & Zhou 2021](https://arxiv.org/abs/2009.04129)).

Three findings in that paper redefine what "best start" means. A parton MPS with truncation error ~0.25 still "work[s] well." A sector-fixed but otherwise random MPS gave δE "almost the same" as a random one, so the correlation structure of the start matters, not just its sector. And in the intermediate-field Kitaev regime, no ansatz helped.

On kagome, the Dirac-spin-liquid ansatz started lowest in energy, yet chiral-spin-liquid starts "decay faster and offset the higher initial energy drawback." Final energies matched random starts to 10⁻⁷–10⁻⁹, but only parton starts gave controlled chirality and the semion sector ([Sun et al. 2024](https://arxiv.org/abs/2203.07321)). Critical SO(5) and SO(6) chains showed "no clear advantage over random initialization" ([Cai, Jin & Zhou 2025](https://arxiv.org/abs/2504.10919)). The method's 2025 review lists finite U and doping as open problems ([Jin et al. 2025](https://arxiv.org/abs/2503.18374)).

The lesson: a start's energy and fidelity are weak predictors of time to solution. Basin and sector correctness, together with the right correlation pattern, are strong ones.

### Cheap construction and continuation set the cost bar

Physics-based starts are nearly free. A gapless N=1025 Gaussian MPS forms "on a laptop in only ~90 seconds" ([Fishman & White 2015](https://arxiv.org/abs/1504.07701)). The "Gutzwiller zipper" projection costs less than the DMRG sweeps that follow it ([Aghaei et al. 2020](https://arxiv.org/abs/2009.12435)). TeMFpy now converts Slater-determinant and Bogoliubov mean-field states into TeNPy MPS ([Hille & Szabó 2025](https://arxiv.org/abs/2510.05227)). Fermi-sea starts already run in production 18-leg t-J studies, without ablation against other starts ([Blatz et al. 2025](https://arxiv.org/abs/2512.15714)). A neural generator must match these near-free baselines on preparation cost.

Continuation is equally cheap per step and likely the strongest competitor in smooth parameter regions. In a chemical-master-equation scan, brute-force cost varied over three orders of magnitude while DMRG sweeps per point varied over only one ([Zima, Nicholson & Gingrich 2025](https://arxiv.org/abs/2501.09692)). Its weaknesses are hysteresis near transitions and the absence of any neighbour for new disorder realizations, geometries or sizes. Those gaps are where amortized prediction has room.

Even routine transfers can mislead. iDMRG, "widely used ... for initializing finite DMRG," can stick in symmetry-protected local minima ([Pfeifer 2015](https://arxiv.org/abs/1505.06266v2)).

### Where the time actually goes

One fact reframes the project. In production, the final high-bond-dimension sweeps dominate cost: FeMoco takes 317,440 core-hours per sweep at D=18,000, while early sweeps are negligible. A seed that only saves cheap warm-up sweeps therefore saves little wall time.

The documented large savings come from elsewhere. One is avoiding metastable episodes that burn high-m sweeps, such as kagome runs metastable to m≈2000–2400. Another is lowering the final bond dimension needed, by about 20% for Kitaev and as a lower fixed-m energy for F₂. A third is replacing multi-start enumeration: 840 FeMoco references, 152 P-cluster basins, hand-seeded stripes. The fourth is amortizing one model over a family of problems.

## Machine learning has circled DMRG initialization without landing on it

**No paper from 2017–2026 was found that trains a neural network or other ML model to generate the DMRG starting MPS and reports sweep or wall-clock savings.** The search covered six research passes, INSPIRE full-text queries and about 25 search variants. The researchers rate confidence that the exact idea is unpublished at about 75–85%. Blocked arXiv full-text search and unreadable ACS pages limit that confidence.

### Three precedents come closest

The first is a 2019 APS March Meeting talk by Marks, Jiang and Devereaux, "Accelerating Density Matrix Renormalization Group Computations with Machine Learning." It claimed improved convergence time for several classes of strongly correlated systems. The abstract names no mechanism and gives no numbers, and no paper or thesis followed ([APS MAR19 C18.7](https://meetings-archive.aps.org/mar/2019/c18/7)). It should still be cited as prior art.

The second is a 2026 "autoresearch" study in which a GPT-based coding agent evolved DMRG protocols under a 20 s budget on chains of length 64. The winning protocols switched to two-site or staged updates, raised the bond dimension and **changed the initial state from random to Néel or ± product states**. That lowered the XXX-chain energy from −28.165820 to −28.175425 ([Mantilla Calderón et al. 2026](https://arxiv.org/abs/2604.25610); numbers from the HTML v2 fetch, not re-checked).

The third is Hamilton-Zero, a ~0.5B-parameter Hamiltonian-conditioned neural tree tensor network. Its zero-shot ground states of quadratic qubit Hamiltonians show median gaps of 4–13% to exact diagonalization, falling to 10⁻³–10⁻²% after fine-tuning. It replaces DMRG rather than seeding it ([Heightman et al. 2026](https://arxiv.org/html/2608.11911)).

### The reverse direction is mature and carries a cautionary number

Pretraining a neural-network quantum state (NQS) on DMRG data cut the variational Monte Carlo steps needed for chemical precision from 2732 to 347 for H₁₀, and from 7376 to 2358 for H₂O. Yet **wall-clock time improved by at most ≈1.6×**, and some checkpoints were slower than no pretraining ([Kan et al., Mathematics 2024](https://doi.org/10.3390/math12030433); time units unstated). In the ANTN hybrid, "the improvement … mainly comes from the effective inductive bias of MPS structure," not from DMRG initialization ([Chen et al. 2023](https://arxiv.org/abs/2304.01996)).

An MPS can be embedded exactly in a recurrent network ([Wu et al. 2023](https://arxiv.org/abs/2206.12363)) or converted approximately into an RBM ([Kaneko & Goto 2025](https://arxiv.org/abs/2506.23550)). The project's direction also has theoretical support. Short-range RBMs obey area laws ([Deng, Li & Das Sarma 2017](https://arxiv.org/abs/1701.04844)), RBMs translate efficiently into tensor networks ([Chen et al. 2018](https://arxiv.org/abs/1701.04831)), and tensor cross interpolation learns an MPS from any amplitude oracle ([Fernández et al. 2025](https://scipost.org/SciPostPhys.18.3.104)). Yet no one has compressed a trained NQS into an MPS and handed it to DMRG.

### Amortized models exist but never feed DMRG

Several Hamiltonian-conditioned models already exist. Transformer quantum states generate "the entire phase diagram" ([Zhang & Di Ventra 2023](https://arxiv.org/abs/2208.01758v4)). Foundation NQS take couplings as input and fine-tune cheaply ([Rende et al. 2025](https://arxiv.org/abs/2502.09488); [Rende et al. 2024](https://arxiv.org/abs/2403.07795)). A hypernetwork conditions an RBM on control parameters ([Tonner, Tran & Kueng 2026](https://arxiv.org/abs/2601.20950); abstract only). A geometry-conditioned NQS is 986× cheaper per geometry than independent optimization and 25.8× cheaper end-to-end on a 161-point N₂ curve ([Fu et al. 2026](https://arxiv.org/abs/2609.37733); abstract-level numbers).

The strongest non-neural amortizer is a reduced basis of greedily chosen DMRG ground states that serves observables anywhere in a parameter domain ([Brehmer et al. 2023](https://arxiv.org/abs/2304.13587)). It is a natural warm-start baseline that has never been used as one.

### ML around the DMRG workflow targets inputs and outputs

In chemistry, machine learning touches the DMRG workflow only at its inputs and outputs. Networks predict DMRG single-orbital entropies for active-space selection, trained on 5,796 transition-metal complexes ([Golub et al. 2020](https://arxiv.org/abs/2011.14715)). Another model predicts mutual information to set orbital ordering ([Golub, Antalík, Beran & Brabec 2023](https://asep.lib.cas.cz/arl-cav/en/detail-cav_un_epca-0566845-Mutual-information-prediction-for-strongly-correlated-systems); effect sizes not retrievable). A graph network corrects low-M energies to within 1 mEh at M=750–1250 ([Golub, Yang, Vlček & Veis 2025](https://arxiv.org/abs/2412.07607)), extended to excitation energies in 2026 ([Golub & Veis 2026, arXiv:2609.12616](https://arxiv.org/abs/2609.12616); abstract only). None of them touches the initial MPS.

Neighbouring fields show what success looks like. A network that predicts the Kohn–Sham density matrix gives a self-consistent-field initial guess "far superior to any other recipes available" ([Hazra, Patil & Sanvito 2024](https://arxiv.org/abs/2401.06533)). Pretrained molecular neural wavefunctions need "only few fine-tuning steps" ([Scherbela, Gerard & Grohs 2023](https://arxiv.org/abs/2307.09337)). Meta-learned and tensor-network-pretrained circuit initializers were publishable because they fixed a real pathology, barren plateaus ([Sauvage et al. 2021](https://arxiv.org/abs/2103.08572); [Rudolph et al. 2023](https://arxiv.org/abs/2208.13673)). DMRG's analogous pathology is metastability and wrong-sector convergence.

### Where the project fits

The proposal is novel as a benchmarked method: every ingredient exists, but they have never been assembled and measured together. It fits in three places, in descending order of expected payoff. The first is **a learned proposal distribution over basins and sectors**, replacing hand pinning, multi-start stripe searches and broken-symmetry enumeration wherever the start decides the answer. The second is **amortized continuation** for families with no converged neighbour: disorder ensembles, new geometries and sizes, and dense parameter scans. The third is **a joint chemistry predictor** that outputs the mutual-information graph, ordering, orbitals and a CI-DEAS-like seed or broken-symmetry pattern together.

It is not a general accelerator for gapped chains, where schedule tuning already supplies the constant factor. The cleanest framing is "Hamiltonian-conditioned generator plus a few DMRG sweeps." DMRG removes the accuracy floor of zero-shot generators, such as Hamilton-Zero's 4–13%. The generator removes DMRG's weakness at choosing a basin.

## A benchmark design the literature has never run

### Measure the dose–response curve before training anything

No study plots sweeps or wall time against initial-state fidelity or energy across many starts for one Hamiltonian. No study counts how often random starts get stuck as a function of model, size and algorithm.

The first experiment needs no neural network. Take converged ground states and degrade them in a controlled way: truncate them to χ₀ ∈ {1, 2, 4, 8, 16}, mix in noise, or substitute a deliberately wrong-basin state. Run each start under one fixed schedule with two-site DMRG plus noise, with DMRG3S and with CBE, each with default and with zero noise. Record sweeps and wall time to a fixed variance and extrapolated energy.

The resulting curve shows whether the dependence is logarithmic, as local theory predicts, or has thresholds at basin boundaries. It also bounds the maximum gain any learned initializer can achieve and shows which Hamiltonians are worth training on.

### Baselines a learned start must beat

| Baseline | Why it is strong | Source |
|---|---|---|
| QN-correct random MPS (linkdims≈10) with bond-dimension ramp and subspace expansion or CBE | Schedule and algorithm alone give 2–6× | [Sehlstedt et al. 2026](https://arxiv.org/html/2607.28369), [Hubig 2015](https://arxiv.org/abs/1501.05504), [ITensor tutorial](https://github.com/ITensor/ITensorMPS.jl/blob/main/docs/src/tutorials/DMRG.md) |
| Best product state (Néel, ±, holes placed at stripe positions) | The 2026 LLM agent's winners; free | [Mantilla Calderón 2026](https://arxiv.org/abs/2604.25610), [Jiang, Scalapino & White 2021](https://arxiv.org/abs/2104.10149) |
| Converged MPS from the nearest parameter point plus a few sweeps | Likely strongest in smooth regions; the first question a reviewer will ask | [Xavier 2018](https://arxiv.org/abs/1809.04029), [Zima 2025](https://arxiv.org/abs/2501.09692) |
| Reduced-basis or interpolated MPS snapshots | Non-neural amortization over a parameter domain | [Brehmer 2023](https://arxiv.org/abs/2304.13587) |
| Gaussian MPS (quasi-1D fermions); Gutzwiller parton MPS (spin liquids); RRG seeds (degenerate chains) | Near-free construction; published random-vs-seeded numbers | [Fishman & White 2015](https://arxiv.org/abs/1504.07701), [Jin, Tu & Zhou 2021](https://arxiv.org/abs/2009.04129), [Block 2021](https://quantumoptics.physics.berkeley.edu/s/2021-Performance-of-the-rigorous-renormalization-group-for-first-order-phase-transitions-and-topolog.pdf) |
| Temporary pinning plus multi-start, compared by extrapolated energy | Current 2D Hubbard and t-J practice | [Qin 2020](https://arxiv.org/abs/1910.08931), [Stoudenmire & White 2012](https://arxiv.org/abs/1105.1374) |
| CI-DEAS, Hartree–Fock or CCSD occupations with Fiedler+GA ordering and split-localized orbitals; broken-symmetry enumeration for clusters | Production chemistry defaults | [ORCA 6.1](https://www.faccts.de/docs/orca/6.1/manual/contents/modelchemistries/dmrg.html), [Zhai 2023](https://arxiv.org/abs/2310.03920), [Zhai 2026](https://arxiv.org/abs/2601.04621) |

### Metrics that separate speed from correctness

"Converged" must mean more than a stable energy. Entropy and long-range correlators lag behind the energy. A low variance shows only that ψ is close to some eigenstate: the check "does not ensure that psi is the ground state, but only one of the eigenstates" ([ITensor DMRG FAQ](https://itensor.github.io/ITensors.jl/stable/faq/DMRG.html)). And fixed-m energies can rank competing states wrongly, as Ehlers et al. and Hagymási showed.

Time to solution should therefore require four things at once: a variance threshold, an energy extrapolated in truncation error, a converged entropy, and a converged target correlator. Report wall time three ways: without network cost, with inference and MPS conversion, and with training cost amortized over a family of instances. The last gives a break-even instance count N*. It matters because the reverse-direction pretraining study turned 3–8× fewer iterations into at most 1.6× in wall time.

Alongside timings, report the probability of landing in the correct sector or basin across seeds and instances, and the final bond dimension needed. Add anytime curves of energy error against cumulative time, medians and 90th-percentile tails (since benefits concentrate in hard instances), and out-of-distribution results at unseen couplings, larger sizes and wider cylinders.

### Concrete testbeds, ordered from calibration to payoff

| Experiment | Systems | What it answers |
|---|---|---|
| A. Calibration (runtime only) | S=1 Heisenberg chain with periodic boundaries (the White/Hubig benchmark); off-critical transverse-field Ising; width-4 Hubbard | Whether a learned start beats a tuned random start when only speed is at stake; the overhead floor |
| B. Cheap basin selection | Mixed-field Ising near the first-order line and ZXZ+XX at N=32 ([Block 2021](https://quantumoptics.physics.berkeley.edu/s/2021-Performance-of-the-rigorous-renormalization-group-for-first-order-phase-transitions-and-topolog.pdf)); 6×6 Kitaev cylinder with published random and Gutzwiller numbers ([Jin 2021](https://arxiv.org/abs/2009.04129)) | Probability of reaching the correct basin or flux sector at affordable sizes |
| C. Amortization | Random-bond XXZ and random-singlet chains; spin-1 bilinear–biquadratic parameter scans; near-critical XXZ at Δ≈1 | Whether one model beats continuation and reduced-basis surrogates where no converged neighbour exists |
| D. 2D competing orders | Hubbard and t-J at 1/8–1/5 doping on width 4 → 6 → 8 cylinders; kagome and triangular YC8–YC12 in both sectors | Transfer across widths where the physics changes, and whether learned starts shorten metastable episodes at large m |
| E. Chemistry | Polycyclic aromatic hydrocarbon active spaces (Golub dataset), N₂ and Cr₂ dissociation curves, [2Fe-2S] and [4Fe-4S] clusters, possibly the announced 50,000-point DMRG-SCF dataset (public availability unverified; [Gugler & Glaser 2025](https://neurips.cc/virtual/2025/126043)) | Whether jointly predicting ordering, orbitals and seed beats Fiedler+GA with CI-DEAS, and whether predicted broken-symmetry patterns can prune reference enumeration |

### Design constraints the evidence imposes on the generator

**Output.** The generator must emit a block-sparse MPS with exact quantum-number labels on every bond, because "the initial guess determines the charge sector of the target state" ([TeNPy v1](https://arxiv.org/abs/2408.02010)). It should be conditioned on sector labels: particle number, S^z or SU(2) label, momentum, spinon parity and chirality sign. It must allow complex amplitudes so chiral phases are reachable. It should produce several diverse seeds rather than one, because the documented practice is multi-start and the hard cases are near-degenerate. A moderate χ₀ suffices; parton starts at truncation error 0.25 already worked.

**Training.** The output is an MPS, so its energy can be computed by exact contraction without Monte Carlo. The loss should therefore be a sum of local energy terms rather than a global fidelity. A lower-risk hybrid lets the network predict mean-field, parton or Gaussian-gate parameters and keeps the cheap Fishman–White or Gutzwiller conversion. That keeps results directly comparable with the Gutzwiller-guided studies of 2021–2025.

**Evaluation.** Evaluation must run both with and without noise. Noise can scramble a good start, while correct bond-level sectors can make noise-free single-site DMRG viable. Approach first-order lines from both sides to detect bias. Apply the symmetry-restoration test: "If DMRG restores a symmetry explicitly broken by the initial state, one has strong evidence against that particular ordering scenario" ([Stoudenmire & White 2012](https://arxiv.org/abs/1105.1374)). Compare extrapolated energies, not fixed-m ones. In exactly the regimes where the network has the most upside, a confidently wrong start costs more than a random one.

### Open questions the project can answer

Several questions remain open, and each is a deliverable in its own right. The most basic is **which property of a start predicts time to solution**. The evidence argues against the start's energy (kagome) and against its fidelity (Kitaev), and points instead to basin, sector and entanglement structure, but no study has varied these systematically.

A second set of questions concerns the optimizer. Nobody has measured how much noise, subspace expansion and CBE preserve or destroy of a good start, or which noise schedule is best when the start is good. The seed-to-seed variance of outcomes is unknown for two-site DMRG, DMRG3S, CBE and VUMPS. It is also unknown whether a supplied start can escape DMRG's low-entanglement bias, or whether DMRG always re-projects onto a minimally entangled or broken state.

A third set concerns transfer and conversion. Embedding a thin cylinder's MPS into a wider one is unmeasured. So are chemistry transfers across basis sets and geometries, and warm starts derived from PEPS, MERA or QMC. Exact RBM conversion, sampled fitting and tensor cross interpolation have never been compared for fidelity per unit cost. Finally, there are no statistics on how often generic starts land in the wrong spin state or broken-symmetry basin of a metal cluster.

## Corrections and verification flags carried from the research notes

The researchers found several commonly repeated attributions to be wrong. Fix these before citing.

| Commonly cited as | What was verified | Source |
|---|---|---|
| Li, Guo, Sun & Chan, P-cluster study, in *Science* | Published in **Nature Chemistry** (Nov 2019) | [arXiv:1810.10196](https://arxiv.org/abs/1810.10196); [Caltech record](https://authors.library.caltech.edu/91401/) |
| Aghaei, Bauer, Shtengel & **Mong** 2020, on Weyl semimetals | Fourth author is **Ryan V. Mishmash**; the title concerns weak Mott insulators on the triangular lattice; no Weyl-semimetal content | [arXiv:2009.12435](https://arxiv.org/abs/2009.12435) |
| Xu, …, Chan, Zhang 2024 (*Science*) | The arXiv author list (Xu, Chung, Qin, Schollwöck, White, Zhang) does **not** include G. K.-L. Chan | [arXiv:2303.08376](https://arxiv.org/abs/2303.08376) |
| Samajdar et al. kagome Rydberg study as PRL 2020 | The kagome paper is **PNAS 118 (2021)**; PRL 2020 is the square-lattice paper | [arXiv:2011.12295](https://arxiv.org/abs/2011.12295) |
| Golub, Yang, Vlček & Veis, CPL 813 (2023), mutual-information prediction | CPL 813, 140297 is by **Golub, Antalík, Beran & Brabec**; Golub–Yang–Vlček–Veis is the JPCL 2025 Δ-ML paper | [ASEP record](https://asep.lib.cas.cz/arl-cav/en/detail-cav_un_epca-0566845-Mutual-information-prediction-for-strongly-correlated-systems) |
| Goldt as co-author of the 2025 foundation-NQS paper | Goldt is not an author; he co-authored the 2024 fine-tuning paper | [arXiv:2502.09488](https://arxiv.org/abs/2502.09488), [arXiv:2403.07795](https://arxiv.org/abs/2403.07795) |
| Rad, Seif & Linke 2022 as a VQE initializer | Demonstrated on a Bars-and-Stripes generative model, **not VQE** | [arXiv:2203.02464](https://arxiv.org/abs/2203.02464) |
| "Computational complexity of PEPS" as the MPS ground-state hardness result | That is Schuch, Wolf, Verstraete & Cirac 2007 on PEPS contraction; the MPS result is Schuch, Cirac & Verstraete 2008 | [quant-ph/0611050](https://arxiv.org/abs/quant-ph/0611050), [arXiv:0802.3351](https://arxiv.org/abs/0802.3351) |
| Eisert on tensor-network barren plateaus | No such paper found; Eisert's relevant result is the 2006 NP-hardness proof | [quant-ph/0609051](https://arxiv.org/abs/quant-ph/0609051) |
| Garcia, Zhao, Bu & Jaffe as an MPS-landscape result | The paper concerns learning scramblers with quantum neural networks | [arXiv:2205.06679](https://arxiv.org/abs/2205.06679) |
| Jin, Natori, Pollmann & Knolle 2022 as a Gutzwiller-boost benchmark | The text read does not describe its DMRG as parton-initialized | [arXiv:2107.13364](https://arxiv.org/abs/2107.13364) |
| Lami, Carleo & Collura, "MPS-based NQS" | The paper is "MPS with backflow correlations," PRB 106, L081111 (2022) | [arXiv:2201.00810](https://arxiv.org/abs/2201.00810) |

Several items could not be verified fully.

**Seen only as an abstract or title, or known through a citing paper.** The 2019 Marks–Jiang–Devereaux talk (abstract only). The JCTC 2025 paper "Bridging the Gap between Transformer-Based Neural Networks and Tensor Networks," whose MPS-to-transformer direction is inferred from a citing paper and shared authors. "Symmetry-Blocked Matrix Product States as a Neural-Network Quantum-State Ansatz," JCTC 22, 8350 (2026), title only, authors unknown. And seven 2026 preprints: [arXiv:2601.20950](https://arxiv.org/abs/2601.20950) (HyperRBM), [arXiv:2609.12616](https://arxiv.org/abs/2609.12616) (Golub & Veis), [arXiv:2609.25384](https://arxiv.org/abs/2609.25384) (lattice compilation), [arXiv:2609.37733](https://arxiv.org/abs/2609.37733) (molecular foundation NQS), [arXiv:2605.30141](https://arxiv.org/abs/2605.30141), [arXiv:2602.15706](https://arxiv.org/abs/2602.15706) and [arXiv:2601.10194](https://arxiv.org/abs/2601.10194).

**Content or effect sizes not retrieved.** The Golub 2023 CPL paper, the paywalled Olivares-Amaya 2015 ordering comparisons, and the 2023 *J. Chem. Phys.* "ML MPS ansatz" paper, whose authors are also unknown.

**Resting on memory, earlier fetches or paraphrase.** Rohwedder & Uschmajew 2013, the Mantilla Calderón numbers (from an earlier HTML v2 fetch, not re-fetched), the Zhu–White "two-spinon sector" wording, and the Pastori et al. 2019 description.

**Venues and details unverified.** The Shen–Qian–Qin Chinese Physics B version; Xavier et al., PRB 98, 195115; Capponi et al., PRB 88, 144416; the Wouters & Van Neck EPJ D reference; volume and page numbers the warm-start notes mark with †; the units of the Kan et al. 2024 timing table; and the public availability of the 50,000-point DMRG-SCF dataset.

## Conclusion

The literature changes the project's question from "fewest sweeps" to "right basin, chosen cheaply." The costs that dwarf warm-up sweeps all come from wrong or uncertain basins: crystals metastable to m≈2400, stripes that win at every affordable bond dimension, flux sectors that random starts always miss, and 78,750 UHF guesses filtered to 840 references for one cluster. The conventional measures of a start also predict little. A quarter-truncated parton start still halved the sweeps on Kitaev, and on kagome a higher-energy ansatz beat the lowest-energy one. A neural network is therefore best built as a learned, sector-conditioned proposal distribution over basins, with DMRG doing the refinement. A network that emits one confident state would reproduce the bias of pinning fields without the multi-start check practitioners use to catch it.

The idea is open, and defending it requires a disciplined order of work. First, measure the curve of sweeps versus start quality. Then beat tuned random schedules and parameter continuation, counting network and amortized training cost. The likeliest early wins are the cheapest testbeds with published random-start failures: Block's 32-site first-order and edge-degenerate chains, and the 6×6 Kitaev cylinder with Gutzwiller numbers to beat. Disorder ensembles come next, since continuation has no neighbour there. In chemistry, the evidence points away from predicting MPS tensors directly. It favours one model that jointly predicts the mutual-information graph, ordering, orbitals and broken-symmetry pattern. On the older, qualitative estimate cited in 2014, ordering and orbitals outweigh the MPS guess by about an order of magnitude. And the expensive step at the frontier is enumerating references, not warming up the MPS.
