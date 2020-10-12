from django.contrib import admin
from .models import BoardModel, ThreadModel, MessageModel, ImageModel, User

# Register your models here.
admin.site.register(BoardModel)
admin.site.register(ThreadModel)
admin.site.register(MessageModel)
admin.site.register(ImageModel)
admin.site.register(User)
