from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import UserRegisterForm


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        """
        authenticated users can not log in again!
        """
        if request.user.is_authenticated:
            return redirect('accounts:profile')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self):
        """
        We add some labels to django built in Authentication form
        """
        form = super().get_form()
        form.fields['username'].label = 'نام کاربری'
        form.fields['username'].widget.attrs['placeholder'] = 'ایمیل / موبایل'
        form.fields['password'].label = 'رمز عبور'
        return form


class UserLogoutView(LoginRequiredMixin, LogoutView):
    pass


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        """
        authenticated users can not register
        """
        if request.user.is_authenticated:
            return redirect('accounts:profile')
        return super().dispatch(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = 'accounts/profile'
