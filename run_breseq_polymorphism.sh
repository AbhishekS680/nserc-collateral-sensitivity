#!/bin/bash
# ==============================================================================
# Title: Run Breseq (polymorphism mode) on paired-end trimmed reads
# Purpose:
#   Automate Breseq runs for all trimmed paired-end FASTQ files in a directory,
#   generating one output folder per sample.
#
# Inputs:
#   - trimmed_samples/*_R1_trimmed.fastq.gz
#   - trimmed_samples/*_R2_trimmed.fastq.gz
#   - Reference genome: sequence.gb
#
# Outputs:
#   - breseq_output/<sample>/   # Breseq results for each sample
#
# Notes:
#   - Uses Breseq in polymorphism mode (-p) to detect mixed variants
#   - Assumes paired-end files follow naming convention:
#       <sample>_R1_trimmed.fastq.gz
#       <sample>_R2_trimmed.fastq.gz
#   - Creates breseq_output/ if it doesn’t exist
# ==============================================================================

mkdir -p breseq_output   # Ensure output directory exists

# Loop over all R1 reads in trimmed_samples/
for R1 in trimmed_samples/*_R1_trimmed.fastq.gz
do
    # Derive sample name from R1 filename
    sample=$(basename "$R1" _R1_trimmed.fastq.gz)

    # Construct R2 filename from sample name
    R2="trimmed_samples/${sample}_R2_trimmed.fastq.gz"

    # Define output directory for this sample
    outdir="breseq_output/${sample}"

    echo "Running Breseq (polymorphism mode) for $sample..."

    # Run Breseq with:
    #   -p : polymorphism mode
    #   -r : reference genome (GenBank format)
    #   -o : output directory
    breseq -p -r sequence.gb -o "$outdir" "$R1" "$R2"
done