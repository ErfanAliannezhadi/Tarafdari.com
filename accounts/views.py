from django import forms
from django.db.models import F
from django.views.generic.base import ContextMixin
from utils import UnauthenticatedRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView, DetailView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, \
    PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from .models import UserModel, FollowModel, EmojiPackageModel, BlockModel, FollowRequestModel, OTPCodeModel
from .forms import UserRegisterForm, UserLoginForm, UserPasswordConfirmForm, UserChangePasswordForm, \
    UserProfileEditForm, UserPhoneVerifyForm


class UserLoginView(UnauthenticatedRequiredMixin, LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = UserLoginForm


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('accounts:login')


class UserRegisterView(UnauthenticatedRequiredMixin, SuccessMessageMixin, CreateView):
    model = UserModel
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_message = 'شما با موفقیت ثبت نام کردید'
    success_url = reverse_lazy('accounts:login')


class UserPasswordResetView(UnauthenticatedRequiredMixin, SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    html_email_template_name = 'accounts/password_reset_email.html'
    success_message = 'ایمیل با موفقیت برای شما ارسال شد'
    success_url = reverse_lazy('accounts:login')


class UserPasswordConfirmView(UnauthenticatedRequiredMixin, SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_message = 'رمز عبور شما با موفقیت تغییر کرد'
    success_url = reverse_lazy('accounts:login')
    form_class = UserPasswordConfirmForm


class ProfileContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context.get('user') is None:
            context['user'] = self.request.user
        context['is_owner'] = (self.request.user == context['user'])
        context['is_followed'] = FollowModel.objects.filter(from_user=self.request.user,
                                                            to_user=context['user']).exists()
        context['is_follow_requested'] = FollowRequestModel.objects.filter(from_user=self.request.user,
                                                                           to_user=context['user']).exists()
        context['does_selected_emoji'] = context['user'].packs.get(from_user=self.request.user, to_user=context['user'])
        context['followers'] = context['user'].followers.order_by('last_online')[:8]
        context['followings'] = context['user'].followings.order_by('last_online')[:8]
        context['followers_count'] = context['user'].followers.count()
        context['followings_count'] = context['user'].followings.count()
        return context


class UserProfileView(ProfileContextMixin, LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'
    model = UserModel
    context_object_name = 'user'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if kwargs.get('pk') is None:
            return redirect('accounts:profile', pk=request.user.pk)
        user = UserModel.objects.get(pk=kwargs['pk'])
        if BlockModel.objects.filter(from_user=request.user, to_user=user).exists():
            messages.error(request, 'شما نمیتوانید وارد این صفحه شوید. شما این کاربر را مسدود کرده اید.')
            return redirect('accounts:profile_without_pk')
        if BlockModel.objects.filter(from_user=user, to_user=request.user).exists():
            messages.error(request, 'شما نمیتوانید وارد این صفحه شوید. این کاربر شما را مسدود کرده است.')
            return redirect('accounts:profile_without_pk')
        return super().dispatch(request, *args, **kwargs)


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs['pk'])
        if FollowModel.objects.filter(from_user=request.user, to_user=user).exists():
            return JsonResponse({
                'response': 'it was followed'
            })
        if user.is_private:
            if FollowRequestModel.objects.filter(from_user=request.user, to_user=user).exists():
                return JsonResponse({
                    'response': 'it was follow requested'
                })
            else:
                FollowRequestModel.objects.create(from_user=request.user, to_user=user)
                return JsonResponse({
                    'response': 'it is follow requested'
                })
        FollowModel.objects.create(from_user=request.user, to_user=user)
        return JsonResponse({
            'response': 'it is followed'
        })


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs['pk'])
        if not FollowModel.objects.filter(from_user=request.user, to_user=user).exists() \
                and not FollowRequestModel.objects.filter(from_user=request.user, to_user=user).exists():
            return JsonResponse({
                'response': 'it was not followed'
            })
        if user.is_private:
            if FollowRequestModel.objects.filter(from_user=request.user, to_user=user).exists():
                FollowRequestModel.objects.get(from_user=request.user, to_user=user).delete()
                return JsonResponse({
                    'response': 'it is unfollow requested'
                })
            elif FollowModel.objects.filter(from_user=request.user, to_user=user).exists():
                FollowModel.objects.filter(from_user=request.user, to_user=user).delete()
                return JsonResponse({
                    'response': 'it is unfollowed'
                })
            else:
                return JsonResponse({
                    'response': 'it was not follow requested'
                })

        FollowModel.objects.get(from_user=request.user, to_user=user).delete()
        return JsonResponse({
            'response': 'it is unfollowed'
        })


class UserEmojiPackageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        emoji_package = EmojiPackageModel.objects.get(from_user=request.user,
                                                      to_user=UserModel.objects.get(pk=kwargs['pk']))
        emoji_request = request.GET.get('emoji')
        match emoji_request:
            case 'heart':
                emoji_package.reverse_heart_emoji()
                return JsonResponse({'response': 'done'})
            case 'trophy':
                emoji_package.reverse_trophy_emoji()
                return JsonResponse({'response': 'done'})
            case 'passion':
                emoji_package.reverse_passion_emoji()
                return JsonResponse({'response': 'done'})
            case _:
                return JsonResponse({'response': 'error'})


class UserProfileEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'accounts/edit_profile.html'
    success_message = 'اطلاعات شما با موفقیت تغییر کرد'
    form_class = UserProfileEditForm

    def get_object(self, queryset=None):
        return self.request.user


class UserChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_message = 'رمز عبور شما با موفقیت تغییر کرد'
    form_class = UserChangePasswordForm


class UserFollowRequestsView(LoginRequiredMixin, ProfileContextMixin, ListView):
    template_name = 'accounts/follow_requests.html'
    context_object_name = 'follower_requests'

    def get_queryset(self):
        return self.request.user.followers_request.all()


class UserFollowRequestDecisionView(View):
    def get(self, request, *args, **kwargs):
        follow_request = FollowRequestModel.objects.get(from_user=UserModel.objects.get(pk=kwargs['pk']),
                                                        to_user=request.user)
        decision = request.GET.get('decision')
        match decision:
            case 'accept':
                follow_request.accept()
            case 'reject':
                follow_request.reject()
        return redirect('accounts:follow_requests')


class UserBlockReportView(LoginRequiredMixin, ProfileContextMixin, ListView):
    template_name = 'accounts/block_report.html'
    context_object_name = 'blocked_users'

    def get_queryset(self):
        queryset = self.request.user.blocked_by.all()
        return queryset


class UserBlockReportDeleteView(LoginRequiredMixin, ProfileContextMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy('accounts:block-report')
    success_message = 'شما این کاربر را آنبلاک کرده اید'

    def get_object(self, queryset=None):
        return BlockModel.objects.get(from_user=self.request.user, to_user=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class UserPhoneVerifyView(LoginRequiredMixin,ProfileContextMixin, FormView):
    template_name = 'accounts/phone_verify.html'

    form_class = UserPhoneVerifyForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_phone_verified:
            messages.success(request, 'شماره تلفن شما تایید شده است')
            return redirect('accounts:profile_without_pk')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        code = form.cleaned_data['otp_code']
        code_instance = OTPCodeModel.objects.get(user=user).code
        if code == code_instance:
            user.is_phone_verified = True
            messages.success(self.request, 'شماره تلفن شما با موفقیت تایید شد')
            return redirect('accounts:profile_without_pk')
        messages.error(self.request, 'کد وارد شده نادرست میباشد')
        return redirect('accounts:phone_verify')

    def form_invalid(self, form):
        pass
