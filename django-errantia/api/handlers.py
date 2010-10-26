from piston.handler import BaseHandler
from slide.models import Slide

class SlideHandler(BaseHandler):
   allowed_methods = ('POST',)
   model = Slide

   def create(self, request, conf_slug, talk_slug):
      pass
