from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.paginator import Paginator
from openpyxl import Workbook
from django.http import HttpResponse

from .forms import (
    CompanyForm,
    EquipmentForm,
    MaintenanceEvidenceForm,
    WorkOrderForm,
)

from .models import (
    Company,
    Equipment,
    MaintenanceEvidence,
    WorkOrder,
)


# =========================================================
# SCOPING WORK ORDERS
# =========================================================
def get_workorders_for_user(user):
    queryset = WorkOrder.objects.filter(
        deleted_at__isnull=True
    )

    if user.is_superuser:
        return queryset

    return queryset.filter(
        owner=user
    )


# =========================================================
# SCOPING EQUIPMENT
# =========================================================
def get_equipment_for_user(user):
    return Equipment.objects.filter(
        deleted_at__isnull=True
    )


# =========================================================
# SCOPING MAINTENANCE EVIDENCE
# =========================================================
def get_evidence_for_user(user):
    queryset = MaintenanceEvidence.objects.filter(
        deleted_at__isnull=True
    )

    if user.is_superuser:
        return queryset

    return queryset.filter(
        work_order__owner=user
    )


# =========================================================
# DASHBOARD
# =========================================================
@login_required
def dashboard(request):
    work_orders = get_workorders_for_user(
        request.user
    )

    context = {
        'work_orders': work_orders,
        'total_work_orders': work_orders.count(),
    }

    return render(
        request,
        'gestion/dashboard.html',
        context
    )


# =========================================================
# WORK ORDER - LISTAR
# =========================================================
@login_required
def workorder_list(request):
    if not request.user.has_perm(
        'gestion.view_workorder'
    ):
        raise PermissionDenied

    work_orders = get_workorders_for_user(
        request.user
    ).select_related(
        'equipment',
        'status',
        'priority',
        'maintenance_type',
        'owner',
    ).order_by(
        'id'
    )

    # =====================================================
    # PAGINACIÓN 5 / 15 / 30 USANDO SESIÓN
    # =====================================================
    allowed_per_page = [
        5,
        15,
        30,
    ]

    if 'per_page' in request.GET:
        try:
            per_page = int(
                request.GET.get(
                    'per_page'
                )
            )

            if per_page not in allowed_per_page:
                per_page = 15

        except (
            TypeError,
            ValueError
        ):
            per_page = 15

        request.session[
            'workorder_per_page'
        ] = per_page

    else:
        per_page = request.session.get(
            'workorder_per_page',
            15
        )

        if per_page not in allowed_per_page:
            per_page = 15

            request.session[
                'workorder_per_page'
            ] = per_page

    paginator = Paginator(
        work_orders,
        per_page
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        'gestion/workorder_list.html',
        {
            'work_orders': page_obj,
            'page_obj': page_obj,
            'per_page': per_page,
            'allowed_per_page': allowed_per_page,
        }
    )


# =========================================================
# WORK ORDER - CREAR
# =========================================================
@login_required
def workorder_create(request):
    if not request.user.has_perm(
        'gestion.add_workorder'
    ):
        raise PermissionDenied

    if request.method == 'POST':
        form = WorkOrderForm(
            request.POST
        )

        if form.is_valid():
            work_order = form.save(
                commit=False
            )

            work_order.owner = request.user
            work_order.save()

            messages.success(
                request,
                'Orden de trabajo creada correctamente.'
            )

            return redirect(
                'gestion:workorder_list'
            )

    else:
        form = WorkOrderForm()

    return render(
        request,
        'gestion/workorder_form.html',
        {
            'form': form,
            'title': 'Crear orden de trabajo',
        }
    )


