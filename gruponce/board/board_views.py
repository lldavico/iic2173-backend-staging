from backend.settings import REDIS_CACHE_ENV
import os
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from gruponce.helpers import get_request_parameters
import gruponce.board.board_services as boards_services
from django.core.cache import cache
from django_redis import get_redis_connection
import redis


print("CREATED REDIS INSTANCE")
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


# DELETE BOARD
@api_view(["DELETE"])
def delete_board(request):
    parameters = get_request_parameters(request)
    board_id = parameters['board_id']
    stat, response = boards_services.delete_board(board_id=board_id)
    if not stat:
        if int(response) == 409:
            # Board already exists "
            return Response({"error": "Board already exists"}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"error": "Error en la consulta"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": response})


# GET BOARDS
@api_view(["GET"])
def get_boards(request):
    print("waa")
    stat, response = boards_services.get_boards()
    if not stat:
        return Response({"error": "Error en la consulta"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"boards": response})

# GET BOARDS FROM CACHE
@api_view(['GET'])
def get_cached_boards(request):
    print("GET CACHED BOARDS")
    try:
        if 'board' in cache:
            # get results from cache
            print("Before cache.get")
            boards = cache.get('board')
            return Response({'boards': boards}, status=status.HTTP_201_CREATED)
    
        else:
            print("Me fui al else")
            stat, response = boards_services.get_boards()
            if not stat:
                return Response({"error": "Error en la consulta"}, status=status.HTTP_400_BAD_REQUEST)
            # store data in cache
            cache.set('board', response, timeout=1800)
            return Response({"boards": response})
            # return Response(results, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(e)
        return False, "Error"