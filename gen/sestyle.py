"""Shared Schneider Electric chart style — Poppins, brand palette, vector PDF out."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import os

FONTDIR = os.path.join(os.path.dirname(__file__), "..", "fonts")
for f in os.listdir(FONTDIR):
    if f.startswith("Poppins") and f.endswith(".ttf"):
        fm.fontManager.addfont(os.path.join(FONTDIR, f))

SE = dict(
    dark="#0A2F24", green="#3DCD58", electric="#5EFF59",
    light="#E7FFD9", gray="#FAFAFA",
    blue="#2040FF", yellow="#FFCE00", cyan="#24F0FF", red="#FF0050",
    border="#E5E3DE", text2="#6B6860", muted="#A8A49C", grid="#E0F0E8",
)

plt.rcParams.update({
    "font.family": "Poppins",
    "font.weight": "regular",
    "pdf.fonttype": 42,
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "axes.edgecolor": SE["grid"],
    "text.color": SE["dark"],
    "axes.labelcolor": SE["dark"],
    "xtick.color": SE["text2"],
    "ytick.color": SE["text2"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "svg.fonttype": "none",
})

def accentbar(fig, y=0.985, x0=0.0, x1=1.0, lw=3.5):
    """The signature Life Green rule across the top of every exhibit."""
    fig.add_artist(plt.Line2D([x0, x1], [y, y], color=SE["green"],
                              linewidth=lw, solid_capstyle="butt"))

def titleblock(fig, title, subtitle=None, x=0.0, y=0.945):
    """Title and subtitle with a constant optical gap, whatever the figure
    height — a fraction of the height alone collides on short exhibits."""
    fig.text(x, y, title, fontsize=13.5, fontweight="bold",
             color=SE["dark"], va="top", ha="left")
    if subtitle:
        dy = 19.0 / (fig.get_figheight() * 72.0)
        fig.text(x, y - dy, subtitle, fontsize=9.5,
                 color=SE["text2"], va="top", ha="left")

def save(fig, name):
    out = os.path.join(os.path.dirname(__file__), "..", "images", name)
    fig.savefig(out, format="pdf")
    print("wrote", out)
