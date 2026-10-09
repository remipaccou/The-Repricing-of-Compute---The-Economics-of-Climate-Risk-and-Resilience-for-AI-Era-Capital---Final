"""Exhibits 19, 20 and 21 — what proactive adaptation does, channel by channel,
and what each action costs per dollar of ClimVaR it removes.

19 and 20: ClimVaR_Results_V8, Adaptation Value, BAU/MEAN, installed base.
21: action widths and costs from plot-and-tools/plots/macc.tex (BAU/MEAN),
drawn in the convention of the Hospitality MACC: break-even on the axis, the
light block above each bar is what is kept for every dollar protected.
"""
import matplotlib.pyplot as plt
from sestyle import SE, accentbar, titleblock, save

CH = {"Business interruption": "#245C46", "Carbon costs": "#AEBDB4",
      "Physical damage": "#3DCD58", "Cooling": "#8FD9A0", "Heat productivity": "#C4E7CE"}
V8 = [  # channel, baseline, proactive (US$bn), reduction as reported by V8
    ("Business interruption", 121.4, 77.4, 36),
    ("Carbon costs", 107.1, 39.7, 63),
    ("Physical damage", 84.1, 63.9, 24),
    ("Cooling", 72.6, 55.3, 24),
    ("Heat productivity", 2.4, 1.7, 28),
]


