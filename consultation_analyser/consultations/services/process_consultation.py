from consultation_analyser.consultations.models import Theme, Answer


class ProcessConsultation:
    def __init__(self, consultation_id):
        self.consultation_id = consultation_id

    def run(self):
        answer_to_process = Answer.objects.filter(question__section__consultation_id=self.consultation_id).first()

        theme = Theme.objects.create(
            label="MY LLM-generated label",
            summary="idk",
            keywords=["we", "are", "keywords"],
        )
        answer_to_process.theme = theme
        answer_to_process.save()

        return True
