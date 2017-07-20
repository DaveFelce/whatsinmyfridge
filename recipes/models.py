from __future__ import unicode_literals
from django.db import models

class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=2000)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'recipe'
        verbose_name_plural = "recipes"


