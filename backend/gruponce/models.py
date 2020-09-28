from django.db import models
from django.utils import timezone


class BoardModel(models.Model):
    board_name = models.CharField(max_length=15)
    board_id = models.CharField(max_length=5, primary_key=True, unique=True)
    creation_date = models.DateTimeField('creation date', auto_now_add=True)
    board_text = models.CharField(max_length=250)


class ThreadModel(models.Model):
    DEFAULT_BOARD_ID = 1
    DEFAULT_NAME = ""
    board = models.ForeignKey(BoardModel, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    thread_name = models.CharField(max_length=100, default=DEFAULT_NAME)


    @property
    def reply_count(self):
        return len(ThreadManager.get_all_messages_in_thread(self)) - 1
    
    @property
    def last_bump(self):
        return MessageManager.get_all_message_by_thread(self.id).last().creation_date
    
    @property
    def first_text(self):
        return MessageManager.get_all_message_by_thread(self.id).first().message_content



class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE)
    message_content = models.CharField(max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True)
    user_nickname = models.CharField(max_length=20)

    class Meta:
        ordering = ['creation_date']


class ImageModel(models.Model):
    image_name = models.CharField(max_length=50)
    message = models.ForeignKey(MessageModel, on_delete=models.CASCADE)


class ThreadManager(models.Manager):

    obj = ThreadModel.objects

    @staticmethod
    def create_new_thread(subject, board_id):
        curr_board = BoardModel.objects.get(board_id = board_id)
        thread = ThreadManager.obj.create(board= curr_board, thread_name=subject)
        thread.save()
        print("Thread created")
        return thread


    @staticmethod
    def get_all_messages_in_thread(thread):
        messages = MessageModel.objects.filter(thread = thread)
        return messages


class MessageManager(models.Manager):

    obj = MessageModel.objects

    @staticmethod
    def create_new_message(thread, message_content, user_nickname='Anonymous'):
        if not message_content:
            return None
        if not user_nickname:
            user_nickname = "Anonymous"
        message = MessageManager.obj.create(
        	thread=thread, message_content=message_content, user_nickname=user_nickname)
        print("CREATED MESSAGE")
        return message

    @staticmethod
    def get_all_message_by_thread(thread_id):
        post_list = MessageModel.objects.filter(
            thread=thread_id).order_by('creation_date')
        return post_list
