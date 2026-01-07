from django.shortcuts import render

def hoja_vida(request):
    datos = {
        "nombre": "Javier Sanchez",
        "contacto": {
            "email": "js6699415@gmail.com",
            "telefono": "0987654321",
            "ciudad": "manta"
        },
        "resumen": "Breve descripción de tu perfil profesional y objetivos.",
        "experiencia": [
            {
                "puesto": "Puesto 1",
                "empresa": "Empresa 1",
                "fechas": "Fecha inicio - Fecha fin",
                "descripcion": "Descripción de responsabilidades y logros."
            },
            {
                "puesto": "Puesto 2",
                "empresa": "Empresa 2",
                "fechas": "Fecha inicio - Fecha fin",
                "descripcion": "Descripción de responsabilidades y logros."
            }
        ],
        "educacion": [
            {
                "titulo": "Título 1",
                "institucion": "Institución 1",
                "anio": "Año de graduación",
                "detalles": "Detalles adicionales."
            },
            {
                "titulo": "Título 2",
                "institucion": "Institución 2",
                "anio": "Año de graduación",
                "detalles": "Detalles adicionales."
            }
        ],
        "habilidades": ["Habilidad 1", "Habilidad 2", "Habilidad 3"]
    }

    return render(request, "hoja.html", datos)
from django.shortcuts import render

def home(request):
    datos = {
        "nombre": "Tu Nombre Completo",
        "contacto": {
            "email": "tuemail@example.com",
            "telefono": "tu teléfono",
            "ciudad": "tu ciudad"
        },
        "resumen": "Breve descripción de tu perfil profesional y objetivos.",
        "experiencia": [
            {
                "puesto": "Puesto 1",
                "empresa": "Empresa 1",
                "fechas": "Fecha inicio - Fecha fin",
                "descripcion": "Descripción de responsabilidades y logros."
            }
        ],
        "educacion": [
            {
                "titulo": "Título 1",
                "institucion": "Institución 1",
                "anio": "Año de graduación",
                "detalles": "Detalles adicionales."
            }
        ],
        "habilidades": ["Habilidad 1", "Habilidad 2", "Habilidad 3"]
    }

    return render(request, "hoja.html", datos)
