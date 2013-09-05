# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TempSettingsHistory'
        db.create_table(u'thermostat_tempsettingshistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('low_boundary', self.gf('django.db.models.fields.FloatField')()),
            ('high_boundary', self.gf('django.db.models.fields.FloatField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'thermostat', ['TempSettingsHistory'])


    def backwards(self, orm):
        # Deleting model 'TempSettingsHistory'
        db.delete_table(u'thermostat_tempsettingshistory')


    models = {
        u'thermostat.temphistory': {
            'Meta': {'object_name': 'TempHistory'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'temp': ('django.db.models.fields.FloatField', [], {})
        },
        u'thermostat.tempsettings': {
            'Meta': {'object_name': 'TempSettings'},
            'high_boundary': ('django.db.models.fields.FloatField', [], {'default': '22.0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_boundary': ('django.db.models.fields.FloatField', [], {'default': '21.5'})
        },
        u'thermostat.tempsettingshistory': {
            'Meta': {'object_name': 'TempSettingsHistory'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'high_boundary': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_boundary': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['thermostat']