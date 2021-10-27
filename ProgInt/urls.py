from django.urls import path
from .views import licz,tempob,glowna

urlpatterns = [
    path('runtm', tempob, name="tempob"),
    path('InBMI', licz, name="licz"),
    path('', glowna, name="glowna"),
    
]