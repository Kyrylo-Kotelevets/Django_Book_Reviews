"""
Views for Books App
"""
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
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
)
from reviews.models import Review

from .forms import BookForm, BookSearchForm
from .models import Book


class BookListView(ListView):
    """
    Displays Books
    """
    model = Book
    context_object_name = 'books'
    template_name = 'books/book_list.html'
    paginate_by = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form = None

    def setup(self, request, *args, **kwargs):
        """
        Creates search form
        """
        self.form = BookSearchForm(request.GET)
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        """Filter books by title or author when parameter is provided,
        otherwise, return all books

        Returns
        -------
        QuerySet
            Set of books, annotated with score field
        """
        queryset = super().get_queryset()

        if self.form.is_valid():
            pattern = self.form.cleaned_data.get('search_pattern')
            if self.form.cleaned_data.get('search_by') == 'title':
                queryset = Book.find_by_title(pattern, queryset)
            if self.form.cleaned_data.get('search_by') == 'author':
                queryset = Book.find_by_author(pattern, queryset)

        queryset = Book.calculate_score(queryset)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Inserts form instance, search and moderator rights parameters
        into template context
        """
        context = super().get_context_data(object_list=object_list, **kwargs)

        if self.form.is_valid() and self.form.cleaned_data.get('search_by') == 'title':
            context['search_pattern'] = self.form.cleaned_data.get('search_pattern')
            context['search_by'] = 'title'
        elif self.form.is_valid() and self.form.cleaned_data.get('search_by') == 'author':
            context['search_pattern'] = self.form.cleaned_data.get('search_pattern')
            context['search_by'] = 'author'
        else:
            context['search_pattern'] = None
            context['search_by'] = None

        context['is_moderator'] = is_moderator(self.request)
        context['form'] = self.form
        return context


class BookDetailView(DetailView):
    """
    Displays information about a book
    """
    model = Book
    context_object_name = 'book'
    template_name = 'books/book_detail.html'
    paginate_by = 10

    def get_context_data(self, **kwargs) -> dict:
        """
        Inserts page number, rating, moderator rights and book reviews into template context
        """
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page') or 1

        reviews_list = Review.get_book_reviews(self.object.pk)
        paginator = Paginator(reviews_list, self.paginate_by)

        context['page_obj'] = paginator.get_page(page_number)
        context['reviews'] = paginator.get_page(page_number)
        context['score'] = Review.get_book_score(self.object.pk)
        context['is_moderator'] = is_moderator(self.request)
        return context


class BookCreateView(ModeratorRequiredMixin, CreateView):
    """
    Book Create View. Only available for moderator or superuser
    """
    model = Book
    form_class = BookForm
    template_name = 'books/book_create_form.html'

    def form_valid(self, form) -> HttpResponseRedirect:
        """
        Saves book and redirects to the book detail page with success message
        """
        book = Book(title=form.cleaned_data['title'],
                    summary=form.cleaned_data['summary'],
                    publication_year=form.cleaned_data['publication_year'],
                    cover_img=form.cleaned_data['cover_img'])
        book.save()
        book.authors.add(*form.cleaned_data['authors'])
        book.genres.add(*form.cleaned_data['genres'])
        book.save()

        messages.success(self.request, 'Book has been added')
        return HttpResponseRedirect(reverse('book-detail', kwargs={'pk': book.pk}))


class BookUpdateView(ModeratorRequiredMixin, UpdateView):
    """
    Book Update View. Only available for moderator or superuser
    """
    model = Book
    form_class = BookForm
    template_name = 'books/book_update_form.html'

    def get_success_url(self):
        """
        Redirects to the book detail page with success message
        """
        messages.info(self.request, f'Information about book "{self.object.title}" has been updated')
        return reverse('book-detail', kwargs={'pk': self.object.pk})


class BookDeleteView(ModeratorRequiredMixin, DeleteView):
    """
    Book Delete View. Only available for moderator or superuser
    """
    model = Book

    def get_success_url(self):
        """
        Redirects to the home page with warning message
        """
        messages.warning(self.request, f'Book "{self.object.title}" "deleted')
        return reverse('blog-home')
