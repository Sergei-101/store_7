from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'id':'form-input-review',
                                                           'class':'form-control form-control_gray',
                                                           'placeholder':'Ваш отзыв',
                                                           'cols':'30',
                                                           'rows':'8'}))


    class Meta:
        model = Review
        fields = ['rating', 'comment']