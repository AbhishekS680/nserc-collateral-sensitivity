import os
import re
import subprocess

# ==============================================================================
# Title: Subtract ancestor mutations from Breseq .gd files
# Purpose:
#   For each evolved sample, subtract mutations found in its ancestor population
#   (AH_S2 or MG_S1) to filter out "lab-adapted" background mutations.
#
# Inputs:
#   - breseq_output/<sample>/output/output.gd      # raw Breseq calls
#   - breseq_output/AH_S2/output/output.gd         # AH ancestor
#   - breseq_output/MG_S1/output/output.gd         # MG ancestor
#
# Outputs:
#   - breseq_output/filtered_gd/<sample>.gd        # filtered .gd (per sample)
#
# Logic:
#   - Samples 1–5 → subtract MG_S1 ancestor
#   - Samples 6–10 → subtract AH_S2 ancestor
#   - Other folders are skipped
#
# Dependencies:
#   - gdtools (Breseq toolkit) must be on PATH
#
# Usage:
#   python subtract_ancestors_gd.py
# ==============================================================================

base_dir = "/Users/abhisheksinha/Desktop/NSERC/breseq_output"
output_dir = os.path.join(base_dir, "filtered_gd")
ah_ancestor = os.path.join(base_dir, "AH_S2/output/output.gd")
mg_ancestor = os.path.join(base_dir, "MG_S1/output/output.gd")

os.makedirs(output_dir, exist_ok=True)

def extract_sample_number(name):
    """Extract the first integer found in the folder name, e.g. 'Cef7' → 7."""
    match = re.search(r'(\d+)', name)
    return int(match.group(1)) if match else None

# Loop over all sample folders in breseq_output
for sample_folder in os.listdir(base_dir):
    sample_path = os.path.join(base_dir, sample_folder, "output", "output.gd")
    
    if not os.path.isfile(sample_path):
        # Skip if no Breseq .gd file is found
        continue

    sample_number = extract_sample_number(sample_folder)
    if sample_number is None:
        # Skip if folder name has no number (e.g. AH_S2, MG_S1)
        continue

    # Assign correct ancestor based on sample numbering
    if 6 <= sample_number <= 10:
        ancestor = ah_ancestor
    elif 1 <= sample_number <= 5:
        ancestor = mg_ancestor
    else:
        continue 

    # Define filtered output path
    output_file = os.path.join(output_dir, f"{sample_folder}.gd")
    print(f"Subtracting {os.path.basename(ancestor)} from {sample_folder} → {output_file}")
    
    # Run gdtools SUBTRACT: removes shared mutations between sample and ancestor
    subprocess.run([
        "gdtools", "SUBTRACT",
        "-o", output_file,
        sample_path,
        ancestor
    ])