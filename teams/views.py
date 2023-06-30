from django.shortcuts import redirect
from django.views.generic import ListView, DeleteView, View
from django.db.models import Case, When, BooleanField
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TeamModel, LeagueModel, UserFollowTeamModel


class ListTeamsView(LoginRequiredMixin, ListView):
    template_name = 'teams/list_teams.html'
    context_object_name = 'teams'
    paginate_by = 20

    def get_queryset(self):
        if self.kwargs['league'] == 'all':
            teams = TeamModel.objects.all()
        else:
            teams = LeagueModel.objects.get(name=self.kwargs['league']).teams.all()
        return teams.annotate(
            is_followed=Case(
                When(followers=self.request.user, then=True),
                default=False,
                output_field=BooleanField()
            ), )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leagues'] = LeagueModel.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        request.session['teams_url_path'] = request.path
        return super().get(request, *args, **kwargs)


class FollowTeamView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        team = TeamModel.objects.get(name=kwargs['team'])
        UserFollowTeamModel.objects.create(user=request.user, team=team)
        return redirect(request.session['teams_url_path'])


class UnfollowTeamView(LoginRequiredMixin, DeleteView):
    model = UserFollowTeamModel

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        team = TeamModel.objects.get(name=self.kwargs['team'])
        return UserFollowTeamModel.objects.get(user=self.request.user, team=team)

    def get_success_url(self):
        return self.request.session['teams_url_path']
