from django.forms import ModelForm
from django.forms.widgets import Textarea
from .models import Review


class ReviewForm(ModelForm):
    """
    Form for Review Model
    """
    class Meta:
        model = Review
        fields = ['title', 'text', 'rating']
        widgets = {'text': Textarea}
