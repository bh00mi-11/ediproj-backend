import os
import csv

csv_path = r"C:\Users\manis\OneDrive\Desktop\ediproj\data\final_assigned_1000.csv"

img_dir = r"C:\Users\manis\OneDrive\Desktop\ediproj\data\ffhq_images"


rows = list(csv.DictReader(open(csv_path)))
images = sorted(os.listdir(img_dir))

print("CSV rows:", len(rows))
print("Images:", len(images))

