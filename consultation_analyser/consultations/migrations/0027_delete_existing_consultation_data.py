# Delete all existing consultation data before changing models.

from django.db import migrations


def delete_all_consultation_data(apps, schema_editor):
    Consultation = apps.get_model("consultations", "Consultation")
    Section = apps.get_model("consultations", "Section")
    Question = apps.get_model("consultations", "Question")
    ConsultationResponse = apps.get_model("consultations", "ConsultationResponse")
    ProcessingRun = apps.get_model("consultations", "ProcessingRun")
    TopicModelMetadata = apps.get_model("consultations", "TopicModelMetadata")
    Theme = apps.get_model("consultations", "Theme")
    Answer = apps.get_model("consultations", "Answer")

    Consultation.objects.all().delete()
    Section.objects.all().delete()
    Question.objects.all().delete()
    ConsultationResponse.objects.all().delete()
    ProcessingRun.objects.all().delete()
    TopicModelMetadata.objects.all().delete()
    Theme.objects.all().delete()
    Answer.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("consultations", "0026_processingrun_unique_slug_consultation"),
    ]

    operations = [migrations.RunPython(delete_all_consultation_data)]
