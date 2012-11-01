from django.core.urlresolvers import resolve

import logging
import pprint

class CommonVariablesMiddleware(object):
    """Introduce commonly used variables into the RequestContext for all
    templates.

    Largely a placeholder for now, just a reference for how to use
    Middleware."""
    def process_view(self, request, view_func, view_args, view_kwargs):
        logger = logging.getLogger("apps.utilities.middleware.CommonVariablesMiddleware.process_view")

        # ---------------------------------------------------------------------
        #   request.url_name: the current 'name' of the resolved URL for
        #   the request path.
        # ---------------------------------------------------------------------
        url_name = resolve(request.path).url_name
        request.url_name = url_name
        # ---------------------------------------------------------------------

