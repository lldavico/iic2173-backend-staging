from rest_framework import serializers
from gruponce.models import ThreadModel

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadModel
        fields = ['id', 'board', 'thread_name', 'creation_date']