from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def get_datos(extra=None):
    datos = {
        "nombre": "Javier Sánchez",
        "cargo": "Estudiante de Tecnologías de la Información",
        "contacto": {
            "email": "js6699415@gmail.com",
            "telefono": "0981738602",
            "ciudad": "Manta, Ecuador"
        },

        "resumen": (
            "Estudiante de Tecnologías de la Información, con formación en "
            "bachillerato en Comercialización y Ventas. Poseo un marcado interés por el área "
            "tecnológica, especialmente en ciberseguridad y protección de la información. "
            "Me caracterizo por ser responsable, proactivo y con capacidad de adaptación y "
            "trabajo en equipo. Mi objetivo profesional es desarrollarme en el ámbito de la "
            "ciberseguridad, fortaleciendo mis conocimientos en redes, sistemas y análisis de "
            "vulnerabilidades."
        ),

        "habilidades": [
            "Conocimientos básicos de redes y seguridad informática",
            "Soporte técnico y mantenimiento básico de equipos",
            "Uso de herramientas ofimáticas",
            "Trabajo en equipo",
            "Responsabilidad y puntualidad"
        ],

        "experiencia": [
            {
                "puesto": "Asistente de Soporte Técnico",
                "empresa": "Farmacias Santa Martha",
                "fechas": "2023 - 2024",
                "descripcion": "Apoyo en tareas básicas del área de sistemas y asistencia técnica."
            },
            {
                "puesto": "Curso completo de Microsoft Access",
                "empresa": "Udemy",
                "fechas": "2025 - 2026",
                "descripcion": "Creación de tablas, consultas, formularios y reportes."
            },
            {
                "puesto": "Curso de Programación Básica",
                "empresa": "Universidad Laica Eloy Alfaro de Manabí",
                "fechas": "2024 - 2025",
                "descripcion": "Fundamentos de lógica y programación."
            },
            {
                "puesto": "Curso de Inglés – Rosetta Stone",
                "empresa": "Universidad / Plataforma Educativa",
                "fechas": "2024 - 2025",
                "descripcion": "Desarrollo de vocabulario y comprensión básica."
            }
        ],

        "educacion": [
            {
                "titulo": "Educación Primaria",
                "institucion": "Unidad Educativa Fiscal José María Córdova",
                "anio": "2016 - 2017"
            },
            {
                "titulo": "Bachiller en Comercialización y Ventas",
                "institucion": "Unidad Educativa Santa Marianita",
                "anio": "2023 - 2024"
            }
        ],

        "idiomas": [
            {"nombre": "Español"},
            {"nombre": "Inglés"}
        ],

        "referencias": [
            {"nombre": "Ing. Leonardo Alonzo", "telefono": "0980489202"},
            {"nombre": "Sr. Rúben Zambrano", "telefono": "0959736436"}
        ]
    }

    # 👉 Sobrescribe SOLO los campos permitidos
    if extra:
        datos["nombre"] = extra.get("nombre", datos["nombre"])
        datos["contacto"]["email"] = extra.get("email", datos["contacto"]["email"])
        datos["contacto"]["telefono"] = extra.get("telefono", datos["contacto"]["telefono"])
        datos["contacto"]["ciudad"] = extra.get("ciudad", datos["contacto"]["ciudad"])

    return datos


def hoja_vida(request):
    if request.method == "POST":
        datos = get_datos(request.POST)
    else:
        datos = get_datos()

    return render(request, "hoja.html", datos)


def descargar_pdf(request):
    datos = get_datos(request.POST if request.method == "POST" else None)
    template = get_template("hoja.html")
    html = template.render(datos)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Hoja_de_Vida_Javier_Sanchez.pdf"'
    pisa.CreatePDF(html, dest=response)

    return response
