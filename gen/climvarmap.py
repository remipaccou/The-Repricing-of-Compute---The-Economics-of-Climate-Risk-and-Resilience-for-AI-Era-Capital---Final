"""ClimVaR choropleth, shared by The Repricing of Compute and The Repricing of
Hospitality (and kept in SERI-RESILIENCY/plot-and-tools/map_templates).

Same six-step green scale as the map_templates TikZ maps, drawn with geopandas
on an Equal Earth projection, in Poppins, with the Life Green accent bar.

Country polygons: Natural Earth 50m admin-0, read from /tmp/ne50.zip
    curl -sL -o /tmp/ne50.zip \
      https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip
"""
import csv
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Rectangle
from shapely.geometry import box
from sestyle import SE, accentbar, titleblock, save

NE = os.environ.get("NE50", "/tmp/ne50.zip")
BIN_COLORS = ["#DCF5E1", "#AAE6B4", "#78D28C", "#46BE64", "#149646", "#006432"]
UNAVAILABLE = "#D9DCD8"   # darker than the lowest bin, so low-risk countries stand out
EDGE = "white"
# Natural Earth codes that differ from the ClimVaR country codes
ALIAS = {"CW": "AN", "SX": "AN", "GB": "GB", "XK": "XK"}


def load_values(path, column):
    with open(path, encoding="utf-8-sig") as f:
        return {r["iso2"].strip().upper(): float(r[column]) for r in csv.DictReader(f)}


def world():
    w = gpd.read_file(f"zip://{NE}")
    code = w["ISO_A2_EH"].where(w["ISO_A2_EH"] != "-99", w["ISO_A2"])
    w["iso2"] = code.replace(ALIAS)
    # Natural Earth draws Morocco to the de facto line; shade it to 27°40'N,
    # the internationally recognized boundary, and leave Western Sahara apart.
    ma, eh = w["iso2"] == "MA", w["iso2"] == "EH"
    if ma.any() and eh.any():
        g = w.loc[ma, "geometry"].iloc[0]
        north = g.intersection(box(-20, 27.6667, 5, 40))
        w.loc[eh, "geometry"] = [w.loc[eh, "geometry"].iloc[0].union(g.difference(north))]
        w.loc[ma, "geometry"] = [north]
    return w[w["CONTINENT"] != "Antarctica"]


def classify(v, edges):
    for i, e in enumerate(edges):
        if v < e:
            return i
    return len(edges)


def pct(v):
    """Default label format: whole per cent from 10% up, one decimal below."""
    return f"{v:.0f}%" if v >= 10 else f"{v:.1f}%"


def draw(values, edges, labels, title, subtitle, out, unit_note,
         extent=None, annotate=None, figsize=(7.6, 4.6), crs="EPSG:8857",
         na_label="No data", fmt=pct, axbox=(0.0, 0.10, 1.0, 0.72)):
    """values: {iso2: value}; edges: 5 upper bounds for 6 bins.

    extent   (lon_min, lon_max, lat_min, lat_max) to zoom on a region.
    annotate {iso2: label} writes the country name and its value. A label is
             either a name (two lines, at the country's representative point)
             or (name, lon, lat, ha): one line at that position, joined to the
             country by a leader line and a dot in the country's colour, for
             states too small to carry their own text; ha=None places the
             two-line label at that position without a leader.
    na_label legend entry for countries without a value."""
    w = world()
    w["val"] = w["iso2"].map(values)
    w = w.to_crs(crs)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes(list(axbox))
    w[w["val"].isna()].plot(ax=ax, color=UNAVAILABLE, edgecolor=EDGE, linewidth=0.3)
    has = w[w["val"].notna()].copy()
    has["col"] = [BIN_COLORS[classify(v, edges)] for v in has["val"]]
    has.plot(ax=ax, color=has["col"], edgecolor=EDGE, linewidth=0.35)
    if extent:
        lo0, lo1, la0, la1 = extent
        n = 40
        lons = [lo0 + (lo1 - lo0) * i / n for i in range(n + 1)]
        lats = [la0 + (la1 - la0) * i / n for i in range(n + 1)]
        edge = gpd.GeoSeries.from_xy(lons * 2 + [lo0] * (n + 1) + [lo1] * (n + 1),
                                     [la0] * (n + 1) + [la1] * (n + 1) + lats * 2,
                                     crs="EPSG:4326").to_crs(crs)
        ax.set_xlim(edge.x.min(), edge.x.max())
        ax.set_ylim(edge.y.min(), edge.y.max())
    ax.set_aspect("equal")
    ax.axis("off")

    if annotate:
        halo = [pe.withStroke(linewidth=2.4, foreground="white")]
        for iso, lab in annotate.items():
            row = has[has["iso2"] == iso]
            if row.empty:
                continue
            p = row.geometry.iloc[0].representative_point()
            v = row["val"].iloc[0]
            if isinstance(lab, str):
                ax.text(p.x, p.y, f"{lab}\n{fmt(v)}", fontsize=7.2, ha="center",
                        va="center", color=SE["dark"], linespacing=1.15,
                        path_effects=halo, zorder=7)
                continue
            name, lon, lat, ha = lab
            t = gpd.GeoSeries.from_xy([lon], [lat], crs="EPSG:4326").to_crs(crs).iloc[0]
            if ha is None:
                ax.text(t.x, t.y, f"{name}\n{fmt(v)}", fontsize=7.2, ha="center",
                        va="center", color=SE["dark"], linespacing=1.15,
                        path_effects=halo, zorder=7)
                continue
            ax.plot([p.x, t.x], [p.y, t.y], color=SE["muted"], lw=0.5, zorder=5)
            ax.plot([p.x], [p.y], "o", ms=4.2, mfc=BIN_COLORS[classify(v, edges)],
                    mec=SE["dark"], mew=0.6, zorder=6)
            pad = {"left": 1, "right": -1}.get(ha, 0) * 60_000
            ax.text(t.x + pad, t.y, f"{name}  {fmt(v)}", fontsize=7.2, ha=ha,
                    va="center", color=SE["dark"], path_effects=halo, zorder=7)

    # legend: six swatches and the unavailable grey; a long last label gets
    # room on both sides so it clears its neighbour and the unit note
    spill = max(0.0, 0.0047 * len(na_label) * 7.6 / figsize[0] - 0.05) / 2
    x = 0.008
    for i, (col, lab) in enumerate(list(zip(BIN_COLORS, labels)) + [(UNAVAILABLE, na_label)]):
        if i == len(labels):
            x += spill
        fig.add_artist(Rectangle((x, 0.045), 0.05, 0.026, transform=fig.transFigure,
                                 facecolor=col, edgecolor=SE["border"], lw=0.4))
        fig.text(x + 0.025, 0.030, lab, fontsize=7.2, ha="center", va="top",
                 color=SE["text2"])
        x += 0.062
    fig.text(x + 0.012 + spill, 0.058, unit_note, fontsize=7.4, va="center",
             color=SE["text2"])

    accentbar(fig, y=0.985)
    titleblock(fig, title, subtitle, x=0.008, y=0.955)
    save(fig, out)
