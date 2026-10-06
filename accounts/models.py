from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone


class PasswordResetCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='password_reset_codes'
    )

    code_hash = models.CharField(
        max_length=128
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    used = models.BooleanField(
        default=False
    )

    def set_code(self, code):
        self.code_hash = make_password(code)

    def check_code(self, code):
        return check_password(
            code,
            self.code_hash
        )

    def is_valid(self):
        return (
            not self.used
            and timezone.now() < self.expires_at
        )

    def __str__(self):
        return (
            f'Reset code for '
            f'{self.user.username}'
        )