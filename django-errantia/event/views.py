# vim: ts=4 sw=4 tw=120 expandtab ai
from django.shortcuts import render_to_response, get_object_or_404

from django.conf import settings
from event.models import Event
from jchat.models import Room

def index(request):
    objects = Conference.objects.exclude(state='done')
    return render_to_response('index.html', {'objects': objects})

def detail(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    chat = Room.objects.get_or_create(event)
    ctx = {'event': event, 'chat_id': chat.id,
            'hookbox_url': settings.ERRANTIA_HOOKBOX_INSTALL,}

    if event.state == 'wait':
        ctx['template'] = 'event/wait.html'
    elif event.state == 'live':
        ctx['template'] = 'event/live.html'
    elif event.state == 'done':
        ctx['template'] = 'event/done.html'

    if 'embed' in request.GET:
        return render_to_response('embed.html',
            ctx)
    else:
        return render_to_response(ctx['template'],
            ctx)
