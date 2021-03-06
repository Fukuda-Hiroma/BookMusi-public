# Generated by Django 3.2 on 2022-06-04 16:54

from django.db import migrations, models
import uuid


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
                ('useruuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='uuid')),
                ('username', models.CharField(max_length=16, unique=True, verbose_name='username')),
                ('nickname', models.CharField(max_length=32, unique=True, verbose_name='nickname')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
