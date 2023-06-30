# Generated by Django 4.1.7 on 2023-05-24 10:53

from django.db import migrations, models
import django.db.models.deletion
import teams.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeagueModel',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='نام تیم')),
            ],
            options={
                'verbose_name': 'لیگ',
            },
        ),
        migrations.CreateModel(
            name='TeamModel',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='نام تیم')),
                ('logo', models.ImageField(upload_to=teams.models.team_logo_path)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.leaguemodel')),
            ],
            options={
                'verbose_name': 'تیم',
            },
        ),
    ]
