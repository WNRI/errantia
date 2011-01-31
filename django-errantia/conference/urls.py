from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<conf_slug>[\w-]+)/(?P<talk_slug>[\w-]+)/$',
        'conference.views.show_talk', name='show_talk'),
    url(r'^(?P<conf_slug>[\w-]+)/$', 'conference.views.show_conf',
        name='show_conf'),
)
