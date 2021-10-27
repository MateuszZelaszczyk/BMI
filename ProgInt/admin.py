from django.contrib import admin
from ProgInt.models import Kalorie


class KalorieAd(admin.ModelAdmin):
    list_display=('id','chory','blekka','lekka','srednia','duza','bduza')


admin.site.register(Kalorie,KalorieAd)
