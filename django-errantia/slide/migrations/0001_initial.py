# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Slide'
        db.create_table('slide_slide', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Talk'])),
            ('slide', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('slide', ['Slide'])


    def backwards(self, orm):

        # Deleting model 'Slide'
        db.delete_table('slide_slide')


    models = {
        'conference.conference': {
            'Meta': {'object_name': 'Conference'},
            'conf_image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'conference.talk': {
            'Meta': {'unique_together': "(('slug', 'conference'),)", 'object_name': 'Talk'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Conference']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'slide.slide': {
            'Meta': {'object_name': 'Slide'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
            'slide': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Talk']"})
        }
    }

    complete_apps = ['slide']
