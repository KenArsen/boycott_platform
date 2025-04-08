from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.account.forms.profile import UserProfileForm


@login_required
def profile_view(request):
    return render(request, "auth/profile.html", {"user": request.user})


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("account:profile")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, "auth/profile_change.html", {"form": form})
