NAVY = "#1f4e79"
INK = "#13304d"
FILL = "#f2f6fb"
FILL2 = "#e3ecf7"
MUTED = "#4a5a6c"
AMBER = "#a8641a"


def _text(x, y, s, size=10, weight=400, anchor="start", fill=INK, style=""):
    return (f'<text x="{x}" y="{y}" font-family="Inter" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill}" {style}>{s}</text>')


def _box(x, y, w, h, fill=FILL, stroke=NAVY, rx=6, sw=1.2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def _arrow(x1, y1, x2, y2, color=NAVY):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.4" marker-end="url(#ah)"/>'


def _mps(x, y, n=6, dx=13, color=NAVY, fill="#ffffff"):
    parts = [f'<line x1="{x}" y1="{y}" x2="{x + dx * (n - 1)}" y2="{y}" stroke="{color}" stroke-width="1.3"/>']
    for i in range(n):
        cx = x + dx * i
        parts.append(f'<line x1="{cx}" y1="{y}" x2="{cx}" y2="{y + 9}" stroke="{color}" stroke-width="1.1"/>')
        parts.append(f'<circle cx="{cx}" cy="{y}" r="4.2" fill="{fill}" stroke="{color}" stroke-width="1.2"/>')
    return "".join(parts)


def fig1():
    W, H = 660, 262
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Pipeline from Hamiltonian to generator to seeds to DMRG refinement">',
         '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{NAVY}"/></marker></defs>']
    top, h = 14, 176
    # Box 1: input
    o.append(_box(0, top, 138, h))
    o.append(_text(12, top + 22, "Input", 12, 650))
    lines = ["Hamiltonian H(&#952;)", "lattice graph", "couplings J, t, U, fields", "MPS path through sites"]
    for i, s in enumerate(lines):
        o.append(_text(12, top + 44 + 15 * i, s, 10, 400, fill=MUTED))
    o.append(_text(12, top + 118, "Target sector", 10, 600))
    for i, s in enumerate(["N, S<tspan baseline-shift='super' font-size='7'>z</tspan> or SU(2) label,", "momentum, chirality"]):
        o.append(_text(12, top + 133 + 14 * i, s, 10, 400, fill=MUTED))
    o.append(_arrow(140, top + h / 2, 160, top + h / 2))
    # Box 2: generator
    x2, w2 = 162, 176
    o.append(_box(x2, top, w2, h, fill=FILL2, sw=1.6))
    o.append(_text(x2 + 12, top + 22, "Generator network", 12, 650))
    o.append(_text(x2 + 12, top + 39, "graph or transformer encoder", 10, 400, fill=MUTED))
    routes = [("A", "mean-field or parton ansatz"), ("B", "symmetric MPS tensors"), ("C", "neural state &#8594; MPS")]
    for i, (k, s) in enumerate(routes):
        yy = top + 50 + 27 * i
        o.append(f'<rect x="{x2 + 10}" y="{yy}" width="{w2 - 20}" height="21" rx="4" fill="#ffffff" stroke="#9fb6d3" stroke-width="0.9"/>')
        o.append(_text(x2 + 19, yy + 14.5, k, 10, 700, fill=NAVY))
        o.append(_text(x2 + 32, yy + 14.5, s, 9.5, 400, fill=INK))
    o.append(_text(x2 + 12, top + 150, "loss: sum of local energy terms", 9.5, 400, fill=MUTED))
    o.append(_text(x2 + 12, top + 164, "+ diversity across the K seeds", 9.5, 400, fill=MUTED))
    o.append(_arrow(x2 + w2 + 2, top + h / 2, x2 + w2 + 20, top + h / 2))
    # Box 3: seeds
    x3, w3 = 360, 122
    o.append(_box(x3, top, w3, h))
    o.append(_text(x3 + 12, top + 22, "K seeds", 12, 650))
    for i in range(3):
        o.append(_mps(x3 + 22, top + 46 + 30 * i, n=6, dx=15))
    o.append(_text(x3 + 12, top + 146, "QN label on every bond", 9.5, 400, fill=MUTED))
    o.append(_text(x3 + 12, top + 160, "complex, &#967;<tspan baseline-shift='sub' font-size='7'>0</tspan> &#8804; 32", 9.5, 400, fill=MUTED))
    o.append(_arrow(x3 + w3 + 2, top + h / 2, x3 + w3 + 20, top + h / 2))
    # Box 4: DMRG
    x4, w4 = 504, 156
    o.append(_box(x4, top, w4, h))
    o.append(_text(x4 + 12, top + 22, "Short DMRG", 12, 650))
    o.append(_text(x4 + 12, top + 37, "refinement", 12, 650))
    for i, s in enumerate(["two-site or CBE sweeps", "from each seed", "select by extrapolated", "energy, then apply the", "symmetry-restoration test"]):
        o.append(_text(x4 + 12, top + 60 + 15 * i, s, 10, 400, fill=MUTED))
    # output pill
    o.append(_arrow(x4 + 118, top + h + 2, x4 + 118, 214))
    o.append(f'<rect x="{x4 + 38}" y="216" width="{w4 - 38}" height="28" rx="14" fill="{NAVY}"/>')
    o.append(_text(x4 + 38 + (w4 - 38) / 2, 234, "ground state in sector", 10, 600, anchor="middle", fill="#ffffff"))
    # feedback loop
    fy = 232
    o.append(f'<path d="M {x4 + 30} {top + h} L {x4 + 30} {fy} L {x2 + w2 / 2} {fy} L {x2 + w2 / 2} {top + h + 3}" fill="none" '
             f'stroke="{AMBER}" stroke-width="1.3" stroke-dasharray="5 3" marker-end="url(#ahb)"/>')
    o.insert(1, '<defs><marker id="ahb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{AMBER}"/></marker></defs>')
    o.append(_text((x4 + 30 + x2 + w2 / 2) / 2, fy + 16, "converged states and timings become training data", 9.5, 500, anchor="middle", fill=AMBER))
    o.append("</svg>")
    return "".join(o)


def fig2():
    W, H = 660, 242
    x0, x1 = 210, 652
    pm = (x1 - x0) / 12.0
    X = lambda m: x0 + pm * m
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Twelve-month plan with five phases and three gates">']
    # axis
    for m in range(0, 13):
        x = X(m)
        o.append(f'<line x1="{x}" y1="22" x2="{x}" y2="190" stroke="#e3e8ef" stroke-width="0.8"/>')
        if m % 2 == 0:
            o.append(_text(x, 14, f"M{m}", 9, 500, anchor="middle", fill=MUTED))
    phases = [
        ("Setup", "harness, baselines, code choice", 0, 1, "#c9d8ea"),
        ("WP1 Calibration", "start quality vs. time-to-solution", 1, 3, "#a9c2df"),
        ("WP2 + WP3 Generator v1", "Route A, 1D basin-selection chains", 3, 6, "#86a8d0"),
        ("WP3 + WP4 Cylinders", "Kitaev 6&#215;6, Hubbard / t-J width 4&#8594;6&#8594;8", 6, 10, "#5f88bb"),
        ("WP5 + write-up", "amortization over families; paper 2", 10, 12, "#3f6ea5"),
    ]
    for i, (name, desc, a, b, col) in enumerate(phases):
        y = 28 + 33 * i
        o.append(_text(0, y + 11, name, 10.5, 650))
        o.append(_text(0, y + 25, desc, 9, 400, fill=MUTED))
        o.append(f'<rect x="{X(a) + 1}" y="{y + 2}" width="{X(b) - X(a) - 2}" height="24" rx="4" fill="{col}"/>')
    # gates
    gates = [("A", 3, "headroom?"), ("B", 6, "beats baselines?"), ("C", 10, "transfers in width?")]
    for g, m, lab in gates:
        x = X(m)
        o.append(f'<line x1="{x}" y1="22" x2="{x}" y2="196" stroke="{AMBER}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        o.append(f'<path d="M {x} 194 L {x + 8} 203 L {x} 212 L {x - 8} 203 Z" fill="{AMBER}"/>')
        o.append(_text(x, 207, g, 9, 700, anchor="middle", fill="#ffffff"))
        o.append(_text(x, 225, f"Gate {g}", 9, 700, anchor="middle", fill=AMBER))
        o.append(_text(x, 236, lab, 8.5, 500, anchor="middle", fill=AMBER))
    o.append("</svg>")
    return "".join(o)
