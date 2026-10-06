from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Company(models.Model):
    name = models.CharField(max_length=100)
    rut = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=100)

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name='areas'
    )

    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.company.name}"


class EquipmentType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class WorkOrderStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=50)
    level = models.PositiveIntegerField(unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MaintenanceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.PROTECT,
        related_name='equipments'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name='equipments'
    )
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    acquisition_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class WorkOrder(models.Model):
    number = models.CharField(max_length=30, unique=True)

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.PROTECT,
        related_name='work_orders'
    )

    status = models.ForeignKey(
        WorkOrderStatus,
        on_delete=models.PROTECT,
        related_name='work_orders'
    )

    priority = models.ForeignKey(
        Priority,
        on_delete=models.PROTECT,
        related_name='work_orders'
    )

    maintenance_type = models.ForeignKey(
        MaintenanceType,
        on_delete=models.PROTECT,
        related_name='work_orders'
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='work_orders'
    )

    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    responsible = models.CharField(max_length=100)
    observations = models.TextField(blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError({
                'end_date': 'End date cannot be earlier than start date.'
            })

    def __str__(self):
        return self.number


class WorkOrderDetail(models.Model):
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name='details'
    )
    activity = models.CharField(max_length=200)
    work_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    observation = models.TextField(blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.activity


class MaintenanceEvidence(models.Model):
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name='evidences'
    )
    description = models.CharField(max_length=200)
    file = models.FileField(
        upload_to='maintenance_evidence/',
        null=True,
        blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.description