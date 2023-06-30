from django.db import models
from django.urls import reverse
from accounts.models import UserModel


def team_logo_path(instance, filename):
    return f'teams/team_{instance.name}/{filename}'


class LeagueModel(models.Model):
    name = models.CharField(max_length=30, verbose_name='نام تیم', primary_key=True)

    class Meta:
        verbose_name = 'لیگ'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('teams:list_teams', kwargs={'league': self.name})


class TeamModel(models.Model):
    name = models.CharField(max_length=30, verbose_name='نام تیم', primary_key=True)
    logo = models.ImageField(upload_to=team_logo_path)
    league = models.ForeignKey(LeagueModel, on_delete=models.CASCADE, related_name='teams')
    followers = models.ManyToManyField(UserModel, through='UserFollowTeamModel', through_fields=('team', 'user'),
                                       related_name='following_teams')

    class Meta:
        verbose_name = 'تیم'

    def __str__(self):
        return self.name


class UserFollowTeamModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    team = models.ForeignKey(TeamModel, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.full_name} - {self.team}'

    class Meta:
        unique_together = ('user', 'team')
        verbose_name = 'کاربر علاقمند به تیم'
