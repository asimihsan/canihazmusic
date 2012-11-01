from django.conf.urls import patterns, url, include

urlpatterns = patterns('apps.search.views',
    url(r'^$', 'search', name='search'),
    url(r'^(?P<slug>[A-Za-z0-9_-]+)/$', 'read_search', name='read_search'),
    url(r'^(?P<slug>[A-Za-z0-9_-]+)/is_finished$', 'is_search_finished', name='is_search_finished'),
)

