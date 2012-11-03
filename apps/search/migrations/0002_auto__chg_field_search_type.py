# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Search.type'
        db.alter_column('search_search', 'type', self.gf('django.db.models.fields.CharField')(max_length=8))

    def backwards(self, orm):

        # Changing field 'Search.type'
        db.alter_column('search_search', 'type', self.gf('django.db.models.fields.CharField')(max_length=2))

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
            'type': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['search']