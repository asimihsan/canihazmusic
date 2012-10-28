from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_safe

import logging

@require_safe
def read_updates(request):
    logger = logging.getLogger("apps.updates.views.read_updates")
    data = {}
    return render_to_response('updates/read_updates.html',
                              data,
                              context_instance = RequestContext(request))


