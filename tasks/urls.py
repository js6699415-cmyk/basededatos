from django.urls import path
from .views import hoja_vida, descargar_pdf

urlpatterns = [
    path('', hoja_vida, name='hoja_vida'),      # ← RAÍZ
    path('pdf/', descargar_pdf, name='descargar_pdf'),
]
