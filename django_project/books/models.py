from datetime import date

from PIL import Image
from authors.models import Author
from django.db import models
from django.db.models import Avg
from django.db.models import Q
from genres.models import Genre


class Book(models.Model):
    """
    Book Model
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField(default=date.today().year)
    cover_img = models.ImageField(upload_to='book_covers', default='book_covers/default.png')
    summary = models.TextField(max_length=1028)

    authors = models.ManyToManyField(Author, blank=True, related_name='books')
    genres = models.ManyToManyField(Genre, blank=True, related_name='books')

    def __repr__(self):
        return self.short_title

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Resizes book cover image if its too bog
        """
        super().save(*args, **kwargs)

        cover = Image.open(self.cover_img.path)

        if cover.height > 1200 or cover.width > 900:
            output_size = (1200, 900)
            cover.thumbnail(output_size)
            cover.save(self.cover_img.path)

    @property
    def short_title(self):
        """
        Used for pretty output in big lists
        """
        if len(self.title) < 25:
            return self.title
        return self.title[:25] + '...'

    @classmethod
    def find_by_title(cls, title: str, queryset=None):
        """
        Return books by matching title
        """
        if queryset is not None:
            return queryset.filter(title__icontains=title)
        return cls.objects.filter(title__icontains=title)

    @classmethod
    def find_by_author(cls, name: str, queryset=None):
        """
        Return books by matching author
        """
        if queryset is not None:
            return queryset.filter(Q(authors__first_name__icontains=name) |
                                   Q(authors__last_name__icontains=name)).prefetch_related('authors')
        return cls.objects.filter(Q(authors__first_name__icontains=name),
                                  Q(authors__last_name__icontains=name)).prefetch_related('authors')

    @classmethod
    def calculate_score(cls, queryset=None):
        """
        Calculates average rating over book reviews
        """
        if queryset is not None:
            return queryset.annotate(score=Avg('review__rating')*10).order_by('-score')
        return cls.objects.annotate(score=Avg('review__rating')*10).order_by('-score')
