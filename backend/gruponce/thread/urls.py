from django.urls import path
from gruponce.thread import thread_views as views

urlpatterns = [
    path(r"create_threads", views.create_thread, name="create_thread"),
    path(r"get_threads", views.get_threads, name="get_threads"),
]