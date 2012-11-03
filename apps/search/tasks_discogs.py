from celery.task import Task, TaskSet
from celery.task.sets import subtask
from celery.registry import tasks
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import discogs_client as discogs

from apps.search.models import Search

class DiscogsSearchTask(Task):
    name = "apps.search.tasks_discogs.DiscogsSearchTask"
    acks_late = True

    def run(self, pk):
        logger.info("DiscogsSearchTask: starting request %s, pk: %s" %
                (self.request.id, pk))
        try:
            search = Search.objects.get(pk = pk)
            return_value = [{"blah3": "blah4"}]
        except:
            logger.exception("DiscogsSearchTask_%s: unhandled exception." % self.request.id)
            raise
        return return_value

