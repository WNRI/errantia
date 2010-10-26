from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import SlideHandler

slide_handler = Resource(SlideHandler)

urlpatterns = patterns('',
   url(r'^slide/(?P<conf_slug>[^/]+)/(?P<talk_slug>[^/]+)/', slide_handler),
)
