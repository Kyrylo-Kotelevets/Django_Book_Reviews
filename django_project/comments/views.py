"""
Views for Comments App
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from helpers.permission_validators import (
    is_moderator,
    OwnerOrModeratorRequiredMixin,
)

from .forms import CommentForm
from .models import Comment


class CommentListView(ListView):
    """
    Displays all comments
    """
    model = Comment
    paginate_by = 10
    context_object_name = 'comments'
    template_name = 'comments/comment_list.html'


class UserCommentListView(ListView):
    """
    Displays user comments
    """
    model = Comment
    paginate_by = 10
    context_object_name = 'comments'
    template_name = 'comments/user_comment.html'

    def get_queryset(self):
        """
        Returns user comments if user exists,
        otherwise returns 404
        """
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Comment.objects.filter(creator=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        """
        Inserts user into template context if user exists,
        otherwise returns 404
        """
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context


class CommentDetailView(DetailView):
    """
    Displays information about a comment
    """
    model = Comment
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """
        Inserts moderator rights into template context
        """
        context = super().get_context_data(**kwargs)
        context['is_have_rights'] = is_moderator(self.request) or (self.object.owner.pk == self.request.user.pk)
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Comment Create View. Only available for authorized users
    """
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_create_form.html'

    def form_valid(self, form):
        """
        Saves comment and redirects to the comment detail page with success message
        """
        comment = Comment(text=form.cleaned_data['text'],
                          review_id=self.kwargs.get('pk'),
                          creator_id=self.request.user.pk)
        comment.save()

        messages.success(self.request, 'Comment has been added')
        return HttpResponseRedirect(reverse('comment-detail', kwargs={'pk': comment.pk}))


class CommentUpdateView(OwnerOrModeratorRequiredMixin, UpdateView):
    """
    Comment Update View. nly available for moderator or superuser or owner
    """
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_update_form.html'

    def get_success_url(self):
        """
        Redirects to comment detail page
        """
        return reverse('comment-detail', kwargs={'pk': self.object.pk})


class CommentDeleteView(OwnerOrModeratorRequiredMixin, DeleteView):
    """
    Comment Delete View. Only available for moderator or superuser or owner
    """
    model = Comment

    def get_success_url(self):
        """
        Redirects to comments list page
        """
        return reverse('comment-list')
