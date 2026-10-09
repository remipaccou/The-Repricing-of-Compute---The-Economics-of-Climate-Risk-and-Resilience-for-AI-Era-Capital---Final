"""Exhibit 17 — ClimVaR of the combined portfolio to 2050, by AI growth scenario.

End values: ClimVaR_Results_V8, AI Scenarios, BAU/MEAN (baseline and proactive).
Start: installed base, US$388B baseline and US$238B proactive. The path between
the two ends is indicative (logistic ramp centred on the early 2030s, when most
AI capacity is built); only the end points are model outputs.
"""
import numpy as np
import matplotlib.pyplot as plt
from sestyle import SE, accentbar, titleblock, save

SC = [  # key, name, baseline 2050, proactive 2050, colour
    ("AWB", "Abundance Without\nBoundaries", 3671, 2536, SE["dark"]),
    ("SAI", "Sustainable AI", 1669, 1134, SE["green"]),
    ("LTG", "Limits to Growth", 1008, 669, "#8FD9A0"),
]
B0, P0 = 388, 238


def path(s, e, t):
    sig = 1 / (1 + np.exp(-8 * (t - 0.4)))
    s0, s1 = 1 / (1 + np.exp(3.2)), 1 / (1 + np.exp(-4.8))
    return s + (e - s) * (sig - s0) / (s1 - s0)


yrs = np.linspace(2026, 2050, 200)
t = (yrs - 2026) / 24

fig, ax = plt.subplots(figsize=(7.6, 4.8))
fig.subplots_adjust(left=0.085, right=0.67, top=0.80, bottom=0.11)

for key, name, be, pe_, col in SC:
    b, p = path(B0, be, t), path(P0, pe_, t)
    ax.fill_between(yrs, p, b, color=col, alpha=0.16 if key != "AWB" else 0.10, lw=0, zorder=1)
    ax.plot(yrs, b, color=col, lw=2.3, zorder=4)
    ax.plot(yrs, p, color=col, lw=1.6, ls=(0, (4, 2.2)), zorder=4)

# right-hand labels, nudged apart by hand where scenarios crowd
LAB = {"AWB": (3671, 2536), "SAI": (1669, 1134), "LTG": (1008, 669)}
NUDGE = {"AWB": (0, 0), "SAI": (40, 60), "LTG": (-90, -90)}
for key, name, be, pe_, col in SC:
    nb, np_ = NUDGE[key]
    tc = col if key != "LTG" else "#2E8B4A"
    ax.text(2050.7, be + nb, f"US\\${be / 1000:.1f}T", fontsize=10, fontweight="bold",
            color=tc, va="center", clip_on=False)
    ax.text(2054.2, be + nb, name, fontsize=7.8, color=SE["dark"], va="center", linespacing=1.3, clip_on=False)
    ax.text(2050.7, pe_ + np_, f"US\\${pe_ / 1000:.1f}T  proactive", fontsize=7.6,
            color=SE["text2"], va="center", clip_on=False)

ax.plot([2026], [B0], "o", ms=4.5, color=SE["dark"], zorder=6, clip_on=False)
ax.plot([2026.6, 2026.6], [B0 + 60, 1220], color=SE["muted"], lw=0.5)
ax.text(2026.4, 1250, "US\\$388B today\nUS\\$238B if adapted",
        fontsize=7.6, color=SE["text2"], va="bottom", linespacing=1.35)

ax.set_xlim(2026, 2050)
ax.set_ylim(0, 4000)
ax.set_xticks([2026, 2030, 2035, 2040, 2045, 2050])
ax.set_yticks([0, 1000, 2000, 3000, 4000])
ax.set_yticklabels(["0", "US\\$1T", "US\\$2T", "US\\$3T", "US\\$4T"], fontsize=8.5)
ax.tick_params(axis="x", labelsize=8.5)
ax.grid(axis="y", color=SE["grid"], lw=0.7, zorder=0)
ax.set_axisbelow(True)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color(SE["grid"])
ax.tick_params(axis="y", length=0)

# key: solid vs dashed
ax.plot([2026.6, 2028.2], [3750, 3750], color=SE["dark"], lw=2.3)
ax.text(2028.5, 3750, "Baseline", fontsize=7.8, va="center", color=SE["dark"])
ax.plot([2031.2, 2032.8], [3750, 3750], color=SE["dark"], lw=1.6, ls=(0, (4, 2.2)))
ax.text(2033.1, 3750, "Proactive adaptation", fontsize=7.8, va="center", color=SE["dark"])
ax.add_patch(plt.Rectangle((2040.6, 3660), 1.6, 180, color=SE["dark"], alpha=0.12, lw=0))
ax.text(2042.5, 3750, "Value protected", fontsize=7.8, va="center", color=SE["dark"])

accentbar(fig, y=0.985)
titleblock(fig, "Adaptation bends the curve but does not flatten it",
           "ClimVaR of the installed base plus AI-era capacity, BAU/MEAN, cumulative over asset lifetimes",
           x=0.008, y=0.955)
save(fig, "ex_ribbons.pdf")
