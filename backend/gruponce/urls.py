from django.urls import path, include

urlpatterns = [
    path(r"users/", include("gruponce.user.urls"), name="users"),
]
