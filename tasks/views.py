import io
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from perfil.models import DatosPersonales, ExperienciaLaboral, CursosRealizados, Reconocimientos, ProductosAcademicos, ProductosLaborales, VentaGarage

def get_perfil():
    return DatosPersonales.objects.filter(perfilactivo=1).first()

def home(request):
    perfil = get_perfil()
    if not perfil:
        perfil = None

    resumen_exp = ExperienciaLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechainiciogestion') if perfil else []
    
    resumen_cursos = CursosRealizados.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []
    
    resumen_rec = Reconocimientos.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []
    
    resumen_acad = ProductosAcademicos.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []
    
    resumen_lab = ProductosLaborales.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []
    
    resumen_garage = VentaGarage.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []

    context = {
        "perfil": perfil,
        "resumen_exp": resumen_exp,
        "resumen_cursos": resumen_cursos,
        "resumen_rec": resumen_rec,
        "resumen_acad": resumen_acad,
        "resumen_lab": resumen_lab,
        "resumen_garage": resumen_garage,
    }
    return render(request, "hoja_de_vida.html", context)

def experiencia(request):
    perfil = get_perfil()
    datos = ExperienciaLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechainiciogestion') if perfil else []
    return render(request, "experiencia.html", {"perfil": perfil, "datos": datos})

def productos_academicos(request):
    perfil = get_perfil()
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
    perfil = get_perfil()
    datos = ProductosLaborales.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, "productos_laborales.html", {"perfil": perfil, "datos": datos})

def exportar_cv(request):
    perfil = get_perfil()
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
        "incl_garage": False,
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
    perfil = get_perfil()
    datos = CursosRealizados.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, "cursos.html", {"perfil": perfil, "datos": datos})

def reconocimiento(request):
    perfil = get_perfil()
    datos = Reconocimientos.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, "reconocimiento.html", {"perfil": perfil, "datos": datos})

def garage(request):
    perfil = get_perfil()
    datos = VentaGarage.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, "garage.html", {"perfil": perfil, "datos": datos})