from rest_framework import serializers
from .models import BoardModel, ThreadModel, MessageModel, ImageModel


class BoardSerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardModel
		fields = ['board_id', 'board_name', 'board_text', 'creation_date']


class ThreadSerializer(serializers.ModelSerializer):
	class Meta:
		model = ThreadModel
		fields = ['id', 'thread_name', 'creation_date']


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = MessageModel
		fields = ['id', 'message_content', 'creation_date', 'user_nickname']


class ImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ImageModel
		fields = ['id', 'image_name']