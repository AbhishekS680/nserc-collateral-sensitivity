#!/usr/bin/env python3
# ==============================================================================
# Title: Export gene coordinates from GenBank file
# Purpose:
#   Parse a reference genome (.gb) and extract CDS gene positions to a CSV.
#   Output is suitable for downstream visualization (e.g., Circos).
#
# Inputs:
#   - ./sequence.gb : reference genome in GenBank format
#
# Outputs:
#   - ./positions_from_gb.csv
#       Columns: chr, start, end, gene
#       (start/end are 1-based, gene name falls back to locus_tag if missing)
#
# Usage:
#   python export_genes_from_gb.py
#
# Dependencies:
#   - Biopython (pip install biopython)
# ==============================================================================

from Bio import SeqIO
import csv
import os

# Resolve paths relative to this script's directory (project root)
script_dir = os.path.dirname(os.path.abspath(__file__))

IN_GB = os.path.join(script_dir, "sequence.gb")
OUT_CSV = os.path.join(script_dir, "positions_from_gb.csv")

# Read reference genome
record = SeqIO.read(IN_GB, "genbank")

# Open CSV for writing gene coordinates
with open(OUT_CSV, "w", newline="") as out:
    w = csv.writer(out)
    # Header row
    w.writerow(["chr", "start", "end", "gene"])  
    
    # Iterate over features, keep only CDS annotations
    for feat in record.features:
        if feat.type != "CDS":
            continue

        # Prefer 'gene', fall back to 'locus_tag'
        gene  = feat.qualifiers.get("gene", [None])[0]
        locus = feat.qualifiers.get("locus_tag", [None])[0]
        name = gene if gene else locus
        if not name:
            continue

        # Convert coordinates to 1-based start, end inclusive
        start = int(feat.location.start) + 1
        end   = int(feat.location.end)

        # Write row
        w.writerow([record.id, start, end, name])

print(f"✅ Wrote {OUT_CSV}")
