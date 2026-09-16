from django.contrib import admin
from .models import (
    Empresa,
    Area,
    TipoEquipo,
    EstadoOrden,
    Equipo,
    OrdenTrabajo
)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'telefono', 'activo')
    search_fields = ('nombre', 'rut')
    list_filter = ('activo',)
    ordering = ('nombre',)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa', 'activo')
    search_fields = ('nombre', 'empresa__nombre')
    list_filter = ('empresa', 'activo')
    ordering = ('nombre',)
    list_select_related = ('empresa',)


@admin.register(TipoEquipo)
class TipoEquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    ordering = ('nombre',)


@admin.register(EstadoOrden)
class EstadoOrdenAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'nombre',
        'tipo_equipo',
        'area',
        'marca',
        'activo',
    )

    search_fields = (
        'codigo',
        'nombre',
        'marca',
        'modelo',
        'numero_serie',
        'area__nombre',
        'tipo_equipo__nombre',
    )

    list_filter = (
        'tipo_equipo',
        'area',
        'activo',
    )

    ordering = ('codigo',)

    list_select_related = (
        'tipo_equipo',
        'area',
    )

@admin.action(description='Cambiar prioridad a ALTA')
def cambiar_prioridad_alta(modeladmin, request, queryset):
    queryset.update(prioridad='ALTA')
    
@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):
    actions = [cambiar_prioridad_alta]
    list_display = (
        'numero_orden',
        'equipo',
        'estado',
        'prioridad',
        'propietario',
        'fecha_inicio',
        'fecha_termino',
        'responsable',
    )

    search_fields = (
        'numero_orden',
        'equipo__codigo',
        'equipo__nombre',
        'responsable',
        'descripcion',
    )

    list_filter = (
        'estado',
        'prioridad',
        'fecha_inicio',
    )

    ordering = ('-fecha_inicio',)

    list_select_related = (
        'equipo',
        'estado',
    )

def get_queryset(self, request):
    qs = super().get_queryset(request)

    if request.user.is_superuser:
        return qs

    return qs.filter(propietario=request.user)

def save_model(self, request, obj, form, change):
    if not request.user.is_superuser:
        obj.propietario = request.user

    super().save_model(request, obj, form, change)

def get_readonly_fields(self, request, obj=None):
    if request.user.is_superuser:
        return ()

    return ('propietario',)