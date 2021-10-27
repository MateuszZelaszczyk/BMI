from django.db import models



class Kalorie(models.Model):
    chory=models.FloatField()
    blekka=models.FloatField()
    lekka=models.FloatField()
    srednia=models.FloatField()
    duza=models.FloatField()
    bduza=models.FloatField()


