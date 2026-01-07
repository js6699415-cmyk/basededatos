from django.urls import path
from .views import hoja_vida

urlpatterns = [
    path('', hoja_vida, name='hoja_vida'),
]
