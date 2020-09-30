from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
import gruponce.session.session_views as views

urlpatterns = [
    path(r'token', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh/', views.MyTokenObtainPairView.as_view(), name='token_refresh'),
]
