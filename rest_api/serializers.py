from rest_framework import serializers

from gestion.models import (
    Area,
    Company,
    Equipment,
    MaintenanceEvidence,
    WorkOrder,
    WorkOrderDetail,
)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company

        fields = [
            'id',
            'name',
            'rut',
            'address',
            'phone',
            'active',
        ]


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area

        fields = [
            'id',
            'name',
            'company',
            'active',
        ]


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment

        fields = [
            'id',
            'code',
            'name',
            'equipment_type',
            'area',
            'brand',
            'model',
            'serial_number',
            'acquisition_date',
            'active',
            'deleted_at',
        ]

        read_only_fields = [
            'deleted_at',
        ]

    def validate_code(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                'El código del equipo debe tener al menos 3 caracteres.'
            )

        return value


class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder

        fields = [
            'id',
            'number',
            'equipment',
            'status',
            'priority',
            'maintenance_type',
            'owner',
            'description',
            'start_date',
            'end_date',
            'responsible',
            'observations',
            'deleted_at',
        ]

        read_only_fields = [
            'deleted_at',
        ]

    def validate(self, data):
        start_date = data.get(
            'start_date',
            getattr(
                self.instance,
                'start_date',
                None
            )
        )

        end_date = data.get(
            'end_date',
            getattr(
                self.instance,
                'end_date',
                None
            )
        )

        if (
            start_date
            and end_date
            and end_date < start_date
        ):
            raise serializers.ValidationError(
                {
                    'end_date': (
                        'La fecha de término no puede '
                        'ser anterior a la fecha de inicio.'
                    )
                }
            )

        return data


class WorkOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderDetail

        fields = [
            'id',
            'work_order',
            'activity',
            'work_hours',
            'observation',
            'deleted_at',
        ]

        read_only_fields = [
            'deleted_at',
        ]


class MaintenanceEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceEvidence

        fields = [
            'id',
            'work_order',
            'description',
            'file',
            'uploaded_at',
            'deleted_at',
        ]

        read_only_fields = [
            'uploaded_at',
            'deleted_at',
        ]