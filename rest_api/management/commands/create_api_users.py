import os

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Crea grupos y usuarios normales para probar la API REST.'

    def handle(self, *args, **options):
        admin_password = os.getenv('API_ADMIN_PASSWORD')
        operator_password = os.getenv('API_OPERATOR_PASSWORD')
        no_role_password = os.getenv('API_NO_ROLE_PASSWORD')

        if not admin_password:
            raise CommandError('Falta API_ADMIN_PASSWORD en el archivo .env')

        if not operator_password:
            raise CommandError('Falta API_OPERATOR_PASSWORD en el archivo .env')

        if not no_role_password:
            raise CommandError('Falta API_NO_ROLE_PASSWORD en el archivo .env')

        admin_group, _ = Group.objects.get_or_create(
            name='API Administrators'
        )

        operator_group, _ = Group.objects.get_or_create(
            name='API Operators'
        )

        users_data = [
            {
                'username': 'api_admin',
                'email': 'api_admin@example.com',
                'password': admin_password,
                'group': admin_group,
            },
            {
                'username': 'api_operator',
                'email': 'api_operator@example.com',
                'password': operator_password,
                'group': operator_group,
            },
            {
                'username': 'api_no_role',
                'email': 'api_no_role@example.com',
                'password': no_role_password,
                'group': None,
            },
        ]

        for data in users_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email']
                },
            )

            user.email = data['email']
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.set_password(data['password'])
            user.save()

            user.groups.clear()

            if data['group']:
                user.groups.add(data['group'])

            status = 'creado' if created else 'actualizado'

            self.stdout.write(
                self.style.SUCCESS(
                    f"{data['username']} {status} correctamente."
                )
            )

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS('Usuarios API listos.')
        )
        self.stdout.write('api_admin -> API Administrators')
        self.stdout.write('api_operator -> API Operators')
        self.stdout.write('api_no_role -> sin grupo API')