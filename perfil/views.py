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

# ... (el resto de las vistas como en tu código hardcodeado)

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