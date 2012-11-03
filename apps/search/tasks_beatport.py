from celery.task import Task, TaskSet
from celery.task.sets import subtask
from celery.registry import tasks
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from apps.search.models import Search

class BeatportSearchTask(Task):
    name = "apps.search.tasks_beatport.BeatportSearchTask"
    acks_late = True

    def run(self, pk):
        logger.info("BeatportSearchTask: starting request %s, pk: %s" %
                (self.request.id, pk))
        try:
            return_value = []
        except:
            logger.exception("BeatportSearchTask_%s: unhandled exception." % self.request.id)
            raise
        return return_value

