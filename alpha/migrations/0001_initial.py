# Generated by Django 4.2.1 on 2024-03-21 17:26

import alpha.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeletedHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=100)),
                ('reserved_seat', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateField(auto_now_add=True, null=True)),
                ('created_on', models.CharField(max_length=40, null=True)),
                ('mobile_number', models.CharField(max_length=12, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('adharcard', models.ImageField(blank=True, null=True, upload_to=alpha.models.upload_path)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=alpha.models.upload_path)),
                ('dob', models.CharField(max_length=50, null=True)),
                ('adress', models.CharField(blank=True, max_length=300, null=True)),
                ('gender', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('facilty', models.CharField(blank=True, max_length=1000, null=True)),
                ('locality', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('imageOne', models.ImageField(blank=True, null=True, upload_to=alpha.models.upload_path)),
                ('imageTwo', models.ImageField(blank=True, null=True, upload_to=alpha.models.upload_path)),
                ('imageThree', models.ImageField(blank=True, null=True, upload_to=alpha.models.upload_path)),
                ('imageFour', models.ImageField(blank=True, null=True, upload_to=alpha.models.upload_path)),
                ('imageFive', models.ImageField(blank=True, null=True, upload_to=alpha.models.upload_path)),
                ('imageSix', models.ImageField(blank=True, null=True, upload_to=alpha.models.upload_path)),
                ('imageSeven', models.ImageField(blank=True, null=True, upload_to=alpha.models.upload_path)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('mobile_number', models.CharField(max_length=12)),
                ('whatsapp_number', models.CharField(blank=True, max_length=12, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('total_seat', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(500), django.core.validators.MinValueValidator(1)])),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LibrarySeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_num', models.IntegerField()),
                ('booked', models.BooleanField(default=False)),
                ('lib', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alpha.library')),
            ],
        ),
        migrations.CreateModel(
            name='SeatReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('mobile_number', models.CharField(max_length=12)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateField(auto_now=True, null=True)),
                ('amount', models.IntegerField(null=True)),
                ('adharcard', models.FileField(blank=True, null=True, upload_to='')),
                ('photo', models.FileField(blank=True, null=True, upload_to='')),
                ('dob', models.DateField(null=True)),
                ('adress', models.CharField(blank=True, max_length=300, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('reserved_seat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='alpha.libraryseat')),
            ],
        ),
        migrations.CreateModel(
            name='HalfTimer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=12, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateField(auto_now=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('adharcard', models.ImageField(blank=True, null=True, upload_to=alpha.models.upload_path)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=alpha.models.upload_path)),
                ('dob', models.DateField(blank=True, null=True)),
                ('adress', models.CharField(blank=True, max_length=300, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True)),
                ('lib_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alpha.library')),
            ],
        ),
        migrations.CreateModel(
            name='ExtraStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=12, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateField(auto_now=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('adharcard', models.ImageField(blank=True, null=True, upload_to=alpha.models.upload_path)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=alpha.models.upload_path)),
                ('dob', models.DateField(blank=True, null=True)),
                ('adress', models.CharField(blank=True, max_length=300, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True)),
                ('lib', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alpha.library')),
            ],
        ),
        migrations.CreateModel(
            name='AmountCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_month', models.DateField(auto_now_add=True, null=True)),
                ('amount', models.IntegerField()),
                ('cost', models.TextField(blank=True, null=True)),
                ('finalCost', models.IntegerField(blank=True, null=True)),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alpha.library')),
            ],
            options={
                'ordering': ('-collection_month',),
            },
        ),
    ]
