from django.db import models
from django.core.urlresolvers import reverse


STATES = (
  ('wait', 'Waiting'),
  ('live', 'Live'),
  ('done', 'Archived'),
)

class Conference(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    conf_image = models.URLField(null=True, blank=True)
    state = models.CharField(max_length=4, choices=STATES, default="wait")
    starting = models.DateTimeField(null=True, blank=True)
    ending = models.DateTimeField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('show_conf', args=(self.slug,))

    def __unicode__(self):
        return self.title


class Talk(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField()
    conference = models.ForeignKey(Conference)
    state = models.CharField(max_length=4, choices=STATES, default="wait")
    starting = models.DateTimeField(null=True, blank=True)
    ending = models.DateTimeField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("slug", "conference"),)

    def get_absolute_url(self):
        return reverse('show_talk', args=(self.conference.slug,
            self.slug,))

    def __unicode__(self):
        return self.title
