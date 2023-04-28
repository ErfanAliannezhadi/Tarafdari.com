from django.contrib import admin
from .models import UserModel, FollowModel
from django.contrib.auth.admin import UserAdmin

admin.site.register(UserModel)
admin.site.register(FollowModel)
