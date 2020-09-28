from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from gruponce.helpers import get_request_parameters
import gruponce.board.board_services as boards_services


# CREATE BOARD
@api_view(["POST"])
def create_board(request):
    parameters = get_request_parameters(request)
    name = parameters['board_name']
    text = parameters['board_text']
    stat, response = boards_services.create_board(board_name=name, board_text=text)
    if not stat:
        if int(response) == 409:
            # Board already exists "
            return Response({"error": "Board already exists"}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"error": "Error en la consulta"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"board": response})

# GET BOARDS
@api_view(["GET"])
def get_boards(request):
    stat, response = boards_services.get_boards()
    if not stat:
        return Response({"error": "Error en la consulta"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"boards": response})