from django.urls import path
from apps.account.views.registration import registration, verify

app_name = "account"

urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", registration, name="registration"),
    path("verify-email/", verify, name="verify-email"),
]
