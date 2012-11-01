from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_safe
import json

import logging

# -----------------------------------------------------------------------------
#   search GET and POST.
# -----------------------------------------------------------------------------
def search(request):
    logger = logging.getLogger("apps.search.views.search")
    logger.debug("entry.")
    data = {}
    return render_to_response('search/search.html',
                              data,
                              context_instance = RequestContext(request))
# -----------------------------------------------------------------------------

def read_search(request, uuid):
    logger = logging.getLogger("apps.search.views.read_search")
    logger.debug("entry.")

def is_search_finished(request, uuid):
    logger = logging.getLogger("apps.search.views.is_search_finished")
    logger.debug("entry.")


