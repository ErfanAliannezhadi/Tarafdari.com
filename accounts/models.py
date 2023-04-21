from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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


class User(AbstractBaseUser, PermissionsMixin):
    """
    This is the User Model of Tarafdari.com
    """
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255, verbose_name='نام')
    last_name = models.CharField(max_length=255, verbose_name='نام خانوادگی')
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')
    about_me = models.TextField(blank=True, null=True, verbose_name='درباره ی من')
    profile_image = models.ImageField(blank=True, null=True,verbose_name='عکس پروفایل')
    cover_image = models.ImageField(blank=True, null=True,verbose_name='عکس کاور')
    background_image = models.ImageField(blank=True, null=True,verbose_name='عکس بکگراند')
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_auther = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    registration_date = models.DateField(auto_now_add=True, verbose_name='تاریخ عضویت')

    class Meta:
        verbose_name = 'کاربر'

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    @property
    def is_staff(self):
        return self.is_admin
