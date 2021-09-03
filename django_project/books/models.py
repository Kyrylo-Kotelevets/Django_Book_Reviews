"""
The module is used to describe database Book model
"""
from datetime import date

from PIL import Image
from authors.models import Author
from django.db import models
from django.db.models import QuerySet, Q, Avg
from genres.models import Genre


class Book(models.Model):
    """
    Entity Model Book
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField(default=date.today().year)
    cover_img = models.ImageField(upload_to='book_covers', default='book_covers/default.png')
    summary = models.TextField(max_length=1028)

    authors = models.ManyToManyField(Author, blank=True, related_name='books')
    genres = models.ManyToManyField(Genre, blank=True, related_name='books')

    def __str__(self) -> str:
        """
        Function for line display of the model
        """
        return self.short_title

    def save(self, *args, **kwargs) -> None:
        """
        Function resizes book cover image if it is too big
        """
        super().save(*args, **kwargs)

        cover = Image.open(self.cover_img.path)

        if cover.height > 1200 or cover.width > 900:
            output_size = (1200, 900)
            cover.thumbnail(output_size)
            cover.save(self.cover_img.path)

    @property
    def short_title(self) -> str:
        """Used for pretty output in big lists

        Returns
        -------
        str
            Book title cut to 25 letters maximum
        """
        if len(self.title) < 25:
            return self.title
        return self.title[:25] + '...'

    @classmethod
    def get_all(cls) -> QuerySet:
        """Returns all objects of the class

        Returns
        -------
        QuerySet
            Set that contains all books
        """
        return cls.objects.all()

    @classmethod
    def find_by_title(cls, title: str, queryset: QuerySet=None) -> QuerySet:
        """Return books set by matching with title pattern

        Parameters
        ----------
        title : str
            Book title pattern for search
        queryset : QuerySet, optional
            QuerySet for filtering (default is None)

        Returns
        -------
        QuerySet
            Set of all matched book by title
        """
        if queryset is not None:
            return queryset.filter(title__icontains=title)
        return cls.objects.filter(title__icontains=title)

    @classmethod
    def find_by_author(cls, name: str, queryset: QuerySet=None) -> QuerySet:
        """Return books set by matching with author pattern

        Parameters
        ----------
        name : str
            Author firstname/lastname pattern for search
        queryset : QuerySet, optional
            QuerySet for filtering (default is None)

        Returns
        -------
        QuerySet
            Set of all matched book by one or more authors
        """
        if queryset is not None:
            return queryset.filter(Q(authors__first_name__icontains=name) |
                                   Q(authors__last_name__icontains=name)).prefetch_related('authors')
        return cls.objects.filter(Q(authors__first_name__icontains=name) |
                                  Q(authors__last_name__icontains=name)).prefetch_related('authors')

    @classmethod
    def calculate_score(cls, queryset: QuerySet=None) -> QuerySet:
        """ Calculates average rating for each book in set over its reviews

        Parameters
        ----------
        queryset : QuerySet, optional
            QuerySet for annotating (default is None)

        Returns
        -------
        QuerySet
            Set of book with calculated score field in range [0, 100]
        """
        if queryset is not None:
            return queryset.annotate(score=Avg('review__rating')*10).order_by('-score')
        return cls.objects.annotate(score=Avg('review__rating')*10).order_by('-score')

    class Meta:
        """
        Class container with metadata
        """
        verbose_name = "Book"
        ordering = ('title',)
