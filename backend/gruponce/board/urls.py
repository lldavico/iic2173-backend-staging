from django.urls import path
from gruponce.board import board_views as views

urlpatterns = [
    path(r"create_board", views.create_board, name="create_board"),
    path(r"delete_board", views.delete_board, name="delete_board"),
    path(r"get_boards", views.get_boards, name="get_boards"),
]
