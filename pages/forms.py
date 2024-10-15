
from django import forms
from ckeditor.widgets import CKEditorWidget
from pages.models import StaticPage

class StaticPageForm(forms.ModelForm):
    class Meta:
        model = StaticPage
        fields = '__all__'
        widgets = {
            'content': CKEditorWidget(),  # Используем CKEditor для поля content
        }
