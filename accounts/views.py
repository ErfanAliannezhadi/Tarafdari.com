from django import forms
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, View
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, \
    PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from .models import UserModel, FollowModel
from .forms import UserRegisterForm


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('accounts:profile')

    def dispatch(self, request, *args, **kwargs):
        """
        authenticated users can not log in again!
        """
        if request.user.is_authenticated:
            messages.warning(request, 'برای ورود ابتدا باید از این حساب خروج کنید')
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


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = UserModel
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_message = 'شما با موفقیت ثبت نام کردید'

    def dispatch(self, request, *args, **kwargs):
        """
        authenticated users can not register
        """
        if request.user.is_authenticated:
            messages.warning(request, 'برای ثبت نام ابتدا باید از این حساب خارج شوید')
            return redirect('accounts:profile', pk=request.user.pk)
        return super().dispatch(request, *args, **kwargs)


class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    html_email_template_name = 'accounts/password_reset_email.html'
    success_message = 'ایمیل با موفقیت برای شما ارسال شد'
    success_url = reverse_lazy('accounts:login')


class UserPasswordConfirm(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_message = 'رمز عبور شما با موفقیت تغییر کرد'
    success_url = reverse_lazy('accounts:login')

    def get_form(self, form_class=None):
        """
        add some label to password reset form
        """
        form = super().get_form()
        form.fields['new_password1'].label = 'رمزعبور جدید'
        form.fields['new_password2'].label = 'تایید رمزعبور جدید'
        return form


class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'
    model = UserModel
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['is_owner'] = (self.request.user == context['user'])
        context['is_followed'] = False
        if FollowModel.objects.filter(from_user=self.request.user, to_user=context['user']).exists():
            context['is_followed'] = True
        return context


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs['pk'])
        if FollowModel.objects.filter(from_user=request.user, to_user=user).exists():
            print('=' * 100)
            return JsonResponse({
                'response': 'it was followed'
            })
        FollowModel.objects.create(from_user=request.user, to_user=user)
        return JsonResponse({
            'response': 'it is followed'
        })


class UserUnfollowView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs['pk'])
        if not FollowModel.objects.filter(from_user=request.user, to_user=user).exists():
            return JsonResponse({
                'response': 'it was not followed'
            })
        FollowModel.objects.get(from_user=request.user, to_user=user).delete()
        return JsonResponse({
            'response': 'it is unfollowed'
        })


class UserProfileEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'accounts/edit_profile.html'
    model = UserModel
    fields = ['first_name', 'last_name', 'profile_image', 'cover_image', 'background_image', 'is_private', 'about_me',
              'email']
    success_message = 'اطلاعات شما با موفقیت تغییر کرد'

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        form.fields['profile_image'].widget = forms.FileInput()
        return form


class UserChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_message = 'رمز عبور شما با موفقیت تغییر کرد'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        form.fields['old_password'].label = 'رمز عبور فعلی'
        form.fields['new_password1'].label = 'رمز عبور جدید'
        form.fields['new_password2'].label = 'تایید رمز عبور جدید'
        return form
