from django import forms
from questions.models import QuestionListSubmission


class QuestionListForm(forms.ModelForm):
    class Meta:
        model = QuestionListSubmission
        fields = ["answers"]

    def __init__(self, *args, **kwargs):
        questions = kwargs.pop("questions", None)
        super().__init__(*args, **kwargs)

        if questions:
            for question in questions:
                get_answer = lambda answer: (answer.value.get("answer"), answer.value)
                choices = [get_answer(answer) for answer in question.answers]
                print(choices)
                self.fields[f"question_{question.id}"] = forms.ChoiceField(
                    label=question.question,
                    choices=choices,
                    widget=forms.RadioSelect,
                )

    def save(self, commit=True):
        submission = super().save(commit=False)
        submission.answers = {
            field: self.cleaned_data[field]
            for field in self.cleaned_data
            if field.startswith("question_")
        }

        if commit:
            submission.save()
        return submission
