from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Area(models.Model):
    nombre = models.CharField(max_length=100)
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='areas'
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.empresa.nombre}"


class TipoEquipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class EstadoOrden(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)

    tipo_equipo = models.ForeignKey(
        TipoEquipo,
        on_delete=models.PROTECT,
        related_name='equipos'
    )

    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name='equipos'
    )

    marca = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    numero_serie = models.CharField(max_length=100, blank=True)

    fecha_adquisicion = models.DateField(
        null=True,
        blank=True
    )

    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class OrdenTrabajo(models.Model):

    PRIORIDADES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]

    numero_orden = models.CharField(
        max_length=30,
        unique=True
    )

    propietario = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    related_name='ordenes_trabajo',
    null=True,
    blank=True
    )

    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.PROTECT,
        related_name='ordenes'
    )

    estado = models.ForeignKey(
        EstadoOrden,
        on_delete=models.PROTECT,
        related_name='ordenes'
    )

    descripcion = models.TextField()

    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDADES,
        default='MEDIA'
    )

    fecha_inicio = models.DateField()

    fecha_termino = models.DateField(
        null=True,
        blank=True
    )

    responsable = models.CharField(
        max_length=100
    )

    observaciones = models.TextField(
        blank=True
    )

    def clean(self):
        if (
            self.fecha_termino
            and self.fecha_inicio
            and self.fecha_termino < self.fecha_inicio
        ):
            raise ValidationError(
                {
                    'fecha_termino':
                    'La fecha de término no puede ser anterior a la fecha de inicio.'
                }
            )

    def __str__(self):
        return self.numero_orden

class DetalleOrden(models.Model):
    orden = models.ForeignKey(
        OrdenTrabajo,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    actividad = models.CharField(max_length=200)

    horas_trabajo = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    observacion = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.actividad