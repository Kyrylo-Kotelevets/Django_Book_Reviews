from django.forms import ModelForm
from django.forms.widgets import Textarea
from .models import Book, Review, Comment


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'text', 'rating']
        widgets = {'text': Textarea}


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': Textarea}


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'summary', 'rating', 'publication_year', 'cover_img', 'authors', 'genres']
        widgets = {'summary': Textarea}