# =========================================================
# WORK ORDER - EDITAR
# =========================================================
@login_required
def workorder_update(request, pk):
    if not request.user.has_perm(
        'gestion.change_workorder'
    ):
        raise PermissionDenied

    work_order = get_object_or_404(
        get_workorders_for_user(
            request.user
        ),
        pk=pk
    )

    if request.method == 'POST':
        form = WorkOrderForm(
            request.POST,
            instance=work_order
        )

        if form.is_valid():
            updated_order = form.save(
                commit=False
            )

            updated_order.owner = work_order.owner
            updated_order.save()

            messages.success(
                request,
                'Orden de trabajo actualizada correctamente.'
            )

            return redirect(
                'gestion:workorder_list'
            )

    else:
        form = WorkOrderForm(
            instance=work_order
        )

    return render(
        request,
        'gestion/workorder_form.html',
        {
            'form': form,
            'title': 'Editar orden de trabajo',
            'work_order': work_order,
        }
    )


# =========================================================
# WORK ORDER - ELIMINAR LÓGICAMENTE
# =========================================================
@login_required
def workorder_delete(request, pk):
    if not request.user.has_perm(
        'gestion.delete_workorder'
    ):
        raise PermissionDenied

    work_order = get_object_or_404(
        get_workorders_for_user(
            request.user
        ),
        pk=pk
    )

    if request.method != 'POST':
        raise PermissionDenied

    work_order.deleted_at = timezone.now()

    work_order.save(
        update_fields=[
            'deleted_at'
        ]
    )

    messages.success(
        request,
        'Orden de trabajo eliminada correctamente.'
    )

    return redirect(
        'gestion:workorder_list'
    )


# =========================================================
# EQUIPMENT - LISTAR
# =========================================================
@login_required
def equipment_list(request):
    if not request.user.has_perm(
        'gestion.view_equipment'
    ):
        raise PermissionDenied

    equipments = get_equipment_for_user(
        request.user
    ).select_related(
        'equipment_type',
        'area',
    ).order_by(
        'id'
    )

    allowed_per_page = [
        5,
        15,
        30,
    ]

    if 'per_page' in request.GET:
        try:
            per_page = int(
                request.GET.get(
                    'per_page'
                )
            )

            if per_page not in allowed_per_page:
                per_page = 15

        except (
            TypeError,
            ValueError
        ):
            per_page = 15

        request.session[
            'equipment_per_page'
        ] = per_page

    else:
        per_page = request.session.get(
            'equipment_per_page',
            15
        )

        if per_page not in allowed_per_page:
            per_page = 15

            request.session[
                'equipment_per_page'
            ] = per_page

    paginator = Paginator(
        equipments,
        per_page
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        'gestion/equipment_list.html',
        {
            'equipments': page_obj,
            'page_obj': page_obj,
            'per_page': per_page,
            'allowed_per_page': allowed_per_page,
        }
    )


# =========================================================
# EQUIPMENT - CREAR
# =========================================================
@login_required
def equipment_create(request):
    if not request.user.has_perm(
        'gestion.add_equipment'
    ):
        raise PermissionDenied

    if request.method == 'POST':
        form = EquipmentForm(
            request.POST
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Equipo creado correctamente.'
            )

            return redirect(
                'gestion:equipment_list'
            )

    else:
        form = EquipmentForm()

    return render(
        request,
        'gestion/equipment_form.html',
        {
            'form': form,
            'title': 'Crear equipo',
        }
    )


# =========================================================
# EQUIPMENT - EDITAR
# =========================================================
@login_required
def equipment_update(request, pk):
    if not request.user.has_perm(
        'gestion.change_equipment'
    ):
        raise PermissionDenied

    equipment = get_object_or_404(
        get_equipment_for_user(
            request.user
        ),
        pk=pk
    )

    if request.method == 'POST':
        form = EquipmentForm(
            request.POST,
            instance=equipment
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Equipo actualizado correctamente.'
            )

            return redirect(
                'gestion:equipment_list'
            )

    else:
        form = EquipmentForm(
            instance=equipment
        )

    return render(
        request,
        'gestion/equipment_form.html',
        {
            'form': form,
            'title': 'Editar equipo',
            'equipment': equipment,
        }
    )


