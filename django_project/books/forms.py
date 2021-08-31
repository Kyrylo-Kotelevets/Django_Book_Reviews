"""
Forms for Books App
"""

from django import forms
from django.forms.widgets import Textarea

from .models import Book


class BookForm(forms.ModelForm):
    """
    Form for Books Model
    """

    class Meta:
        model = Book
        fields = ['title', 'summary', 'publication_year', 'cover_img', 'authors', 'genres']
        widgets = {'summary': Textarea}


class BookSearchForm(forms.Form):
    """
    Form for Books Search
    """
    SEARCH_BY = (
        ('title', 'Title'),
        ('author', 'Author'),
    )

    search_pattern = forms.CharField(required=False, initial='', max_length=32)
    search_by = forms.CharField(required=False, initial='Title', widget=forms.Select(choices=SEARCH_BY))
