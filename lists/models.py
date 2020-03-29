from django.db import models

# Create your models here.

# real Django model inherits from Model


class Item(models.Model):
    text = models.TextField(default='')
