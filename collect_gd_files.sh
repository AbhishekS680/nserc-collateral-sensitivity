#!/bin/bash
# ==============================================================================
# Title: Collect and rename Breseq .gd files
# Purpose:
#   Copy each sample’s Breseq output.gd file into a single folder (filtered_gd),
#   renaming the files to match their sample names.
#
# Inputs:
#   - breseq_output/<sample>/output/output.gd
#
# Outputs:
#   - filtered_gd/<sample>.gd
#
# Usage:
#   bash collect_gd_files.sh
#
# Notes:
#   - Creates DEST_DIR if it doesn’t exist
#   - Skips any sample directories missing output/output.gd
# ==============================================================================

# Define base directories (relative to project root)
BRESEQ_DIR="$project_root/breseq_output"
DEST_DIR="$project_root/filtered_gd"

# Create the destination folder if it doesn't exist
mkdir -p "$DEST_DIR"

# Loop through each sample directory inside breseq_output
for sample_dir in "$BRESEQ_DIR"/*; do
    # Get the sample name from folder name
    sample_name=$(basename "$sample_dir")

    # Define full path to the output.gd file
    gd_file="$sample_dir/output/output.gd"

    # Check if output.gd exists for this sample
    if [[ -f "$gd_file" ]]; then
        # Copy and rename to DEST_DIR/<sample>.gd
        cp "$gd_file" "$DEST_DIR/${sample_name}.gd"
    fi
done

echo "✅ All output.gd files copied and renamed to sample names."
