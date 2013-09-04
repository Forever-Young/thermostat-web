# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TempHistory'
        db.create_table(u'thermostat_temphistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('temp', self.gf('django.db.models.fields.FloatField')()),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'thermostat', ['TempHistory'])

        # Adding model 'TempSettings'
        db.create_table(u'thermostat_tempsettings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('low_boundary', self.gf('django.db.models.fields.FloatField')(default=21.5)),
            ('high_boundary', self.gf('django.db.models.fields.FloatField')(default=22.0)),
        ))
        db.send_create_signal(u'thermostat', ['TempSettings'])


    def backwards(self, orm):
        # Deleting model 'TempHistory'
        db.delete_table(u'thermostat_temphistory')

        # Deleting model 'TempSettings'
        db.delete_table(u'thermostat_tempsettings')


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
        }
    }

    complete_apps = ['thermostat']