def axstyle(ax, axis="x"):
    ax.grid(axis=axis, color=SE["grid"], lw=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(axis == "y")
    ax.spines["left"].set_color(SE["grid"])
    ax.spines["bottom"].set_color(SE["grid"])


# ---------------------------------------------------------------- Exhibit 19
fig, ax = plt.subplots(figsize=(7.6, 3.9))
fig.subplots_adjust(left=0.215, right=0.84, top=0.78, bottom=0.14)
for i, (ch, b, p, red) in enumerate(V8):
    ax.barh(i, b, height=0.62, color=SE["light"], edgecolor=CH[ch], lw=1.0, zorder=2)
    ax.barh(i, p, height=0.62, color=CH[ch], edgecolor="white", lw=0.8, zorder=3)
    ax.text(b + 2.0, i, f"−{red:.0f}%", va="center", fontsize=9.5,
            fontweight="bold", color=SE["dark"])
    ax.text(b + 15.5, i, f"US\\${b:.0f}B to US\\${p:.0f}B", va="center",
            fontsize=7.8, color=SE["text2"])
ax.set_yticks(range(len(V8)))
ax.set_yticklabels([v[0] for v in V8], fontsize=9.2, color=SE["dark"])
ax.invert_yaxis()
ax.set_xlim(0, 130)
ax.set_xticks([0, 25, 50, 75, 100, 125])
ax.set_xticklabels(["0", "US\\$25B", "US\\$50B", "US\\$75B", "US\\$100B", "US\\$125B"], fontsize=8.2)
ax.tick_params(axis="y", length=0)
axstyle(ax)
fig.text(0.215, 0.035, "Outline: baseline ClimVaR.   Filled: residual after proactive adaptation.",
         fontsize=7.6, color=SE["text2"])
accentbar(fig, y=0.985)
titleblock(fig, "Carbon compresses fastest; physical channels hold",
           "ClimVaR by channel before and after proactive adaptation, installed base, BAU/MEAN",
           x=0.008, y=0.955)
save(fig, "ex_butterfly.pdf")

# ---------------------------------------------------------------- Exhibit 20
steps = sorted([(ch, b - p) for ch, b, p, _ in V8], key=lambda x: -x[1])
base, resid = 387.6, 237.9
fig, ax = plt.subplots(figsize=(7.6, 3.6))
fig.subplots_adjust(left=0.10, right=0.98, top=0.76, bottom=0.18)
xs = list(range(len(steps) + 2))
ax.bar(0, base, color=SE["muted"], width=0.62, zorder=3)
ax.text(0, base + 8, "US\\$388B", ha="center", fontsize=9.5, fontweight="bold", color=SE["dark"])
level = base
for k, (ch, d) in enumerate(steps, start=1):
    ax.bar(k, d, bottom=level - d, color=CH[ch], width=0.62, edgecolor="white", zorder=3)
    ax.plot([k - 1 + 0.31, k - 0.31], [level, level], color=SE["muted"], lw=0.7, zorder=2)
    ax.text(k, level + 8, f"−US\\${d:.0f}B" if d >= 1 else f"−US\\${d:.1f}B",
            ha="center", fontsize=8.6, fontweight="semibold", color=SE["dark"])
    level -= d
k = len(steps) + 1
ax.plot([k - 1 + 0.31, k - 0.31], [level, level], color=SE["muted"], lw=0.7, zorder=2)
ax.bar(k, resid, color=SE["dark"], width=0.62, zorder=3)
ax.text(k, resid + 8, "US\\$238B", ha="center", fontsize=9.5, fontweight="bold", color=SE["dark"])
labels = ["Baseline"] + [c.replace(" ", "\n", 1) for c, _ in steps] + ["After proactive\nadaptation"]
ax.set_xticks(xs)
ax.set_xticklabels(labels, fontsize=8.2, color=SE["dark"], linespacing=1.25)
ax.set_ylim(0, 440)
ax.set_yticks([0, 100, 200, 300, 400])
ax.set_yticklabels(["0", "US\\$100B", "US\\$200B", "US\\$300B", "US\\$400B"], fontsize=8.2)
ax.tick_params(axis="x", length=0)
ax.tick_params(axis="y", length=0)
axstyle(ax, axis="y")
ax.spines["left"].set_visible(False)
accentbar(fig, y=0.985)
titleblock(fig, "US\\$150 billion protected, channel by channel",
           "From baseline to proactive adaptation, installed base, BAU/MEAN, net of adaptation cost",
           x=0.008, y=0.955)
save(fig, "ex_waterfall.pdf")

# ---------------------------------------------------------------- Exhibit 21
ACTIONS = [  # name, US$bn protected, cost per dollar protected, channel
    ("PPA procurement", 22, 0.04, "Carbon costs"),
    ("Thermal shift", 12, 0.08, "Cooling"),
    ("Liquid cooling", 20, 0.12, "Cooling"),
    ("Climate siting", 20, 0.18, "Physical damage"),
    ("Supply chain diversification", 25, 0.25, "Business interruption"),
    ("Microgrid", 18, 0.32, "Business interruption"),
    ("Envelope hardening", 10, 0.40, "Physical damage"),
    ("Predictive maint.", 8, 0.48, "Business interruption"),
    ("Retrofit", 5, 0.58, "Physical damage"),
    ("Wind enclosure", 12, 0.65, "Business interruption"),
]
BE = 1.0
WRAP = {"Supply chain diversification": "Supply chain\ndiversification",
        "Envelope hardening": "Envelope\nhardening", "Predictive maint.": "Predictive\nmaintenance",
        "Wind enclosure": "Wind\nenclosure", "Climate siting": "Climate\nsiting"}
fig, ax = plt.subplots(figsize=(7.6, 4.5))
fig.subplots_adjust(left=0.105, right=0.86, top=0.77, bottom=0.21)
left = 0
for name, w, c, ch in ACTIONS:
    ax.bar(left, c, width=w, align="edge", color=CH[ch], edgecolor="white", lw=1.4, zorder=4)
    ax.bar(left, BE - c, bottom=c, width=w, align="edge", color=SE["light"],
           edgecolor="white", lw=1.4, zorder=3)
    xc, small = left + w / 2, w < 10
    ax.text(xc, 0.965, WRAP.get(name, name), rotation=90, ha="center", va="top",
            fontsize=6.8 if small else 7.4, color=SE["dark"], linespacing=1.15, zorder=6)
    if w >= 8:
        ax.text(xc, c + 0.014, f"\\${c:.2f}", ha="center", va="bottom", fontsize=7.2,
                fontweight="semibold", color=SE["dark"], zorder=6)
    else:
        ax.text(xc, c - 0.02, f"\\${c:.2f}", rotation=90, ha="center", va="top",
                fontsize=6.6, fontweight="semibold", color="white", zorder=6)
    left += w
ax.plot([0, left], [BE, BE], color=SE["dark"], lw=1.2, ls=(0, (4, 2.4)), zorder=7)
ax.text(left + 2, BE + 0.012, "Break-even", ha="left", va="bottom", fontsize=9.2,
        fontweight="semibold", color=SE["dark"], clip_on=False)
ax.text(left + 2, BE - 0.02, "\\$1.00 of cost for\n\\$1.00 protected", ha="left",
        va="top", fontsize=8, color=SE["text2"], linespacing=1.4, clip_on=False)
ax.set_xlim(0, left)
ax.set_ylim(0, 1.12)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["\\$0", "\\$0.25", "\\$0.50", "\\$0.75", "\\$1.00"], fontsize=8.4)
ax.set_xticks([0, 50, 100, 150])
ax.set_xticklabels(["\\$0", "US\\$50B", "US\\$100B", "US\\$150B"], fontsize=8.4)
ax.set_ylabel("Cost of protecting one dollar of ClimVaR", fontsize=8.8, labelpad=8)
ax.set_xlabel("Cumulative ClimVaR protected", fontsize=8.8, labelpad=6)
axstyle(ax, axis="y")
# channel key
kx = 0.105
for ch in ["Carbon costs", "Cooling", "Physical damage", "Business interruption"]:
    fig.add_artist(plt.Rectangle((kx, 0.045), 0.016, 0.024, transform=fig.transFigure,
                                 facecolor=CH[ch], edgecolor="none"))
    fig.text(kx + 0.022, 0.057, ch, fontsize=7.6, va="center", color=SE["dark"])
    kx += 0.05 + 0.0105 * len(ch)
accentbar(fig, y=0.985)
titleblock(fig, "Every action costs less than the risk it removes",
           "Width is the ClimVaR each action protects; height is what protecting one dollar of it costs.\n"
           "The light block above each bar is what is kept.",
           x=0.008, y=0.955)
save(fig, "ex_macc.pdf")
