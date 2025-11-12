import os
import shutil
from pathlib import Path

import pandas as pd

# Paths
text_folder = Path("data/spaccc/raw_txt/")
output_folder = Path("data/spaccc/brat_output/")

# Convert multiple TSVs (train/test)
for split in ["train", "test"]:
    (output_folder / split).mkdir(parents=True, exist_ok=True)

    # Collect all TSV files for the split
    tsv_files = list(Path("data/spaccc").glob(f"{split}*.tsv"))
    if not tsv_files:
        print(f"⚠️ No TSV files found for {split}, skipping.")
        continue

    print(
        f"Found {len(tsv_files)} TSV files for {split}: {[f.name for f in tsv_files]}"
    )

    # Load and concatenate all TSVs for this split
    dfs = []
    for tsv_file in tsv_files:
        df = pd.read_csv(tsv_file, sep="\t")
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)

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

        # Write text to output folder
        output_txt_path = output_folder / split / f"{filename}.txt"
        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        # Create .ann file
        output_ann_path = output_folder / split / f"{filename}.ann"
        with open(output_ann_path, "w", encoding="utf-8") as f:
            for i, row in enumerate(group.itertuples(), start=1):
                span_text = text[row.start_span : row.end_span]
                f.write(
                    f"T{i}\t{row.label} {row.start_span} {row.end_span}\t{span_text}\n"
                )

    print(f"✅ Converted {split} split to BRAT format.")

print("🎉 Conversion completed!")


# --- Optional: copy test folder to create an empty 'test_pred' version ---

source_folder = Path("data/spaccc/test")
target_folder = Path("data/spaccc/test_pred")

os.makedirs(target_folder, exist_ok=True)

for filename in os.listdir(source_folder):
    source_file = source_folder / filename
    target_file = target_folder / filename

    if filename.endswith(".txt"):
        shutil.copy2(source_file, target_file)
    elif filename.endswith(".ann"):
        # Create empty .ann files
        with open(target_file, "w") as f:
            pass

print(f"📂 Copied BRAT folder to '{target_folder}' with empty .ann files.")
