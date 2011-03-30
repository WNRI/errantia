from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse


STATES = (
  ('wait', 'Waiting'),
  ('live', 'Live'),
  ('done', 'Archived'),
)

class Event(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    state = models.CharField(max_length=4, choices=STATES, default="wait")
    starting = models.DateTimeField(null=True, blank=True)
    ending = models.DateTimeField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    description = models.TextField(null=True, blank=True)
    waiting_teaser = models.TextField(null=True, blank=True)

    hashtag = models.CharField(max_length=16, null=True, blank=True)
    video_url = models.URLField(default=settings.ERRANTIA_VIDEO_STREAM)

    def get_absolute_url(self):
        return reverse('show_event', args=(self.slug,))

    def __unicode__(self):
        return self.title
