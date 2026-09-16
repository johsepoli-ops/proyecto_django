from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission

from gestion.models import (
    Empresa,
    Area,
    TipoEquipo,
    EstadoOrden,
    Equipo,
    OrdenTrabajo,
    DetalleOrden,
)


class Command(BaseCommand):
    help = 'Carga datos de prueba para la evaluación'

    def handle(self, *args, **options):

        self.stdout.write('Cargando datos de prueba...')

        # Usuario administrador
        admin, _ = User.objects.get_or_create(
            username='admin_demo',
            defaults={
                'email': 'admin@demo.cl',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )

        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True
        admin.set_password('AdminDemo2026!')
        admin.save()

        # Usuario limitado
        operador, _ = User.objects.get_or_create(
            username='operador_demo',
            defaults={
                'email': 'operador@demo.cl',
                'is_staff': True,
                'is_superuser': False,
                'is_active': True,
            }
        )

        operador.is_staff = True
        operador.is_superuser = False
        operador.is_active = True
        operador.set_password('OperadorDemo2026!')
        operador.save()

        operador.user_permissions.clear()

        permisos = Permission.objects.filter(
            codename__in=[
                'view_equipo',
                'view_ordentrabajo',
                'add_ordentrabajo',
                'change_ordentrabajo',
            ]
        )

        operador.user_permissions.set(permisos)

        # Empresa
        empresa, _ = Empresa.objects.get_or_create(
            rut='76.123.456-7',
            defaults={
                'nombre': 'Empresa Demo',
                'direccion': 'La Serena',
                'telefono': '512345678',
                'activo': True,
            }
        )

        # Área
        area, _ = Area.objects.get_or_create(
            nombre='Mantención',
            empresa=empresa,
            defaults={
                'activo': True,
            }
        )

        # Tipo de equipo
        tipo_equipo, _ = TipoEquipo.objects.get_or_create(
            nombre='Bomba',
            defaults={
                'descripcion': 'Equipo de bombeo',
                'activo': True,
            }
        )

        # Estado de orden
        estado, _ = EstadoOrden.objects.get_or_create(
            nombre='Pendiente',
            defaults={
                'descripcion': 'Orden pendiente de ejecución',
            }
        )

        # Equipo
        equipo, _ = Equipo.objects.get_or_create(
            codigo='EQ-001',
            defaults={
                'nombre': 'Bomba Principal',
                'tipo_equipo': tipo_equipo,
                'area': area,
                'marca': 'Demo',
                'modelo': 'X1',
                'numero_serie': 'SERIE-001',
                'activo': True,
            }
        )

        # Orden admin
        orden_admin, _ = OrdenTrabajo.objects.get_or_create(
            numero_orden='OT-001',
            defaults={
                'equipo': equipo,
                'estado': estado,
                'descripcion': 'Mantención preventiva',
                'prioridad': 'MEDIA',
                'fecha_inicio': '2026-09-16',
                'responsable': 'Administrador Demo',
                'propietario': admin,
                'observaciones': 'Orden perteneciente al administrador',
            }
        )

        # Orden operador
        orden_operador, _ = OrdenTrabajo.objects.get_or_create(
            numero_orden='OT-002',
            defaults={
                'equipo': equipo,
                'estado': estado,
                'descripcion': 'Mantención correctiva',
                'prioridad': 'MEDIA',
                'fecha_inicio': '2026-09-16',
                'responsable': 'Operador Demo',
                'propietario': operador,
                'observaciones': 'Orden perteneciente al operador',
            }
        )

        # Detalles inline
        DetalleOrden.objects.get_or_create(
            orden=orden_admin,
            actividad='Revisión general',
            defaults={
                'horas_trabajo': 2.00,
                'observacion': 'Sin novedades',
            }
        )

        DetalleOrden.objects.get_or_create(
            orden=orden_operador,
            actividad='Inspección de componentes',
            defaults={
                'horas_trabajo': 1.50,
                'observacion': 'Actividad de prueba',
            }
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Datos de prueba cargados correctamente.'
            )
        )

        self.stdout.write('')
        self.stdout.write(
            'Administrador: admin_demo / AdminDemo2026!'
        )
        self.stdout.write(
            'Operador: operador_demo / OperadorDemo2026!'
        )