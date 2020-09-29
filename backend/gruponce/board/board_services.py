from gruponce.models import BoardModel
from gruponce.board.serializer import BoardSerializer


def create_board(board_name, board_text):
    """Creates a new Board in the Database
        - board_name (str): Name of the board
        - board_text (str): Description of the board
    """
    try:
        board_ins = BoardModel.objects.create(board_name=board_name, board_text=board_text, board_id=board_name[:5])
        res = BoardSerializer(board_ins).data

        return True, res

    except Exception as e:
        return False, e.args[0]


def delete_board(board_id):
    """Remove Board from Database
        - board_id (str): Id of the board
    """
    try:
        if not BoardModel.objects.filter(board_id=board_id).exists():
            raise Exception(410)

        board = BoardModel.objects.filter(board_id=board_id)

        board.delete()
        return True, "Successfully deleted"

    except Exception as e:
        print(e)
        return False, e.args[0]


def get_boards():
    """Return all Boards created"""
    try:
        boards = BoardModel.objects.all()
        res = [BoardSerializer(board).data for board in boards]
        return True, res

    except Exception as e:
        print(e)
        return False, "Error"
