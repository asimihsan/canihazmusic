from django.conf.urls import patterns, url, include

urlpatterns = patterns('apps.search.views',
    url(r'^$', 'search', name='search'),
)

