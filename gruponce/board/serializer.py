from rest_framework import serializers
from gruponce.models import BoardModel

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardModel
        fields = ['board_id', 'board_name', 'board_text', 'creation_date']
