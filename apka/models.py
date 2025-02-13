import datetime

from django.db import models
from django.utils import timezone

class Pytanie(models.Model):
    pytanie_text = models.CharField(max_length=200)
    data_pub = models.DateTimeField("data publikacji")
    def __str__(self):
        return self.pytanie_text
    def ostatnio_opublikowane(self):
        return self.data_pub >= timezone.now() - datetime.timedelta(days=1)

class Wybor(models.Model):
    pytanie = models.ForeignKey(Pytanie, on_delete=models.CASCADE)
    wybor_text = models.CharField(max_length=200)
    glosy = models.IntegerField(default=0)
    def __str__(self):
        return self.wybor_text
# Create your models here.
