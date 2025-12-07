from django.urls import path

from .views import AccountLoginView, AccountLogoutView, ProfileUpdateView, SignupView

urlpatterns = [
    path("login/", AccountLoginView.as_view(), name="account_login"),
    path("logout/", AccountLogoutView.as_view(), name="account_logout"),
    path("signup/", SignupView.as_view(), name="account_signup"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
]
