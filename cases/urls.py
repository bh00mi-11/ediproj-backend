from django.urls import path
from .views import submit_case, verify_case, delete_case  # import delete_case

urlpatterns = [
    path("submit/", submit_case),
    path("verify/<str:case_id>/", verify_case),
    path("delete/<str:case_id>/", delete_case),  # NEW: Delete endpoint
]
