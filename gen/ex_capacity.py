"""Exhibit 7b — installed data center capacity under the three AI growth scenarios.

Source: dc_inputs_DYNAMIC_v7_5_1_3SC, sheet SCENARIO_INFO. AI electricity demand
(TWh) at 2025, 2030, 2035 (Paccou & Wijnhoven 2024) and extrapolated to 2050,
converted to IT capacity with GW = (TWh - 100) / (1.25 x 8.76 x 0.85), then
scaled so that each 2050 value matches the facility database. Points are joined
by a monotone curve; no sensitivity band is drawn because none is computed.
"""
import numpy as np
import matplotlib.pyplot as plt
from sestyle import SE, accentbar, titleblock, save

YEARS = np.array([2025, 2030, 2035, 2040, 2045, 2050])
TWH = {
    "LTG": [100, 510, 570, 605, 642, 682],
    "SAI": [100, 620, 785, 910, 1055, 1223],
    "AWB": [100, 880, 1370, 1749, 2232, 2848],
}
INSTALLED = 90.8
ADDED_2050 = {"LTG": 62.9, "SAI": 121.2, "AWB": 295.6}      # GW, facility database
NAMES = {"LTG": "Limits to Growth", "SAI": "Sustainable AI",
         "AWB": "Abundance Without\nBoundaries"}
COLS = {"LTG": "#8FD9A0", "SAI": SE["green"], "AWB": SE["dark"]}


def pchip(x, y, xs):
    """Monotone cubic interpolation (Fritsch–Carlson), no scipy needed."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    h = np.diff(x); d = np.diff(y) / h
    m = np.zeros_like(y)
    m[0], m[-1] = d[0], d[-1]
    for k in range(1, len(x) - 1):
        if d[k - 1] * d[k] > 0:
            w1, w2 = 2 * h[k] + h[k - 1], h[k] + 2 * h[k - 1]
            m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k])
    out = np.empty_like(xs, dtype=float)
    for i, v in enumerate(xs):
        k = min(np.searchsorted(x, v, side="right") - 1, len(x) - 2)
        t = (v - x[k]) / h[k]
        h00, h10 = 2*t**3 - 3*t**2 + 1, t**3 - 2*t**2 + t
        h01, h11 = -2*t**3 + 3*t**2, t**3 - t**2
        out[i] = h00*y[k] + h10*h[k]*m[k] + h01*y[k+1] + h11*h[k]*m[k+1]
    return out


fig, ax = plt.subplots(figsize=(7.6, 4.4))
fig.subplots_adjust(left=0.085, right=0.68, top=0.80, bottom=0.12)
xs = np.linspace(2025, 2050, 200)

ax.axhline(INSTALLED, color=SE["muted"], lw=0.8, ls=(0, (3, 2)), zorder=2)
ax.text(2025.3, INSTALLED - 7, "Installed base today: 90.8 GW, 8,572 facilities",
        fontsize=7.8, color=SE["text2"], va="top")

for key in ["AWB", "SAI", "LTG"]:
    tw = np.array(TWH[key], float)
    added = (tw - tw[0]) / (tw[-1] - tw[0]) * ADDED_2050[key]
    gw = INSTALLED + added
    ys = pchip(YEARS, gw, xs)
    ax.fill_between(xs, INSTALLED, ys, color=COLS[key], alpha=0.12 if key != "AWB" else 0.06, lw=0, zorder=1)
    ax.plot(xs, ys, color=COLS[key], lw=2.4, zorder=4, solid_capstyle="round")
    ax.scatter(YEARS[1:], gw[1:], s=14, color=COLS[key], zorder=5,
               edgecolor="white", linewidth=0.8)
    end = gw[-1]
    fig_y = end
    ax.text(2050.8, end, f"{INSTALLED + ADDED_2050[key]:.0f} GW",
            fontsize=10.5, fontweight="bold", color=COLS[key] if key != "LTG" else "#2E8B4A",
            va="center", ha="left", clip_on=False)
    ax.text(2054.6, end, f"{NAMES[key]}\n+{ADDED_2050[key]:.0f} GW by 2050",
            fontsize=7.8, color=SE["dark"], va="center", ha="left",
            linespacing=1.35, clip_on=False)

ax.set_xlim(2025, 2050)
ax.set_ylim(0, 420)
ax.set_xticks([2025, 2030, 2035, 2040, 2045, 2050])
ax.set_yticks([0, 100, 200, 300, 400])
ax.set_yticklabels(["0", "100", "200", "300", "400 GW"], fontsize=8.5)
ax.tick_params(axis="x", labelsize=8.5)
ax.grid(axis="y", color=SE["grid"], lw=0.7, zorder=0)
ax.set_axisbelow(True)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color(SE["grid"])
ax.tick_params(axis="y", length=0)

accentbar(fig, y=0.985)
titleblock(fig, "Three paths for AI-era capacity",
           "Global data center IT capacity, GW. Scenarios are nested: "
           "Limits to Growth within Sustainable AI within Abundance.",
           x=0.008, y=0.955)
save(fig, "ex_capacity.pdf")
