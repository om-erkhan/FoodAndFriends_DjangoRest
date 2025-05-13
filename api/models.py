from django.db import models
 
class User(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=100)
    