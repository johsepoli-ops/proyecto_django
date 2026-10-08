from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    AreaViewSet,
    CompanyViewSet,
    EquipmentViewSet,
    MaintenanceEvidenceViewSet,
    WorkOrderDetailViewSet,
    WorkOrderViewSet,
)


router = DefaultRouter()

router.register(
    r'companies',
    CompanyViewSet,
    basename='company'
)

router.register(
    r'areas',
    AreaViewSet,
    basename='area'
)

router.register(
    r'equipment',
    EquipmentViewSet,
    basename='equipment'
)

router.register(
    r'work-orders',
    WorkOrderViewSet,
    basename='work-order'
)

router.register(
    r'work-order-details',
    WorkOrderDetailViewSet,
    basename='work-order-detail'
)

router.register(
    r'maintenance-evidences',
    MaintenanceEvidenceViewSet,
    basename='maintenance-evidence'
)


urlpatterns = [
    path(
        '',
        include(router.urls)
    ),

    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]