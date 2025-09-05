import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# ==============================================================================
# Title: Generate color legend for Circos plots
# Purpose:
#   Create a standalone legend mapping antibiotics to their Circos colors.
#   Useful for adding as an image (PNG) alongside Circos outputs.
#
# Inputs:
#   - Hardcoded antibiotic names and hex colors (must match Circos config)
#
# Outputs:
#   - cef_str_legend.png : PNG image containing legend boxes + labels
#
# Usage:
#   python make_circos_legend.py
#
# Dependencies:
#   - matplotlib
# ==============================================================================

# Antibiotics and colors used in Circos
antibiotics = [
    ("LB", "#fc9272"),
    ("Cef", "#9ecae1"),
    ("Str", "#a1d99b"),
    ("CefStr", "#bcbddc"),
]

# Create legend entries (colored squares with labels)
legend_elements = [
    Patch(facecolor=color, edgecolor="black", label=label)
    for label, color in antibiotics
]

# Create a blank figure sized to number of antibiotics
fig, ax = plt.subplots(figsize=(4, len(antibiotics)))
ax.axis("off")  # hide axes

# Add the legend to the figure
ax.legend(
    handles=legend_elements,
    loc="center",
    frameon=False,   # no border around legend
    fontsize=20,     # larger font for readability
    markerscale=2.0  # enlarge color boxes
)

# Save legend as a high-resolution PNG
plt.savefig(
    "./cef_str_legend.png",
    dpi=600,
    bbox_inches="tight"
)
