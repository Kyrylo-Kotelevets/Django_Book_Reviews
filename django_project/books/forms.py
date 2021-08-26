from django.forms import ModelForm
from django.forms.widgets import Textarea
from .models import Book


class BookForm(ModelForm):
    """
    Form for Books Model
    """
    class Meta:
        model = Book
        fields = ['title', 'summary', 'publication_year', 'cover_img', 'authors', 'genres']
        widgets = {'summary': Textarea}
