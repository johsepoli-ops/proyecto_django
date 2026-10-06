from django.urls import path

from . import views


app_name = 'gestion'


urlpatterns = [
    # =====================================================
    # WORK ORDERS
    # =====================================================
    path(
        'orders/',
        views.workorder_list,
        name='workorder_list'
    ),

    path(
        'orders/export/excel/',
        views.export_workorders_excel,
        name='export_workorders_excel'
    ),

    path(
        'orders/new/',
        views.workorder_create,
        name='workorder_create'
    ),

    path(
        'orders/<int:pk>/edit/',
        views.workorder_update,
        name='workorder_update'
    ),

    path(
        'orders/<int:pk>/delete/',
        views.workorder_delete,
        name='workorder_delete'
    ),

    # =====================================================
    # EQUIPMENT
    # =====================================================
    path(
        'equipment/',
        views.equipment_list,
        name='equipment_list'
    ),

    path(
        'equipment/new/',
        views.equipment_create,
        name='equipment_create'
    ),

    path(
        'equipment/<int:pk>/edit/',
        views.equipment_update,
        name='equipment_update'
    ),

    path(
        'equipment/<int:pk>/delete/',
        views.equipment_delete,
        name='equipment_delete'
    ),

    # =====================================================
    # COMPANY
    # =====================================================
    path(
        'companies/',
        views.company_list,
        name='company_list'
    ),

    path(
        'companies/new/',
        views.company_create,
        name='company_create'
    ),

    path(
        'companies/<int:pk>/edit/',
        views.company_update,
        name='company_update'
    ),

    path(
        'companies/<int:pk>/delete/',
        views.company_delete,
        name='company_delete'
    ),

    # =====================================================
    # MAINTENANCE EVIDENCE
    # =====================================================
    path(
        'evidences/',
        views.evidence_list,
        name='evidence_list'
    ),

    path(
        'evidences/new/',
        views.evidence_create,
        name='evidence_create'
    ),

    path(
        'evidences/<int:pk>/edit/',
        views.evidence_update,
        name='evidence_update'
    ),

    path(
        'evidences/<int:pk>/delete/',
        views.evidence_delete,
        name='evidence_delete'
    ),
]