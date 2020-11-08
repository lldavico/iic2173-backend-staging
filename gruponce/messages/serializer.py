from rest_framework import serializers
from ..models import MessageModel
from ..user.serializer import UserMessageSerializer


class MessageSerializer(serializers.ModelSerializer):
    user_sender = UserMessageSerializer()
    message_content = serializers.SerializerMethodField()
    class Meta:
        model = MessageModel
        fields = ['thread', 'message_content', 'creation_date', 'user_sender']

    def get_message_content(self, obj):
        if obj.is_censored:
            return "THIS MESSAGE HAS BEEN CENSORED"
        else:
            return obj.message_content