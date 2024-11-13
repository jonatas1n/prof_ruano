from django import forms
from questions.models import QuestionListSubmission
from django.utils import timezone


class QuestionListForm(forms.ModelForm):
    class Meta:
        model = QuestionListSubmission
        fields = ["answers"]

    def __init__(self, *args, **kwargs):
        questions = kwargs.pop("questions", None)
        super().__init__(*args, **kwargs)

        if questions:
            for question in questions:
                subjects = [subject.name for subject in question.subjects.all()]

                get_answer = lambda answer: (answer.value.get("answer"), answer.value)
                choices = [get_answer(answer) for answer in question.answers]

                self.fields[f"question_{question.id}"] = forms.ChoiceField(
                    label={"label": question.question, "subjects": subjects},
                    choices=choices,
                    widget=forms.RadioSelect,
                )

    def save(self, submission_id=None):
        submission = QuestionListSubmission.objects.get(pk=submission_id)
        print(self.cleaned_data)
        submission.answers = {
            field: self.cleaned_data[field]
            for field in self.cleaned_data
            if field.startswith("question_")
        }
        submission.is_finished = True
        submission.finished_at = timezone.now()
        results = submission.get_results()
        submission.result = results
        submission.save()
        return submission


class JsonUploadForm(forms.Form):
    list_title = forms.CharField(label="Título da Lista")
    json_data = forms.FileField()

class JsonMassiveForm(forms.Form):
    json_data = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Arquivos JSON' )
