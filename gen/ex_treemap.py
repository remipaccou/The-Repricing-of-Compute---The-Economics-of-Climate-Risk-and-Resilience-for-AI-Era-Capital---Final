"""Exhibit 13 — US$388 billion by region and channel.

Area is proportional to ClimVaR. Regions are laid out two per row, widths in
proportion to their total; inside each region, channels are vertical tiles in
descending order. Source: ClimVaR_Results_V8, Channel Decomposition, BAU/MEAN,
installed base, no adaptation.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from sestyle import SE, accentbar, titleblock, save

CH = {"Business interruption": "#245C46", "Carbon costs": "#AEBDB4",
      "Physical damage": "#3DCD58", "Cooling": "#8FD9A0", "Heat productivity": "#C4E7CE"}
SHORT = {"Business interruption": "Interruption", "Carbon costs": "Carbon",
         "Physical damage": "Damage", "Cooling": "Cooling", "Heat productivity": "Heat"}
WHITE_TEXT = {"Business interruption"}

REG = {
    "United States": (108.3, 27.6, {"Business interruption": 48.4, "Cooling": 27.3,
                                    "Physical damage": 20.3, "Carbon costs": 11.5,
                                    "Heat productivity": 0.8}),
    "China": (110.5, 55.8, {"Carbon costs": 35.9, "Physical damage": 33.3,
                            "Business interruption": 31.3, "Cooling": 9.6,
                            "Heat productivity": 0.4}),
    "Europe": (106.7, 53.1, {"Carbon costs": 44.5, "Business interruption": 25.9,
                             "Cooling": 23.4, "Physical damage": 12.3,
                             "Heat productivity": 0.5}),
    "APMEA": (62.0, 28.2, {"Physical damage": 18.2, "Business interruption": 15.8,
                           "Carbon costs": 15.1, "Cooling": 12.3,
                           "Heat productivity": 0.6}),
}
ROWS = [["United States", "China"], ["Europe", "APMEA"]]
TOTAL = sum(v[0] for v in REG.values())

fig = plt.figure(figsize=(7.6, 5.2))
ax = fig.add_axes([0.008, 0.10, 0.984, 0.71])
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

GAP = 1.6
row_tot = [sum(REG[r][0] for r in row) for row in ROWS]
row_h = [100 * t / TOTAL for t in row_tot]
y_top = 100
for row, rh, rt in zip(ROWS, row_h, row_tot):
    x = 0
    for name in row:
        tot, inten, chans = REG[name]
        w = 100 * tot / rt
        x0, y0, ww, hh = x + GAP / 2, y_top - rh + GAP / 2, w - GAP, rh - GAP
        head = 11.0
        ax.text(x0 + 0.6, y0 + hh - 1.0, name, fontsize=10, fontweight="bold",
                color=SE["dark"], va="top")
        ax.text(x0 + 0.6, y0 + hh - 6.2, f"US${tot:.0f}B ClimVaR   ·   {inten:.0f}% of enterprise value",
                fontsize=7.6, color=SE["text2"], va="top")
        ih = hh - head
        cx = x0
        for ch, v in sorted(chans.items(), key=lambda kv: -kv[1]):
            tw = ww * v / tot
            ax.add_patch(Rectangle((cx, y0), tw, ih, facecolor=CH[ch],
                                   edgecolor="white", lw=1.6))
            col = "white" if ch in WHITE_TEXT else SE["dark"]
            if tw > 5.5:
                lab = SHORT[ch] if tw > 10 else {"Interruption": "BI"}.get(SHORT[ch], SHORT[ch])
                fs = 8 if tw > 10 else 7.2
                ax.text(cx + tw / 2, y0 + ih / 2 + 2.2, lab, ha="center",
                        va="center", fontsize=fs, fontweight="semibold", color=col)
                ax.text(cx + tw / 2, y0 + ih / 2 - 2.6, f"US${v:.0f}B", ha="center",
                        va="center", fontsize=7.6, color=col)
            elif tw > 3.0:
                ax.text(cx + tw / 2, y0 + ih / 2, f"{v:.0f}", ha="center",
                        va="center", fontsize=7, color=col)
            cx += tw
        x += w
    y_top -= rh

# legend
lx = 0.008
for ch, colr in CH.items():
    fig.add_artist(Rectangle((lx, 0.045), 0.016, 0.022, transform=fig.transFigure,
                             facecolor=colr, edgecolor="none"))
    fig.text(lx + 0.022, 0.056, ch, fontsize=7.6, color=SE["dark"], va="center")
    lx += 0.022 + 0.0105 * len(ch) + 0.03

accentbar(fig, y=0.985)
titleblock(fig, "Four regions, four risk structures",
           "ClimVaR on the installed base by region and channel, BAU/MEAN. "
           "Area is proportional to US$ value.", x=0.008, y=0.955)
save(fig, "ex_treemap.pdf")
