from django.urls import path
from gruponce.authorization_grant_provider import authorization_views as views


urlpatterns = [
    path(r"get_authorization_grant", views.AuthorizationView.as_view(), name="get_authorization_grant")
]
