from books.models import Book
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


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

    class Meta:
        ordering = ['-date_posted']

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
