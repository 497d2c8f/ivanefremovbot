from .models import Task, Tag
from rest_framework import serializers


__all__ = [
	'TagSerializer',
	'TaskSerializer',
]


class TagSerializer(serializers.ModelSerializer):

	class Meta:

		model = Tag
		fields = ['pk', 'telegram_user_id', 'text']
		read_only_fields = ['pk', 'telegram_user_id']

	def create(self, validated_data):

		telegram_user_id=self.context['request'].COOKIES['telegram_user_id']
		tag = Tag.objects.create(telegram_user_id=telegram_user_id, text=validated_data['text'])
		return tag


class TaskSerializer(serializers.ModelSerializer):

	class Meta:

		model = Task
		fields = ['pk', 'title', 'description', 'telegram_user_id', 'tag', 'created', 'deadline']
		read_only_fields = ['pk', 'telegram_user_id', 'created']

	def create(self, validated_data):

		telegram_user_id=self.context['request'].COOKIES['telegram_user_id']
		return Task.objects.create(
			telegram_user_id=telegram_user_id,
			title = validated_data['title'],
			description = validated_data['description'],
			tag = validated_data.get('tag')
		)
