from celery.task import Task, TaskSet
from celery.task.sets import subtask
from celery.registry import tasks
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import requests
import json
import datetime

# -----------------------------------------------------------------------------
#   Constants.
# -----------------------------------------------------------------------------
USER_AGENT = "CanIHazMusic/0.1 +http://icanhazmusic.herokuapp.com"
EMAIL = "asim.ihsan@gmail.com"
HEADERS = {"User-Agent": USER_AGENT, "From": "asim.ihsan@gmail.com"}
SEARCH_URI = "http://api.discogs.com/database/search"
RETURN_ROOT_URI = "http://www.discogs.com"
# -----------------------------------------------------------------------------

from apps.search.models import Search

class DiscogsSearchTask(Task):
    """Search on Discogs.

    Notes:
        -   Discogs have a 1/s rate limit.
    """
    name = "apps.search.tasks_discogs.DiscogsSearchTask"
    acks_late = True
    rate_limit = "1/s"

    def run(self, pk, sort_by_date=True):
        logger.info("DiscogsSearchTask: starting request %s, pk: %s, sort_by_date: %s" %
                (self.request.id, pk, sort_by_date))
        try:
            # -----------------------------------------------------------------
            #   Perform search.
            # -----------------------------------------------------------------
            search = Search.objects.get(pk = pk)
            payload = {"q": search.query,
                       "type": "release"}
            if sort_by_date == True:
                logger.debug("sort by date.")
                payload["sort"] = "year"
                payload["sort_order"] = "desc"
            r = requests.get(SEARCH_URI, params=payload, headers=HEADERS)
            if r.status_code != requests.codes.ok:
                logger.error("request status code %s not OK." % r.status_code)
            data = json.loads(r.text)
            results = data["results"]
            # -----------------------------------------------------------------

            # -----------------------------------------------------------------
            #   Sanitize and normalize output.
            # -----------------------------------------------------------------
            return_value = []
            permitted_types = set(["release"])
            for result in results:
                if result["type"] not in permitted_types:
                    continue
                return_subvalue = {}
                return_subvalue["type"] = result["type"]
                return_subvalue["uri"] = RETURN_ROOT_URI + result["uri"]
                return_subvalue["title"] = result["title"]
                return_subvalue["image"] = result["thumb"]
                return_subvalue["label"] = result["label"][0]
                if "year" in result:
                    date = datetime.date(int(result["year"]),
                                         month = 1,
                                         day = 1)
                    return_subvalue["date"] = date
                    return_subvalue["date_as_string"] = "%s" % date.year
                else:
                    return_subvalue["date"] = datetime.date(year=1970, month=1, day=1)
                    return_subvalue["date_as_string"] = "Unknown"
                return_subvalue["source"] = "Discogs"
                return_value.append(return_subvalue)
            # -----------------------------------------------------------------
        except:
            logger.exception("DiscogsSearchTask_%s: unhandled exception." % self.request.id)
            raise
        return return_value

