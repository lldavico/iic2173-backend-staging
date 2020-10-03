from gruponce.models import User, MessageModel, ThreadModel
from gruponce.user.user_services import verify_user_exists
from gruponce.thread.thread_services import verify_thread_exists
from gruponce.messages.serializer import MessageSerializer


def create_message(thread_id, sender_id, message_content):
    """Creates Messages instance
    PARAMS:
    - thread_id (<int>): Id of the Thread where the message was created
    - sender_id (<int>): Id of the Message sender
    - message_content (<str>): String containing the content of the message"""

    # TODO: Validate input to avoid SQL Injection

    try:
        # Verify if user exists
        if not verify_user_exists(('id', sender_id)):
            print(f"User {sender_id} dont exists")
            raise Exception(404)

        # Verify if thread exists
        if not verify_thread_exists(('id', thread_id)):
            print(f"Thread {thread_id} dont exists")
            raise Exception(404)

        # Create Message
        user_inst = User.objects.get(id=sender_id)
        thread_inst = ThreadModel.objects.get(id=thread_id)

        message_ins = MessageModel.objects.create(thread=thread_inst,
                                                message_content=message_content,
                                                user_sender=user_inst)
        res = MessageSerializer(message_ins).data

        return True, res

    except Exception as e:
        return False, e.args[0]


def get_all_messages():
    """Retrieves all messages in database"""
    return [MessageSerializer(message).data for message in MessageModel.objects.all()]


def get_thread_messages(thread_id):
    """Retrieves Messages from a Thread
    PARAMS
    - thread_id (<int>): Id of the a Thread"""

    try:
        # Verify if thread exists
        if not verify_thread_exists(('id', thread_id)):
            print(f"Thread {thread_id} dont exists")
            raise Exception(404)

        # Get Messages
        res = [MessageSerializer(message).data for message in MessageModel.objects.filter(thread__id=thread_id)]

        return True, res

    except Exception as e:
        return False, e.args[0]


def get_my_messages(user_id, thread_id=None):
    """Returns the messages sended by a user
    PARAMS:
    - user_id (<int>): Id of the user
    - thread_id *OPTIONAL (<int>): Thread Id to filter the user messages, if not provided, all messages are retrieved
    """

    try:
        params = {'user_sender__id': user_id}
        # Verify if thread exists
        if thread_id is not None:
            if not verify_thread_exists(('id', thread_id)):
                print(f"Thread {thread_id} dont exists")
                raise Exception(404)
            params['thread__id'] = thread_id

        messages = MessageModel.objects.filter(**params)
        # Get User Messages
        res = [MessageSerializer(message).data for message in messages]

        return True, res

    except Exception as e:
        return False, e.args[0]
