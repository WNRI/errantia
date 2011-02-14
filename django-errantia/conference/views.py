# vim: ts=4 sw=4 tw=120 expandtab ai
from django.shortcuts import render_to_response, get_object_or_404

from django.conf import settings
from conference.models import Conference, Talk
from jchat.models import Room

def show_talk(request, conf_slug, talk_slug):
    talk = get_object_or_404(Talk, conference__slug=conf_slug, slug=talk_slug)

    if talk.state == 'wait':
        template = 'conference/talk_wait.html'
    elif talk.state == 'live':
        template = 'conference/talk_live.html'
        video_url = settings.ERRANTIA_VIDEO_STREAM
    elif talk.state == 'done':
        template = 'conference/talk_done.html'

    if 'embed' in request.GET:
        return render_to_response('conference/embed.html',
            {'talk': talk, 'template': template, })
    else:
        return render_to_response(template,
            {'talk': talk, })

def show_conf(request, conf_slug):
    conf = get_object_or_404(Conference, slug=conf_slug)
    chat = Room.objects.get_or_create(conf)
    ctx = {'conf': conf, 'chat_id': chat.id,
            'video_url': settings.ERRANTIA_VIDEO_STREAM,
            'hookbox_url': settings.ERRANTIA_HOOKBOX_INSTALL,}

    if conf.state == 'wait':
        ctx['template'] = 'conference/conf_wait.html'
    elif conf.state == 'live':
        ctx['template'] = 'conference/conf_live.html'
    elif conf.state == 'done':
        ctx['template'] = 'conference/conf_done.html'

    if 'embed' in request.GET:
        return render_to_response('conference/embed.html',
            ctx)
    else:
        return render_to_response(ctx['template'],
            ctx)
