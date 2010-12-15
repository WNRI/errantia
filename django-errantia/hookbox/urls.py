from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
   url(r'^create_channel', create_channel),
   url(r'^connect', connect),
   url(r'^subscribe', subscribe),
   url(r'^publish', publish),
)
