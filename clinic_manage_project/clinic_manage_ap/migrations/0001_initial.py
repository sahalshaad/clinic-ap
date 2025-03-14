# Generated by Django 5.1.5 on 2025-02-25 05:54

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
                ('date', models.DateField(default=datetime.date.today)),
                ('Name', models.CharField(max_length=100)),
                ('Age', models.CharField(max_length=100)),
                ('Gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=50)),
                ('Description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='doc_signup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docname', models.CharField(max_length=100)),
                ('docnumber', models.CharField(max_length=100)),
                ('docemail', models.CharField(max_length=100)),
                ('docqualification', models.CharField(max_length=50)),
                ('docspecialisation', models.CharField(max_length=50)),
                ('docgender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=50)),
                ('docusername', models.CharField(max_length=50)),
                ('docpassword', models.CharField(max_length=50)),
                ('docphoto', models.FileField(blank=True, null=True, upload_to='photos/')),
            ],
        ),
        migrations.CreateModel(
            name='login_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Login',
                'verbose_name_plural': 'Logins',
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SlotPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_booked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='doctor_time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('Fromtime', models.TimeField()),
                ('Totime', models.TimeField()),
                ('Drname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_manage_ap.doc_signup')),
            ],
        ),
        migrations.CreateModel(
            name='feedback_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=1000)),
                ('Drname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_manage_ap.doc_signup')),
            ],
        ),
        migrations.AddField(
            model_name='doc_signup',
            name='login',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_manage_ap.login_data'),
        ),
        migrations.CreateModel(
            name='medical_notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('priscription', models.CharField(max_length=200)),
                ('symptoms', models.CharField(max_length=100)),
                ('diagnosis', models.CharField(max_length=100)),
                ('doctors', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_manage_ap.doc_signup')),
                ('patients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_manage_ap.booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='slot_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_manage_ap.slotperiod'),
        ),
        migrations.CreateModel(
            name='Slots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NoOfSlots', models.CharField(max_length=100)),
                ('status', models.TextField(default='Free')),
                ('booked_slots', models.TextField(default='')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_manage_ap.doctor_time')),
            ],
        ),
        migrations.AddField(
            model_name='slotperiod',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slot_periods', to='clinic_manage_ap.slots'),
        ),
        migrations.CreateModel(
            name='user_signup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usr_name', models.CharField(max_length=100)),
                ('usr_number', models.CharField(max_length=100)),
                ('usr_mail', models.CharField(max_length=100)),
                ('usr_age', models.CharField(max_length=100)),
                ('usr_username', models.CharField(max_length=100)),
                ('user_password', models.CharField(max_length=100)),
                ('user_photo', models.FileField(blank=True, null=True, upload_to='photos/')),
                ('login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_manage_ap.login_data')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_manage_ap.user_signup'),
        ),
    ]
