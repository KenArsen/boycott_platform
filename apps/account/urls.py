from django.urls import path

from apps.account.views.authentication import login_view, logout_view
from apps.account.views.password import (
    CustomPasswordChangeView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
)
from apps.account.views.profile import profile_edit, profile_view
from apps.account.views.registration import registration, verify

app_name = "account"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile-edit/", profile_edit, name="profile-edit"),
    path("register/", registration, name="register"),
    path("verify-email/", verify, name="verify-email"),
]

urlpatterns += [
    path("password-change/", CustomPasswordChangeView.as_view(), name="password-change"),
    path("password-reset/", CustomPasswordResetView.as_view(), name="password-reset"),
    path("password-reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password-reset-confirm"),
]
