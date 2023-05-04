from django.contrib import admin
from django.urls import path
from .views import ProfileEditView

urlpatterns = [
    path("edit_profile/", ProfileEditView.as_view(), name="edit_profile")
]
