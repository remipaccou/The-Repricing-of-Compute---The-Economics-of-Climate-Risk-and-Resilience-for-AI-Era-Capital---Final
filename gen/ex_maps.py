"""Exhibits 15a/15b and 21a/21b — ClimVaR by country, installed base, BAU/MEAN.

Data: SERI-RESILIENCY/plot-and-tools/map_templates (copied to gen/data).
Bins follow the map_templates; the 5-year share uses the bin edges its labels
state (20, 25, 30, 35, 40), which the original template had offset.
"""
import os
from climvarmap import load_values, draw

D = os.path.join(os.path.dirname(__file__), "data")

draw(load_values(os.path.join(D, "climvar_abs_values.csv"), "climvar_busd"),
     [0.01, 0.1, 1, 10, 100], ["<0.01", "0.01–0.1", "0.1–1", "1–10", "10–100", "100+"],
     "Where the dollars sit",
     "Absolute ClimVaR by country, installed base, BAU/MEAN",
     "ex_map_abs.pdf", "US$ billions")

draw(load_values(os.path.join(D, "climvar_bau_values.csv"), "climvar_pct"),
     [20, 40, 60, 80, 100], ["0–20", "20–40", "40–60", "60–80", "80–100", "100+"],
     "Where the risk is most intense",
     "ClimVaR as a share of enterprise value by country, installed base, BAU/MEAN",
     "ex_map_pct.pdf", "% of enterprise value")

draw(load_values(os.path.join(D, "temporal_values.csv"), "climvar_pct"),
     [20, 25, 30, 35, 40], ["0–20", "20–25", "25–30", "30–35", "35–40", "40+"],
     "How much of the loss arrives early",
     "Share of each country's ClimVaR that falls in the next five years, BAU/MEAN",
     "ex_map_temporal_pct.pdf", "% of total ClimVaR")

draw(load_values(os.path.join(D, "temporal_abs_values.csv"), "climvar_busd"),
     [0.01, 0.1, 1, 10, 15], ["<0.01", "0.01–0.1", "0.1–1", "1–10", "10–15", "15+"],
     "Where the early loss is largest",
     "ClimVaR falling in the next five years by country, BAU/MEAN",
     "ex_map_temporal_abs.pdf", "US$ billions")
