# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django_hstore.fields import DictionaryField

class Models(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.TextField(unique=True, blank=True)
    lstar = models.FloatField(blank=True, null=True)
    mdot = models.FloatField(blank=True, null=True)
    tstar = models.FloatField(blank=True, null=True)
    teff = models.FloatField(blank=True, null=True)
    vel_law = models.IntegerField(blank=True, null=True)
    cl_par_1 = models.FloatField(blank=True, null=True)
    cl_par_2 = models.FloatField(blank=True, null=True)
    hyd_mass_frac = models.FloatField(blank=True, null=True)
    hyd_rel_frac = models.FloatField(blank=True, null=True)
    ions = models.TextField(blank=True)  # This field type is a guess.
    params = DictionaryField()
    vadat = DictionaryField()

    class Meta:
        managed = False
        db_table = 'models'

class ObsCont(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    model = models.ForeignKey(Models, db_column='model', blank=True, null=True)
    freq = models.FloatField(blank=True, null=True)
    lamb = models.FloatField(db_column='lambda', blank=True, null=True)
    fnu = models.FloatField(blank=True, null=True)
    flambda = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obs_cont'


class ObsFin(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    model = models.ForeignKey(Models, db_column='model', blank=True, null=True)
    freq = models.FloatField(blank=True, null=True)
    lamb = models.FloatField(db_column='lambda', blank=True, null=True)
    fnu = models.FloatField(blank=True, null=True)
    flambda = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obs_fin'


class Species(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    model = models.ForeignKey(Models, db_column='model', blank=True, null=True)
    name = models.TextField(blank=True)
    mass_frac = models.FloatField(blank=True, null=True)
    rel_frac = models.FloatField(blank=True, null=True)
    z_z_sun = models.FloatField(blank=True, null=True)
    z_sun = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'species'
