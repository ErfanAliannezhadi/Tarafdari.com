from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('password/reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password/reset-confirm/<uidb64>/<token>/', views.UserPasswordConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password/change/', views.UserChangePasswordView.as_view(), name='change_password'),
    path('profile/', views.UserProfileView.as_view(), name='profile_without_pk'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.UserProfileEditView.as_view(), name='edit_profile'),
    path('profile/follow-requests/', views.UserFollowRequestsView.as_view(), name='follow_requests'),
    path('profile/follow-request/<int:pk>/decision/', views.UserFollowRequestDecisionView.as_view(),
         name='follow_request_decision'),
    path('profile/block-reports-list/', views.UserBlockReportsView.as_view(), name='block_reports'),
    path('profile/block-report/<int:pk>/delete/', views.UserBlockReportDeleteView.as_view(),
         name='block-report_delete'),
    path('user/<int:pk>/block-report/', views.UserBlockReportView.as_view(), name='block_report'),
    path('follow/user/<int:pk>/', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/user/<int:pk>/', views.UserUnfollowView.as_view(), name='user_unfollow'),
    path('follow-request/user/<int:pk>/', views.UserFollowRequestView.as_view(), name='user_follow_request'),
    path('unfollow-request/user/<int:pk>/', views.UserUnfollowRequestView.as_view(), name='user_unfollow_request'),
    path('emoji/pack/user/<int:pk>/', views.UserEmojiPackageView.as_view(), name='emoji_package'),
    path('profile/phone-verify/', views.UserPhoneVerifyView.as_view(), name='phone_verify'),
]
