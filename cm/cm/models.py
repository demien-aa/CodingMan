from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=200)
    app_id = models.BigIntegerField(null=True, )
    times = models.BigIntegerField(null=True, )

    class Meta:
        app_label = 'cm'


class App(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    icon = models.CharField(max_length=500)
    weight = models.BigIntegerField(null=True, )

    class Meta:
        app_label = 'cm'


class Tag_Similarity(models.Model):
    base_tag = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    similarity = models.FloatField()

    class Meta:
        app_label = 'cm'