from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('password/reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
]