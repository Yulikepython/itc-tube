from django.urls import path
from .views import ProfileUpdateView

urlpatterns = [
    path("<int:pk>/", ProfileUpdateView.as_view(), name="profile-update"),
]