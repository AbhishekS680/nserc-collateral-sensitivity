# ==============================================================================
# Title: Merge gene positions with mutation counts
# Purpose:
#   Combine GenBank-derived CDS coordinates with grouped mutation counts by gene.
#   Produces a table suitable for Circos heatmaps or other genomic visualizations.
#
# Inputs:
#   - positions_from_gb.csv : coordinates extracted from sequence.gb
#       (columns: chr, start, end, gene)
#   - grouped_mutations.csv : wide table of mutation counts per condition
#       (rows = gene labels, cols = antibiotic/treatment groups)
#
# Outputs:
#   - circos_heatmap_all.csv : merged table (comma-separated)
#   - circos_heatmap_all.tsv : merged table (tab-separated)
#
# Matching details:
#   - Handles composite labels like "ais ← / → arnB" by splitting into tokens
#   - Case-insensitive match to positions_from_gb gene names
#   - If multiple genes match, counts are added to each
#   - Genes with no matches remain in output with zeros
#
# Usage:
#   python merge_positions_with_counts.py
#
# Dependencies:
#   - pandas
# ==============================================================================

import re
import sys
import pandas as pd
from pathlib import Path

# ====== CONFIG: edit paths if needed ======
GB_POSITIONS_CSV = "/Users/abhisheksinha/Desktop/NSERC/circos/positions_from_gb.csv"
GROUPED_COUNTS_CSV = "/Users/abhisheksinha/Desktop/NSERC/circos/grouped_mutations.csv"
OUT_CSV = "/Users/abhisheksinha/Desktop/NSERC/circos/circos_heatmap_all.csv"
OUT_TSV = "/Users/abhisheksinha/Desktop/NSERC/circos/circos_heatmap_all.tsv"
# =========================================

def pick_gene_label_column(df: pd.DataFrame) -> str:
    """Heuristically select the column that contains gene labels."""
    candidates = [c for c in df.columns if c is not None]
    preferred = ["Row Labels", "row labels", "gene", "Gene", "Genes", "ID", "Id", "name", "Name"]
    for p in preferred:
        for c in candidates:
            if c.strip().lower() == p.strip().lower():
                return c

    # If first column looks text-like, assume it’s the label column
    first = candidates[0]
    if df[first].astype(str).str.contains(r"[A-Za-z]", regex=True).mean() > 0.5:
        return first

    # Fall back to first column
    return first

def clean_gene_tokens(label: str) -> list[str]:
    """
    Extract alphanumeric tokens from a label for gene matching.
    Example: 'ampH ← / → sbmA' -> ['AMPH','SBMA'] (uppercased for consistency)
    """
    if label is None:
        return []
    tokens = re.findall(r"[A-Za-z0-9_]+", str(label))
    return [t.upper() for t in tokens if t.strip()]

def main():
    # --- Load positions table ---
    pos = pd.read_csv(GB_POSITIONS_CSV)
    required_cols = {"chr", "start", "end", "gene"}
    if not required_cols.issubset(set(pos.columns)):
        sys.exit(f"ERROR: positions file must have columns {required_cols}, found {set(pos.columns)}")

    # Uppercase gene column for case-insensitive matching
    pos = pos.copy()
    pos["__GENE_UP__"] = pos["gene"].astype(str).str.upper()
    pos = pos.drop_duplicates("__GENE_UP__", keep="first")  # keep first if duplicates
    gene_upper_to_real = dict(zip(pos["__GENE_UP__"], pos["gene"]))
    valid_gene_set = set(gene_upper_to_real.keys())

    # --- Load grouped mutation counts ---
    gm = pd.read_csv(GROUPED_COUNTS_CSV)
    gene_col = pick_gene_label_column(gm)
    value_cols = [c for c in gm.columns if c != gene_col]

    # Ensure numeric counts; replace non-numeric with 0.0
    for c in value_cols:
        gm[c] = pd.to_numeric(gm[c], errors="coerce").fillna(0.0)

    # Initialize per-gene matrix with zeros (one row per gene in positions)
    value_frame = pd.DataFrame(0.0, index=pos["gene"].tolist(), columns=value_cols)

    # --- Populate counts from grouped_mutations ---
    matched_rows = 0
    multi_map_rows = 0
    no_match_rows = 0

    for _, row in gm.iterrows():
        label = row[gene_col]
        series_vals = row[value_cols]  # numeric values
        tokens = clean_gene_tokens(label)

        # Keep only tokens found in positions
        hits_up = [t for t in tokens if t in valid_gene_set]

        if not hits_up:
            no_match_rows += 1
            continue
        if len(hits_up) > 1:
            multi_map_rows += 1

        for up in hits_up:
            real = gene_upper_to_real[up]
            # Add values (if same gene appears multiple times, counts accumulate)
            value_frame.loc[real, value_cols] += series_vals.values

        matched_rows += 1

    # --- Merge positions + counts ---
    merged = pos.drop(columns="__GENE_UP__").merge(
        value_frame.reset_index().rename(columns={"index": "gene"}),
        on="gene",
        how="left",
    )

    # Replace any NaNs with zeros
    for c in value_cols:
        merged[c] = merged[c].fillna(0.0)

    # Sort by genomic order
    merged = merged.sort_values(["chr", "start", "end", "gene"]).reset_index(drop=True)

    # --- Write outputs ---
    merged.to_csv(OUT_CSV, index=False)
    merged.to_csv(OUT_TSV, sep="\t", index=False)

    # --- Console summary ---
    print(f"Wrote CSV: {OUT_CSV}")
    print(f"Wrote TSV: {OUT_TSV}")
    print("---- Summary ----")
    print(f"Grouped rows processed: {len(gm)}")
    print(f"Matched rows (>=1 gene hit): {matched_rows}")
    print(f"Rows with multiple gene hits: {multi_map_rows}")
    print(f"Rows with no gene hits: {no_match_rows}")
    print(f"Genes in positions table: {len(pos)}")
    print(f"Genes with any nonzero counts: {(value_frame.sum(axis=1) > 0).sum()}")

if __name__ == "__main__":
    main()