# =========================================================
# EQUIPMENT - ELIMINAR LÓGICAMENTE
# =========================================================
@login_required
def equipment_delete(request, pk):
    if not request.user.has_perm(
        'gestion.delete_equipment'
    ):
        raise PermissionDenied

    equipment = get_object_or_404(
        get_equipment_for_user(
            request.user
        ),
        pk=pk
    )

    if request.method != 'POST':
        raise PermissionDenied

    equipment.deleted_at = timezone.now()

    equipment.save(
        update_fields=[
            'deleted_at'
        ]
    )

    messages.success(
        request,
        'Equipo eliminado correctamente.'
    )

    return redirect(
        'gestion:equipment_list'
    )


# =========================================================
# COMPANY - LISTAR
# =========================================================
@login_required
def company_list(request):
    if not request.user.has_perm(
        'gestion.view_company'
    ):
        raise PermissionDenied

    companies = Company.objects.filter(
        active=True
    ).order_by(
        'name'
    )

    return render(
        request,
        'gestion/company_list.html',
        {
            'companies': companies,
        }
    )


# =========================================================
# COMPANY - CREAR
# =========================================================
@login_required
def company_create(request):
    if not request.user.has_perm(
        'gestion.add_company'
    ):
        raise PermissionDenied

    if request.method == 'POST':
        form = CompanyForm(
            request.POST
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Empresa creada correctamente.'
            )

            return redirect(
                'gestion:company_list'
            )

    else:
        form = CompanyForm()

    return render(
        request,
        'gestion/company_form.html',
        {
            'form': form,
            'title': 'Crear empresa',
        }
    )


# =========================================================
# COMPANY - EDITAR
# =========================================================
@login_required
def company_update(request, pk):
    if not request.user.has_perm(
        'gestion.change_company'
    ):
        raise PermissionDenied

    company = get_object_or_404(
        Company.objects.filter(
            active=True
        ),
        pk=pk
    )

    if request.method == 'POST':
        form = CompanyForm(
            request.POST,
            instance=company
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Empresa actualizada correctamente.'
            )

            return redirect(
                'gestion:company_list'
            )

    else:
        form = CompanyForm(
            instance=company
        )

    return render(
        request,
        'gestion/company_form.html',
        {
            'form': form,
            'title': 'Editar empresa',
            'company': company,
        }
    )


# =========================================================
# COMPANY - DESACTIVAR
# =========================================================
@login_required
def company_delete(request, pk):
    if not request.user.has_perm(
        'gestion.delete_company'
    ):
        raise PermissionDenied

    company = get_object_or_404(
        Company,
        pk=pk
    )

    if request.method != 'POST':
        raise PermissionDenied

    company.active = False

    company.save(
        update_fields=[
            'active'
        ]
    )

    messages.success(
        request,
        'Empresa desactivada correctamente.'
    )

    return redirect(
        'gestion:company_list'
    )


# =========================================================
# MAINTENANCE EVIDENCE - LISTAR
# =========================================================
@login_required
def evidence_list(request):
    if not request.user.has_perm(
        'gestion.view_maintenanceevidence'
    ):
        raise PermissionDenied

    evidences = get_evidence_for_user(
        request.user
    ).select_related(
        'work_order',
        'work_order__equipment',
        'work_order__owner',
    ).order_by(
        '-uploaded_at'
    )

    allowed_per_page = [
        5,
        15,
        30,
    ]

    if 'per_page' in request.GET:
        try:
            per_page = int(
                request.GET.get(
                    'per_page'
                )
            )

            if per_page not in allowed_per_page:
                per_page = 15

        except (
            TypeError,
            ValueError
        ):
            per_page = 15

        request.session[
            'evidence_per_page'
        ] = per_page

    else:
        per_page = request.session.get(
            'evidence_per_page',
            15
        )

        if per_page not in allowed_per_page:
            per_page = 15

            request.session[
                'evidence_per_page'
            ] = per_page

    paginator = Paginator(
        evidences,
        per_page
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        'gestion/evidence_list.html',
        {
            'evidences': page_obj,
            'page_obj': page_obj,
            'per_page': per_page,
            'allowed_per_page': allowed_per_page,
        }
    )


