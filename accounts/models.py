from django.utils import timezone
from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse
from ckeditor.fields import RichTextField
from kavenegar import *


def user_profile_image_path(instance, filename):
    return f'accounts/user_{instance.pk}/profile_image/{filename}'


def user_cover_image_path(instance, filename):
    return f'accounts/user_{instance.pk}/cover_image/{filename}'


def user_background_image_path(instance, filename):
    return f'accounts/user_{instance.pk}/background_image/{filename}'


class UserManager(BaseUserManager):
    """
    This is the Manager of User Model
    """

    def create_user(self, first_name, last_name, email, phone_number, password):
        """
        This method creates a user and returns it
        """
        if not first_name:
            raise ValueError('user must have first name!')
        if not last_name:
            raise ValueError('user must have last name!')
        if not email:
            raise ValueError('user must have email!')
        if not phone_number:
            raise ValueError('user must have phone number!')
        user = self.model(first_name=first_name, last_name=last_name, email=self.normalize_email(email),
                          phone_number=phone_number)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, phone_number, password):
        """
        This method is like create_user, but it creates a superuser!
        """
        user = self.create_user(first_name, last_name, email, phone_number, password)
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    This is the User Model of Tarafdari.com
    """
    first_name = models.CharField(max_length=10, verbose_name='نام')
    last_name = models.CharField(max_length=10, verbose_name='نام خانوادگی')
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')
    about_me = RichTextField(blank=True, null=True, verbose_name='درباره ی من')
    profile_image = models.ImageField(blank=True, null=True, verbose_name='عکس پروفایل',
                                      upload_to=user_profile_image_path, default='accounts/defaults/avatar-default.png')
    cover_image = models.ImageField(blank=True, null=True, verbose_name='عکس کاور', upload_to=user_cover_image_path,
                                    default='accounts/defaults/cover.jpg')
    background_image = models.ImageField(blank=True, null=True, verbose_name='عکس پس زمینه',
                                         upload_to=user_background_image_path)
    is_private = models.BooleanField(default=False, verbose_name='خصوصی')
    is_active = models.BooleanField(default=True)
    is_auther = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    registration_date = models.DateField(auto_now_add=True, verbose_name='تاریخ عضویت')
    last_online = models.DateTimeField(verbose_name='آخرین انلاین', blank=True, null=True, auto_now_add=True)

    # users relations
    followings = models.ManyToManyField('self', symmetrical=False, through='FollowModel',
                                        through_fields=('from_user', 'to_user'), related_name='followers')
    blocking = models.ManyToManyField('self', symmetrical=False, through='BlockModel',
                                      through_fields=('from_user', 'to_user'), related_name='blockers')
    followings_request = models.ManyToManyField('self', symmetrical=False, through='FollowRequestModel',
                                                through_fields=('from_user', 'to_user'),
                                                related_name='followers_request')
    emojis_pack = models.ManyToManyField('self', symmetrical=False, through='EmojiPackageModel',
                                         through_fields=('from_user', 'to_user'), related_name='packs_emojis')

    class Meta:
        verbose_name = 'کاربر'

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.id})

    @property
    def is_online(self):
        time_difference = timezone.now() - self.last_online
        return time_difference.total_seconds() < timezone.timedelta(minutes=10).total_seconds()

    @property
    def number_of_heart_emojis(self):
        return self.packs.filter(heart=True).count()

    @property
    def number_of_trophy_emojis(self):
        return self.packs.filter(trophy=True).count()

    @property
    def number_of_passion_emojis(self):
        return self.packs.filter(passion=True).count()

    def __str__(self):
        return f'{self.full_name} - {self.email} - {self.phone_number}'


class FollowModel(models.Model):
    """
    A model representing a follower/following relationship between users.

    Attributes:
        from_user (ForeignKey): The user who is following another user.
        to_user (ForeignKey): The user who is being followed by another user.
    """
    from_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='following_set')
    to_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='follower_set')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'دنبال کردن'
        unique_together = ['from_user', 'to_user']
        constraints = [models.CheckConstraint(check=~(models.Q(to_user=models.F('from_user'))),
                                              name='any_one_cant_follows_it_self')]

    def __str__(self):
        return f'{self.from_user.full_name} follows {self.to_user.full_name}'


class FollowRequestModel(models.Model):
    from_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='self_follow_requests')
    to_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='other_follow_requests')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'درخواست دنبال کردن'
        unique_together = ['from_user', 'to_user']
        constraints = [models.CheckConstraint(check=~(models.Q(from_user=models.F('to_user'))),
                                              name='any_one_cant_request_to_follows_it_self')]
        ordering = ['date']

    def accept(self):
        FollowModel.objects.create(from_user=self.from_user, to_user=self.to_user)
        self.delete()

    def reject(self):
        self.delete()


class BlockModel(models.Model):
    CHOICES_OF_REASON = [
        ('A', 'گزارش این شناسه کاربری'),
        ('B', 'گزارش مطالب و دیدگاه‌های این کاربر'),
        ('C', 'هیچی، فقط با این کاربر حال نمی‌کنم'),
        ('D', 'دلایل دیگری وجود دارد')
    ]
    from_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='blocked_by')
    to_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='blocked_users')
    reason = models.CharField(max_length=1, choices=CHOICES_OF_REASON)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'بلاک کردن کاربر'
        unique_together = ['from_user', 'to_user']

    def __str__(self):
        return f'{self.from_user.full_name} has blocked {self.to_user.full_name}'


class EmojiPackageModel(models.Model):
    """
    This model represents Emoji Package of users. you can see these emojis in profile page of every user,
    in the top of about me part.
    from_user is the user who turn on or turn off emoji package of to_user
    """
    from_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='packs')
    heart = models.BooleanField(default=False)
    trophy = models.BooleanField(default=False)
    passion = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'پکیج کاربر'
        unique_together = ['from_user', 'to_user']

    def reverse_heart_emoji(self):
        self.heart = not self.heart
        self.save()

    def reverse_trophy_emoji(self):
        self.trophy = not self.trophy
        self.save()

    def reverse_passion_emoji(self):
        self.passion = not self.passion
        self.save()

    def __str__(self):
        return f'{self.from_user.full_name} packs {self.to_user.full_name}'


class OTPCodeModel(models.Model):
    """
    OTP Code for user's phone number verification
    """
    phone_number = models.CharField(max_length=11, primary_key=True)
    code = models.CharField(max_length=6)

    def send_otp_code(self):
        try:
            api = KavenegarAPI(
                '364172347A732F79384D46713577756E49396B384A7958694471715A32496F342F5449446970796C7872773D')
            params = {
                'sender': '',
                'receptor': self.phone_number,
                'message': f'کد تایید شما {self.code}',
            }
            response = api.sms_send(params=params)
            print(response)
        except APIException as e:
            print(e)
        except HTTPException as e:
            print(e)
