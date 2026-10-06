import os
import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission

from gestion.models import (
    Company,
    Area,
    EquipmentType,
    WorkOrderStatus,
    Priority,
    MaintenanceType,
    Equipment,
    WorkOrder,
    WorkOrderDetail,
)


class Command(BaseCommand):
    help = 'Carga usuarios y datos de prueba reproducibles'

    def handle(self, *args, **kwargs):

        self.stdout.write('Creando usuarios...')

        # =====================================================
        # USUARIO ADMINISTRADOR
        # =====================================================
        admin_user, _ = User.objects.get_or_create(
            username='admin_demo'
        )

        admin_user.email = 'admin_demo@example.com'
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True

        admin_user.set_password(
            os.getenv(
                'ADMIN_DEMO_PASSWORD',
                'Cambiar123!'
            )
        )

        admin_user.save()

        # =====================================================
        # USUARIO OPERADOR
        # =====================================================
        operator_user, _ = User.objects.get_or_create(
            username='operator_demo'
        )

        operator_user.email = 'operator_demo@example.com'
        operator_user.is_staff = True
        operator_user.is_superuser = False
        operator_user.is_active = True

        operator_user.set_password(
            os.getenv(
                'OPERATOR_DEMO_PASSWORD',
                'Cambiar123!'
            )
        )

        operator_user.save()

        # =====================================================
        # USUARIO LECTOR
        # =====================================================
        viewer_user, _ = User.objects.get_or_create(
            username='viewer_demo'
        )

        viewer_user.email = 'viewer_demo@example.com'
        viewer_user.is_staff = True
        viewer_user.is_superuser = False
        viewer_user.is_active = True

        viewer_user.set_password(
            os.getenv(
                'VIEWER_DEMO_PASSWORD',
                'Cambiar123!'
            )
        )

        viewer_user.save()

        # =====================================================
        # PERMISOS OPERADOR
        # =====================================================
        operator_permissions = Permission.objects.filter(
            codename__in=[
                'view_equipment',
                'view_workorder',
                'add_workorder',
                'change_workorder',
            ]
        )

        operator_user.user_permissions.set(
            operator_permissions
        )

        # =====================================================
        # PERMISOS LECTOR
        # =====================================================
        viewer_permissions = Permission.objects.filter(
            codename__in=[
                'view_equipment',
                'view_workorder',
            ]
        )

        viewer_user.user_permissions.set(
            viewer_permissions
        )

        self.stdout.write(
            'Creando tablas maestras...'
        )

        # =====================================================
        # COMPANIES
        # =====================================================
        companies = []

        for i in range(1, 6):

            company, _ = Company.objects.get_or_create(
                rut=f'76.000.{i:03d}-{i}',
                defaults={
                    'name': f'Company {i}',
                    'address': f'Address {i}',
                    'phone': f'5123400{i}',
                    'active': True,
                }
            )

            companies.append(company)

        # =====================================================
        # AREAS
        # =====================================================
        areas = []

        for company in companies:

            for j in range(1, 3):

                area, _ = Area.objects.get_or_create(
                    name=f'Area {j} - {company.name}',
                    company=company,
                    defaults={
                        'active': True
                    }
                )

                areas.append(area)

        # =====================================================
        # EQUIPMENT TYPES
        # =====================================================
        equipment_types = []

        equipment_type_names = [
            'Pump',
            'Motor',
            'Compressor',
            'Conveyor',
            'Generator',
            'Valve',
        ]

        for name in equipment_type_names:

            equipment_type, _ = (
                EquipmentType.objects.get_or_create(
                    name=name,
                    defaults={
                        'description': (
                            f'Equipment type {name}'
                        ),
                        'active': True,
                    }
                )
            )

            equipment_types.append(
                equipment_type
            )

        # =====================================================
        # WORK ORDER STATUS
        # =====================================================
        statuses = []

        status_names = [
            'Pending',
            'In Progress',
            'Completed',
            'Cancelled',
        ]

        for name in status_names:

            status, _ = (
                WorkOrderStatus.objects.get_or_create(
                    name=name,
                    defaults={
                        'description': (
                            f'Status {name}'
                        ),
                        'active': True,
                    }
                )
            )

            statuses.append(status)

        # =====================================================
        # PRIORITIES
        # =====================================================
        priorities = []

        priority_data = [
            ('Low', 1),
            ('Medium', 2),
            ('High', 3),
            ('Critical', 4),
        ]

        for name, level in priority_data:

            priority, _ = Priority.objects.get_or_create(
                level=level,
                defaults={
                    'name': name,
                    'active': True,
                }
            )

            priorities.append(priority)

        # =====================================================
        # MAINTENANCE TYPES
        # =====================================================
        maintenance_types = []

        maintenance_type_names = [
            'Preventive',
            'Corrective',
            'Predictive',
            'Inspection',
        ]

        for name in maintenance_type_names:

            maintenance_type, _ = (
                MaintenanceType.objects.get_or_create(
                    name=name,
                    defaults={
                        'description': (
                            f'{name} maintenance'
                        ),
                        'active': True,
                    }
                )
            )

            maintenance_types.append(
                maintenance_type
            )

        self.stdout.write(
            'Creando equipos...'
        )

        # =====================================================
        # EQUIPMENTS
        # =====================================================
        equipments = []

        for i in range(1, 201):

            equipment, _ = Equipment.objects.get_or_create(
                code=f'EQ-{i:04d}',
                defaults={
                    'name': f'Equipment {i}',
                    'equipment_type': random.choice(
                        equipment_types
                    ),
                    'area': random.choice(
                        areas
                    ),
                    'brand': (
                        f'Brand {random.randint(1, 10)}'
                    ),
                    'model': (
                        f'Model {random.randint(1, 20)}'
                    ),
                    'serial_number': (
                        f'SERIAL-{i:05d}'
                    ),
                    'acquisition_date': (
                        date.today()
                        - timedelta(
                            days=random.randint(
                                30,
                                3000
                            )
                        )
                    ),
                    'active': True,
                    'deleted_at': None,
                }
            )

            equipments.append(equipment)

        self.stdout.write(
            'Creando órdenes de trabajo...'
        )

        # =====================================================
        # WORK ORDERS
        # =====================================================
        users = [
            admin_user,
            operator_user,
            viewer_user,
        ]

        work_orders = []

        for i in range(1, 701):

            start_date = (
                date.today()
                - timedelta(
                    days=random.randint(
                        0,
                        365
                    )
                )
            )

            work_order, _ = (
                WorkOrder.objects.get_or_create(
                    number=f'WO-{i:05d}',
                    defaults={
                        'equipment': random.choice(
                            equipments
                        ),
                        'status': random.choice(
                            statuses
                        ),
                        'priority': random.choice(
                            priorities
                        ),
                        'maintenance_type': random.choice(
                            maintenance_types
                        ),
                        'owner': random.choice(
                            users
                        ),
                        'description': (
                            f'Maintenance work order {i}'
                        ),
                        'start_date': start_date,
                        'end_date': (
                            start_date
                            + timedelta(
                                days=random.randint(
                                    1,
                                    10
                                )
                            )
                        ),
                        'responsible': (
                            f'Technician '
                            f'{random.randint(1, 30)}'
                        ),
                        'observations': (
                            f'Observation {i}'
                        ),
                        'deleted_at': None,
                    }
                )
            )

            work_orders.append(
                work_order
            )

        self.stdout.write(
            'Creando detalles de órdenes...'
        )

        # =====================================================
        # BORRAR SOLO DETALLES GENERADOS POR ESTE SEED
        # =====================================================
        WorkOrderDetail.objects.filter(
            activity__startswith=(
                'Maintenance activity '
            )
        ).delete()

        # =====================================================
        # CREAR EXACTAMENTE 300 DETALLES
        # =====================================================
        for i in range(1, 301):

            work_order = work_orders[
                (i - 1) % len(work_orders)
            ]

            WorkOrderDetail.objects.create(
                work_order=work_order,
                activity=(
                    f'Maintenance activity {i}'
                ),
                work_hours=round(
                    random.uniform(1, 8),
                    2
                ),
                observation=(
                    f'Detail observation {i}'
                ),
                deleted_at=None,
            )

        # =====================================================
        # TOTAL DE REGISTROS DE NEGOCIO
        # =====================================================
        total_records = (
            Company.objects.count()
            + Area.objects.count()
            + EquipmentType.objects.count()
            + WorkOrderStatus.objects.count()
            + Priority.objects.count()
            + MaintenanceType.objects.count()
            + Equipment.objects.count()
            + WorkOrder.objects.count()
            + WorkOrderDetail.objects.count()
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Seed completado correctamente. '
                f'Total registros de negocio: '
                f'{total_records}'
            )
        )