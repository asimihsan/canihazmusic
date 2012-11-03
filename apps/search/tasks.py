from celery.task import Task, TaskSet
from celery.task.sets import subtask
from celery.registry import tasks
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from apps.search.models import Search

# -----------------------------------------------------------------------------
#   -   Search task does not direct return a result because instead it
#       persists it in the database so mark with ignore_result.
#   -   Search task is idempotent (it's safe to execute more than once) so
#       mark with acks_late.
# -----------------------------------------------------------------------------
class MainSearchTask(Task):
    """Execute a search. Will execute a set of other search tasks, aggregate
    the results, and then persist the results in the database.

        source_filepath: integer. Primary key of the respective Search object.
    """
    name = "apps.search.tasks.MainSearchTask"
    ignore_result = True
    acks_late = True

    def run(self, pk, **kwargs):
        logger.info("MainSearchTask: starting request %s. pk: %s" %
                (self.request.id,
                 pk))
        try:
            # -----------------------------------------------------------------
            #   Attempt to get Search object, or raise Exception.
            # -----------------------------------------------------------------
            try:
                search = Search.objects.get(pk = pk)
            except Search.DoesNotExist:
                logger.exception("Search object does not exist.")
                raise
            # -----------------------------------------------------------------

            # -----------------------------------------------------------------
            #   Execute chained subtasks to get results, and a final
            #   subtask to persist all the results.
            # -----------------------------------------------------------------
            # -----------------------------------------------------------------

        except:
            logger.exception("main_search_task_%s: unhandled exception." % self.request.id)
            raise

tasks.register(MainSearchTask)

