from rest_framework import viewsets, generics, permissions
from .serializers import *
from .models import *


class TaskModelViewSet(viewsets.ModelViewSet):

	serializer_class = TaskSerializer
	lookup_field = 'title'

	def get_queryset(self):

		telegram_user_id=self.request.COOKIES['telegram_user_id']
		queryset = Task.objects.filter(telegram_user_id=telegram_user_id)
		return queryset


class TagModelViewSet(viewsets.ModelViewSet):

	serializer_class = TagSerializer
	lookup_field = 'text'

	def get_queryset(self):

		telegram_user_id=self.request.COOKIES['telegram_user_id']
		queryset = Tag.objects.filter(telegram_user_id=telegram_user_id)
		return queryset
