"""Exhibit 11 — the transmission map: hazard, risk channel, scope of the loss.

Channel and scope totals: ClimVaR_Results_V8, BAU/MEAN, installed base.
Hazard totals: as published in the paper (Shapley attribution). The V8 workbook
does not hold the hazard-by-channel matrix, so hazard-to-channel ribbons follow
the model's mapping rules (carbon pricing to carbon costs, heat to cooling and
heat productivity, wildfire to damage, drought to interruption) and split wind
and flood between interruption and damage to close each channel total. The
residual between the published hazard totals and the channel totals is shown
as "Unattributed".
"""
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
from sestyle import SE, accentbar, titleblock, save

TOTAL = 387.6

C = {
    "Carbon pricing": "#AEBDB4", "Wind": "#1F8C32", "Extreme heat": "#8FD9A0",
    "River flood": "#3DCD58", "Coastal flood": "#7FBFA3", "Drought": "#C4E7CE",
    "Wildfire": "#0A2F24", "Unattributed": "#D5DBD7",
    "Business interruption": "#245C46", "Carbon costs": "#AEBDB4",
    "Physical damage": "#3DCD58", "Cooling": "#8FD9A0", "Heat productivity": "#C4E7CE",
    "Direct operations": "#5E8F79", "Upstream supply chain": "#0A2F24",
}

COL1 = [("Carbon pricing", 107.1), ("Wind", 89.0), ("Extreme heat", 73.0),
        ("River flood", 49.0), ("Coastal flood", 24.0), ("Drought", 18.0),
        ("Wildfire", 14.0), ("Unattributed", 13.5)]
COL2 = [("Business interruption", 121.4), ("Carbon costs", 107.1),
        ("Physical damage", 84.0), ("Cooling", 72.6), ("Heat productivity", 2.4)]
COL3 = [("Direct operations", 170.0), ("Upstream supply chain", 217.6)]

L12 = [("Carbon pricing", "Carbon costs", 107.0), ("Unattributed", "Carbon costs", 0.1),
       ("Wind", "Business interruption", 60.0), ("Wind", "Physical damage", 29.0),
       ("Extreme heat", "Cooling", 70.6), ("Extreme heat", "Heat productivity", 2.4),
       ("River flood", "Business interruption", 21.0), ("River flood", "Physical damage", 28.0),
       ("Coastal flood", "Business interruption", 11.0), ("Coastal flood", "Physical damage", 13.0),
       ("Drought", "Business interruption", 18.0), ("Wildfire", "Physical damage", 14.0),
       ("Unattributed", "Business interruption", 11.4),
       ("Unattributed", "Cooling", 2.0)]
L23 = [("Business interruption", "Direct operations", 10.9),
       ("Business interruption", "Upstream supply chain", 110.5),
       ("Carbon costs", "Upstream supply chain", 107.1),
       ("Physical damage", "Direct operations", 84.0),
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
        ax.text(x, y - 2.6, f"US${v:.0f}B    {v / TOTAL * 100:.0f}%",
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
