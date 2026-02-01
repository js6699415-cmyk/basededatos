import io
import requests
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from pypdf import PdfWriter

from perfil.models import (
    DatosPersonales, ExperienciaLaboral,
    CursosRealizados, Reconocimientos,
    ProductosAcademicos, ProductosLaborales, VentaGarage        
)

def get_perfil():
    return DatosPersonales.objects.filter(perfilactivo=1).first()

def home(request):
    perfil = get_perfil()

    # ✅ Cursos para mostrar en la principal
    resumen_cursos = [
        {"nombrecurso": "SQL - Curso completo de Bases de Datos (SQL y MySQL).", "totalhoras": 40, "rutacertificado": None},
        {"nombrecurso": "Python básico - Introducción a programación.", "totalhoras": 30, "rutacertificado": None},
        {"nombrecurso": "Microsoft Access - Gestión de bases de datos.", "totalhoras": 20, "rutacertificado": None},
    ]

    # ✅ Reconocimientos para mostrar en la principal
    resumen_rec = [
        {"descripcionreconocimiento": "Reconocimiento académico", "entidadpatrocinadora": "ULEAM", "fechareconocimiento": "2025-01-01"},
    ]

    # ✅ Experiencia agregada (basada en tu view de experiencia)
    resumen_exp = [
        {
            "cargodesempenado": "Desarrollador Web",
            "nombrempresa": "Empresa Demo",
            "lugarempresa": "Manta, Ecuador",
            "fechainiciogestion": "2024-01-01",
            "fechafingestion": None,  # None significa "Actualidad"
            "descripcionfunciones": "Desarrollo de aplicaciones web con Django.\nMantenimiento de sistemas.",
        },
        # Agrega más experiencias aquí si quieres
    ]

    context = {
        "perfil": perfil,
        "resumen_exp": resumen_exp,  # Ahora incluye experiencia
        "resumen_cursos": resumen_cursos,
        "resumen_rec": resumen_rec,
        "resumen_acad": [],
        "resumen_lab": [],
        "resumen_garage": [],
    }

    return render(request, "hoja_de_vida.html", context)

def experiencia(request):
    # Datos hardcodeados para la página de experiencia (iguales a resumen_exp para consistencia)
    datos = [
        {
            "cargodesempenado": "Desarrollador Web",
            "nombrempresa": "Empresa Demo",
            "lugarempresa": "Manta, Ecuador",
            "fechainiciogestion": "2024-01-01",
            "fechafingestion": None,
            "descripcionfunciones": "Desarrollo de aplicaciones web con Django.\nMantenimiento de sistemas.",
            "nombrecontactoempresarial": "Juan Pérez",  # Agregado para el template de experiencia
            "telefonocontactoempresarial": "0991234567",
            "sitiowebempresa": "https://empresa-demo.com",
            "rutacertificado": None,
        },
        # Agrega más si quieres
    ]
    return render(request, "experiencia.html", {"perfil": get_perfil(), "datos": datos})

def productos_academicos(request):
    perfil = get_perfil()
    
    # ✅ Productos académicos hardcodeados (puedes cambiar a DB queries más tarde)
    # Basado en campos típicos de ProductosAcademicos (ajusta según tu modelo)
    productos_acad = [
        {
            "titulo": "Investigación en Inteligencia Artificial",
            "descripcion": "Estudio sobre aplicaciones de IA en educación.",
            "tipo": "Publicación",
            "fecha": "2023-05-15",
            "entidad": "ULEAM",
            "rutaarchivo": None,  # Para certificados o archivos
        },
        {
            "titulo": "Tesis de Maestría en Desarrollo Web",
            "descripcion": "Análisis de frameworks modernos para aplicaciones web.",
            "tipo": "Tesis",
            "fecha": "2022-12-01",
            "entidad": "Universidad Nacional",
            "rutaarchivo": None,
        },
        # Agrega más productos aquí si quieres
    ]
    
    context = {
        "perfil": perfil,
        "productos_acad": productos_acad,
    }
    
    return render(request, "productos_academicos.html", context)

def productos_laborales(request):
    perfil = get_perfil()

    datos = [
        {
            "id": 1,
            "nombreproducto": "Sistema de Inventario",
            "descripcion": "CRUD + reportes + login.",
            "url_proyecto": "https://github.com/"
        },
        {
            "id": 2,
            "nombreproducto": "Landing Profesional",
            "descripcion": "Sitio responsive para portafolio.",
            "url_proyecto": "https://github.com/"
        },
    ]

    return render(request, "productos_laborales.html", {
        "perfil": perfil,
        "datos": datos
    })

