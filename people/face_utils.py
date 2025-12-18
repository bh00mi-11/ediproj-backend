from deepface import DeepFace
import numpy as np
import cv2

def get_embedding(image_bytes):
    # Convert bytes → OpenCV image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # DeepFace embedding
    embedding = DeepFace.represent(img, model_name="VGG-Face")[0]["embedding"]
    return embedding
