from celery.task import Task, TaskSet
from celery.task.sets import subtask
from celery.registry import tasks

from django.db import transaction

from apps.search.models import Search

