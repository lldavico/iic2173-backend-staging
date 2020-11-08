from rest_framework import serializers
from gruponce.models import BoardModel
from gruponce.user.serializer import UserSerializer, UserMessageSerializer
class BoardSerializer(serializers.ModelSerializer):

    allowed_users = UserMessageSerializer(many = True)
    class Meta:
        model = BoardModel
        fields = ['board_id', 'board_name', 'board_text', 'creation_date','private','is_open','allowed_users']
