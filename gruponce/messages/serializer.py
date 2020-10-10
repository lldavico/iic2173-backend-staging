from rest_framework import serializers
from ..models import MessageModel
from ..user.serializer import UserMessageSerializer


class MessageSerializer(serializers.ModelSerializer):
    user_sender = UserMessageSerializer()

    class Meta:
        model = MessageModel
        fields = ['thread', 'message_content', 'creation_date', 'user_sender']
