from django import forms
from ckeditor.widgets import CKEditorWidget
from products.models import Product, Feature

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': CKEditorWidget(),  # Используем CKEditorWidget для поля description
        }

class ProductFilterForm(forms.Form):
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Характеристики"
    )