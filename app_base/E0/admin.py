from django.contrib import admin
from E0.models.board_model import BoardModel, ThreadModel, MessageModel
admin.site.register(BoardModel)
admin.site.register(ThreadModel)
admin.site.register(MessageModel)
# Register your models here.


