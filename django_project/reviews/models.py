from books.models import Book
from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet, Avg
from django.utils import timezone


class Review(models.Model):
    """
    Entity Model Review
    """
    RATINGS = zip(range(1, 10 + 1), range(1, 10 + 1))

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    date_posted = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=2056)
    rating = models.IntegerField(choices=RATINGS)

    def __str__(self) -> str:
        """
        Function for line display of the model
        """
        return self.short_text

    @property
    def owner(self) -> User:
        """Field for permission checks

        Returns
        -------
        strUser
            Owner(creator) of review
        """
        return self.creator

    @property
    def short_text(self) -> str:
        """Used for pretty output in big lists

        Returns
        -------
        str
            Review title cut to 128 letters maximum
        """
        if len(self.text) < 128:
            return self.text
        return self.text[:128] + '...'

    @classmethod
    def find_by_title(cls, title: str, queryset: QuerySet=None) -> QuerySet:
        """Return reviews set by matching with title pattern

        Parameters
        ----------
        title : str
            Review title pattern for search
        queryset : QuerySet, optional
            QuerySet for filtering (default is None)

        Returns
        -------
        QuerySet
            Set of all matched reviews by title
        """
        if queryset is not None:
            return queryset.filter(title__icontains=title)
        return cls.objects.filter(title__icontains=title)

    @classmethod
    def get_book_reviews(cls, pk: int) -> QuerySet:
        """ Returns all reviews for book

        Parameters
        ----------
        pk : int
            Book pk/id for filtering

        Returns
        -------
        QuerySet
            Set of reviews, for provided book
        """
        return cls.objects.filter(book__pk=pk)

    @classmethod
    def get_book_score(cls, pk: int) -> float:
        """ Calculate rating of the book over its reviews

        Parameters
        ----------
        pk : int
            Book pk/id for filtering

        Returns
        -------
        float
            Average score over book reviews in range [0, 100]
        """
        return Review.get_book_reviews(pk).aggregate(Avg('rating'))['rating__avg'] * 10

    @classmethod
    def get_user_review(cls, pk: int) -> QuerySet:
        """ Returns all reviews owned by user

        Parameters
        ----------
        pk : int
            User pk/id for filtering

        Returns
        -------
        QuerySet
            Set of reviews, owned by provided user
        """
        return cls.objects.filter(creator__pk=pk)

    class Meta:
        """
        Class container with metadata
        """
        verbose_name = "Review"
        ordering = ['-date_posted']
