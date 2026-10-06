from django.contrib import admin
from .models import (
    Company,
    Area,
    EquipmentType,
    WorkOrderStatus,
    Priority,
    MaintenanceType,
    Equipment,
    WorkOrder,
    WorkOrderDetail,
    MaintenanceEvidence,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'rut', 'phone', 'active')
    search_fields = ('name', 'rut')
    list_filter = ('active',)
    ordering = ('name',)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'active')
    search_fields = ('name', 'company__name')
    list_filter = ('company', 'active')
    ordering = ('name',)
    list_select_related = ('company',)

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    search_fields = ('name',)
    list_filter = ('active',)
    ordering = ('name',)


@admin.register(WorkOrderStatus)
class WorkOrderStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    search_fields = ('name',)
    list_filter = ('active',)
    ordering = ('name',)


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'active')
    search_fields = ('name',)
    list_filter = ('active',)
    ordering = ('level',)


@admin.register(MaintenanceType)
class MaintenanceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    search_fields = ('name',)
    list_filter = ('active',)
    ordering = ('name',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'equipment_type',
        'area',
        'brand',
        'active',
        'deleted_at',
    )

    search_fields = (
        'code',
        'name',
        'brand',
        'model',
        'serial_number',
        'area__name',
        'equipment_type__name',
    )

    list_filter = (
        'equipment_type',
        'area',
        'active',
    )

    ordering = ('code',)

    list_select_related = (
        'equipment_type',
        'area',
    )


class WorkOrderDetailInline(admin.TabularInline):
    model = WorkOrderDetail
    extra = 1


class MaintenanceEvidenceInline(admin.TabularInline):
    model = MaintenanceEvidence
    extra = 1


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    inlines = [
        WorkOrderDetailInline,
        MaintenanceEvidenceInline,
    ]

    list_display = (
        'number',
        'equipment',
        'status',
        'priority',
        'maintenance_type',
        'owner',
        'start_date',
        'end_date',
        'responsible',
        'deleted_at',
    )

    search_fields = (
        'number',
        'equipment__code',
        'equipment__name',
        'responsible',
        'description',
    )

    list_filter = (
        'status',
        'priority',
        'maintenance_type',
        'start_date',
    )

    ordering = ('-start_date',)

    list_select_related = (
        'equipment',
        'status',
        'priority',
        'maintenance_type',
        'owner',
    )


@admin.register(WorkOrderDetail)
class WorkOrderDetailAdmin(admin.ModelAdmin):
    list_display = (
        'work_order',
        'activity',
        'work_hours',
        'deleted_at',
    )

    search_fields = (
        'work_order__number',
        'activity',
    )

    list_filter = (
        'deleted_at',
    )

    list_select_related = (
        'work_order',
    )


@admin.register(MaintenanceEvidence)
class MaintenanceEvidenceAdmin(admin.ModelAdmin):
    list_display = (
        'work_order',
        'description',
        'uploaded_at',
        'deleted_at',
    )

    search_fields = (
        'work_order__number',
        'description',
    )

    list_filter = (
        'uploaded_at',
        'deleted_at',
    )

    list_select_related = (
        'work_order',
    )