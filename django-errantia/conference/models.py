from django.db import models

class Conference(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    conf_image = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.title

class Talk(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField()
    conference = models.ForeignKey(Conference)

    class Meta:
        unique_together = (("slug", "conference"),)

    def __unicode__(self):
        return self.title
