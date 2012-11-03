from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_safe
from django.utils.html import escape
from django.db import transaction

import json
import logging

from apps.search.models import Search
from apps.search.tasks import MainSearchTask

# -----------------------------------------------------------------------------
#   search GET and POST.
# -----------------------------------------------------------------------------
def search(request):
    logger = logging.getLogger("apps.search.views.search")
    logger.debug("entry.")

    query = request.GET.get('q', None)
    if query:
        logger.debug("query present.")
        return search_execute_query(request)

    data = {}
    return render_to_response('search/search.html',
                              data,
                              context_instance = RequestContext(request))

#@transaction.commit_manually
def search_execute_query(request):
    logger = logging.getLogger("apps.search.views.search_execute_query")
    logger.debug("entry.")

    # -------------------------------------------------------------------------
    #   Initialize local variables, validate assumptions.
    # -------------------------------------------------------------------------
    query = request.GET.get('q', None)
    logger.debug("query: %s" % query)
    assert query, "query is None"
    clean_query = escape(query)
    logger.debug("clean_query: %s" % clean_query)

    genre_exact = []
    logger.debug("genre_exact: %s" % genre_exact)
    artist_exact = []
    logger.debug("artist_exact: %s" % artist_exact)

    search_type = 'all'
    logger.debug("search_type: %s" % search_type)
    assert search_type in Search.type_lookup, "search_type '%s' is invalid" % search_type

    data = {}
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    #   -   Persist the search in the database.
    #   -   If successfully persisted, start the celery task for the search.
    # -------------------------------------------------------------------------
    try:
        logger.debug("creating Search object.")
        search = Search.objects.create(query = clean_query,
                                       genre_exact = genre_exact,
                                       artist_exact = artist_exact,
                                       type = search_type)
    except:
        logger.exception("Exception on creating Search object.")
        #transaction.rollback()
        raise
    else:
        logger.debug("Committing transaction and starting search for pk: %s" % search.pk)
        #transaction.commit()
        try:
            MainSearchTask.delay(search.pk)
        except:
            logger.exception("Unhandled exception starting main_search_task")
            raise
    # -------------------------------------------------------------------------

    data["clean_query"] = clean_query

    return render_to_response('search/search.html',
                              data,
                              context_instance = RequestContext(request))
    return None
# -----------------------------------------------------------------------------

def read_search(request, uuid):
    logger = logging.getLogger("apps.search.views.read_search")
    logger.debug("entry.")

def is_search_finished(request, uuid):
    logger = logging.getLogger("apps.search.views.is_search_finished")
    logger.debug("entry.")


