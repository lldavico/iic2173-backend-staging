from django.urls import path, include

urlpatterns = [
    path(r"users/", include("gruponce.user.urls"), name="users"),
    path(r"session/", include("gruponce.session.urls"), name="session"),
    path(r"boards/", include("gruponce.board.urls"), name="boards"),
    path(r"threads/", include("gruponce.thread.urls"), name="threads"),
    path(r"messages/", include("gruponce.messages.urls"), name="messages"),
]
