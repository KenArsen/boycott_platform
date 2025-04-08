from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.account.forms.authentication import LoginForm


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Аутентификация пользователя
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_email_verified:
                    login(request, user)
                    messages.success(request, "Вы успешно вошли в систему.")
                    return redirect("home")
                else:
                    messages.error(request, "Пожалуйста, подтвердите ваш email перед входом.")
            else:
                messages.error(request, "Неверный email или пароль.")
    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect("account:login")
