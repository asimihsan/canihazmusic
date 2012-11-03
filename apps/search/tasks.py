from celery.task import Task, TaskSet
from celery.task.sets import subtask
from celery.registry import tasks
from celery import group, chain, chord
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import pprint
import operator

from apps.search.models import Search
from apps.search.tasks_discogs import DiscogsSearchTask
from apps.search.tasks_beatport import BeatportSearchTask

class CommitSearchResultsTask(Task):
    name = "apps.search.tasks.CommitSearchResultsTask"
    ignore_result = True

    def run(self, results, pk):
        logger.info("CommitSearchResultsTask: starting request %s. pk: %s" %
                (self.request.id,
                 pk))
        try:
            # -----------------------------------------------------------------
            #   Sort and flatten the results.
            #
            #   Remember that sorting in Python is stable, so we can sort
            #   ascending by title and then descening by date without
            #   re-ordering by title.
            # -----------------------------------------------------------------
            flattened_results = [item for sublist in results for item in sublist]
            flattened_results.sort(key = operator.itemgetter("title"))
            flattened_results.sort(key = operator.itemgetter("date"), reverse=True)
            # -----------------------------------------------------------------

            # -----------------------------------------------------------------
            #   Persist the results, mark the search as finished.
            # -----------------------------------------------------------------
            search = Search.objects.get(pk = pk)
            search.is_finished = True
            search.results = flattened_results
            search.save()
            # -----------------------------------------------------------------
        except:
            logger.exception("CommitSearchResultsTask_%s: unhandled exception" % self.request.id)
            raise

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
    subtask_classes = [DiscogsSearchTask, BeatportSearchTask]

    def run(self, pk):
        logger.info("MainSearchTask: starting request %s. pk: %s" %
                (self.request.id,
                 pk))
        try:
            # -----------------------------------------------------------------
            #   Execute subtasks to get results, and a final
            #   subtask to persist all the results.
            #
            #   Using a chord allows MainSearchTask to return immediately,
            #   execute subtasks in parallel, and then commit results in a
            #   final task.
            #
            #   Perform an initial get of the Search object to confirm it
            #   exists before launching subtasks.
            # -----------------------------------------------------------------
            search = Search.objects.get(pk = pk)
            subtasks = [subtask_class.subtask((search.pk, )) for subtask_class in self.subtask_classes]
            callback = CommitSearchResultsTask.subtask((search.pk, ))
            chord(subtasks)(callback)
            # -----------------------------------------------------------------

        except:
            logger.exception("MainSearchTask_%s: unhandled exception." % self.request.id)
            raise

tasks.register(MainSearchTask)

