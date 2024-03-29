from django.conf.urls.defaults import *
from django.contrib import admin

from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    #(r'^$', 'django.views.generic.simple.redirect_to', {'url':'/live/clim-atic-2010/', 'permanent': False}),
    (r'^hookbox/', include('hookbox.urls')),
    (r'^conf/', include('conference.urls')),
    (r'^chat/', include('jchat.urls')),
    (r'^api/', include('api.urls')),
    (r'^$', 'conference.views.index'),

    (r'^admin/', include(admin.site.urls)),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^e/', include('event.urls')),
)
