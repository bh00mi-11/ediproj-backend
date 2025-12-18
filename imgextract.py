import csv
import os
import shutil

# ---- CONFIG ----
CSV_PATH = r"C:\Users\manis\OneDrive\Desktop\ediproj\data\final_assigned_1000.csv"
SOURCE_IMG_DIR = r"C:\Users\manis\OneDrive\Desktop\ediproj\data\ffhq_images"
TARGET_IMG_DIR = r"C:\Users\manis\OneDrive\Desktop\ediproj\data\ffhq_images_subset"
IMAGE_COL = "final_image"   # Your column name
# -----------------

# Create target folder if not exists
os.makedirs(TARGET_IMG_DIR, exist_ok=True)

# Load CSV
with open(CSV_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"CSV rows found: {len(rows)}")

copied = 0
missing = []

for row in rows:
    image_name = row[IMAGE_COL].strip()

    src_path = os.path.join(SOURCE_IMG_DIR, image_name)
    dest_path = os.path.join(TARGET_IMG_DIR, image_name)

    if os.path.exists(src_path):
        shutil.copy(src_path, dest_path)
        copied += 1
    else:
        missing.append(image_name)

print("------------------------------------------------")
print(f"Images successfully copied: {copied}")
print(f"Missing images: {len(missing)}")

if missing:
    print("\nThese images were NOT found in the source folder:")
    for m in missing:
        print(" -", m)
