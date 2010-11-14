from django.shortcuts import render_to_response, get_object_or_404

from conference.models import Conference, Talk
from jchat.models import Room

def show_talk(request, conf_slug, talk_slug):
    talk = get_object_or_404(Talk, conference__slug=conf_slug, slug=talk_slug)
    return render_to_response('conference/show.html', {'talk': talk,})

def show_conf(request, conf_slug):
    conf = get_object_or_404(Conference, slug=conf_slug)
    chat = Room.objects.get_or_create(conf)

    template = 'live/conference.html'
    if 'embed' in request.GET:
        template = 'live/conference-embed.html'

    return render_to_response(template, {'conf': conf, 'chat_id': chat.id})
