from django.contrib import admin
from .models import *


class TeamAdmin(admin.ModelAdmin):
    raw_id_fields = ('league',)


admin.site.register(TeamModel, TeamAdmin)
admin.site.register(LeagueModel)
admin.site.register(UserFollowTeamModel)
