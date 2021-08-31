from django import forms
from django.forms.widgets import Textarea

from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Form for Review Model
    """
    class Meta:
        model = Review
        fields = ['title', 'text', 'rating']
        widgets = {'text': Textarea}


class ReviewSearchForm(forms.Form):
    """
    Form for Reviews Search
    """
    SEARCH_BY = (
        ('title', 'Title'),
    )

    search_pattern = forms.CharField(required=False, initial='', max_length=32)
    search_by = forms.CharField(required=False, initial='Title', widget=forms.Select(choices=SEARCH_BY))
