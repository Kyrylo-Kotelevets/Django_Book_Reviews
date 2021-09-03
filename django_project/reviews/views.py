"""
Views for Reviews App
"""
from comments.models import Comment
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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

from .forms import ReviewForm, ReviewSearchForm
from .models import Review


class ReviewListView(ListView):
    """
    Displays Reviews
    """
    model = Review
    context_object_name = 'reviews'
    template_name = 'reviews/review_list.html'
    paginate_by = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form = None

    def setup(self, request, *args, **kwargs):
        """
        Creates search form
        """
        self.form = ReviewSearchForm(request.GET)
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        """Filter books by title when parameter is provided,
        otherwise, return all reviews

        Returns
        -------
        QuerySet
            Set of reviews
        """
        queryset = super().get_queryset()

        if self.form.is_valid():
            pattern = self.form.cleaned_data.get('search_pattern')
            if self.form.cleaned_data.get('search_by') == 'title':
                queryset = Review.find_by_title(pattern, queryset)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Inserts form instance, search parameters and moderator rights
        into template context
        """
        context = super().get_context_data(object_list=object_list, **kwargs)

        if self.form.is_valid() and self.form.cleaned_data.get('search_by') == 'title':
            context['search_pattern'] = self.form.cleaned_data.get('search_pattern')
            context['search_by'] = 'title'
        else:
            context['search_pattern'] = None
            context['search_by'] = None

        context['search_val'] = self.request.GET.get('search')
        context['is_moderator'] = is_moderator(self.request)
        context['form'] = self.form
        return context


class UserReviewListView(ListView):
    """
    Displays user reviews
    """
    model = Review
    paginate_by = 10
    context_object_name = 'reviews'
    template_name = 'reviews/user_review.html'

    def get_queryset(self):
        """
        Returns user reviews if user exists,
        otherwise returns 404
        """
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Review.objects.filter(creator=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        """
        Inserts user into template context if user exists,
        otherwise returns 404
        """
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context


class ReviewDetailView(DetailView):
    """
    Displays information about a review
    """
    model = Review
    paginate_by = 10

    def get_context_data(self, **kwargs) -> dict:
        """
        Inserts page number, moderator/commentator rights and review comments into template context
        """
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page') or 1

        reviews_list = Comment.get_review_comment(self.object.pk)
        paginator = Paginator(reviews_list, self.paginate_by)

        context['page_obj'] = paginator.get_page(page_number)
        context['comments'] = paginator.get_page(page_number).object_list

        context['is_have_rights'] = is_moderator(self.request) or (self.object.owner.pk == self.request.user.pk)
        context['can_comment'] = is_moderator(self.request) or (self.object.owner.pk != self.request.user.pk)
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Review Create View. Only available for moderator/superuser or owner
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create_form.html'

    def form_valid(self, form) -> HttpResponseRedirect:
        """
        Saves review and redirects to the review detail page with success message
        """
        review = Review(title=form.cleaned_data['title'],
                        text=form.cleaned_data['text'],
                        rating=form.cleaned_data['rating'],
                        book_id=self.kwargs.get('pk'),
                        creator_id=self.request.user.pk)
        review.save()

        messages.success(self.request, 'Review has been added')
        return HttpResponseRedirect(reverse('review-detail', kwargs={'pk': review.pk}))


class ReviewUpdateView(OwnerOrModeratorRequiredMixin, UpdateView):
    """
    Review Update View. Only available for moderator/superuser or owner
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_update_form.html'
    success_url = '../'


class ReviewDeleteView(OwnerOrModeratorRequiredMixin, DeleteView):
    """
    Review Delete View. Only available for moderator/superuser or owner
    """
    model = Review

    def get_success_url(self):
        """
        Redirects to the home page with warning message
        """
        messages.warning(self.request, f'Review "{self.object.title}" "deleted')
        return reverse('review-list')


def about(request):
    """
    Just about page
    """
    return render(request, 'reviews/about.html', {'title': 'About'})
