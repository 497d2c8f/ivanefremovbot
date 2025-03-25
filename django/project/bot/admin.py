from django.contrib import admin
from .models import Task, Tag


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

	list_display = ['title', 'description', 'created', 'telegram_user_id']
	list_display_links = ['title']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

	list_display = ['text', 'telegram_user_id']
