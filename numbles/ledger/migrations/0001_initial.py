# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Total'
        db.create_table(u'ledger_total', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'ledger', ['Total'])

        # Adding model 'Account'
        db.create_table(u'ledger_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('total', self.gf('django.db.models.fields.related.ForeignKey')(related_name='accounts', to=orm['ledger.Total'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('include_in_balance', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'ledger', ['Account'])

        # Adding model 'Year'
        db.create_table(u'ledger_year', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='years', to=orm['ledger.Account'])),
            ('year', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'ledger', ['Year'])

        # Adding model 'Transaction'
        db.create_table(u'ledger_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', to=orm['ledger.Account'])),
            ('year', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', to=orm['ledger.Year'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('reconciled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('linked', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Transaction'], null=True, blank=True)),
        ))
        db.send_create_signal(u'ledger', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Total'
        db.delete_table(u'ledger_total')

        # Deleting model 'Account'
        db.delete_table(u'ledger_account')

        # Deleting model 'Year'
        db.delete_table(u'ledger_year')

        # Deleting model 'Transaction'
        db.delete_table(u'ledger_transaction')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ledger.account': {
            'Meta': {'object_name': 'Account'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_in_balance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'total': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accounts'", 'to': u"orm['ledger.Total']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'ledger.total': {
            'Meta': {'object_name': 'Total'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'ledger.transaction': {
            'Meta': {'ordering': "('date',)", 'object_name': 'Transaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'to': u"orm['ledger.Account']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linked': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Transaction']", 'null': 'True', 'blank': 'True'}),
            'reconciled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'to': u"orm['ledger.Year']"})
        },
        u'ledger.year': {
            'Meta': {'object_name': 'Year'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'years'", 'to': u"orm['ledger.Account']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['ledger']