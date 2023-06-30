from django.urls import path
from . import views

app_name = 'teams'
urlpatterns = [
    path('<str:league>/', views.ListTeamsView.as_view(), name='list_teams'),
    path('<str:team>/follow/', views.FollowTeamView.as_view(), name='follow_team'),
    path('<str:team>/unfollow/', views.UnfollowTeamView.as_view(), name='unfollow_team'),
]
