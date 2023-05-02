from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse


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
        This method is like create_user but it creates a superuser!
        """
        user = self.create_user(first_name, last_name, email, phone_number, password)
        user.is_admin = True
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
    about_me = models.TextField(blank=True, null=True, verbose_name='درباره ی من')
    profile_image = models.ImageField(blank=True, null=True, verbose_name='عکس پروفایل',
                                      upload_to=user_profile_image_path)
    cover_image = models.ImageField(blank=True, null=True, verbose_name='عکس کاور', upload_to=user_cover_image_path)
    background_image = models.ImageField(blank=True, null=True, verbose_name='عکس پس زمینه',
                                         upload_to=user_background_image_path)
    is_private = models.BooleanField(default=False, verbose_name='خصوصی')
    is_active = models.BooleanField(default=True)
    is_auther = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    registration_date = models.DateField(auto_now_add=True, verbose_name='تاریخ عضویت')
    last_online = models.DateTimeField(verbose_name='آخرین انلاین', blank=True, null=True)

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

    def __str__(self):
        return f'{self.full_name} - {self.email} - {self.phone_number}'


class FollowModel(models.Model):
    from_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='followings')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'دنبال کردن'
        unique_together = ['from_user', 'to_user']
        constraints = [models.CheckConstraint(check=~(models.Q(from_user=models.F('to_user'))),
                                              name='any_one_cant_follows_it_self')]

    def __str__(self):
        return f'{self.from_user.full_name} follows {self.to_user.full_name}'
