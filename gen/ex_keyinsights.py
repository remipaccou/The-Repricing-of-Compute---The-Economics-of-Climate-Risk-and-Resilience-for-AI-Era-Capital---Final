"""Executive summary, page 2: the four numbers the paper stands on.

Four tiles in a 2 x 2 grid. Each tile states a figure, what it measures in
words, and a small chart that shows the figure rather than repeating it.
The x11 tile is labelled as business interruption supply chain amplification:
it is the ratio of interruption transmitted through suppliers to interruption
arising on site, and nothing broader.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from sestyle import SE, accentbar, titleblock, save

BI_DIRECT, BI_SUPPLY = 11.0, 110.4      # US$bn, BAU/MEAN, installed base (91% upstream)
REGIONS = [("China", 55.8), ("Europe", 53.1), ("APMEA", 28.2), ("United States", 27.6)]
PLANS = [("Baseline", 388), ("Selective", 305), ("Proactive", 238)]

fig = plt.figure(figsize=(7.6, 5.6))
accentbar(fig, y=0.985)
titleblock(fig, "Key insights",
           "Climate value at risk on global data center infrastructure, BAU/MEAN pathway, "
           "8,572 facilities in 120 countries", x=0.008, y=0.955)

# tile geometry in figure coordinates
X = [0.008, 0.512]
Y = [0.455, 0.035]
W, H = 0.480, 0.385


def tile(ix, iy, big, label, note):
    x, y = X[ix], Y[iy]
    fig.add_artist(Rectangle((x, y), W, H, transform=fig.transFigure,
                             facecolor=SE["gray"], edgecolor=SE["border"], lw=0.8, zorder=-5))
    fig.add_artist(plt.Line2D([x, x + 0.06], [y + H, y + H], color=SE["green"],
                              lw=3.0, transform=fig.transFigure, solid_capstyle="butt"))
    fig.text(x + 0.022, y + H - 0.035, big, fontsize=27, fontweight="bold",
             color=SE["dark"], va="top")
    fig.text(x + 0.022, y + H - 0.135, label, fontsize=9.6, fontweight="semibold",
             color=SE["dark"], va="top")
    fig.text(x + 0.022, y + H - 0.175, note, fontsize=7.6, color=SE["text2"],
             va="top", linespacing=1.4)
    return x, y


# 1. headline value at risk: one bar of enterprise value with the share at risk
x, y = tile(0, 0, "US\\$388B", "Climate value at risk on the installed base",
            "38.3% of US\\$1,012B aggregate enterprise value")
ax = fig.add_axes([x + 0.022, y + 0.045, W - 0.044, 0.07])
ax.barh(0, 1012, color=SE["light"], height=0.6, edgecolor="none")
ax.barh(0, 388, color=SE["dark"], height=0.6, edgecolor="none")
ax.text(388 / 2, 0, "at risk  US\\$388B", color="white", fontsize=7.6,
        ha="center", va="center", fontweight="semibold")
ax.text(388 + (1012 - 388) / 2, 0, "rest of enterprise value", color=SE["text2"],
        fontsize=7.4, ha="center", va="center")
ax.set_xlim(0, 1012); ax.set_ylim(-0.5, 0.5); ax.axis("off")

# 2. intensity by region
x, y = tile(1, 0, "28–56%", "Climate risk intensity by region",
            "ClimVaR as a share of regional enterprise value")
ax = fig.add_axes([x + 0.16, y + 0.025, W - 0.25, 0.135])
for i, (r, v) in enumerate(REGIONS):
    ax.barh(i, v, color=SE["green"] if v > 50 else "#8FD9A0", height=0.62, edgecolor="none")
    ax.text(-2, i, r, ha="right", va="center", fontsize=7.6, color=SE["dark"])
    ax.text(v + 1.5, i, f"{v:.0f}%", ha="left", va="center", fontsize=7.6,
            fontweight="semibold", color=SE["dark"])
ax.set_xlim(0, 66); ax.invert_yaxis(); ax.axis("off")

# 3. x11: interruption arriving through suppliers vs arising on site
x, y = tile(0, 1, "×11", "Business interruption supply chain amplification",
            "Interruption transmitted through suppliers is eleven times\n"
            "the interruption arising on site")
ax = fig.add_axes([x + 0.022, y + 0.03, W - 0.044, 0.10])
ax.barh(1, BI_DIRECT, color=SE["dark"], height=0.62, edgecolor="none")
ax.barh(0, BI_SUPPLY, color=SE["green"], height=0.62, edgecolor="none")
ax.text(BI_DIRECT + 2, 1, "On site   US\\$11B", va="center", fontsize=7.6, color=SE["dark"])
ax.text(BI_SUPPLY / 2, 0, "Through suppliers   US\\$110B", va="center", ha="center",
        fontsize=7.6, color=SE["dark"], fontweight="semibold")
ax.set_xlim(0, 122); ax.set_ylim(-0.5, 1.5); ax.axis("off")

# 4. adaptation
x, y = tile(1, 1, "30–39%", "Risk reduced through adaptation",
            "Positive net return in every scenario tested")
ax = fig.add_axes([x + 0.16, y + 0.025, W - 0.25, 0.12])
for i, (p, v) in enumerate(PLANS):
    ax.barh(i, v, color=[SE["muted"], "#8FD9A0", SE["green"]][i], height=0.62, edgecolor="none")
    ax.text(-6, i, p, ha="right", va="center", fontsize=7.6, color=SE["dark"])
    ax.text(v + 12, i, f"US\\${v}B", ha="left", va="center", fontsize=7.6,
            fontweight="semibold", color=SE["dark"])
ax.set_xlim(0, 500); ax.invert_yaxis(); ax.axis("off")

save(fig, "ex_keyinsights.pdf")
