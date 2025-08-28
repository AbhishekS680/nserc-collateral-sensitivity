#!/bin/bash
# ==============================================================================
# Title: Trim paired-end Illumina reads with Trimmomatic
# Purpose:
#   Run Trimmomatic on a batch of FASTQ pairs flagged by FastQC/MultiQC 
#   for adapter content issues. Produces paired and unpaired read files.
#
# Inputs:
#   - adapter_content_warnfail_samples.txt : two-column file with sample ID + status
#       (first column must contain filenames like SAMPLE_R1_001.fastq.gz)
#   - Raw FASTQ files in INPUT_DIR with naming:
#       <base>_R1_001.fastq.gz
#       <base>_R2_001.fastq.gz
#   - Custom adapter fasta (custom_combined.fa)
#
# Outputs (per sample) in OUTPUT_DIR:
#   <base>_R1_paired.fastq.gz
#   <base>_R1_unpaired.fastq.gz
#   <base>_R2_paired.fastq.gz
#   <base>_R2_unpaired.fastq.gz
#
# Usage:
#   bash trim_reads_trimmomatic.sh
# Notes:
#   - THREADS controls parallelism
#   - Status column in sample list is optional (just echoed)
#   - Creates OUTPUT_DIR if it doesn’t exist
# ==============================================================================

ADAPTERS=~/adapters/custom_combined.fa   # Adapter fasta for ILLUMINACLIP
THREADS=4                                # Number of threads for Trimmomatic
INPUT_DIR=~/250328_NestSeq_1-101_Wong    # Directory containing raw FASTQ files
OUTPUT_DIR=~/trimmed_reads               # Directory for trimmed outputs

mkdir -p $OUTPUT_DIR                     # Ensure output directory exists

# Loop over sample list: "<sample> <status>"
while read sample status; do
  # Strip _R1/_R2 suffix and _001 to get base sample name
  base=$(echo $sample | sed -E 's/_R[12]_001//')

  echo "Trimming sample $base ($status)..."

  # Run Trimmomatic in paired-end mode
  trimmomatic PE -threads $THREADS \
    $INPUT_DIR/${base}_R1_001.fastq.gz $INPUT_DIR/${base}_R2_001.fastq.gz \
    $OUTPUT_DIR/${base}_R1_paired.fastq.gz $OUTPUT_DIR/${base}_R1_unpaired.fastq.gz \
    $OUTPUT_DIR/${base}_R2_paired.fastq.gz $OUTPUT_DIR/${base}_R2_unpaired.fastq.gz \
    ILLUMINACLIP:$ADAPTERS:2:30:10 \   # Adapter trimming
    LEADING:3 TRAILING:3 \             # Trim low-quality bases at ends
    SLIDINGWINDOW:4:15 \               # Sliding window trim (window=4, minQ=15)
    MINLEN:36                          # Drop reads shorter than 36 bases

done < adapter_content_warnfail_samples.txt