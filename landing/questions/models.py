from django.db import models
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.blocks import BooleanBlock, StructBlock, RichTextBlock

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.utils import timezone

from datetime import timedelta

class QuestionListIndex(Page):
    parent_page_types = ["home.LandingPage"]
    is_creatable = False

    default_instructions = RichTextField(max_length=255, verbose_name="Instruções padrões para a realização dos testes", null=True, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        context["lists"] = QuestionList.objects.live()
        active_submission = QuestionListSubmission.get_active_submissions(request.user)
        if active_submission:
            active_list = active_submission.questionsList
            context["active_list"] = active_list
            
        return context

    content_panels = Page.content_panels + [
        FieldPanel("default_instructions"),
    ]

    @method_decorator(login_required)
    def serve(self, request, *args, **kwargs):
        context = self.get_context(request)
        if request.method == "POST":
            question_list_id = request.POST.get("list_id")
            question_list = QuestionList.objects.get(id=question_list_id)
            list_submission = question_list.start_list(request)
            if list_submission:
                return redirect(list_submission)
            context["error"] = "Você já está fazendo uma prova"
        
        args = (request, context)
        return super().serve(request, *args, **kwargs)

class QuestionItem(Orderable):
    question_list = ParentalKey("questions.QuestionList", related_name="questions")
    question = RichTextField(max_length=255, verbose_name="Enunciado da questão")
    answers = StreamField(
        [
            (
                "option", StructBlock([
                    ("answer", RichTextBlock()),
                    ("is_correct", BooleanBlock(default=False, required=False)),
                ])
            )
        ], null=True, blank=True, max_num=5, min_num=2, verbose_name="Alternativas"
    )

    panels = [
        FieldPanel("question"),
        FieldPanel("answers"),
    ]

class QuestionList(Page):
    parent_page_types = ["questions.QuestionListIndex"]
    duration = models.IntegerField(verbose_name="Duração em minutos", default=120)
    instructions = RichTextField(max_length=255, verbose_name="Instruções", null=True, blank=True)
    
    def start_list(self, request):
        existing_submissions = QuestionListSubmission.get_active_submissions(request.user)
        if existing_submissions:
            return
        submission = QuestionListSubmission.objects.create(user=request.user, questionsList=self, answers={})
        return submission

    content_panels = Page.content_panels + [
        InlinePanel("questions", label="Questões"),
        FieldPanel("duration"),
        FieldPanel("instructions"),
    ]
    class Meta:
        verbose_name = "Lista de Questões"

    @property
    def list_size(self):
        return len(self.questions)
    
    def get_answers(self, answers):
        pass

    @method_decorator(login_required)
    def serve(self, request, *args, **kwargs):
        active_submission = QuestionListSubmission.get_active_submissions(request.user)
        if active_submission:
            active_list = active_submission.questionsList
            if not active_list:
                return (redirect('home:landing_page'))
            if active_list != self:
                return redirect(active_submission)

        if request.method == "POST":
            submission = QuestionListSubmission.objects.create(user=request.user, questionsList=self, answers=request.POST)

            return redirect('/question-list-index')
        return super().serve(request, *args, **kwargs)

class QuestionListSubmission(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    questionsList = models.ForeignKey("questions.QuestionList", on_delete=models.CASCADE)
    answers = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_finished = models.BooleanField(default=False)
    
    def is_active(self):
        duration = self.questionsList.duration
        return not self.is_finished and self.created_at + timedelta(minutes=duration) > timezone.now()
    
    @staticmethod
    def get_active_submissions(user):
        user_submission = QuestionListSubmission.objects.filter(user=user, is_finished=False).first()
        if not user_submission:
            return None
        return user_submission

    def __str__(self):
        return f"{self.user.email} - {self.questionsList.title}"
