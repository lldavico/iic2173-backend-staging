from gruponce.models import ThreadModel, ThreadManager
from gruponce.thread.serializer import ThreadSerializer


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
