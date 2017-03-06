from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Noticepoint(models.Model):
    fromxp = models.FloatField()
    fromyp = models.FloatField()
    targetxp = models.FloatField()
    targetyp = models.FloatField()
    type = models.IntegerField()
    content = models.TextField()

    def __unicode__(self):
        return self.content
