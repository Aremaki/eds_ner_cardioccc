import os

# Path to your BRAT folder
brat_folder = "test"

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
