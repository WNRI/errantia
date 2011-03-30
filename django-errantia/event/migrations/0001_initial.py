# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Event'
        db.create_table('event_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='wait', max_length=4)),
            ('starting', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('ending', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('waiting_teaser', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('hashtag', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal('event', ['Event'])


    def backwards(self, orm):
        
        # Deleting model 'Event'
        db.delete_table('event_event')


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
            'waiting_teaser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['event']
