import os
import csv
from django.core.management.base import BaseCommand
from pymongo import MongoClient
import gridfs
from deepface import DeepFace
from django.conf import settings


class Command(BaseCommand):
    help = "Import CSV + Images into MongoDB + Generate Embeddings"

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str, required=True)
        parser.add_argument("--img-dir", type=str, required=True)

    def handle(self, *args, **options):
        csv_file = options["file"]
        img_dir = options["img_dir"]

        # Connect to Mongo
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.MONGO_DB_NAME]
        people = db.people
        fs = gridfs.GridFS(db)

        self.stdout.write(self.style.SUCCESS("Connected to MongoDB"))

        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for idx, row in enumerate(reader):
                image_name = row.get("final_image")   # your column name

                if not image_name:
                    self.stdout.write(self.style.WARNING(
                        f"Row {idx}: No image name found"
                    ))
                    continue

                file_path = os.path.join(img_dir, image_name)

                if not os.path.exists(file_path):
                    self.stdout.write(self.style.WARNING(
                        f"Row {idx}: Image not found → {file_path}"
                    ))
                    continue

                # Store image in GridFS ----------------------
                with open(file_path, "rb") as img_file:
                    file_id = fs.put(img_file, filename=image_name)

                # Generate embedding -------------------------
                embedding = None
                try:
                    result = DeepFace.represent(
                        img_path=file_path,
                        model_name="VGG-Face",
                        detector_backend="skip",   # important!
                        enforce_detection=False
                    )
                    embedding = result[0]["embedding"]

                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"Embedding error for {image_name}: {e}"
                    ))

                # Insert into MongoDB ------------------------
                doc = {
                    "csv_data": row,          # store all CSV columns
                    "image_file_id": file_id, # gridfs reference
                    "embedding": embedding
                }

                people.insert_one(doc)

                self.stdout.write(self.style.SUCCESS(
                    f"Imported {idx+1}: {image_name}"
                ))

        self.stdout.write(self.style.SUCCESS("DONE ✔ All rows imported"))
