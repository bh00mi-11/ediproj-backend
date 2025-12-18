from django.urls import path
from . import views

urlpatterns = [
    path("submit/", views.submit_case),
    path("verify/<str:case_id>/", views.verify_case),
    path("all/", views.get_all_cases),
    
]
