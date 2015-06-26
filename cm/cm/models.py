from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=200)
    app_id = models.BigIntegerField(null=True, )
    times = models.BigIntegerField(null=True, )

    class Meta:
        app_label = 'cm'
