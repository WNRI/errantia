# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.video_url'
        db.add_column('event_event', 'video_url', self.gf('django.db.models.fields.URLField')(default='http://video.errantia.org/video.ogv', max_length=200), keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.video_url'
        db.delete_column('event_event', 'video_url')


    models = {
        'event.event': {
            'Meta': {'object_name': 'Event'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ending': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hashtag': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'starting': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'wait'", 'max_length': '4'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'video_url': ('django.db.models.fields.URLField', [], {'default': "'http://video.errantia.org/video.ogv'", 'max_length': '200'}),
            'waiting_teaser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['event']
