from __future__ import unicode_literals


from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User

# Create your models here.


class Grabit(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(unique=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    graph = JSONField(default=list)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

