import os
import shutil
from pathlib import Path

import pandas as pd

# Paths
text_folder = Path("data/spaccc/raw_txt/")
output_folder = Path("data/spaccc/brat_output/")


# Load TSV
for split in ["test", "train"]:
    (output_folder / split).mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(f"data/spaccc/{split}.tsv", sep="\t")
    # Group by filename
    grouped = df.groupby("filename")

    for filename, group in grouped:
        # Read raw text
        text_path = text_folder / split / f"{filename}.txt"
        if not text_path.exists():
            print(f"Warning: {text_path} not found, skipping.")
            continue

        with open(text_path, encoding="utf-8") as f:
            text = f.read()

        # Write the text to output folder
        output_txt_path = output_folder / split / f"{filename}.txt"
        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        # Create the .ann file
        output_ann_path = output_folder / split / f"{filename}.ann"
        with open(output_ann_path, "w", encoding="utf-8") as f:
            for i, row in enumerate(group.itertuples(), start=1):
                # Brat format: T<ID> <LABEL> <START> <END> <TEXT>
                span_text = text[row.start_span : row.end_span]
                f.write(
                    f"T{i}\t{row.label} {row.start_span} {row.end_span}\t{span_text}\n"
                )

    print(f"Converted {split} split.")

print("Conversion completed!")

# Path to your original BRAT folder
source_folder = "data/spaccc/test"
# Path to the new folder (will be created)
target_folder = "data/spaccc/test_pred"

# Create target folder if it doesn't exist
os.makedirs(target_folder, exist_ok=True)

# Iterate over all files in the source folder
for filename in os.listdir(source_folder):
    source_file = os.path.join(source_folder, filename)
    target_file = os.path.join(target_folder, filename)

    if filename.endswith(".txt"):
        # Copy txt files as-is
        shutil.copy2(source_file, target_file)
    elif filename.endswith(".ann"):
        # Create empty ann files
        with open(target_file, "w") as f:
            pass  # creates an empty file

print(f"Copied BRAT folder to '{target_folder}' with empty .ann files.")
