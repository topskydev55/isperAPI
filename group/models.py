# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from account.models import Tuser


# Create your models here.
class AllGroups(models.Model):
    name = models.CharField(max_length=48)
    comment = models.CharField(max_length=256)
    publish = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")))
    default = models.IntegerField(default=0)
    groupManagers = models.ManyToManyField(Tuser)

    class Meta:
        db_table = "t_allGroups"

    def __unicode__(self):
        return self.name