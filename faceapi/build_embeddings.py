from deepface import DeepFace
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "data", "ffhq_images_subset")

print("🔹 Dataset path:", DATASET_DIR)

image_files = [
    f for f in os.listdir(DATASET_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

if not image_files:
    raise Exception("❌ No images found in dataset!")

print(f"🔹 Found {len(image_files)} images")
print("🔹 Building embeddings cache...")

DeepFace.find(
    img_path=os.path.join(DATASET_DIR, image_files[0]),
    db_path=DATASET_DIR,
    enforce_detection=False,
    detector_backend="opencv",
    model_name="VGG-Face"
)

print("✅ Embeddings cached successfully")
