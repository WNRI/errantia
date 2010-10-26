from django.db import models
from conference.models import Talk

def upload_folder(instance, filename):
   return 'slides/%s/%s/%s' % (instance.talk.conference.slug, instance.talk.slug, filename)

class Slide(models.Model):
    num = models.PositiveSmallIntegerField(blank=True)
    talk = models.ForeignKey(Talk)
    slide = models.ImageField(upload_to=upload_folder)
    added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        try:
            self.num = Slide.objects.filter(talk=self.talk).order_by('-num')[0].num + 1
        except Slide.DoesNotExist:
            self.num = 0

        super(Slide, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s:%d' % (self.talk, self.num)
