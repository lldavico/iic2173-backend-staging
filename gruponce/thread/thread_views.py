from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from gruponce.helpers import get_request_parameters
import gruponce.thread.thread_services as thread_services


# CREATE THREAD
@api_view(["POST"])
def create_thread(request):
    parameters = get_request_parameters(request)
    subject = parameters['subject']
    board_id = parameters['board_id']
    stat, response = thread_services.create_thread(subject =subject, board_id =board_id)
    if not stat:
        if int(response) == 409:
            # Thread creation failed "
            return Response({"error": "Thread creation failed."}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"error": "Error en la consulta"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"thread": response})

# GET THREADS
@api_view(["GET"])
def get_threads(request):
    stat, response = thread_services.get_threads()
    if not stat:
        return Response({"error": "Error en la consulta"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"threads": response})


# GET BOARD THREAD
@api_view(["GET"])
def get_board_threads(request, board_id=None):
    if board_id is None:
        return Response({"error": "Invalid Board"}, status=status.HTTP_400_BAD_REQUEST)
    stat, response = thread_services.get_board_threads(board_id=board_id)
    if not stat:
        return Response({"error": response}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"threads": response})