from rest_framework import viewsets

from gestion.models import (
    Area,
    Company,
    Equipment,
    MaintenanceEvidence,
    WorkOrder,
    WorkOrderDetail,
)

from .permissions import IsApiRoleAllowed
from .serializers import (
    AreaSerializer,
    CompanySerializer,
    EquipmentSerializer,
    MaintenanceEvidenceSerializer,
    WorkOrderDetailSerializer,
    WorkOrderSerializer,
)


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [
        IsApiRoleAllowed,
    ]

    def get_queryset(self):
        return Company.objects.filter(
            active=True
        ).order_by(
            'id'
        )

    def perform_destroy(self, instance):
        instance.active = False
        instance.save(
            update_fields=[
                'active'
            ]
        )


class AreaViewSet(viewsets.ModelViewSet):
    serializer_class = AreaSerializer
    permission_classes = [
        IsApiRoleAllowed,
    ]

    def get_queryset(self):
        return Area.objects.filter(
            active=True
        ).select_related(
            'company'
        ).order_by(
            'id'
        )

    def perform_destroy(self, instance):
        instance.active = False
        instance.save(
            update_fields=[
                'active'
            ]
        )


class EquipmentViewSet(viewsets.ModelViewSet):
    serializer_class = EquipmentSerializer
    permission_classes = [
        IsApiRoleAllowed,
    ]

    def get_queryset(self):
        return Equipment.objects.filter(
            deleted_at__isnull=True
        ).select_related(
            'equipment_type',
            'area',
        ).order_by(
            'id'
        )

    def perform_destroy(self, instance):
        from django.utils import timezone

        instance.deleted_at = timezone.now()

        instance.save(
            update_fields=[
                'deleted_at'
            ]
        )


class WorkOrderViewSet(viewsets.ModelViewSet):
    serializer_class = WorkOrderSerializer
    permission_classes = [
        IsApiRoleAllowed,
    ]

    def get_queryset(self):
        return WorkOrder.objects.filter(
            deleted_at__isnull=True
        ).select_related(
            'equipment',
            'status',
            'priority',
            'maintenance_type',
            'owner',
        ).order_by(
            'id'
        )

    def perform_destroy(self, instance):
        from django.utils import timezone

        instance.deleted_at = timezone.now()

        instance.save(
            update_fields=[
                'deleted_at'
            ]
        )


class WorkOrderDetailViewSet(
    viewsets.ReadOnlyModelViewSet
):
    serializer_class = WorkOrderDetailSerializer
    permission_classes = [
        IsApiRoleAllowed,
    ]

    def get_queryset(self):
        return WorkOrderDetail.objects.filter(
            deleted_at__isnull=True
        ).select_related(
            'work_order'
        ).order_by(
            'id'
        )


class MaintenanceEvidenceViewSet(
    viewsets.ReadOnlyModelViewSet
):
    serializer_class = MaintenanceEvidenceSerializer
    permission_classes = [
        IsApiRoleAllowed,
    ]

    def get_queryset(self):
        return MaintenanceEvidence.objects.filter(
            deleted_at__isnull=True
        ).select_related(
            'work_order'
        ).order_by(
            'id'
        )