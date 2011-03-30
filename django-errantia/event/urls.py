from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<event_slug>[\w-]+)/$', 'event.views.detail',
        name='show_event'),
)
