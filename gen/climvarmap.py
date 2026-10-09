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
from sestyle import SE, accentbar, titleblock, save

NE = os.environ.get("NE50", "/tmp/ne50.zip")
BIN_COLORS = ["#DCF5E1", "#AAE6B4", "#78D28C", "#46BE64", "#149646", "#006432"]
UNAVAILABLE = "#E4E6E3"
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
    return w[w["CONTINENT"] != "Antarctica"]


def classify(v, edges):
    for i, e in enumerate(edges):
        if v < e:
            return i
    return len(edges)


def draw(values, edges, labels, title, subtitle, out, unit_note,
         extent=None, annotate=None, figsize=(7.6, 4.6), crs="EPSG:8857"):
    """values: {iso2: value}; edges: 5 upper bounds for 6 bins.
    extent: (lon_min, lon_max, lat_min, lat_max) to zoom; annotate: {iso2: (name, dx, dy)}
    places a label with the value next to each listed country (offsets in km)."""
    w = world()
    w["val"] = w["iso2"].map(values)
    w = w.to_crs(crs)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0.0, 0.10, 1.0, 0.72])
    w[w["val"].isna()].plot(ax=ax, color=UNAVAILABLE, edgecolor=EDGE, linewidth=0.3)
    has = w[w["val"].notna()].copy()
    has["col"] = [BIN_COLORS[classify(v, edges)] for v in has["val"]]
    has.plot(ax=ax, color=has["col"], edgecolor=EDGE, linewidth=0.35)
    if extent:
        box = gpd.GeoSeries.from_xy([extent[0], extent[1]], [extent[2], extent[3]],
                                    crs="EPSG:4326").to_crs(crs)
        ax.set_xlim(box.x.min(), box.x.max())
        ax.set_ylim(box.y.min(), box.y.max())
    ax.set_aspect("equal")
    ax.axis("off")

    if annotate:
        halo = [pe.withStroke(linewidth=2.4, foreground="white")]
        for iso, (name, dx, dy) in annotate.items():
            row = has[has["iso2"] == iso]
            if row.empty:
                continue
            p = row.geometry.iloc[0].representative_point()
            v = row["val"].iloc[0]
            tx, ty = p.x + dx * 1000, p.y + dy * 1000
            if dx or dy:
                ax.plot([p.x, tx], [p.y, ty], color=SE["muted"], lw=0.5, zorder=5)
                ax.plot([p.x], [p.y], "o", ms=2.6, color=SE["dark"], zorder=6)
            ax.text(tx, ty, f"{name}\n{v:.0f}%", fontsize=7, ha="center",
                    va="center", color=SE["dark"], linespacing=1.15,
                    path_effects=halo, zorder=7)

    # legend: six swatches and the unavailable grey
    x = 0.008
    for col, lab in list(zip(BIN_COLORS, labels)) + [(UNAVAILABLE, "No data")]:
        fig.add_artist(Rectangle((x, 0.045), 0.05, 0.026, transform=fig.transFigure,
                                 facecolor=col, edgecolor=SE["border"], lw=0.4))
        fig.text(x + 0.025, 0.030, lab, fontsize=7.2, ha="center", va="top",
                 color=SE["text2"])
        x += 0.062
    fig.text(x + 0.012, 0.058, unit_note, fontsize=7.4, va="center", color=SE["text2"])

    accentbar(fig, y=0.985)
    titleblock(fig, title, subtitle, x=0.008, y=0.955)
    save(fig, out)
