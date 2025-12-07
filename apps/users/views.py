from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import CustomerSignupForm, ProfileForm
from .models import User


class AccountLoginView(LoginView):
    template_name = "users/login.html"


class AccountLogoutView(LogoutView):
    next_page = reverse_lazy("catalog")


class SignupView(CreateView):
    model = User
    form_class = CustomerSignupForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("catalog")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user
