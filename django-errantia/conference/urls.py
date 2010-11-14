from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<conf_slug>[\w-]+)/(?P<talk_slug>[\w-]+)/$', 'conference.views.show_talk'),
    (r'^(?P<conf_slug>[\w-]+)/$', 'conference.views.show_conf'),
)
