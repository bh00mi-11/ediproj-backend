from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pymongo import MongoClient
import gridfs
from bson import ObjectId
from tempfile import NamedTemporaryFile
import os

from .email_utils import send_match_email, send_no_match_email
from .deepface_match import match_face


client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
fs = gridfs.GridFS(db)


# ---------------- SUBMIT CASE ----------------
@csrf_exempt
def submit_case(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    # ✅ VALIDATE ROLE
    role = request.POST.get("role")
    allowed_submit_roles = ["family", "ngo", "police", "admin"]

    if role not in allowed_submit_roles:
        return JsonResponse({"error": "Unauthorized role"}, status=403)

    image = request.FILES.get("photo")
    notification_email = request.POST.get("notification_email")

    if not image:
        return JsonResponse({"error": "Photo required"}, status=400)

    if not notification_email or "@" not in notification_email:
        return JsonResponse({"error": "Valid email required"}, status=400)

    image_id = fs.put(image.read(), filename=image.name)

    case = {
        "submitted_by": role,  # ✅ SAFE & CORRECT
        "full_name": request.POST.get("full_name"),
        "age": int(request.POST.get("age", 0)),
        "gender": request.POST.get("gender"),
        "birthdate": request.POST.get("birthdate"),
        "contact_number": request.POST.get("contact_number"),
        "notification_email": notification_email,
        "last_seen_location": request.POST.get("last_seen_location"),
        "additional_details": request.POST.get("additional_details"),
        "image_id": image_id,
        "verified": False,
        "matched": False,
        "verification_reason": None,
        "matched_person": None,
        "verified_by": None,
    }

    case_id = db.cases.insert_one(case).inserted_id
    return JsonResponse({"success": True, "case_id": str(case_id)})

# ---------------- VERIFY CASE ----------------

@csrf_exempt
def verify_case(request, case_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    case = db.cases.find_one({"_id": ObjectId(case_id)})
    if not case:
        return JsonResponse({"error": "Case not found"}, status=404)

    # Load image
    image_bytes = fs.get(case["image_id"]).read()
    with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    try:
        matched = match_face(tmp_path)
    except Exception as e:
        os.remove(tmp_path)
        return JsonResponse({"error": str(e)}, status=500)

    os.remove(tmp_path)

    # ❌ No face match
    if not matched:
     _update(case_id, False, "Face not matched")
    try:
        # This email now clearly says no match was found
        send_no_match_email(case.get("notification_email"), case)
    except Exception as e:
        print("No-match email error:", e)
    return _response(False, "No match found")


    # ✅ FACE MATCHED → check textual info if needed
    matched_person_data = {
        "full_name": os.path.splitext(matched["identity"])[0],
        "distance": matched["distance"]
    }

    # For demo, we treat face match alone as verification
    _update(case_id, True, "Face matched", matched_person_data)

    try:
        send_match_email(case.get("notification_email"), case, matched_person_data)
    except Exception as e:
        print("Match email error:", e)

    return _response(True, "Verified successfully", matched_person_data)


# ----------------- HELPERS -----------------
def _update(case_id, success, reason, matched_person=None, verifier_role=None):
    db.cases.update_one(
        {"_id": ObjectId(case_id)},
        {"$set": {
            "verified": success,
            "matched": success,
            "verification_reason": reason,
            "matched_person": matched_person,
            "verified_by": verifier_role
        }}
    )


def _response(success, reason, matched_person=None, verifier_role=None):
    return JsonResponse({
        "success": success,
        "verified": success,
        "reason": reason,
        "matched_person": matched_person,
        "verified_by": verifier_role
    })


# ---------------- GET PENDING CASES ----------------
def get_all_cases(request):
    cases = db.cases.find({"verified": False})
    result = []

    for c in cases:
        result.append({
            "_id": str(c["_id"]),
            "full_name": c.get("full_name"),
            "age": c.get("age"),
            "gender": c.get("gender"),
            "birthdate": c.get("birthdate"),
            "contact_number": c.get("contact_number"),
            "notification_email": c.get("notification_email"),
            "last_seen_location": c.get("last_seen_location"),
            "additional_details": c.get("additional_details"),
        })

    return JsonResponse(result, safe=False)
