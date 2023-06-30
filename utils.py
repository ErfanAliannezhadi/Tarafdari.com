from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.views.generic.base import ContextMixin
from accounts.models import FollowModel, FollowRequestModel, UserModel, BlockModel


class UnauthenticatedRequiredMixin:
    """
    Mixin that allows unauthenticated users to access the view.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        authenticated users can not log in again!
        """
        if request.user.is_authenticated:
            messages.warning(request, 'برای ورود ابتدا باید از این حساب خروج کنید')
            return redirect('accounts:profile', pk=request.user.pk)
        return super().dispatch(request, *args, **kwargs)


class UnBlockedRequiredMixin:
    """
    Block the access if each one of the users block the other one
    """

    def dispatch(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs['pk'])
        if BlockModel.objects.filter(from_user=request.user, to_user=user).exists():
            messages.error(request, 'شما نمیتوانید وارد این صفحه شوید. شما این کاربر را مسدود کرده اید.')
            return redirect('accounts:profile_without_pk')
        if BlockModel.objects.filter(from_user=user, to_user=request.user).exists():
            messages.error(request, 'شما نمیتوانید وارد این صفحه شوید. این کاربر شما را مسدود کرده است.')
            return redirect('accounts:profile_without_pk')
        return super().dispatch(request, *args, **kwargs)


class PublicUserProfileRequiredMixin:
    """
    block the access to Private Profiles
    """

    def dispatch(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs['pk'])
        if user.is_private:
            is_followed = FollowModel.objects.filter(from_user=request.user, to_user=user)
            if not is_followed:
                messages.error(request, 'شما نمیتوانید به این صفحه دسترسی داشته باشید')
                return redirect('accounts:profile', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class PrivateUserProfileRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs['pk'])
        if not user.is_private:
            return redirect('accounts:profile', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class ProfileContextMixin(ContextMixin):
    """
    shares same context data between the views which its templates extends 'accounts/base_profile.html'
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context.get('user') is None:
            if self.kwargs.get('pk') is None:
                context['user'] = self.request.user
            else:
                context['user'] = UserModel.objects.get(pk=self.kwargs['pk'])
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
        context['following_teams'] = context['user'].following_teams.all()[:5]
        return context
