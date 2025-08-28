#!/bin/bash
# ==============================================================================
# Title: Annotate combined .gd files into an HTML mutation matrix
# Purpose:
#   Use gdtools ANNOTATE to merge all filtered .gd files and produce an
#   interactive HTML report of mutations relative to the reference genome.
#
# Inputs:
#   - sequence.gb                   # Reference genome in GenBank format
#   - filtered_gd/*.gd              # Per-sample filtered Breseq mutation files
#
# Outputs:
#   - mutation_matrix.html          # Combined annotated mutation matrix (HTML)
#
# Usage:
#   bash annotate_mutations_html.sh
#
# Notes:
#   - Requires gdtools (part of Breseq) in PATH
#   - The HTML output can be opened in any web browser
# ==============================================================================

gdtools ANNOTATE \
  -r /Users/abhisheksinha/Desktop/NSERC/breseq/sequence.gb \
  -o /Users/abhisheksinha/Desktop/NSERC/breseq/mutation_matrix.html \
  -f HTML \
  /Users/abhisheksinha/Desktop/NSERC/breseq/filtered_gd/*.gd