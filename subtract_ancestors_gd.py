import re
import subprocess
from pathlib import Path

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

BASE_DIR = Path(__file__).resolve().parent / "breseq_output"
OUTPUT_DIR = BASE_DIR / "filtered_gd"
AH_ANCESTOR = BASE_DIR / "AH_S2" / "output" / "output.gd"
MG_ANCESTOR = BASE_DIR / "MG_S1" / "output" / "output.gd"

OUTPUT_DIR.mkdir(exist_ok=True)

def extract_sample_number(name: str) -> int | None:
    """Extract the first integer found in the folder name, e.g. 'Cef7' → 7."""
    match = re.search(r"(\d+)", name)
    return int(match.group(1)) if match else None

# Loop over all sample folders in breseq_output
for sample_folder in BASE_DIR.iterdir():
    sample_path = sample_folder / "output" / "output.gd"

    if not sample_path.is_file():
        # Skip if no Breseq .gd file is found
        continue

    sample_number = extract_sample_number(sample_folder.name)
    if sample_number is None:
        # Skip if folder name has no number (e.g. AH_S2, MG_S1)
        continue

    # Assign correct ancestor based on sample numbering
    if 6 <= sample_number <= 10:
        ancestor = AH_ANCESTOR
    elif 1 <= sample_number <= 5:
        ancestor = MG_ANCESTOR
    else:
        continue

    # Define filtered output path
    output_file = OUTPUT_DIR / f"{sample_folder.name}.gd"
    print(f"Subtracting {ancestor.name} from {sample_folder.name} → {output_file}")

    # Run gdtools SUBTRACT: removes shared mutations between sample and ancestor
    subprocess.run([
        "gdtools", "SUBTRACT",
        "-o", str(output_file),
        str(sample_path),
        str(ancestor)
    ])
