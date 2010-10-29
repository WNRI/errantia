from django.shortcuts import render_to_response, get_object_or_404

from conference.models import Conference, Talk
from jchat.models import Room

def show(request, conf_slug):
    conf = get_object_or_404(Conference, slug=conf_slug)
    chat = Room.objects.get_or_create(conf)

    template = 'live/conference.html'
    if 'embed' in request.GET:
        template = 'live/conference-embed.html'

    return render_to_response(template, {'conf': conf, 'chat_id': chat.id})

def show2(request, conf_slug):
    conf = get_object_or_404(Conference, slug=conf_slug)
    chat = Room.objects.get_or_create(conf)

    template = 'live/conference2.html'
    if 'embed' in request.GET:
        template = 'live/conference-embed.html'

    return render_to_response(template, {'conf': conf, 'chat_id': chat.id})
