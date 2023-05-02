from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('password/reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', views.UserPasswordConfirm.as_view(),
         name='password_reset_confirm'),
    path('password/change/', views.UserChangePasswordView.as_view(), name='change_password'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.UserProfileEditView.as_view(), name='edit_profile'),
    path('follow/user/<int:pk>/', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/user/<int:pk>/', views.UserUnfollowView.as_view(), name='user_unfollow'),
]
