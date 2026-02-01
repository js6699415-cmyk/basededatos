# opp/urls.py (ajusta este archivo)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Cambia la importación de 'tasks' a 'perfil', ya que tus vistas están en la app 'perfil'
from perfil import views  # Cambié 'from tasks import views' a 'from perfil import views'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Agrega tus rutas aquí, por ejemplo:
    path('', views.home, name='home'),
    path('experiencia/', views.experiencia, name='experiencia'),
    path('productos_academicos/', views.productos_academicos, name='productos_academicos'),
    path('productos_laborales/', views.productos_laborales, name='productos_laborales'),
    path('cursos/', views.cursos, name='cursos'),
    path('reconocimientos/', views.reconocimiento, name='reconocimientos'),  # Nota: en tu código es 'reconocimiento', no 'reconocimientos'
    path('garage/', views.garage, name='garage'),
    path('exportar_cv/', views.exportar_cv, name='exportar_cv'),  # O 'pdf_datos_personales' si prefieres el nombre original
]

# Para servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)