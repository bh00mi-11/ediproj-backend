from deepface import DeepFace
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "data", "ffhq_images_subset")

# Adjust threshold: lower → stricter match
THRESHOLD = 0.65  

def match_face(uploaded_image_path):
    dfs = DeepFace.find(
        img_path=uploaded_image_path,
        db_path=DATASET_DIR,
        enforce_detection=False,
        detector_backend="opencv",
        model_name="VGG-Face",
        silent=True
    )

    if not dfs or dfs[0].empty:
        return None

    best_match = dfs[0].iloc[0]
    distance = float(best_match["distance"])
    print("🔍 Face distance:", distance)

    if distance <= THRESHOLD:
        # Only return actual dataset identity if available
        identity_name = os.path.basename(best_match["identity"])
        if identity_name.lower().endswith((".jpg", ".png")):
            return {
                "identity": identity_name,
                "distance": distance
            }
    
    # If distance > threshold or identity invalid → treat as NO MATCH
    return None

