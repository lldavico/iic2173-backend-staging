from django.urls import path
from gruponce.messages import messages_views as views

urlpatterns = [
    path(r"create_message", views.create_message, name="create_message"),
    path(r"get_all_messages", views.get_all_messages, name="get_all_messages"),
    path(r"get_thread_messages/<int:thread_id>", views.get_thread_messages, name="get_thread_messages"),
    path(r"get_my_messages", views.get_my_messages, name="get_my_messages"),
]
