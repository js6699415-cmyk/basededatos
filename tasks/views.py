import io
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import DatosPersonales, ExperienciaLaboral, CursosRealizados, Reconocimientos, ProductosAcademicos, ProductosLaborales, VentaGarage  # Importa todos los modelos necesarios

# ✅ PERFIL (diccionario) - Mantén como respaldo si lo necesitas para otras partes
def get_perfil():
    return {
        "nombres": "Irvin Javier",
        "apellidos": "Sanchez Lopez",
        "descripcionperfil": "Aficionado a aprender nuevas formas de aplicar tecnología e Inteligencia Artificial",
        "cargo": "Desarrollador en Formación",  # Agregado como sugerencia anterior
        "email": "js6699415@gmail.com",  # Agregado (basado en "email_contacto" original)
        "cedula": "13112345678",  # Agregado (basado en "numerocedula" original)
        "telefono": "0995002629",  # Agregado (basado en "telefonofijo" original)
        "nacionalidad": "Ecuatoriano",  # Agregado
        "ubicacion": "Manta",  # Agregado (basado en "direcciondomiciliaria" original)
        "estado_civil": "Soltero", 
        "fechanacimiento": "30 de mayo de 2006",
        "foto": "JGP/static/img/foto.jpg",
    }

def home(request):
    # Obtén el perfil activo desde la DB (ajusta si no usas perfilactivo)
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    if not perfil:
        # Si no hay perfil activo, usa datos por defecto o redirige
        perfil = None  # O crea un perfil dummy si es necesario

    # Consulta experiencia activa
    resumen_exp = ExperienciaLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechainiciogestion') if perfil else []

    # Consulta cursos activos
    resumen_cursos = CursosRealizados.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []

    # Consulta reconocimientos activos
    resumen_rec = Reconocimientos.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []

    # Consulta productos académicos activos
    resumen_acad = ProductosAcademicos.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []

    # Consulta productos laborales activos
    resumen_lab = ProductosLaborales.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []

    # Consulta garage activos
    resumen_garage = VentaGarage.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []

    context = {
        "perfil": perfil,  # Ahora es una instancia del modelo, no un dict
        "resumen_exp": resumen_exp,
        "resumen_cursos": resumen_cursos,
        "resumen_rec": resumen_rec,
        "resumen_acad": resumen_acad,
        "resumen_lab": resumen_lab,
        "resumen_garage": resumen_garage,
    }

    return render(request, "hoja_de_vida.html", context)

def experiencia(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    datos = ExperienciaLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechainiciogestion') if perfil else []
    return render(request, "experiencia.html", {"perfil": perfil, "datos": datos})

def productos_academicos(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    productos_acad = ProductosAcademicos.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []
    context = {
        "perfil": perfil,
        "productos_acad": productos_acad,
    }
    return render(request, "productos_academicos.html", context)

def productos_laborales(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    datos = ProductosLaborales.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, "productos_laborales.html", {
        "perfil": perfil,
        "datos": datos
    })

def exportar_cv(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    items = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else []
    cursos = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else []
    reconocimientos = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else []
    productos = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else []
    productos_laborales = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else []
    garage = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else []

    context = {
        "perfil": perfil,
        "items": items,
        "cursos": cursos,
        "reconocimientos": reconocimientos,
        "productos": productos,
        "productos_laborales": productos_laborales,
        "garage": garage,
        "incl_experiencia": True,
        "incl_cursos": True,
        "incl_logros": True,
        "incl_proyectos": True,
        "incl_garage": False,  # Cambia a True si agregas datos
    }

    html = render_to_string("cv_pdf.html", context)

    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

    if pdf.err:
        return HttpResponse("❌ Error generando PDF. Revisa cv_pdf.html")

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="CV_Irvin_Javier_Sanchez_Lopez.pdf"'
    return response

def cursos(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    datos = CursosRealizados.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, "cursos.html", {
        "perfil": perfil,
        "datos": datos
    })

def reconocimiento(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    datos = Reconocimientos.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, "reconocimiento.html", {
        "perfil": perfil,
        "datos": datos
    })

def garage(request):
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    datos = VentaGarage.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, "garage.html", {
        "perfil": perfil,
        "datos": datos
    })