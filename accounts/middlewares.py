from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse


class LastOnlineMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.last_online = timezone.now()
            request.user.save()
        response = self.get_response(request)
        return response


class UserPhoneVerifyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not (request.path in [reverse('accounts:logout'), reverse('accounts:phone_verify'),
                                 '/media/accounts/defaults/avatar-default.png', '/media/accounts/defaults/cover.jpg']):
            if request.user.is_authenticated and not request.user.is_phone_verified:
                return redirect('accounts:phone_verify')
        response = self.get_response(request)
        return response
