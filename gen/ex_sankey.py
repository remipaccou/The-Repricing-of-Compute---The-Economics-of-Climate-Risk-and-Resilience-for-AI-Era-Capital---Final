"""Exhibit 11 — fine hazards, five channels, where the loss arises.

Amounts are the driver-to-scope bands in sankey_repricing.tex (US$387.5B,
nothing left over). Each hazard keeps the direct-operation and supply-chain
split measured there. Wind is US$60.4B through business interruption into
the supply chain and US$7.2B through business interruption into direct
operations. Flood is US$37.4B supply chain and US$85.0B direct operations.
"""
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
from sestyle import SE, accentbar, titleblock, save

TOTAL = 387.5

C = {
    "Flood": "#3DCD58", "Carbon pricing": "#AEBDB4", "Extreme heat": "#8FD9A0",
    "Wind": "#1F8C32", "Drought": "#C4E7CE", "Fire": "#0A2F24",
    "Business interruption": "#245C46", "Carbon costs": "#AEBDB4",
    "Physical damage": "#3DCD58", "Cooling": "#8FD9A0", "Heat productivity": "#C4E7CE",
    "Direct operations": "#5E8F79", "Upstream supply chain": "#0A2F24",
}

COL1 = [("Wind", 67.6), ("Drought", 13.6), ("Flood", 122.4),
        ("Carbon pricing", 107.0), ("Fire", 1.9), ("Extreme heat", 75.0)]
COL2 = [("Business interruption", 118.6), ("Carbon costs", 107.0),
        ("Physical damage", 86.9), ("Cooling", 72.6), ("Heat productivity", 2.4)]
COL3 = [("Upstream supply chain", 218.3), ("Direct operations", 169.2)]

# Link order is top-to-bottom within each bar, so wind's lower slice
# (US$7.2B) is the whole of business interruption that exits to direct
# operations, and its upper slice (US$60.4B) exits to the supply chain.
L12 = [("Wind", "Business interruption", 60.4),
       ("Drought", "Business interruption", 13.6),
       ("Flood", "Business interruption", 37.4),
       ("Wind", "Business interruption", 7.2),
       ("Flood", "Physical damage", 85.0),
       ("Fire", "Physical damage", 1.9),
       ("Carbon pricing", "Carbon costs", 107.0),
       ("Extreme heat", "Cooling", 72.6),
       ("Extreme heat", "Heat productivity", 2.4)]
L23 = [("Business interruption", "Upstream supply chain", 111.4),
       ("Business interruption", "Direct operations", 7.2),
       ("Carbon costs", "Upstream supply chain", 106.9),
       ("Carbon costs", "Direct operations", 0.1),
       ("Physical damage", "Direct operations", 86.9),
       ("Cooling", "Direct operations", 72.6),
       ("Heat productivity", "Direct operations", 2.4)]

H = 100.0
MINH = 1.4
XN = {0: (0.00, 0.028), 1: (0.345, 0.373), 2: (0.965, 0.993)}
HALO = [pe.withStroke(linewidth=2.6, foreground="white")]


def layout(nodes, gap):
    hs = [max(v / TOTAL * H, MINH) for _, v in nodes]
    scale = (H - gap * (len(nodes) - 1)) / sum(hs)
    hs = [h * scale for h in hs]
    out, y = {}, H
    for (name, v), h in zip(nodes, hs):
        out[name] = (y - h, y, v)
        y -= h + gap
    return out


P1, P2, P3 = layout(COL1, 3.2), layout(COL2, 2.6), layout(COL3, 3.2)

fig = plt.figure(figsize=(7.6, 4.6))
ax = fig.add_axes([0.150, 0.02, 0.77, 0.80])
ax.set_xlim(-0.11, 1.11)
ax.set_ylim(-12, H + 4)
ax.axis("off")


def ribbon(x0, x1, y0a, y0b, y1a, y1b, colour, alpha=0.42):
    t = np.linspace(0, 1, 140)
    s = 3 * t**2 - 2 * t**3
    ax.fill_between(x0 + (x1 - x0) * t,
                    y0a + (y1a - y0a) * s, y0b + (y1b - y0b) * s,
                    color=colour, alpha=alpha, lw=0, zorder=2)


