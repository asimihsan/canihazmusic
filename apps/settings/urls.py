from django.conf.urls import patterns, url, include

urlpatterns = patterns('apps.settings.views',
    url(r'^$', 'settings', name='settings'),
)

