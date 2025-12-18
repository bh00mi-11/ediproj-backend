from deepface import DeepFace
import os

DATASET_DIR = "dataset"

def match_face(uploaded_image_path):
    result = DeepFace.find(
        img_path=uploaded_image_path,
        db_path=DATASET_DIR,
        enforce_detection=False
    )

    if result and not result[0].empty:
        matched_path = result[0].iloc[0]["identity"]
        return os.path.basename(matched_path)

    return None
