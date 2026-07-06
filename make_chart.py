import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

# ---- palette (references/palette.md) ----
SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
BLUE = "#2a78d6"    # categorical slot 1 -> Commercial
AQUA = "#1baf7a"    # categorical slot 2 -> Research

years = list(range(2015, 2026))
commercial = [799, 777, 836, 852, 928, 1253, 1259, 1124, 1062, 1139, 1210]
research   = [765, 892, 836, 742, 750, 929, 809, 741, 662, 716, 750]
total = [c + r for c, r in zip(commercial, research)]

highlight_years = {2015, 2020, 2023, 2025}  # start, COVID peak, trough, latest

fig, ax = plt.subplots(figsize=(10.5, 7), dpi=200)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

bar_w = 0.62
gap_lw = 2.2  # surface-color gap between stacked segments, in points

# gridlines first (recessive, behind bars)
y_ticks = [0, 500, 1000, 1500, 2000, 2500]
for yt in y_ticks:
    ax.axhline(yt, color=GRID, linewidth=1, zorder=0)

x = list(range(len(years)))

for i, (xi, c, r) in enumerate(zip(x, commercial, research)):
    # bottom segment: Commercial (square at baseline)
    ax.add_patch(Rectangle(
        (xi - bar_w / 2, 0), bar_w, c,
        facecolor=BLUE, edgecolor=SURFACE, linewidth=gap_lw, zorder=2,
    ))
    # top segment: Research, rounded data-end
    ax.add_patch(FancyBboxPatch(
        (xi - bar_w / 2, c), bar_w, r,
        boxstyle=f"round,pad=0,rounding_size=0.05",
        facecolor=AQUA, edgecolor=SURFACE, linewidth=gap_lw, zorder=2,
        mutation_aspect=1,
    ))

# selective direct labels: total, only at the story beats
for xi, yr, t in zip(x, years, total):
    if yr in highlight_years:
        ax.text(xi, t + 60, f"{t:,}", ha="center", va="bottom",
                 fontsize=11.5, color=INK_PRIMARY, fontweight="bold", zorder=3)

ax.set_xlim(-0.7, len(years) - 0.3)
ax.set_ylim(0, 2500)

ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=10.5, color=INK_SECONDARY)

ax.set_yticks(y_ticks)
ax.set_yticklabels([f"{v:,}" for v in y_ticks], fontsize=10, color=INK_MUTED)

# baseline / axis
ax.spines["bottom"].set_color(BASELINE)
ax.spines["bottom"].set_linewidth(1.2)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", length=0)

# title / subtitle
fig.text(0.06, 0.965, "FDA New IND Application Receipts, 2015–2025",
          fontsize=17, fontweight="bold", color=INK_PRIMARY, ha="left")
fig.text(0.06, 0.93,
          "CDER drug & non-biosimilar biologic INDs — annual totals, commercial vs. research",
          fontsize=11, color=INK_SECONDARY, ha="left")

# legend (always present for 2+ series)
legend_y = 0.885
fig.patches.append(Rectangle((0.062, legend_y - 0.006), 0.018, 0.018,
                              transform=fig.transFigure, facecolor=BLUE,
                              edgecolor="none"))
fig.text(0.088, legend_y + 0.003, "Commercial", fontsize=10.5, color=INK_SECONDARY, va="center")
fig.patches.append(Rectangle((0.205, legend_y - 0.006), 0.018, 0.018,
                              transform=fig.transFigure, facecolor=AQUA,
                              edgecolor="none"))
fig.text(0.231, legend_y + 0.003, "Research", fontsize=10.5, color=INK_SECONDARY, va="center")

# footnote / source
fig.text(0.06, 0.02,
         "Source: FDA CDER “IND Receipts” annual reports (fda.gov/drugs/ind-activity/ind-receipts). "
         "FDA publishes these figures annually only — no monthly breakdown exists.",
         fontsize=8.3, color=INK_MUTED, ha="left")

plt.subplots_adjust(left=0.09, right=0.97, top=0.86, bottom=0.09)

out_path = "/tmp/claude-0/-root-project/4b9721b7-cd29-484a-8f31-9e921828c338/scratchpad/fda-ind-trends/fda_ind_receipts_2015_2025.png"
fig.savefig(out_path, facecolor=SURFACE)
print("saved", out_path)
