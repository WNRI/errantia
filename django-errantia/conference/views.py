# vim: ts=4 sw=4 tw=120 expandtab ai
from django.shortcuts import render_to_response, get_object_or_404

from conference.models import Conference, Talk
from jchat.models import Room

def show_talk(request, conf_slug, talk_slug):
    talk = get_object_or_404(Talk, conference__slug=conf_slug, slug=talk_slug)
    return render_to_response('conference/show.html', {'talk': talk,})

def show_conf(request, conf_slug):
    conf = get_object_or_404(Conference, slug=conf_slug)
    chat = Room.objects.get_or_create(conf)

    if conf.state == 'wait':
        template = 'conference/conf_wait.html'
    elif conf.state == 'live':
        template = 'conference/conf_live.html'
    elif conf.state == 'done':
        template = 'conference/conf_done.html'

    if 'embed' in request.GET:
        return render_to_response('conference/embed.html',
            {'conf': conf, 'chat_id': chat.id, 'template': template})
    else:
        return render_to_response(template,
            {'conf': conf, 'chat_id': chat.id})
