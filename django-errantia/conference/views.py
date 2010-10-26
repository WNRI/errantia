from django.shortcuts import render_to_response, get_object_or_404

from conference.models import Conference, Talk

def show(request, conf_slug, talk_slug):
    talk = get_object_or_404(Talk, conference__slug=conf_slug, slug=talk_slug)
    return render_to_response('conference/show.html', {'talk': talk,})
