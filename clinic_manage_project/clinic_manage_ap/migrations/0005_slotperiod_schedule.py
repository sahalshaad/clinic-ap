# Generated by Django 5.1.5 on 2025-02-26 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_manage_ap', '0004_remove_slotperiod_slot_slotperiod_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='slotperiod',
            name='schedule',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='clinic_manage_ap.doctor_time'),
            preserve_default=False,
        ),
    ]
