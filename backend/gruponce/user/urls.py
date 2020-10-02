from django.urls import path
from gruponce.user import user_views as views

urlpatterns = [
    path(r"create_user", views.create_user, name="create_user"),
]
