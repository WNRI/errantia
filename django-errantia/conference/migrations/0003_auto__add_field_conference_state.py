# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Conference.state'
        db.add_column('conference_conference', 'state', self.gf('django.db.models.fields.CharField')(default='wait', max_length=4), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Conference.state'
        db.delete_column('conference_conference', 'state')


    models = {
        'conference.conference': {
            'Meta': {'object_name': 'Conference'},
            'conf_image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'wait'", 'max_length': '4'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'conference.talk': {
            'Meta': {'unique_together': "(('slug', 'conference'),)", 'object_name': 'Talk'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Conference']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'wait'", 'max_length': '4'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['conference']
