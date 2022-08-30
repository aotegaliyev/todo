from django.contrib.auth.models import User as DjangoUser
from django.db import models


class Task(models.Model):
    PRIORITY_TYPES = (
        ('important', 'important'),
        ('urgent', 'urgent'),
    )

    author = models.ForeignKey(DjangoUser, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=300, null=False)
    priority = models.CharField(max_length=50, choices=PRIORITY_TYPES, null=True, blank=True)
    notify_sent = models.BooleanField(default=0)
    deadline = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'todo_tasks'

    def __str__(self):
        return 'ID: {}, {}: {}'.format(self.id, self.author.first_name, self.title)
