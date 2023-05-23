from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(UserModel)
admin.site.register(FollowModel)
admin.site.register(FollowRequestModel)
admin.site.register(EmojiPackageModel)
admin.site.register(BlockModel)
admin.site.register(OTPCodeModel)
