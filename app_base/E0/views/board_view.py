from django.views.generic import TemplateView, DetailView
from E0.models.board_model import BoardModel, ThreadModel, MessageModel, MessageManager, ThreadManager
from django.shortcuts import get_object_or_404, render
from E0.forms import forms
from django.db import models
from django.shortcuts import redirect

from django.http import Http404, HttpRequest


class BoardView(DetailView):
    model = BoardModel
    template_name = "board.html"

    @staticmethod
    def get_board(request, board_id):
        board = get_object_or_404(BoardModel, board_id=board_id)
        thread_list = ThreadView.get_all_threads_by_board(board_id)
        ctx = {'board': board, 'thread_list': thread_list}
        return render(request, "board.html", ctx)


class MessageView(DetailView):

    @staticmethod
    def get_all_posts_by_thread(thread_id):
        post_list = MessageModel.objects.filter(
            thread=thread_id).order_by('creation_date')
        return post_list


class ThreadView(DetailView):
    model = ThreadModel
    template_name = "thread.html"

    @staticmethod
    def thread(request, board_id, thread_id=None):
        if request.method == "GET":
            thread = get_object_or_404(
                ThreadModel, id=thread_id, board=board_id)
            post_list = MessageView.get_all_posts_by_thread(
                thread_id=thread_id)
            print("GET REQUEST", request.GET)
            return render(request, ThreadView.template_name, {"thread": thread, "post_list": post_list})
        elif request.method == "POST":
            if thread_id is None:
                thread = ThreadView.post_thread(request, board_id)
                thread_id = thread.id
            return ThreadView.post_to_existing_thread(request, board_id, thread_id)

    @staticmethod
    def get_thread(board_id, thread_id):
        thread = get_object_or_404(ThreadModel, id=thread_id)

    @staticmethod
    def new_thread(request, board_id):
        print(board_id)
        if request.method == "POST":
            return ThreadView.post_thread(request, board_id=board_id)

    @staticmethod
    def get_all_threads_by_board(board_id):
        return ThreadModel.objects.filter(board=board_id).order_by('-creation_date')

    @staticmethod
    def post_to_existing_thread(request, board_id, thread_id):
        text = request.POST['text']
        print("post REQUEST:", request.POST)

        if text:
            thread = ThreadModel.objects.get(pk=thread_id)
            message = MessageManager.create_new_message(
                thread=thread, message_content=text, user_nickname=request.POST['name'])
            post_list = MessageView.get_all_posts_by_thread(
                thread_id=thread_id)
            return render(request, ThreadView.template_name, {"thread": thread, 'post_list': post_list})

    @staticmethod
    def post_thread(request, board_id, thread_id=None):
        try:
            subject = request.POST["subject"]
            content = request.POST["text"]
            if not subject and not content:
                return Http404("Couldn't create thread. ")
            if thread_id is None:
                thread = ThreadManager.create_new_thread(
                    request.POST['subject'], board_id)
            #     message = MessageManager.create_new_message(
            #         thread=thread, message_content=request.POST['text'], user_nickname=request.POST['name'])
            # if thread and message:
                return thread

        except Exception:
            return Http404("Couldn't create thread. ")