def exportar_cv(request):
    perfil = get_perfil()

    # Experiencia para el PDF (igual que en home)
    items = [
        {
            "cargodesempenado": "Desarrollador Web",
            "nombrempresa": "Empresa Demo",
            "lugarempresa": "Manta, Ecuador",
            "fechainiciogestion": "2024-01-01",
            "fechafingestion": None,
            "descripcionfunciones": "Desarrollo de aplicaciones web con Django.\nMantenimiento de sistemas.",
        },
        # Agrega más si quieres
    ]

    # si por ahora no usas BD, deja listas manuales:
    cursos = [
        {"nombrecurso": "SQL - Curso completo de Bases de Datos (SQL y MySQL).", "totalhoras": 40},
        {"nombrecurso": "Python básico - Introducción a programación.", "totalhoras": 30},
        {"nombrecurso": "Microsoft Access - Gestión de bases de datos.", "totalhoras": 20},
    ]
    reconocimientos = [
        {"tiporeconocimiento": "Reconocimiento académico", "descripcionreconocimiento": "ULEAM"},
    ]

    context = {
        "perfil": perfil,
        "items": items,  # Ahora incluye experiencia
        "cursos": cursos,
        "reconocimientos": reconocimientos,
        "show_exp": True,
        "show_cursos": True,
        "show_rec": True,
    }

    html = render_to_string("cv_pdf.html", context)

    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

    if pdf.err:
        return HttpResponse("❌ Error generando PDF. Revisa cv_pdf.html")

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="CV_Irvin_Javier_Sanchez_Lopez.pdf"'
    return response

# ... (todo lo anterior igual)

def cursos(request):
    perfil = get_perfil()

    # Tus datos hardcodeados de cursos, ajustados a los campos del template
    datos = [
        {
            "nombrecurso": "SQL - Curso completo de Bases de Datos (SQL y MySQL).",
            "entidadpatrocinadora": "ULEAM",
            "fechafin": "2023-12-01",  # Fecha de fin
            "totalhoras": 40,
            "descripcioncurso": "Curso avanzado en SQL y MySQL para gestión de bases de datos.",
            "rutacertificado": None,  # Sin archivo, así que no se mostrará
        },
        {
            "nombrecurso": "Python básico - Introducción a programación.",
            "entidadpatrocinadora": "Platzi",
            "fechafin": "2023-06-01",
            "totalhoras": 30,
            "descripcioncurso": "Introducción a la programación con Python.",
            "rutacertificado": None,
        },
        {
            "nombrecurso": "Microsoft Access - Gestión de bases de datos.",
            "entidadpatrocinadora": "Microsoft",
            "fechafin": "2023-03-01",
            "totalhoras": 20,
            "descripcioncurso": "Gestión de bases de datos con Microsoft Access.",
            "rutacertificado": None,
        },
    ]

    return render(request, "cursos.html", {
        "perfil": perfil,
        "datos": datos
    })

# Elimina esta función (cursos_view) ya que no la necesitas
# from django.shortcuts import render
# from .models import Perfil, Curso  # Ajusta según tus modelos

# def cursos_view(request):
#     perfil = Perfil.objects.first()  # O filtra por usuario si es necesario
#     datos = Curso.objects.all()  # O filtra si hay más lógica
#     return render(request, 'cursos.html', {'perfil': perfil, 'datos': datos})
def reconocimiento(request):
    perfil = get_perfil()

    # ✅ Datos hardcodeados para reconocimientos (ajusta según tus campos)
    datos = [
        {
            "descripcionreconocimiento": "Reconocimiento por excelencia académica en el programa de Ingeniería.",
            "fechareconocimiento": "2023-05-15",
            "rutacertificado": None,  # Sin archivo por ahora; agrega URL si tienes PDF
            "archivo_reconocimiento_completo": None,  # Para descargar todo, si tienes un ZIP
        },
        {
            "descripcionreconocimiento": "Premio al mejor proyecto laboral en desarrollo web.",
            "fechareconocimiento": "2024-01-10",
            "rutacertificado": None,
            "archivo_reconocimiento_completo": None,
        },
        # Agrega más si quieres
    ]

    return render(request, "reconocimiento.html", {
        "perfil": perfil,
        "datos": datos
    })
def garage(request):
    perfil = get_perfil()

    # ✅ Datos hardcodeados para items de garage (ajusta según tus campos y agrega más items)
    datos = [
        {
            "nombreproducto": "Taladro Inalámbrico Bosch",
            "descripcion": "Taladro profesional en excelente estado, incluye batería y cargador. Ideal para trabajos de carpintería y construcción.",
            "valordelbien": 150.00,
            "estadoproducto": "Bueno",
            "foto_producto": None,  # Sin imagen por ahora; agrega URL si tienes (e.g., "/media/imagenes/taladro.jpg")
            "documento_interes": None,  # Sin PDF por ahora; agrega URL si tienes ficha técnica
            "idperfilconqueestaactivo": {
                "email_contacto": "js6699415@gmail.com"  # Email para contactar (ajusta)
            }
        },
        {
            "nombreproducto": "Kit de Herramientas Stanley",
            "descripcion": "Set completo de herramientas manuales: martillo, destornilladores, alicates. Estado regular, pero funcional.",
            "valordelbien": 80.00,
            "estadoproducto": "Regular",
            "foto_producto": None,
            "documento_interes": None,
            "idperfilconqueestaactivo": {
                "email_contacto": "js6699415@gmail.com"
            }
        },
        {
            "nombreproducto": "Computadora Portátil Dell",
            "descripcion": "Laptop usada para desarrollo, con Windows 10, 8GB RAM, procesador i5. Perfecta para programar.",
            "valordelbien": 300.00,
            "estadoproducto": "Bueno",
            "foto_producto": None,
            "documento_interes": None,
            "idperfilconqueestaactivo": {
                "email_contacto": "js6699415@gmail.com"
            }
        },
        # Agrega más items aquí si quieres
    ]

    return render(request, "garage.html", {  # Cambiado de "reconocimiento.html" a "garage.html"
        "perfil": perfil,
        "datos": datos
    })