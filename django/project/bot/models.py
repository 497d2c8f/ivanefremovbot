from django.db import models
from django.utils.timezone import now


__all__ = [
	'Task',
	'Tag',
]


class Task(models.Model):

	telegram_user_id = models.BigIntegerField()
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=1000, default=None, blank=True, null=True)
	tag = models.ForeignKey('Tag', blank=True, null=True, default=None, on_delete=models.SET_NULL)
	created = models.DateTimeField(auto_now_add=True)
	deadline = models.DateTimeField(blank=True, null=True)

	class Meta:

		unique_together = [["telegram_user_id", "title"]]


class Tag(models.Model):

	telegram_user_id = models.BigIntegerField()
	text = models.CharField(max_length=50)

	class Meta:

		unique_together = [["telegram_user_id", "text"]]

	def __str__(self):

		return self.text
