from random import randint
from utils import UnauthenticatedRequiredMixin, ProfileContextMixin, UnBlockedRequiredMixin, \
    PublicUserProfileRequiredMixin, PrivateUserProfileRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, \
    PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import UserModel, FollowModel, EmojiPackageModel, BlockModel, FollowRequestModel, OTPCodeModel
from .forms import UserRegisterForm, UserLoginForm, UserPasswordConfirmForm, UserChangePasswordForm, \
    UserProfileEditForm, UserPhoneVerifyForm, UserBlockReportForm


class UserLoginView(UnauthenticatedRequiredMixin, LoginView):
    """A view for handling user login functionality."""

    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = UserLoginForm


class UserLogoutView(LoginRequiredMixin, LogoutView):
    """A view for handling user logout functionality."""

    next_page = reverse_lazy('accounts:login')


class UserRegisterView(UnauthenticatedRequiredMixin, SuccessMessageMixin, CreateView):
    """A view for handling user registration functionality."""

    model = UserModel
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_message = 'شما با موفقیت ثبت نام کردید'
    success_url = reverse_lazy('accounts:login')


class UserPasswordResetView(UnauthenticatedRequiredMixin, SuccessMessageMixin, PasswordResetView):
    """A view for handling user password reset functionality."""

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


class UserProfileView(ProfileContextMixin, LoginRequiredMixin, UnBlockedRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'
    model = UserModel
    context_object_name = 'user'

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk') is None:
            return redirect('accounts:profile', pk=request.user.pk)
        return super().dispatch(request, *args, **kwargs)


class UserFollowView(LoginRequiredMixin, UnBlockedRequiredMixin, PublicUserProfileRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs['pk'])
        FollowModel.objects.update_or_create(from_user=request.user, to_user=user)
        return redirect('accounts:profile', pk=kwargs['pk'])


class UserUnfollowView(LoginRequiredMixin, UnBlockedRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        FollowModel.objects.get(from_user=self.request.user, to_user=kwargs['pk']).delete()
        return redirect('accounts:profile', pk=kwargs['pk'])


class UserFollowRequestView(LoginRequiredMixin, UnBlockedRequiredMixin, PrivateUserProfileRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs['pk'])
        FollowRequestModel.objects.update_or_create(from_user=request.user, to_user=user)
        return redirect('accounts:profile', pk=kwargs['pk'])


class UserUnfollowRequestView(LoginRequiredMixin, UnBlockedRequiredMixin, DeleteView):

    def get(self, request, *args, **kwargs):
        FollowRequestModel.objects.get(from_user=self.request.user, to_user=kwargs['pk']).delete()
        return redirect('accounts:profile', pk=kwargs['pk'])


class UserEmojiPackageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        emoji_package = EmojiPackageModel.objects.get(from_user=request.user,
                                                      to_user=UserModel.objects.get(pk=kwargs['pk']))
        emoji_request = request.GET.get('emoji')
        match emoji_request:
            case 'heart':
                emoji_package.reverse_heart_emoji()
            case 'trophy':
                emoji_package.reverse_trophy_emoji()
            case 'passion':
                emoji_package.reverse_passion_emoji()
            case _:
                pass
        return redirect('accounts:profile', pk=kwargs['pk'])


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


class UserBlockReportsView(LoginRequiredMixin, ProfileContextMixin, ListView):
    template_name = 'accounts/block_reports.html'
    context_object_name = 'blocked_users'

    def get_queryset(self):
        queryset = self.request.user.blocked_by.all()
        return queryset


class UserBlockReportDeleteView(LoginRequiredMixin, ProfileContextMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy('accounts:block_reports')
    success_message = 'شما این کاربر را آنبلاک کرده اید'

    def get_object(self, queryset=None):
        return BlockModel.objects.get(from_user=self.request.user, to_user=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class UserPhoneVerifyView(LoginRequiredMixin, ProfileContextMixin, FormView):
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
        if 'send-again' in form.data:
            otp_code = OTPCodeModel.objects.update_or_create(phone_number=self.request.user.phone_number,
                                                             code=randint(100000, 999999))
            otp_code.send_otp_code()
            return render(self.request, self.template_name, {'form': self.form_class()})
        code_instance = OTPCodeModel.objects.get(phone_number=user.phone_number).code
        if code == code_instance:
            user.is_phone_verified = True
            user.save()
            messages.success(self.request, 'شماره تلفن شما با موفقیت تایید شد')
            return redirect('accounts:profile_without_pk')
        messages.error(self.request, 'کد وارد شده نادرست میباشد')
        return self.form_invalid(form)

    def form_invalid(self, form):
        if 'send-again' in form.data:
            otp_code = OTPCodeModel.objects.get(phone_number=self.request.user.phone_number)
            otp_code.code = randint(100000, 999999)
            otp_code.send_otp_code()
            otp_code.save()
            return render(self.request, self.template_name, {'form': self.form_class()})
        return render(self.request, self.template_name, {'form': form})


class UserBlockReportView(ProfileContextMixin, LoginRequiredMixin, UnBlockedRequiredMixin, FormView):
    template_name = 'accounts/block_report.html'
    form_class = UserBlockReportForm

    def form_valid(self, form):
        user = UserModel.objects.get(pk=self.kwargs['pk'])
        BlockModel.objects.create(from_user=self.request.user, to_user=user,
                                  reason=form.cleaned_data['reason'])
        return redirect('accounts:profile_without_pk')


class UserFollowingListView(ListView):
    paginate_by = 20
    template_name = 'accounts/'

    def get_queryset(self):
        return UserModel.objects.get(pk=self.kwargs['pk']).followings.all()


class UserFollowersListView(ListView):
    paginate_by = 20
    template_name = accounts

    def get_queryset(self):
        return UserModel.objects.get(pk=self.kwargs['pk']).followings.all()