# =========================================================
# MAINTENANCE EVIDENCE - CREAR
# =========================================================
@login_required
def evidence_create(request):
    if not request.user.has_perm(
        'gestion.add_maintenanceevidence'
    ):
        raise PermissionDenied

    if request.method == 'POST':
        form = MaintenanceEvidenceForm(
            request.POST,
            request.FILES
        )

    else:
        form = MaintenanceEvidenceForm()

    # Solo permite seleccionar órdenes
    # accesibles para el usuario actual.
    form.fields[
        'work_order'
    ].queryset = get_workorders_for_user(
        request.user
    )

    if (
        request.method == 'POST'
        and form.is_valid()
    ):
        form.save()

        messages.success(
            request,
            'Evidencia creada correctamente.'
        )

        return redirect(
            'gestion:evidence_list'
        )

    return render(
        request,
        'gestion/evidence_form.html',
        {
            'form': form,
            'title': 'Agregar evidencia',
        }
    )


# =========================================================
# MAINTENANCE EVIDENCE - EDITAR
# =========================================================
@login_required
def evidence_update(request, pk):
    if not request.user.has_perm(
        'gestion.change_maintenanceevidence'
    ):
        raise PermissionDenied

    evidence = get_object_or_404(
        get_evidence_for_user(
            request.user
        ),
        pk=pk
    )

    if request.method == 'POST':
        form = MaintenanceEvidenceForm(
            request.POST,
            request.FILES,
            instance=evidence
        )

    else:
        form = MaintenanceEvidenceForm(
            instance=evidence
        )

    form.fields[
        'work_order'
    ].queryset = get_workorders_for_user(
        request.user
    )

    if (
        request.method == 'POST'
        and form.is_valid()
    ):
        form.save()

        messages.success(
            request,
            'Evidencia actualizada correctamente.'
        )

        return redirect(
            'gestion:evidence_list'
        )

    return render(
        request,
        'gestion/evidence_form.html',
        {
            'form': form,
            'title': 'Editar evidencia',
            'evidence': evidence,
        }
    )


# =========================================================
# MAINTENANCE EVIDENCE - ELIMINAR LÓGICAMENTE
# =========================================================
@login_required
def evidence_delete(request, pk):
    if not request.user.has_perm(
        'gestion.delete_maintenanceevidence'
    ):
        raise PermissionDenied

    evidence = get_object_or_404(
        get_evidence_for_user(
            request.user
        ),
        pk=pk
    )

    if request.method != 'POST':
        raise PermissionDenied

    evidence.deleted_at = timezone.now()

    evidence.save(
        update_fields=[
            'deleted_at'
        ]
    )

    messages.success(
        request,
        'Evidencia eliminada correctamente.'
    )

    return redirect(
        'gestion:evidence_list'
    )
@login_required
def export_workorders_excel(request):
    if not request.user.has_perm(
        'gestion.view_workorder'
    ):
        raise PermissionDenied

    work_orders = get_workorders_for_user(
        request.user
    ).select_related(
        'equipment',
        'status',
        'priority',
        'maintenance_type',
        'owner',
    ).order_by(
        'id'
    )

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = 'Work Orders'

    headers = [
        'Number',
        'Equipment',
        'Status',
        'Priority',
        'Maintenance Type',
        'Description',
        'Start Date',
        'End Date',
        'Responsible',
        'Owner',
    ]

    worksheet.append(
        headers
    )

    for work_order in work_orders:

        worksheet.append(
            [
                work_order.number,
                str(
                    work_order.equipment
                ),
                str(
                    work_order.status
                ),
                str(
                    work_order.priority
                ),
                str(
                    work_order.maintenance_type
                ),
                work_order.description,
                work_order.start_date,
                work_order.end_date,
                work_order.responsible,
                work_order.owner.username,
            ]
        )

    response = HttpResponse(
        content_type=(
            'application/'
            'vnd.openxmlformats-officedocument.'
            'spreadsheetml.sheet'
        )
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; '
        'filename="work_orders.xlsx"'
    )

    workbook.save(
        response
    )

    return response