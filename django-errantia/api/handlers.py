from piston.handler import BaseHandler
from piston.utils import rc, FormValidationError

from conference.models import Talk, Conference
from slide.models import Slide, SlideForm
from jchat.models import Room, Message

class SlideHandler(BaseHandler):
    model = Slide

    def create(self, request, talk__conference__slug, talk__slug):
       form = SlideForm(request.POST, request.FILES)
       if form.is_valid():
           obj = form.save(commit=False)
           obj.talk = Talk.objects.get(conference__slug=talk__conference__slug, slug=talk__slug)
           obj.save()
           return rc.CREATED
       else:
           raise FormValidationError(form)

    def read(self, request, talk__conference__slug):
        talk = Talk.objects.filter(conference__slug=talk__conference__slug).order_by("-added")[0]
        obj = Slide.objects.filter(talk=talk).order_by("-added")

        return obj

class SlideNewestHandler(BaseHandler):
    model = Slide
    allowed_methods = ('GET',)

    def read(self, request, conf_slug):
        obj = Slide.objects.filter(talk__conference__slug=conf_slug).order_by("-added")[0]

        return obj

class ConfHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, conf_slug):
        conf = Conference.objects.get(slug=conf_slug)

        try:
            talks = Talk.objects.filter(conference__slug=conf_slug) \
                    .order_by("-starting", "-added")
            slides = Slide.objects.filter(talk=talks[0]).order_by("-added")[0]
        except IndexError:
            talks = {}
            slides = {}

        room = Room.objects.get_or_create(conf)
        #room.msgs = room.messages()

        return {
                'conf':conf,
                'talks': talks,
                'slides': slides,
                'room': room,
                }
