from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

User = get_user_model()

@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    data = json.loads(request.body)

    if User.objects.filter(username=data["username"]).exists():
        return JsonResponse({"error": "User exists"}, status=400)

    User.objects.create_user(
        username=data["username"],
        email=data.get("email"),
        password=data["password"],
        first_name=data.get("first_name", ""),
        last_name=data.get("last_name", ""),
        role=data.get("role", "family")
    )

    return JsonResponse({"success": True})


@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    if not user.check_password(password):
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({
        "success": True,
        "username": user.username,
        "role": user.role
    })
