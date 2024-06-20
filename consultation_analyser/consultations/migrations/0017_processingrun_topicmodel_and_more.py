# Generated by Django 5.0.6 on 2024-06-20 14:45

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("consultations", "0016_alter_answer_theme"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProcessingRun",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "consultation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="consultations.consultation",
                    ),
                ),
            ],
            options={
                "ordering": ["created_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TopicModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "processing_run",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="consultations.processingrun",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="consultations.question",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="topicmodel",
            constraint=models.UniqueConstraint(
                fields=("processing_run", "question"),
                name="unique_topic_model_question_run",
            ),
        ),
    ]
