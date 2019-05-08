from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class translate(models.Model):
    ip = models.CharField(max_length = 20)
    word = models.TextField()
    translate = models.TextField()
    updated = models.DateTimeField(auto_now = True)


class chat(models.Model):
    sender = models.CharField(max_length = 20)
    sendto = models.CharField(max_length = 20)
    ip_from = models.CharField(max_length = 20)
    ip_to = models.CharField(max_length = 20)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content