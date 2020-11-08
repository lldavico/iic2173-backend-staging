from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.decorators import login_required

from gruponce.messages import messages_services
from gruponce.helpers import analyze, get_request_parameters, get_user_from_meta

from django.core.cache import cache

@api_view(["POST"])
@login_required()
def create_message(request):
    parameters = get_request_parameters(request)
    user = get_user_from_meta(request)
    thread_id = parameters['threadId']
    sender_id = user.id
    message_content = parameters['messageContent']
    stat, response = messages_services.create_message(thread_id=thread_id,
                                                sender_id=sender_id,
                                                message_content=message_content
                                                )
    if not stat:
        return Response({"error": response}, status=status.HTTP_400_BAD_REQUEST)
    comprehend_result = analyze(message_content)
    response["AWSSentiment"] = comprehend_result
    return Response({"messageData": response})


@api_view(["GET"])
@login_required()
def get_all_messages(request):
    response = messages_services.get_all_messages()
    return Response({"messages": response})


@api_view(["GET"])
def get_thread_messages(request, thread_id=None):
    if thread_id is None or type(thread_id) != int:
        return Response({"error": "Invalid Thread"}, status=status.HTTP_400_BAD_REQUEST)
    stat, response = messages_services.get_thread_messages(thread_id=thread_id)
    if not stat:
        return Response({"error": response}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"messages": response})


@api_view(["POST"])

@login_required()
def get_my_messages(request):
    try:
        user = get_user_from_meta(request)
        parameters = get_request_parameters(request)
        thread_id = parameters.get('threadId', None)
        stat, response = messages_services.get_my_messages(user_id=user.id, thread_id=thread_id)
        if not stat:
            return Response({"error": response}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"messages": response})
    except Exception as e:
        return Response({ 'error': 'Error po mi rey' }, status=status.HTTP_400_BAD_REQUEST)

# GET BOARDS FROM CACHE
@api_view(['GET'])
def get_cached_thread_messages(request, thread_id=None):
    if thread_id is None or type(thread_id) != int:
        return Response({"error": "Invalid Thread"}, status=status.HTTP_400_BAD_REQUEST)
    elif 'thread_message' + str(thread_id) in cache:
        # get results from cache
        thread_messages = cache.get('thread_message' + str(thread_id))
        return Response({'messages': thread_messages}, status=status.HTTP_201_CREATED)
 
    else:
        stat, response = messages_services.get_thread_messages(thread_id)
        if not stat:
            return Response({"error": "Error en la consulta"}, status=status.HTTP_400_BAD_REQUEST)
        # store data in cache
        cache.set('thread_message' + str(thread_id), response, timeout=30)
        return Response({"messages": response})