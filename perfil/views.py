# perfil/views.py

import io
import requests
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from pypdf import PdfWriter, PdfReader

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

    # Obtener parámetros de la URL para incluir secciones (igual que en tu código original)
    incl_exp = request.GET.get('exp') == 'true'
    incl_cursos = request.GET.get('cursos') == 'true'
    incl_logros = request.GET.get('logros') == 'true'
    incl_proy = request.GET.get('proy') == 'true'
    incl_garage = request.GET.get('garage') == 'true'

    # Usar datos hardcodeados como en tu código, pero filtrados por los parámetros
    experiencias = [
        {
            "cargodesempenado": "Desarrollador Web",
            "nombrempresa": "Empresa Demo",
            "lugarempresa": "Manta, Ecuador",
            "fechainiciogestion": "2024-01-01",
            "fechafingestion": None,
            "descripcionfunciones": "Desarrollo de aplicaciones web con Django.\nMantenimiento de sistemas.",
            "rutacertificado": None,  # Campo de tu código hardcodeado
        },
    ] if incl_exp else []

    cursos_objs = [
        {"nombrecurso": "SQL - Curso completo de Bases de Datos (SQL y MySQL).", "totalhoras": 40, "rutacertificado": None},
        {"nombrecurso": "Python básico - Introducción a programación.", "totalhoras": 30, "rutacertificado": None},
        {"nombrecurso": "Microsoft Access - Gestión de bases de datos.", "totalhoras": 20, "rutacertificado": None},
    ] if incl_cursos else []

    reco_objs = [
        {"descripcionreconocimiento": "Reconocimiento académico", "entidadpatrocinadora": "ULEAM", "fechareconocimiento": "2025-01-01", "rutacertificado": None},
    ] if incl_logros else []

    garage_items = [
        {
            "nombreproducto": "Taladro Inalámbrico Bosch",
            "descripcion": "Taladro profesional en excelente estado, incluye batería y cargador. Ideal para trabajos de carpintería y construcción.",
            "valordelbien": 150.00,
            "estadoproducto": "Bueno",
            "foto_producto": None,
            "documento_interes": None,  # Campo de tu código hardcodeado
            "idperfilconqueestaactivo": {
                "email_contacto": "js6699415@gmail.com"
            }
        },
        # Agrega más si quieres
    ] if incl_garage else []

    academicos = [] if incl_proy else []  # Dejar vacío por ahora, como en tu código
    laborales = [] if incl_proy else []  # Dejar vacío por ahora, como en tu código

    # Renderizar el template (usando cv_pdf.html como en tu código, pero ajustado para incluir todo)
    template = get_template('cv_pdf.html')  # Cambia a 'cv_pdf_maestro.html' si prefieres el del original
    html = template.render({
        'perfil': perfil, 
        'items': experiencias,  # Usando 'items' como en tu código
        'productos': academicos,
        'productos_laborales': laborales, 
        'cursos': cursos_objs, 
        'reconocimientos': reco_objs,
        'garage': garage_items,
        'incl_experiencia': incl_exp,
        'incl_proyectos': incl_proy,
        'incl_cursos': incl_cursos,
        'incl_logros': incl_logros,
        'incl_garage': incl_garage
    })
    
    buffer_cv = io.BytesIO()
    pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=buffer_cv)

    writer = PdfWriter()
    buffer_cv.seek(0)
    try:
        reader_base = PdfReader(buffer_cv)
        for page in reader_base.pages:
            writer.add_page(page)
    except:
        pass

    # Función para pegar certificados (igual que en tu código original, pero adaptada a los campos hardcodeados)
    def pegar_certificados(queryset, nombre_campo):
        for obj in queryset:
            archivo = obj.get(nombre_campo, None)  # Usar .get() ya que son diccionarios
            if archivo and hasattr(archivo, 'url'):  # Si es un FileField, pero en hardcode es None o string
                try:
                    r = requests.get(archivo.url, timeout=15)
                    if r.status_code == 200:
                        writer.append(io.BytesIO(r.content))
                except Exception as e:
                    print(f"Error pegando: {e}")
                    continue
            elif archivo and isinstance(archivo, str):  # Si es una URL string
                try:
                    r = requests.get(archivo, timeout=15)
                    if r.status_code == 200:
                        writer.append(io.BytesIO(r.content))
                except Exception as e:
                    print(f"Error pegando: {e}")
                    continue

    # Pegar certificados según los parámetros
    if incl_exp: pegar_certificados(experiencias, 'rutacertificado')
    if incl_cursos: pegar_certificados(cursos_objs, 'rutacertificado')
    if incl_logros: pegar_certificados(reco_objs, 'rutacertificado')
    if incl_garage: pegar_certificados(garage_items, 'documento_interes')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Portafolio_{perfil.apellidos if perfil else "Usuario"}.pdf"'
    writer.write(response)
    writer.close()
    
    return response

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

def reconocimientos(request):
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