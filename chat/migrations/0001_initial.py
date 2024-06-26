# Generated by Django 4.2.1 on 2024-03-21 17:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='image_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=100, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('photo', models.ImageField(null=True, upload_to='')),
                ('adharcard', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='student_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=50, null=True)),
                ('mobile_number', models.CharField(max_length=12, null=True)),
                ('uuid', models.CharField(max_length=20, null=True)),
                ('dob', models.DateField(null=True)),
                ('adharcard', models.CharField(max_length=50, null=True)),
                ('photo', models.CharField(max_length=50, null=True)),
                ('stream', models.CharField(max_length=50, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True)),
                ('expires_at', models.DateTimeField(auto_now_add=True)),
                ('submitted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign', models.CharField(max_length=64, null=True, unique=True)),
                ('expires_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
