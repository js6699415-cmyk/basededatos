from django.contrib import admin
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos, 
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage
)

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'numerocedula', 'email_contacto', 'perfilactivo')  # Agregué 'perfilactivo' para ver el estado activo
    list_filter = ('sexo', 'estadocivil', 'nacionalidad', 'perfilactivo')  # Filtros por género, estado civil, etc.
    search_fields = ('nombres', 'apellidos', 'numerocedula', 'email_contacto')  # Búsqueda por nombre, cédula, email
    fields = (
        'idperfil', 'fotoperfil', 
        'nombres', 'apellidos', 'descripcionperfil', 
        'email_contacto', 'telefonofijo', 'telefonoconvencional',
        'numerocedula', 'nacionalidad', 'fechanacimiento', 'lugarnacimiento',
        'sexo', 'estadocivil', 'licenciaconducir',
        'direcciondomiciliaria', 'direcciontrabajo', 'sitioweb', 'perfilactivo'
    )
    readonly_fields = ('idperfil',)  # ID auto-generado, no editable

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'fechafingestion', 'activarparaqueseveaenfront')  # Agregué fechas y estado
    list_filter = ('activarparaqueseveaenfront', 'nombrempresa', 'fechainiciogestion')  # Filtros por empresa, fecha, estado
    search_fields = ('cargodesempenado', 'nombrempresa', 'lugarempresa')  # Búsqueda por cargo, empresa, lugar
    raw_id_fields = ('idperfilconqueestaactivo',)  # Mejora rendimiento para foreign key
    fields = (
        'idexperiencilaboral', 'idperfilconqueestaactivo', 'cargodesempenado', 
        'nombrempresa', 'lugarempresa', 'emailempresa', 'sitiowebempresa', 
        'nombrecontactoempresarial', 'telefonocontactoempresarial', 'fechainiciogestion', 
        'fechafingestion', 'descripcionfunciones', 'activarparaqueseveaenfront', 'rutacertificado'
    )
    readonly_fields = ('idexperiencilaboral',)  # ID auto-generado

@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    list_display = ('descripcionreconocimiento', 'tiporeconocimiento', 'entidadpatrocinadora', 'fechareconocimiento', 'activarparaqueseveaenfront')  # Agregué fecha y estado
    list_filter = ('tiporeconocimiento', 'fechareconocimiento', 'activarparaqueseveaenfront')  # Filtros por tipo, fecha, estado
    search_fields = ('descripcionreconocimiento', 'entidadpatrocinadora', 'nombrecontactoauspicia')  # Búsqueda por descripción, entidad, contacto
    raw_id_fields = ('idperfilconqueestaactivo',)
    fields = (
        'idreconocimiento', 'idperfilconqueestaactivo', 'tiporeconocimiento', 
        'fechareconocimiento', 'descripcionreconocimiento', 'entidadpatrocinadora',
        'nombrecontactoauspicia', 'telefonocontactoauspicia', 'activarparaqueseveaenfront',
        'rutacertificado'
    )
    readonly_fields = ('idreconocimiento',)

@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = ('nombrecurso', 'entidadpatrocinadora', 'totalhoras', 'fechainicio', 'fechafin', 'activarparaqueseveaenfront')  # Agregué fechas y estado
    list_filter = ('activarparaqueseveaenfront', 'entidadpatrocinadora', 'fechainicio')  # Filtros por entidad, fecha, estado
    search_fields = ('nombrecurso', 'entidadpatrocinadora', 'nombrecontactoauspicia')  # Búsqueda por nombre, entidad, contacto
    raw_id_fields = ('idperfilconqueestaactivo',)
    fields = (
        'idcursorealizado', 'idperfilconqueestaactivo', 'nombrecurso', 
        'fechainicio', 'fechafin', 'totalhoras', 'descripcioncurso', 
        'entidadpatrocinadora', 'nombrecontactoauspicia', 'telefonocontactoauspicia', 
        'emailempresapatrocinadora', 'activarparaqueseveaenfront', 'rutacertificado'
    )
    readonly_fields = ('idcursorealizado',)

@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'activarparaqueseveaenfront')  # Mantiene básico, pero agregué estado
    list_filter = ('clasificador', 'activarparaqueseveaenfront')  # Filtros por clasificador y estado
    search_fields = ('nombrerecurso', 'clasificador', 'descripcion')  # Búsqueda por nombre, clasificador, descripción
    raw_id_fields = ('idperfilconqueestaactivo',)
    fields = (
        'idproductoacademico', 'idperfilconqueestaactivo', 'nombrerecurso', 
        'clasificador', 'descripcion', 'activarparaqueseveaenfront'
    )
    readonly_fields = ('idproductoacademico',)

@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto', 'activarparaqueseveaenfront')  # Mantiene básico, pero agregué estado
    list_filter = ('fechaproducto', 'activarparaqueseveaenfront')  # Filtros por fecha y estado
    search_fields = ('nombreproducto', 'descripcion')  # Búsqueda por nombre y descripción
    raw_id_fields = ('idperfilconqueestaactivo',)
    fields = (
        'idproductoslaborales', 'idperfilconqueestaactivo', 'nombreproducto', 
        'fechaproducto', 'descripcion', 'url_proyecto', 'activarparaqueseveaenfront'
    )
    readonly_fields = ('idproductoslaborales',)

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'valordelbien', 'estadoproducto', 'activarparaqueseveaenfront')  # Mantiene básico, pero agregué estado
    list_filter = ('estadoproducto', 'activarparaqueseveaenfront')  # Filtros por estado del producto y activación
    search_fields = ('nombreproducto', 'descripcion')  # Búsqueda por nombre y descripción
    raw_id_fields = ('idperfilconqueestaactivo',)
    fields = (
        'idventagarage', 'idperfilconqueestaactivo', 'nombreproducto', 
        'estadoproducto', 'descripcion', 'valordelbien', 'activarparaqueseveaenfront', 
        'documento_interes'  # Incluido para PDFs/fichas técnicas
    )
    readonly_fields = ('idventagarage',)

