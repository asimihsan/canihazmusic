from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_safe

import logging

def search(request):
    logger = logging.getLogger("apps.search.views.search")
    data = {}
    return render_to_response('search/search.html',
                              data,
                              context_instance = RequestContext(request))


