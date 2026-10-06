from django import forms
from PIL import Image

from .models import (
    Company,
    Equipment,
    MaintenanceEvidence,
    WorkOrder,
)


class WorkOrderForm(forms.ModelForm):

    class Meta:
        model = WorkOrder

        fields = [
            'number',
            'equipment',
            'status',
            'priority',
            'maintenance_type',
            'description',
            'start_date',
            'end_date',
            'responsible',
            'observations',
        ]

        widgets = {
            'start_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
            'end_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 4
                }
            ),
            'observations': forms.Textarea(
                attrs={
                    'rows': 4
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get(
            'start_date'
        )

        end_date = cleaned_data.get(
            'end_date'
        )

        if (
            start_date
            and end_date
            and end_date < start_date
        ):
            self.add_error(
                'end_date',
                (
                    'La fecha de término no puede '
                    'ser anterior a la fecha de inicio.'
                )
            )

        return cleaned_data


class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment

        fields = [
            'code',
            'name',
            'equipment_type',
            'area',
            'brand',
            'model',
            'serial_number',
            'acquisition_date',
            'active',
        ]

        widgets = {
            'acquisition_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
        }


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company

        fields = [
            'name',
            'rut',
            'address',
            'phone',
            'active',
        ]


class MaintenanceEvidenceForm(forms.ModelForm):

    class Meta:
        model = MaintenanceEvidence

        fields = [
            'work_order',
            'description',
            'file',
        ]

    def clean_file(self):
        uploaded_file = self.cleaned_data.get(
            'file'
        )

        if not uploaded_file:
            return uploaded_file

        # Máximo 5 MB
        max_size = 5 * 1024 * 1024

        if uploaded_file.size > max_size:
            raise forms.ValidationError(
                'El archivo no puede superar los 5 MB.'
            )

        allowed_extensions = [
            'jpg',
            'jpeg',
            'png',
        ]

        extension = (
            uploaded_file.name
            .split('.')[-1]
            .lower()
        )

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                'Solo se permiten archivos JPG, JPEG o PNG.'
            )

        try:
            image = Image.open(
                uploaded_file
            )

            image.verify()

        except Exception:
            raise forms.ValidationError(
                'El archivo no contiene una imagen válida.'
            )

        uploaded_file.seek(0)

        return uploaded_file