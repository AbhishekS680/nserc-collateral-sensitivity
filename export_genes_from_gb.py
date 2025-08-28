# ==============================================================================
# Title: Export gene coordinates from GenBank file
# Purpose:
#   Parse a reference genome (.gb) and extract CDS gene positions to a CSV.
#   Output is suitable for downstream visualization (e.g., Circos).
#
# Inputs:
#   - sequence.gb : reference genome in GenBank format
#
# Outputs:
#   - positions_from_gb.csv
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

IN_GB  = "/Users/abhisheksinha/Desktop/NSERC/circos/sequence.gb"
OUT_CSV = "/Users/abhisheksinha/Desktop/NSERC/circos/positions_from_gb.csv"

# Read reference genome
record = SeqIO.read(IN_GB, "genbank")

# Open CSV for writing gene coordinates
with open(OUT_CSV, "w", newline="") as out:
    w = csv.writer(out)
    # Header row: like BED format but with gene name
    w.writerow(["chr", "start", "end", "gene"])  
    
    # Iterate over features, keep only CDS annotations
    for feat in record.features:
        if feat.type != "CDS":
            continue

        # Prefer 'gene', fall back to 'locus_tag' if gene is missing
        gene  = feat.qualifiers.get("gene", [None])[0]
        locus = feat.qualifiers.get("locus_tag", [None])[0]
        name = gene if gene else locus
        if not name:
            continue

        # Convert coordinates to 1-based start, end inclusive
        start = int(feat.location.start) + 1
        end   = int(feat.location.end)

        # Write row: chromosome ID, start, end, gene name
        w.writerow([record.id, start, end, name])

print("Wrote", OUT_CSV)