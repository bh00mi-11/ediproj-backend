import csv

CSV_PATH = "final_assigned_1000.csv"

def get_person_by_image(image_name):
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["image_path"].endswith(image_name):
                return row
    return None
