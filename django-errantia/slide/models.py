from django.db import models
from django.forms import ModelForm
from django.core import serializers
import urllib
import urllib2

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
        except (Slide.DoesNotExist, IndexError):
            self.num = 0

        payload = urllib.quote_plus('{"slide": "%s", "num": %d}' % (self.slide.url, self.num,))
        url = 'http://%s/rest/publish?secret=%s&channel_name=%s&payload=%s' % \
            ('velmont.hosted.hookbox.org', 'odin-rest', 'errantia-slides', payload,)
        print url
        try:
            print urllib2.urlopen(url).read()
        except urllib2.HTTPError:
            pass

        super(Slide, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s:%d' % (self.talk, self.num)

class SlideForm(ModelForm):
    class Meta:
        model = Slide
        exclude = ('talk',)
