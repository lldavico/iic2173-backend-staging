from gruponce.models import ThreadModel, ThreadManager
from gruponce.thread.serializer import ThreadSerializer


def verify_thread_exists(thread_tuple):
    """Verify if thread exist. Receives a tuple with the parameter to verify and the value of it
    PARAMS:
        - thread_tuple (tuple[<field>, <value>]): Field corresponds to the param of evaluation, and value corresponds to that field value
        Example: ("id", 19); ("thread_name", "Threaddy Mercury")
    """
    if thread_tuple[0] == "id":
        print("---Verifying Thread by ID")
        return ThreadModel.objects.filter(id=thread_tuple[1])
    elif thread_tuple[0] == "thread_name":
        print("---Verifying Thread by THREAD_NAME")
        return ThreadModel.objects.filter(thread_name=thread_tuple[1])
    else:
        print("Invalid input")
        return False


def create_thread(subject, board_id):
    """Creates a new Thread in the Database
        - subject (str): Subject of the thread. Very short description.
        - board_id (str): ID of the current board.
    """
    try:
        thread_ins = ThreadManager.create_new_thread(subject, board_id)
        res = ThreadSerializer(thread_ins).data
        return True, res

    except Exception as e:
        return False, e.args[0]


def get_threads():
    """Return all Threads created"""
    try:
        threads = ThreadModel.objects.all()
        res = [ThreadSerializer(thread).data for thread in threads]
        return True, res

    except Exception as e:
        print(e)
        return False, "Error"
