from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<conf_slug>[\w-]+)/(?P<talk_slug>[\w-]+)/$',
        'conference.views.show_talk', name='errantia:show_talk'),
    (r'^(?P<conf_slug>[\w-]+)/$', 'conference.views.show_conf',
        name='errantia:show_conf'),
)
