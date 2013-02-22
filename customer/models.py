from django.db import models

from processes.models import Task

class Invoice(models.Model):

    year  =  models.IntegerField()
    month =  models.IntegerField()

    task = models.ForeignKey(Task)
    link = models.CharField(max_length = 300)