from django.urls import path

from api.views import signup

urlpatterns = [
    path("signup/", signup, name="signup"),
]
