"""Exhibit 24 — three sites, three risk structures.

Channel shares of site-level ClimVaR, from Exhibit 22 (V8 model results,
BAU/MEAN). One 100% bar per site, read left to right.
"""
import matplotlib.pyplot as plt
from sestyle import SE, accentbar, titleblock, save

CH = {"Business interruption": "#245C46", "Cooling": "#8FD9A0",
      "Physical damage": "#3DCD58", "Carbon costs": "#AEBDB4", "Heat productivity": "#C4E7CE"}
SHORT = {"Business interruption": "Interruption", "Cooling": "Cooling",
         "Physical damage": "Damage", "Carbon costs": "Carbon", "Heat productivity": "Heat"}
SITES = [  # name, profile, total US$M, intensity, {channel: US$M}
    ("Site A (US South)", "The supply chain problem", 902, "46.5%",
     {"Business interruption": 384, "Cooling": 336, "Physical damage": 143,
      "Carbon costs": 28, "Heat productivity": 11}),
    ("Site B (France)", "The flood trap", 3560, "167%",
     {"Business interruption": 374, "Cooling": 459, "Physical damage": 2678,
      "Carbon costs": 42, "Heat productivity": 6}),
    ("Site C (S. China)", "The triple threat", 517, "37.6%",
     {"Business interruption": 276, "Cooling": 96, "Physical damage": 29,
      "Carbon costs": 113, "Heat productivity": 4}),
]

fig, ax = plt.subplots(figsize=(7.6, 3.6))
fig.subplots_adjust(left=0.215, right=0.80, top=0.76, bottom=0.17)
for i, (name, prof, tot, inten, ch) in enumerate(SITES):
    s = sum(ch.values())
    left = 0
    for k in CH:
        v = ch[k] / s * 100
        ax.barh(i, v, left=left, height=0.6, color=CH[k], edgecolor="white", lw=1.2, zorder=3)
        col = "white" if k == "Business interruption" else SE["dark"]
        if v >= 9:
            lab = SHORT[k] if v >= 15 else {"Interruption": "BI"}.get(SHORT[k], SHORT[k])
            ax.text(left + v / 2, i + 0.06, lab, ha="center", va="bottom",
                    fontsize=7.6, fontweight="semibold", color=col)
            ax.text(left + v / 2, i + 0.06, f"{v:.0f}%", ha="center", va="top",
                    fontsize=7.6, color=col)
        elif v >= 3:
            ax.text(left + v / 2, i, f"{v:.0f}", ha="center", va="center",
                    fontsize=6.8, color=col)
        left += v
    ax.text(-2, i - 0.12, name, ha="right", va="center", fontsize=9, fontweight="bold",
            color=SE["dark"])
    ax.text(-2, i + 0.20, prof, ha="right", va="center", fontsize=7.6, color=SE["text2"])
    ax.text(102, i - 0.12, f"US\\${tot:,}M", ha="left", va="center", fontsize=9.5,
            fontweight="bold", color=SE["dark"])
    ax.text(102, i + 0.20, f"{inten} of enterprise value", ha="left", va="center",
            fontsize=7.6, color=SE["text2"])
ax.set_xlim(0, 100)
ax.set_ylim(2.55, -0.55)
ax.axis("off")
kx = 0.12
for k, c in CH.items():
    fig.add_artist(plt.Rectangle((kx, 0.05), 0.016, 0.03, transform=fig.transFigure,
                                 facecolor=c, edgecolor="none"))
    fig.text(kx + 0.022, 0.065, k, fontsize=7.4, va="center", color=SE["dark"])
    kx += 0.036 + 0.0088 * len(k)
accentbar(fig, y=0.985)
titleblock(fig, "Three sites, three risk structures",
           "Share of site-level ClimVaR by channel, with total ClimVaR and intensity, BAU/MEAN",
           x=0.008, y=0.955)
save(fig, "ex_cases.pdf")
