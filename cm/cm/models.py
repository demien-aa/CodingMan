from django.db import models


class Tag(models.Model):
    tag_id = models.BigIntegerField()
    label = models.CharField(max_length=200)

    # class Meta:
    #     db_table = 'tag'