from django.forms import ModelForm
from django.forms.widgets import Textarea

from .models import Comment


class CommentForm(ModelForm):
    """
    Form for Comments Model
    """
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': Textarea}
