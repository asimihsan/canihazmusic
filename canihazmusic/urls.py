from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'canihazmusic.views.home', name='home'),
    # url(r'^canihazmusic/', include('canihazmusic.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

# Cheap hack to get Heroku to work
# Reference: http://stackoverflow.com/questions/9047054/heroku-handling-static-files-in-django-app
if not settings.DEBUG:
    urlpatterns += patterns('',
        (4'^static/(?P<path>.*)$', 'django.views.static.server', {'document_root': settings.STATIC_ROOT}),
    )

