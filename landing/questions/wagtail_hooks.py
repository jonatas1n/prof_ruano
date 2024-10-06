from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.admin.menu import MenuItem
from wagtail import hooks
from django.urls import path, reverse
from .models import QuestionList, QuestionItem
from .views import import_from_json_view


class QuestionItemInlinePanel(InlinePanel):
    model = QuestionItem
    panels = [
        FieldPanel("question"),
        FieldPanel("subjects"),
        FieldPanel("answers"),
    ]


class QuestionListAdmin(ModelAdmin):
    model = QuestionList
    menu_label = "Listas"
    menu_icon = "list-ul"
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ("title", "duration")
    search_fields = "title"
    panels = [
        FieldPanel("title"),
        FieldPanel("duration"),
        FieldPanel("instructions"),
        InlinePanel("questions"),
    ]

modeladmin_register(QuestionListAdmin)


@hooks.register('register_admin_urls')
def import_from_json():
    return [
        path('import_json/', import_from_json_view, name='import_json'),
    ]

@hooks.register('register_settings_menu_item')
def register_import_json_menu_item():
    return MenuItem(
        'Importar JSON',  # Nome do item de menu
        reverse('import_json'),  # URL para o endpoint (nome da URL do seu view)
        classnames='icon icon-download',  # Ícone do Wagtail, opcional
        order=10000  # Ordem do item no menu
    )