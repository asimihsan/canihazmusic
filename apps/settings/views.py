from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_safe

import logging

def settings(request):
    logger = logging.getLogger("apps.settings.views.settings")
    data = {}
    return render_to_response('settings/settings.html',
                              data,
                              context_instance = RequestContext(request))

