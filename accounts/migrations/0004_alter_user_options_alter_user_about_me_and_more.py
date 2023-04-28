# Generated by Django 4.1.7 on 2023-04-23 12:17

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_user_last_active_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'کاربر'},
        ),
        migrations.AlterField(
            model_name='user',
            name='about_me',
            field=models.TextField(blank=True, null=True, verbose_name='درباره ی من'),
        ),
        migrations.AlterField(
            model_name='user',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.user_background_image_path, verbose_name='عکس بکگراند'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.user_cover_image_path, verbose_name='عکس کاور'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.user_profile_image_path, verbose_name='عکس پروفایل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='registration_date',
            field=models.DateField(auto_now_add=True, verbose_name='تاریخ عضویت'),
        ),
    ]
