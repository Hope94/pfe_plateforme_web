from django.db import models


# Model générer depuis la base de donnée droidsec en utilisant la commande inspectdb
class AndroidMetadata(models.Model):
    locale = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'android_metadata'


class ApiPermissionMapping(models.Model):
    field_id = models.IntegerField(db_column='_id', blank=True, null=True)  # Field renamed because it started with '_'.
    api = models.TextField(blank=True, null=True)
    permission = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_permission_mapping'


class FeatureWeightMapping(models.Model):
    field_id = models.IntegerField(db_column='_id', blank=True, null=True)  # Field renamed because it started with '_'.
    feature = models.TextField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feature_weight_mapping'


class Parameter(models.Model):
    intercept = models.FloatField(blank=True, null=True)
    threshold = models.FloatField(blank=True, null=True)
    summalignantfeatures = models.FloatField(db_column='sumMalignantFeatures', blank=True, null=True)  # Field name made lowercase.
    sumbenignfeatures = models.FloatField(db_column='sumBenignFeatures', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'parameter'


class SuspiciousApis(models.Model):
    field_id = models.IntegerField(db_column='_id', blank=True, null=True)  # Field renamed because it started with '_'.
    api = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suspicious_apis'
