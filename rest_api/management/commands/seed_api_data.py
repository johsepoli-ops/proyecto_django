import random
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from gestion.models import (
    Area,
    Company,
    Equipment,
    EquipmentType,
    MaintenanceEvidence,
    MaintenanceType,
    Priority,
    WorkOrder,
    WorkOrderDetail,
    WorkOrderStatus,
)


class Command(BaseCommand):
    help = 'Completa datos de prueba para la evaluación API hasta superar 2000 registros de dominio.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Iniciando carga de datos para API...')

        company = Company.objects.filter(active=True).first()
        if not company:
            company = Company.objects.create(
                name='Empresa API Demo',
                rut='99.999.999-9',
                address='Dirección Demo',
                phone='999999999',
                active=True,
            )

        area = Area.objects.filter(active=True).first()
        if not area:
            area = Area.objects.create(
                name='Área API Demo',
                company=company,
                active=True,
            )

        equipment_type = EquipmentType.objects.filter(active=True).first()
        if not equipment_type:
            equipment_type = EquipmentType.objects.create(
                name='Tipo API Demo',
                description='Tipo de equipo para datos de prueba API',
                active=True,
            )

        status = WorkOrderStatus.objects.filter(active=True).first()
        if not status:
            status = WorkOrderStatus.objects.create(
                name='Pendiente API',
                description='Estado para datos de prueba API',
                active=True,
            )

        priority = Priority.objects.filter(active=True).first()
        if not priority:
            priority = Priority.objects.create(
                name='Media API',
                level=99,
                active=True,
            )

        maintenance_type = MaintenanceType.objects.filter(active=True).first()
        if not maintenance_type:
            maintenance_type = MaintenanceType.objects.create(
                name='Preventivo API',
                description='Mantención preventiva para pruebas API',
                active=True,
            )

        owner = User.objects.filter(is_active=True).first()
        if not owner:
            self.stdout.write(
                self.style.ERROR(
                    'No existe ningún usuario activo. Ejecuta primero create_api_users.'
                )
            )
            return

        # --------------------------------------------------
        # EQUIPMENT -> mínimo 300
        # --------------------------------------------------

        equipment_target = 300
        current_equipment = Equipment.objects.count()

        for i in range(current_equipment + 1, equipment_target + 1):
            Equipment.objects.get_or_create(
                code=f'API-EQ-{i:04d}',
                defaults={
                    'name': f'Equipo API {i}',
                    'equipment_type': equipment_type,
                    'area': area,
                    'brand': f'Marca {random.randint(1, 10)}',
                    'model': f'Modelo {random.randint(1, 20)}',
                    'serial_number': f'API-SERIAL-{i:05d}',
                    'acquisition_date': date.today()
                    - timedelta(days=random.randint(30, 2500)),
                    'active': True,
                },
            )

        equipments = list(
            Equipment.objects.filter(deleted_at__isnull=True)
        )

        # --------------------------------------------------
        # WORK ORDER -> mínimo 1200
        # --------------------------------------------------

        work_order_target = 1200
        current_work_orders = WorkOrder.objects.count()

        for i in range(current_work_orders + 1, work_order_target + 1):
            start_date = date.today() - timedelta(
                days=random.randint(1, 365)
            )

            WorkOrder.objects.get_or_create(
                number=f'API-OT-{i:05d}',
                defaults={
                    'equipment': random.choice(equipments),
                    'status': status,
                    'priority': priority,
                    'maintenance_type': maintenance_type,
                    'owner': owner,
                    'description': f'Orden de trabajo API número {i}',
                    'start_date': start_date,
                    'end_date': None,
                    'responsible': f'Técnico API {random.randint(1, 30)}',
                    'observations': 'Registro generado para evaluación API.',
                },
            )

        work_orders = list(
            WorkOrder.objects.filter(deleted_at__isnull=True)
        )

        # --------------------------------------------------
        # WORK ORDER DETAIL -> mínimo 650
        # --------------------------------------------------

        detail_target = 650
        current_details = WorkOrderDetail.objects.count()

        for i in range(current_details + 1, detail_target + 1):
            WorkOrderDetail.objects.create(
                work_order=random.choice(work_orders),
                activity=f'Actividad API {i}',
                work_hours=random.randint(1, 8),
                observation='Detalle generado automáticamente para la evaluación.',
            )

        # --------------------------------------------------
        # MAINTENANCE EVIDENCE -> mínimo 60
        # --------------------------------------------------

        evidence_target = 60
        current_evidences = MaintenanceEvidence.objects.count()

        for i in range(current_evidences + 1, evidence_target + 1):
            MaintenanceEvidence.objects.create(
                work_order=random.choice(work_orders),
                description=f'Evidencia API {i}',
            )

        # --------------------------------------------------
        # RESUMEN
        # --------------------------------------------------

        counts = {
            'Company': Company.objects.count(),
            'Area': Area.objects.count(),
            'Equipment': Equipment.objects.count(),
            'WorkOrder': WorkOrder.objects.count(),
            'WorkOrderDetail': WorkOrderDetail.objects.count(),
            'MaintenanceEvidence': MaintenanceEvidence.objects.count(),
        }

        total = sum(counts.values())

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Carga finalizada.'))
        self.stdout.write(str(counts))
        self.stdout.write(self.style.SUCCESS(f'TOTAL REGISTROS = {total}'))

        if total >= 2000:
            self.stdout.write(
                self.style.SUCCESS(
                    'Requisito de mínimo 2000 registros cumplido.'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    'Aún no se alcanzan los 2000 registros.'
                )
            )