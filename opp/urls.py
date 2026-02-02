from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Importa las vistas específicamente desde perfil.views para evitar errores de atributo
from perfil.views import (
    home, experiencia, productos_academicos, productos_laborales, 
    cursos, reconocimiento, garage, exportar_cv
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('experiencia/', experiencia, name='experiencia'),
    path('productos_academicos/', productos_academicos, name='productos_academicos'),
    path('productos_laborales/', productos_laborales, name='productos_laborales'),
    path('cursos/', cursos, name='cursos'),
    path('reconocimientos/', reconocimientos, name='reconocimientos'),  # Mantuve 'reconocimiento' como en tu código
    path('garage/', garage, name='garage'),
    path('exportar_cv/', exportar_cv, name='exportar_cv'),
]

# Para servir archivos media y static en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)