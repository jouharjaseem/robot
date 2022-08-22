from django.db import models

# Create your models here.

class Person(models.Model):
    identiy = models.IntegerField()
    content = models.TextField()