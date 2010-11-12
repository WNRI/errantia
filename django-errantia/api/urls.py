from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import SlideHandler, SlideNewestHandler

slide_handler = Resource(SlideHandler)
slide_newest_handler = Resource(SlideNewestHandler)

urlpatterns = patterns('',
   url(r'^slide/new/(?P<conf_slug>[^/]+)/', slide_newest_handler),
   url(r'^slide/(?P<talk__conference__slug>[^/]+)/(?P<talk__slug>[^/]+)/', slide_handler),
   url(r'^slide/(?P<talk__conference__slug>[^/]+)/', slide_handler),
)
