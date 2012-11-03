# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Search'
        db.create_table('search_search', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('query', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('genre_exact', self.gf('jsonfield.fields.JSONField')(default={})),
            ('artist_exact', self.gf('jsonfield.fields.JSONField')(default={})),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(db_index=True, unique=True, max_length=32, blank=True)),
            ('is_finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('results_as_json', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('search', ['Search'])


    def backwards(self, orm):
        # Deleting model 'Search'
        db.delete_table('search_search')


    models = {
        'search.search': {
            'Meta': {'object_name': 'Search'},
            'artist_exact': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'genre_exact': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'results_as_json': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['search']