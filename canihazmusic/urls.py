from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^updates/', include('apps.updates.urls')),
    url(r'^search', include('apps.search.urls')),
    url(r'^settings/', include('apps.settings.urls')),
    url(r'^$|^index.htm$|^index.html$', 'apps.landing.views.index', name='index'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

# Cheap hack to get Heroku to work
# Reference: http://stackoverflow.com/questions/9047054/heroku-handling-static-files-in-django-app
urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

