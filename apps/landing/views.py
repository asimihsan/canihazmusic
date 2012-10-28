from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_safe

import logging

@require_safe
def index(request):
    logger = logging.getLogger("apps.landing.views.index")
    data = {}
    return render_to_response('landing/index.html',
                              data,
                              context_instance = RequestContext(request))


