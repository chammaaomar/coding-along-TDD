from django.db import models

# Create your models here.
# real Django model inherits from Model


class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, null=True)
