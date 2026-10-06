import secrets
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import PasswordResetCode


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(
            request,
            'Usuario o contraseña incorrectos.'
        )

    return render(
        request,
        'accounts/login.html'
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(
                request,
                'No existe un usuario asociado a ese correo.'
            )
            return render(
                request,
                'accounts/forgot_password.html'
            )

        PasswordResetCode.objects.filter(
            user=user,
            used=False
        ).update(used=True)

        code = f'{secrets.randbelow(1000000):06d}'

        reset_code = PasswordResetCode(
            user=user,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        reset_code.set_code(code)
        reset_code.save()

        request.session['reset_user_id'] = user.id
        request.session['reset_code_id'] = reset_code.id

        messages.success(
            request,
            f'Código generado: {code}'
        )

        return redirect(
            'accounts:verify_reset_code'
        )

    return render(
        request,
        'accounts/forgot_password.html'
    )


def verify_reset_code(request):
    user_id = request.session.get('reset_user_id')
    reset_code_id = request.session.get('reset_code_id')

    if not user_id or not reset_code_id:
        messages.error(
            request,
            'Debes iniciar nuevamente la recuperación.'
        )
        return redirect(
            'accounts:forgot_password'
        )

    try:
        reset_code = PasswordResetCode.objects.get(
            id=reset_code_id,
            user_id=user_id
        )
    except PasswordResetCode.DoesNotExist:
        messages.error(
            request,
            'El código de recuperación no es válido.'
        )
        return redirect(
            'accounts:forgot_password'
        )

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()

        if not code.isdigit() or len(code) != 6:
            messages.error(
                request,
                'El código debe tener exactamente 6 dígitos.'
            )
            return render(
                request,
                'accounts/verify_reset_code.html'
            )

        if not reset_code.is_valid():
            messages.error(
                request,
                'El código está vencido o ya fue utilizado.'
            )
            return redirect(
                'accounts:forgot_password'
            )

        if not reset_code.check_code(code):
            messages.error(
                request,
                'El código ingresado es incorrecto.'
            )
            return render(
                request,
                'accounts/verify_reset_code.html'
            )

        request.session['reset_code_verified'] = True

        return redirect(
            'accounts:reset_password'
        )

    return render(
        request,
        'accounts/verify_reset_code.html'
    )


def reset_password(request):
    user_id = request.session.get('reset_user_id')
    reset_code_id = request.session.get('reset_code_id')
    verified = request.session.get('reset_code_verified')

    if not user_id or not reset_code_id or not verified:
        messages.error(
            request,
            'Debes verificar primero el código de recuperación.'
        )
        return redirect(
            'accounts:forgot_password'
        )

    try:
        user = User.objects.get(id=user_id)

        reset_code = PasswordResetCode.objects.get(
            id=reset_code_id,
            user=user
        )

    except (
        User.DoesNotExist,
        PasswordResetCode.DoesNotExist
    ):
        messages.error(
            request,
            'La recuperación ya no es válida.'
        )
        return redirect(
            'accounts:forgot_password'
        )

    if not reset_code.is_valid():
        messages.error(
            request,
            'El código está vencido o ya fue utilizado.'
        )
        return redirect(
            'accounts:forgot_password'
        )

    if request.method == 'POST':
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if password1 != password2:
            messages.error(
                request,
                'Las contraseñas no coinciden.'
            )
            return render(
                request,
                'accounts/reset_password.html'
            )

        if len(password1) < 10:
            messages.error(
                request,
                'La contraseña debe tener al menos 10 caracteres.'
            )
            return render(
                request,
                'accounts/reset_password.html'
            )

        if not any(char.isupper() for char in password1):
            messages.error(
                request,
                'La contraseña debe contener al menos una mayúscula.'
            )
            return render(
                request,
                'accounts/reset_password.html'
            )

        if not any(char.islower() for char in password1):
            messages.error(
                request,
                'La contraseña debe contener al menos una minúscula.'
            )
            return render(
                request,
                'accounts/reset_password.html'
            )

        if not any(char.isdigit() for char in password1):
            messages.error(
                request,
                'La contraseña debe contener al menos un número.'
            )
            return render(
                request,
                'accounts/reset_password.html'
            )

        if password1.isalnum():
            messages.error(
                request,
                'La contraseña debe contener al menos un carácter especial.'
            )
            return render(
                request,
                'accounts/reset_password.html'
            )

        try:
            validate_password(
                password1,
                user=user
            )
        except ValidationError as error:
            for message in error.messages:
                messages.error(
                    request,
                    message
                )

            return render(
                request,
                'accounts/reset_password.html'
            )

        user.set_password(password1)
        user.save()

        reset_code.used = True
        reset_code.save()

        request.session.pop(
            'reset_user_id',
            None
        )

        request.session.pop(
            'reset_code_id',
            None
        )

        request.session.pop(
            'reset_code_verified',
            None
        )

        messages.success(
            request,
            'Contraseña actualizada correctamente.'
        )

        return redirect(
            'accounts:login'
        )

    return render(
        request,
        'accounts/reset_password.html'
    )