from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
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
    ModeratorRequiredMixin,
    OwnerOrModeratorRequiredMixin,
    DifferentUserRequiredMixin,
)

from .forms import CommentForm, ReviewForm, BookForm
from .models import Post, Book, Review, Comment


class CommentListView(ListView):
    model = Comment
    template_name = 'reviews/comment_list.html'
    context_object_name = 'comments'
    paginate_by = 10
    ordering = ['-date_posted']


class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10
    ordering = ['-date_posted']

    def get_queryset(self):
        search = self.request.GET.get('search')

        if search:
            return Review.objects.filter(title__icontains=search)
        else:
            return Review.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_val'] = self.request.GET.get('search')
        return context


class BookListView(ListView):
    model = Book
    template_name = 'reviews/home.html'
    context_object_name = 'books'
    paginate_by = 10
    ordering = ['rating']

    def get_queryset(self):
        search = self.request.GET.get('search')

        if search:
            return Book.objects.filter(title__icontains=search)
        else:
            return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_val'] = self.request.GET.get('search')
        context['is_moderator'] = is_moderator(self.request)
        return context


class UserCommentListView(ListView):
    model = Comment
    template_name = 'reviews/user_comment.html'
    context_object_name = 'comments'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Comment.objects.filter(creator=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context


class UserReviewListView(ListView):
    model = Review
    template_name = 'reviews/user_review.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Review.objects.filter(creator=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'reviews/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class BookDetailView(DetailView):
    model = Book
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page') or 1

        reviews_list = Review.get_book_reviews(self.object.pk)
        paginator = Paginator(reviews_list, self.paginate_by)

        context['page_obj'] = paginator.get_page(page_number)
        context['reviews'] = paginator.get_page(page_number).object_list
        context['is_moderator'] = is_moderator(self.request)
        return context


class BookCreateView(ModeratorRequiredMixin, CreateView):
    model = Book
    template_name = 'reviews/book_create_form.html'
    form_class = BookForm

    def form_valid(self, form):
        print(form.cleaned_data['cover_img'])
        book = Book(title=form.cleaned_data['title'],
                    summary=form.cleaned_data['summary'],
                    rating=form.cleaned_data['rating'],
                    publication_year=form.cleaned_data['publication_year'],
                    cover_img=form.cleaned_data['cover_img'])
        book.save()
        book.authors.add(*form.cleaned_data['authors'])
        book.genres.add(*form.cleaned_data['genres'])
        book.save()

        messages.success(self.request, 'Book has been added')
        return HttpResponseRedirect(reverse('book-detail', kwargs={'pk': book.pk}))


class BookUpdateView(ModeratorRequiredMixin, UpdateView):
    model = Book
    template_name = 'reviews/book_update_form.html'
    form_class = BookForm

    def get_success_url(self):
        messages.info(self.request, f'Information about book "{self.object.title}" has been updated')
        return reverse('book-detail', kwargs={'pk': self.object.pk})


class BookDeleteView(ModeratorRequiredMixin, DeleteView):
    model = Book

    def get_success_url(self):
        messages.warning(self.request, f'Book "{self.object.title}" "deleted')
        return reverse('blog-home')


class ReviewDetailView(DetailView):
    model = Review
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page') or 1

        reviews_list = Comment.get_review_comment(self.object.pk)
        paginator = Paginator(reviews_list, self.paginate_by)

        context['page_obj'] = paginator.get_page(page_number)
        context['comments'] = paginator.get_page(page_number).object_list

        context['is_have_rights'] = is_moderator(self.request) or (self.object.owner.pk == self.request.user.pk)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'reviews/review_create_form.html'
    form_class = ReviewForm

    def form_valid(self, form):
        review = Review(title=form.cleaned_data['title'],
                        text=form.cleaned_data['text'],
                        rating=form.cleaned_data['rating'],
                        book_id=self.kwargs.get('pk'),
                        creator_id=self.request.user.pk)
        review.save()
        return HttpResponseRedirect(reverse('review-detail', kwargs={'pk': review.pk}))


class ReviewUpdateView(OwnerOrModeratorRequiredMixin, UpdateView):
    model = Review
    template_name = 'reviews/review_update_form.html'
    form_class = ReviewForm

    def get_success_url(self):
        return reverse('review-detail', kwargs={'pk': self.object.pk})


class ReviewDeleteView(OwnerOrModeratorRequiredMixin, DeleteView):
    model = Review

    def get_success_url(self):
        return reverse('review-list')


class CommentDetailView(DetailView):
    model = Comment
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_have_rights'] = is_moderator(self.request) or (self.object.owner.pk == self.request.user.pk)
        return context


class CommentCreateView(LoginRequiredMixin, DifferentUserRequiredMixin, CreateView):
    model = Comment
    template_name = 'reviews/comment_create_form.html'
    form_class = CommentForm

    def form_valid(self, form):
        comment = Comment(text=form.cleaned_data['text'],
                          review_id=self.kwargs.get('pk'),
                          creator_id=self.request.user.pk)
        comment.save()
        return HttpResponseRedirect(reverse('comment-detail', kwargs={'pk': comment.pk}))


class CommentUpdateView(OwnerOrModeratorRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'reviews/comment_update_form.html'

    def get_success_url(self):
        return reverse('comment-detail', kwargs={'pk': self.object.pk})


class CommentDeleteView(OwnerOrModeratorRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('comment-list')


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'reviews/about.html', {'title': 'About'})
