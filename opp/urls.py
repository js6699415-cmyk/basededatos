# urls.py
from django.contrib import admin
from django.urls import path
from django.conf import settings  # Para configuración de medios
from django.conf.urls.static import static  # Para servir archivos de medios
from tasks import views  # Tu app es 'tasks', así que lo mantengo

urlpatterns = [
    path("admin/", admin.site.urls),
    

    path("", views.home, name="home"),
    path("experiencia/", views.experiencia, name="experiencia"),

    path("academicos/", views.productos_academicos, name="productos_academicos"),
    path("laborales/", views.productos_laborales, name="productos_laborales"),

    path("exportar-cv/", views.exportar_cv, name="exportar_cv"),
    path("cursos/", views.cursos, name="cursos"),  # Solo una línea (eliminé el duplicado)

    path("reconocimiento/", views.reconocimiento, name="reconocimiento"),
    path('garage/', views.garage, name='garage'),
       # URL para reconocimiento (sin 's')

    # ... otras URLs si las tienes
]

# Configuración para servir archivos de medios en desarrollo (solo si DEBUG=True)
# Esto funciona con Cloudinary (si está configurado) o con almacenamiento local (MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Agregado para media