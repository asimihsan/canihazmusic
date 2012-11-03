# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Search.results_as_json'
        db.delete_column('search_search', 'results_as_json')

        # Adding field 'Search.results'
        db.add_column('search_search', 'results',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Search.results_as_json'
        db.add_column('search_search', 'results_as_json',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'Search.results'
        db.delete_column('search_search', 'results')


    models = {
        'search.search': {
            'Meta': {'object_name': 'Search'},
            'artist_exact': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'genre_exact': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'results': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['search']