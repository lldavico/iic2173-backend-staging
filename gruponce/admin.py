from django.contrib import admin
from .models import BoardModel, ThreadModel, MessageModel, ImageModel

# Register your models here.
admin.site.register(BoardModel)
admin.site.register(ThreadModel)
admin.site.register(MessageModel)
admin.site.register(ImageModel)
