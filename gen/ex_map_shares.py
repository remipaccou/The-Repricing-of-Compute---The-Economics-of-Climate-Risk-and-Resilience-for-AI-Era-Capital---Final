"""Exhibit 16 — what the loss is made of: share of each risk channel in
national ClimVaR, installed base, BAU/MEAN.

Five small maps on the shared ClimVaR basemap (climvarmap.world: Natural
Earth 50m, Equal Earth, Western Sahara apart), one per channel, all on the
same five-step scale. Shares within a country sum to 100%.

Data, in order of preference:
  data/channel_share_values.csv  iso2 and one column per channel, in % of the
                                 country's ClimVaR (the model output).
  data/channel_share_bins.csv    the bin index (0-4) of each share, read back
                                 from the vector paths of the v2-review
                                 figure (PR #1, M365 Copilot output). That
                                 figure was drawn on Natural Earth 110m and
                                 joined on ISO_A2, so France and Norway
                                 (ISO_A2 = -99 there) and the small states
                                 absent at 110m carry no value. Those
                                 countries are shown as "value pending" until
                                 the values file replaces the bins.
Countries in climvar_bau_values.csv (a facility in the database) without a
channel value are hatched; countries outside it are the usual no-data grey.
"""
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from climvarmap import world, UNAVAILABLE, EDGE
from sestyle import SE, accentbar, titleblock, save

D = os.path.join(os.path.dirname(__file__), "data")
CHANNELS = [("business_interruption", "Business interruption"),
            ("carbon_costs", "Carbon costs"),
            ("physical_damage", "Physical damage"),
            ("cooling", "Cooling"),
            ("heat_productivity", "Heat productivity")]
EDGES = [10, 25, 50, 75]                     # upper bounds of the first four bins
LABELS = ["0–10", "10–25", "25–50", "50–75", "75–100"]
COLORS = ["#DCF5E1", "#AAE6B4", "#78D28C", "#149646", "#006432"]
PENDING_HATCH = "////////"


def classify(v):
    for i, e in enumerate(EDGES):
        if v < e:
            return i
    return len(EDGES)


def load_bins():
    """{channel: {iso2: bin}} from the values file if present, else the bins."""
    vals = os.path.join(D, "channel_share_values.csv")
    if os.path.exists(vals):
        rows = list(csv.DictReader(open(vals, encoding="utf-8-sig")))
        return {c: {r["iso2"].strip().upper(): classify(float(r[c]))
                    for r in rows if r[c].strip()} for c, _ in CHANNELS}, "values"
    rows = list(csv.DictReader(open(os.path.join(D, "channel_share_bins.csv"),
                                    encoding="utf-8-sig")))
    return {c: {r["iso2"].strip().upper(): int(r[c]) for r in rows if r[c].strip()}
            for c, _ in CHANNELS}, "bins"


def main():
    bins, source = load_bins()
    with open(os.path.join(D, "climvar_bau_values.csv"), encoding="utf-8-sig") as f:
        in_db = {r["iso2"].strip().upper() for r in csv.DictReader(f)}

    w = world().to_crs("EPSG:8857")
    # each panel is 2.5 in wide (about 45 km per pixel at 300 dpi), so 4 km
    # of simplification is invisible and keeps the PDF near 1 MB
    w["geometry"] = w.geometry.simplify(4000, preserve_topology=True)
    bx0, by0, bx1, by1 = w.total_bounds
    aspect = (bx1 - bx0) / (by1 - by0)

    # 3 x 2 grid in inches: five maps, the sixth cell holds the legend
    W, gapx, head, lab, gapy, foot = 7.6, 0.10, 0.66, 0.24, 0.10, 0.04
    mw = (W - 2 * gapx) / 3
    mh = mw / aspect
    H = head + 2 * (lab + mh) + gapy + foot
    fig = plt.figure(figsize=(W, H))
    cells = []                                   # (x0, y0) of each map, in inches
    for i in range(2):
        y0 = H - head - (i + 1) * (lab + mh) - i * gapy
        for j in range(3):
            cells.append((j * (mw + gapx), y0))

    pending_any = False
    for (col, name), (x0, y0) in zip(CHANNELS, cells):
        ax = fig.add_axes([x0 / W, y0 / H, mw / W, mh / H])
        ax.set_xlim(bx0, bx1)
        ax.set_ylim(by0, by1)
        b = bins[col]
        w["bin"] = w["iso2"].map(b)
        none = w[w["bin"].isna() & ~w["iso2"].isin(in_db)]
        pend = w[w["bin"].isna() & w["iso2"].isin(in_db)]
        has = w[w["bin"].notna()].copy()
        none.plot(ax=ax, color=UNAVAILABLE, edgecolor=EDGE, linewidth=0.15)
        if len(pend):
            pending_any = True
            pend.plot(ax=ax, facecolor="white", edgecolor=SE["muted"],
                      hatch=PENDING_HATCH, linewidth=0.15)
        has.plot(ax=ax, color=[COLORS[int(v)] for v in has["bin"]],
                 edgecolor=EDGE, linewidth=0.18)
        ax.set_xlim(bx0, bx1)
        ax.set_ylim(by0, by1)
        ax.set_aspect("equal")
        ax.axis("off")
        fig.text((x0 + 0.03) / W, (y0 + mh + 0.05) / H, name, fontsize=8.6,
                 fontweight="semibold", color=SE["dark"], va="bottom", ha="left")

    # legend in the sixth cell, laid out in inches
    lx, ly = cells[5]
    lx += 0.22
    top = ly + mh + 0.05
    fig.text(lx / W, top / H, "Share of national ClimVaR (%)", fontsize=7.6,
             color=SE["text2"], va="bottom")
    sw, sh, step = 0.34, 0.16, 0.42
    sy = top - 0.30
    for k, (c, txt) in enumerate(zip(COLORS, LABELS)):
        x = lx + k * step
        fig.add_artist(Rectangle((x / W, sy / H), sw / W, sh / H, transform=fig.transFigure,
                                 facecolor=c, edgecolor=SE["border"], lw=0.4))
        fig.text((x + sw / 2) / W, (sy - 0.05) / H, txt, fontsize=7.0, ha="center",
                 va="top", color=SE["text2"])
    extra = [(UNAVAILABLE, None, "No facility in the database")]
    if pending_any:
        extra.append(("white", PENDING_HATCH, "Facility, value pending"))
    for k, (c, h, txt) in enumerate(extra):
        y = sy - 0.48 - k * 0.26
        fig.add_artist(Rectangle((lx / W, y / H), sw / W, sh / H, transform=fig.transFigure,
                                 facecolor=c, hatch=h, lw=0.4,
                                 edgecolor=SE["muted"] if h else SE["border"]))
        fig.text((lx + sw + 0.10) / W, (y + sh / 2) / H, txt, fontsize=7.0,
                 va="center", color=SE["text2"])

    accentbar(fig, y=0.985)
    titleblock(fig, "What the loss is made of",
               "Share of each risk channel in national ClimVaR, installed base, BAU/MEAN",
               x=0.008, y=0.955)
    save(fig, "ex_map_shares.pdf")
    print("source:", source)


if __name__ == "__main__":
    main()
