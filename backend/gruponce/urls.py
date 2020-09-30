from django.urls import path, include

urlpatterns = [
    path(r"boards/", include("gruponce.board.urls"), name="boards"),
    path(r"threads/", include("gruponce.thread.urls"), name="threads"),
]
