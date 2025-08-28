# pip install matplotlib pandas upsetplot
# https://upsetplot.readthedocs.io/en/stable/

import pandas as pd
from upsetplot import UpSet, from_contents   # from_contents expects a dict: {set_name: [elements]}
import matplotlib.pyplot as plt

# ==============================================================================
# Title: Generate UpSet plot from mutation matrix
# Purpose:
#   Take a gene × condition mutation count matrix and create an UpSet plot
#   showing intersections of mutated genes across antibiotic treatments.
#
# Inputs:
#   - grouped_mutations.csv
#       * Rows = genes
#       * Columns = treatments (values = mutation counts)
#
# Outputs:
#   - intersection_data.csv : expanded table of intersections (for reference)
#   - upset_plot.svg        : UpSet diagram (saved in SVG format)
#
# Usage:
#   python make_upset_plot.py
#
# Notes:
#   - Only genes with value > 0 in a given treatment are considered
#   - Uses upsetplot: https://upsetplot.readthedocs.io
# ==============================================================================

# Load gene × condition mutation count matrix
data = pd.read_csv('/Users/abhisheksinha/Desktop/NSERC/breseq/upset_plots/grouped_mutations.csv', index_col=0)

# Convert to dictionary format: {condition: [genes with mutations]}
contents = {}
for col in data.columns:
    contents[col] = data[data[col] > 0].index.tolist()

# Convert dictionary → UpSet-compatible DataFrame
upset_data = from_contents(contents)

# Save expanded intersection table for downstream reference
upset_data.reset_index().to_csv(
    "/Users/abhisheksinha/Desktop/NSERC/breseq/upset_plots/intersection_data.csv",
    index=False
)

# Create and save UpSet plot
UpSet(
    upset_data,
    subset_size='count',       # show counts on subsets
    show_counts=True,          # label subset sizes
    sort_by='degree',          # order intersections by degree
    sort_categories_by='-input' # order categories (columns) by input order
).plot()

plt.savefig(
    '/Users/abhisheksinha/Desktop/NSERC/breseq/upset_plots/upset_plot.svg',
    format='svg'
)
plt.show()

# To explore options:
# from upsetplot import UpSet
# help(UpSet)