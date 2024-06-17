# Generated by Django 5.0.6 on 2024-06-17 16:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("consultations", "0019_remove_theme_unique_up_to_question_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="topicmodel",
            options={},
        ),
        migrations.AddField(
            model_name="topicmodel",
            name="question",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="consultations.question",
            ),
        ),
        migrations.AddConstraint(
            model_name="topicmodel",
            constraint=models.UniqueConstraint(
                fields=("processing_run", "question"),
                name="unique_topic_model_question_run",
            ),
        ),
    ]
