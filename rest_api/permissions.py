from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsApiRoleAllowed(BasePermission):
    """
    Reglas de acceso:
    - api_admin: lectura y escritura.
    - api_operator: solo lectura.
    - api_no_role: sin acceso.
    - usuario sin autenticar: DRF/JWT responderá 401.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        group_names = set(
            user.groups.values_list(
                'name',
                flat=True
            )
        )

        if 'API Administrators' in group_names:
            return True

        if 'API Operators' in group_names:
            return request.method in SAFE_METHODS

        return False