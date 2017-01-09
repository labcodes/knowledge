from django.db import models

# Create your models here.


class Link(models.Model):
    title = models.CharField(max_length=250)
    link = models.URLField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)