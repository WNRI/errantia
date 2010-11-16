# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Conference'
        db.create_table('conference_conference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('conf_image', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('conference', ['Conference'])

        # Adding model 'Talk'
        db.create_table('conference_talk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('conference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Conference'])),
        ))
        db.send_create_signal('conference', ['Talk'])

        # Adding unique constraint on 'Talk', fields ['slug', 'conference']
        db.create_unique('conference_talk', ['slug', 'conference_id'])


    def backwards(self, orm):

        # Removing unique constraint on 'Talk', fields ['slug', 'conference']
        db.delete_unique('conference_talk', ['slug', 'conference_id'])

        # Deleting model 'Conference'
        db.delete_table('conference_conference')

        # Deleting model 'Talk'
        db.delete_table('conference_talk')


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
        }
    }

    complete_apps = ['conference']
