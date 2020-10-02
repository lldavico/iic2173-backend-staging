from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from gruponce.messages import messages_services
from gruponce.helpers import get_request_parameters, get_user_from_meta


@api_view(["POST"])
def create_message(request):
    parameters = get_request_parameters(request)
    thread_id = parameters['threadId']
    sender_id = parameters['senderId']
    message_content = parameters['messageContent']
    response = messages_services.create_message(thread_id=thread_id,
                                                sender_id=sender_id,
                                                message_content=message_content
                                                )
    return Response({"response": response})


@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def get_all_messages(request):
    user = get_user_from_meta(request.META)
    if not user or not user.is_superuser:
        return Response({"error": "Unauthorized"},
                        status=status.HTTP_401_UNAUTHORIZED)
    response = messages_services.get_all_messages()
    return Response({"orders": response})


@api_view(["GET"])
def get_thread_messages(request, thread_id=None):
    if thread_id is None or type(thread_id) != int:
        return Response({"error": "Invalid Thread"}, status=status.HTTP_400_BAD_REQUEST)
    stat, response = messages_services.get_thread_messages(thread_id=thread_id)
    if not stat:
        return Response({"error": response}, status=status.HTTP_400_BAD_REQUEST)
    return Response(response)
