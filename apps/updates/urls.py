from django.conf.urls import patterns, url, include

urlpatterns = patterns('apps.updates.views',
    url(r'^$', 'read_updates', name='read_updates'),
)

