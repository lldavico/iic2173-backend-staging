from django.urls import path, include

urlpatterns = [
    path(r"boards/", include("gruponce.board.urls"), name="boards"),
]
