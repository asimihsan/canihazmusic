from celery.task import Task, TaskSet
from celery.task.sets import subtask
from celery.registry import tasks
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import requests
import json
import datetime
import pprint

from apps.search.models import Search

# -----------------------------------------------------------------------------
#   Constants.
# -----------------------------------------------------------------------------
USER_AGENT = "CanIHazMusic/0.1 +http://icanhazmusic.herokuapp.com"
EMAIL = "asim.ihsan@gmail.com"
HEADERS = {"User-Agent": USER_AGENT, "From": "asim.ihsan@gmail.com"}
SEARCH_URI = "http://api.beatport.com/catalog/3/search"
RETURN_ROOT_URI = "http://www.beatport.com"
# -----------------------------------------------------------------------------

class BeatportSearchTask(Task):
    name = "apps.search.tasks_beatport.BeatportSearchTask"
    acks_late = True

    def run(self, pk, sort_by_date=True):
        logger.info("BeatportSearchTask: starting request %s, pk: %s, sort_by_date: %s" %
                (self.request.id, pk, sort_by_date))
        try:
            # -----------------------------------------------------------------
            #   Perform search.
            # -----------------------------------------------------------------
            search = Search.objects.get(pk = pk)
            payload = {"query": search.query,
                        "perPage": 100}
            if sort_by_date == True:
                logger.debug("sort by date.")
                payload["sortBy"] = "releaseDateASC"
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
                result_uri = "/release/%s/%s" % (result["slug"], result["sku"].split("-")[1])
                return_subvalue["uri"] = RETURN_ROOT_URI + result_uri
                return_subvalue["title"] = "%s - %s" % (result["artists"][0]["name"], result["name"])
                return_subvalue["label"] = result["label"]["name"]
                if "images" in result and "medium" in result["images"]:
                    return_subvalue["image"] = result["images"]["medium"]["url"]
                else:
                    return_subvalue["image"] = ""
                date_elems = result["releaseDate"].split("-")
                date = datetime.date(year = int(date_elems[0]),
                                     month = int(date_elems[1]),
                                     day = int(date_elems[2]))
                return_subvalue["date"] = date
                return_subvalue["date_as_string"] = "%s" % result["releaseDate"]
                return_subvalue["source"] = "Beatport"
                return_value.append(return_subvalue)
            # -----------------------------------------------------------------
        except:
            logger.exception("BeatportSearchTask_%s: unhandled exception." % self.request.id)
            raise
        return return_value

