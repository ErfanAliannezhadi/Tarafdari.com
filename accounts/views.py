from django.shortcuts import render
from django.views import View

class UserLoginView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')
