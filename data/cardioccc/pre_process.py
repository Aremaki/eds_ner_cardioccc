import os
import shutil

# Path to your BRAT folder
brat_folder = "data/cardioccc/test"

# Mapping of Spanish → English labels
label_map = {
    "ENFERMEDAD": "DISEASE",
    "PROCEDIMIENTO": "PROCEDURE",
    "SINTOMA": "SYMPTOM",
    "FARMACO": "MEDICATION",
}

# Process all .ann files
for filename in os.listdir(brat_folder):
    if filename.endswith(".ann"):
        ann_path = os.path.join(brat_folder, filename)

        with open(ann_path, encoding="utf-8") as f:
            content = f.read()

        # Replace labels
        for spanish, english in label_map.items():
            content = content.replace(f"\t{spanish} ", f"\t{english} ")

        # Write back to file
        with open(ann_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Updated labels in: {filename}")

print("🎉 All .ann files updated successfully!")

# Path to your original BRAT folder
source_folder = "data/cardioccc/test"
# Path to the new folder (will be created)
target_folder = "data/cardioccc/test_pred"

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
