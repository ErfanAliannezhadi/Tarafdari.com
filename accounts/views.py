from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import UserRegisterForm


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('accounts:profile')

    def dispatch(self, request, *args, **kwargs):
        """
        authenticated users can not log in again!
        """
        if request.user.is_authenticated:
            return redirect('accounts:profile', pk=request.user.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_form(self):
        """
        We add some labels and error messages to django built in Authentication form
        """
        form = super().get_form()
        form.fields['username'].label = 'نام کاربری'
        form.fields['username'].error_messages['required'] = 'نام کاربری اجباری است'
        form.fields['username'].widget.attrs['placeholder'] = 'ایمیل / موبایل'
        form.fields['password'].label = 'رمز عبور'
        form.fields['password'].error_messages['required'] = 'رمز عبور اجباری است'
        form.error_messages = {
            'invalid_login': 'رمز عبور یا ایمیل نامعتبر است',
            'inactive': 'این حساب غیرفعال شده است'
        }
        return form


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('accounts:login')


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        """
        authenticated users can not register
        """
        if request.user.is_authenticated:
            return redirect('accounts:profile', pk=request.user.pk)
        return super().dispatch(request, *args, **kwargs)


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts./password_reset.html'


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = 'accounts/profile.html'
