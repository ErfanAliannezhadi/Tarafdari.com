from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin


class UnauthenticatedRequiredMixin(AccessMixin):
    """
    Mixin that allows unauthenticated users to access the view.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        authenticated users can not log in again!
        """
        if request.user.is_authenticated:
            print('='*100)
            messages.warning(request, 'برای ورود ابتدا باید از این حساب خروج کنید')
            return redirect('accounts:profile', pk=request.user.pk)
        return super().dispatch(request, *args, **kwargs)
