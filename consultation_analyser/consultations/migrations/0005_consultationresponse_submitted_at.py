# Generated by Django 5.0.4 on 2024-05-03 14:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("consultations", "0004_consultation_users"),
    ]

    operations = [
        migrations.AddField(
            model_name="consultationresponse",
            name="submitted_at",
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
            preserve_default=False,
        ),
    ]
