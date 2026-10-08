from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from gestion.views import dashboard


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'accounts/',
        include('accounts.urls')
    ),

    path(
        'api/',
        include('rest_api.urls')
    ),

    path(
        '',
        dashboard,
        name='dashboard'
    ),

    path(
        '',
        include('gestion.urls')
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )