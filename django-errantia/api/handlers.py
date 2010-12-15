from piston.handler import BaseHandler
from piston.utils import rc, FormValidationError

from conference.models import Talk
from slide.models import Slide, SlideForm

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
