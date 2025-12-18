import os, tempfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import gridfs
from django.conf import settings
from bson.objectid import ObjectId
from .deepface_match import match_face
from .csv_loader import get_person_by_image
from .email_utils import send_match_email

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
fs = gridfs.GridFS(db)

@csrf_exempt
def submit_case(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    image = request.FILES.get("photo")
    data = request.POST.dict()

    # Save image temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        for chunk in image.chunks():
            tmp.write(chunk)
        temp_path = tmp.name

    matched_filename = match_face(temp_path)
    matched_person = None
    if matched_filename:
        matched_person = get_person_by_image(matched_filename)

    # Save image to GridFS
    image_id = fs.put(image.read(), filename=image.name)

    case = {
        "submitted_by": data.get("role"),
        "data": data,
        "image_id": image_id,
        "matched": bool(matched_person),
        "matched_person": matched_person,
        "verified": False
    }

    db.cases.insert_one(case)

    return JsonResponse({
        "success": True,
        "matched": bool(matched_person),
        "person": matched_person
    })

@csrf_exempt
def verify_case(request, case_id):
    case = db.cases.find_one({"_id": case_id})
    if not case:
        return JsonResponse({"error": "Not found"}, status=404)

    db.cases.update_one(
        {"_id": case_id},
        {"$set": {"verified": True}}
    )

    if case.get("matched_person"):
        send_match_email(
            case["matched_person"]["contact"],
            case["matched_person"]
        )

    return JsonResponse({"verified": True})

from .models import Case  # make sure this matches your model

@csrf_exempt
def delete_case(request, case_id):
    if request.method == "DELETE":
        try:
            # Convert string ID to Mongo ObjectId
            result = db.cases.delete_one({"_id": ObjectId(case_id)})
            if result.deleted_count == 1:
                return JsonResponse({"success": True, "message": "Case deleted successfully"})
            else:
                return JsonResponse({"success": False, "message": "Case not found"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"})
