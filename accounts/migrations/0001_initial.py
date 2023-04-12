# Generated by Django 4.1.7 on 2023-03-09 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=11, unique=True)),
                ('about_me', models.TextField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('background_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('is_private', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_auther', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('last_active', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
