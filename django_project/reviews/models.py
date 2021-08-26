from datetime import date

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Genre(models.Model):
    """
    Book genre model
    """
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    """
    Author Model
    """
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    class Meta:
        unique_together = ('first_name', 'last_name', )

    def __str__(self):
        return self.first_name + " " + self.last_name


class Book(models.Model):
    """
    Book Model
    """
    title = models.CharField(max_length=255)
    rating = models.FloatField()
    publication_year = models.IntegerField(default=date.today().year)
    cover_img = models.ImageField(upload_to='book_covers', default='book_covers/default.png')
    summary = models.TextField(max_length=1028)

    authors = models.ManyToManyField('Author', blank=True, related_name='books')
    genres = models.ManyToManyField('Genre', blank=True, related_name='books')

    class Meta:
        ordering = ['-rating']

    def __repr__(self):
        return self.short_title

    def __str__(self):
        return self.title

    @property
    def short_title(self):
        if len(self.title) < 25:
            return self.title
        return self.title[:25] + '...'


class Review(models.Model):
    """
    Review Model
    """

    RATINGS = zip(range(1, 10 + 1), range(1, 10 + 1))

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    date_posted = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=2056)
    rating = models.IntegerField(choices=RATINGS)

    def __repr__(self):
        return self.creator.username + ' : ' + self.book.title

    def __str__(self):
        return self.short_text

    @property
    def owner(self):
        return self.creator

    @property
    def short_text(self):
        if len(self.text) < 128:
            return self.text
        return self.text[:128] + '...'

    @classmethod
    def get_book_reviews(cls, pk: int):
        return cls.objects.filter(book__pk=pk)

    @classmethod
    def get_user_review(cls, pk: int):
        return cls.objects.filter(creator__pk=pk)


class Comment(models.Model):
    """
    Comment Model
    """
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    date_posted = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=1028)

    def __repr__(self) -> str:
        return self.creator.username + " : " + str(self.review.pk)

    def __str__(self) -> str:
        return self.text[:100]

    @property
    def owner(self):
        return self.creator

    @property
    def short_text(self):
        if len(self.text) < 128:
            return self.text
        return self.text[:128] + '...'

    @classmethod
    def get_review_comment(cls, pk: int):
        return cls.objects.filter(review__pk=pk)

    @classmethod
    def get_user_comment(cls, pk: int):
        return cls.objects.filter(creator__pk=pk)