for pos, xr in ((P1, XN[0]), (P2, XN[1]), (P3, XN[2])):
    for name, (b, t, _) in pos.items():
        ax.add_patch(plt.Rectangle((xr[0], b), xr[1] - xr[0], t - b,
                                   color=C[name], lw=0, zorder=4))

for links, (pa, xa), (pb, xb), colour_from in (
        (L12, (P1, XN[0][1]), (P2, XN[1][0]), "dst"),
        (L23, (P2, XN[1][1]), (P3, XN[2][0]), "src")):
    out = {k: v[1] for k, v in pa.items()}
    inn = {k: v[1] for k, v in pb.items()}
    for src, dst, val in links:
        hs = val / pa[src][2] * (pa[src][1] - pa[src][0])
        hd = val / pb[dst][2] * (pb[dst][1] - pb[dst][0])
        ribbon(xa, xb, out[src] - hs, out[src], inn[dst] - hd, inn[dst],
               C[dst if colour_from == "dst" else src],
               alpha=0.42 if val > 1.0 else 0.66)
        out[src] -= hs
        inn[dst] -= hd


def declutter(items, minsep, lo, hi):
    ys = [y for _, y in items]
    for i in range(1, len(ys)):
        ys[i] = min(ys[i], ys[i - 1] - minsep)
    if ys[-1] < lo:
        ys = [y + (lo - ys[-1]) for y in ys]
    for i in range(len(ys) - 2, -1, -1):
        ys[i] = max(ys[i], ys[i + 1] + minsep)
    return [(items[i][0], min(ys[i], hi)) for i in range(len(ys))]


def label(pos, x, ha, minsep, anchor, halo=False, lo=3.0):
    items = [(n, (b + t) / 2) for n, (b, t, _) in pos.items()]
    for name, y in declutter(items, minsep, lo, H - 1.0):
        b, t, v = pos[name]
        yc = (b + t) / 2
        if abs(y - yc) > 1.2:
            xm = x + (anchor - x) * 0.25
            ax.plot([anchor, xm, xm], [yc, yc, y],
                    color=SE["muted"], lw=0.5, zorder=3,
                    solid_joinstyle="round")
        kw = dict(path_effects=HALO) if halo else {}
        ax.text(x, y + 2.0, name, ha=ha, va="center", fontsize=8.4,
                fontweight="semibold", color=SE["dark"], zorder=6, **kw)
        amount = f"{v:.0f}" if abs(v - round(v)) < 0.05 else f"{v:.1f}"
        share = f"{v / TOTAL * 100:.1f}" if v / TOTAL < 0.01 else f"{v / TOTAL * 100:.0f}"
        ax.text(x, y - 2.6, f"US${amount}B    {share}%",
                ha=ha, va="center", fontsize=7.3, color=SE["text2"],
                zorder=6, **kw)


label(P1, XN[0][0] - 0.016, "right", 11.0, anchor=XN[0][0], lo=-10.0)
label(P2, XN[1][1] + 0.016, "left", 10.4, anchor=XN[1][1], halo=True, lo=-26.0)
label(P3, XN[2][0] - 0.016, "right", 11.0, anchor=XN[2][0], halo=True, lo=-10.0)

for x, name, ha in ((XN[0][0], "HAZARD", "left"),
                    (XN[1][0], "RISK CHANNEL", "left"),
                    (XN[2][1], "WHERE THE LOSS ARISES", "right")):
    ax.text(x, H + 5.0, name, fontsize=7.4, color=SE["text2"],
            ha=ha, va="bottom", fontweight="semibold")

accentbar(fig, y=0.985)
titleblock(fig, "How US$388 billion is transmitted",
           "ClimVaR on the installed base by hazard, risk channel and scope, BAU/MEAN, US$ billions",
           x=0.008, y=0.958)
save(fig, "ex_sankey.pdf")
