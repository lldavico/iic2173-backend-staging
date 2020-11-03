from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from gruponce.helpers import get_request_parameters
import gruponce.user.user_services as user_services
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated


@api_view(["POST"])
def create_user(request):
    parameters = get_request_parameters(request)
    first_name = parameters['firstName']
    last_name = parameters['lastName']
    username = parameters['username']
    password = parameters['password']
    email = parameters['email']
    response = user_services.create_user(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,
        email=email,
    )
    return Response({"userData": response})
