from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<conf_slug>[\w-]+)/$', 'live.views.show'),
)
