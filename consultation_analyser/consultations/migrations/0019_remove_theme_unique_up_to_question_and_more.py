# Generated by Django 5.0.6 on 2024-06-17 15:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "consultations",
            "0018_alter_processingrun_options_alter_topicmodel_options_and_more",
        ),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="theme",
            name="unique_up_to_question",
        ),
        migrations.RemoveField(
            model_name="theme",
            name="question",
        ),
        migrations.AddConstraint(
            model_name="theme",
            constraint=models.UniqueConstraint(
                fields=("topic_id", "topic_model"), name="unique_id_per_model"
            ),
        ),
    ]
