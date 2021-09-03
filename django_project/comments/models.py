"""
The module is used to describe database Comment model
"""
from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from reviews.models import Review


class Comment(models.Model):
    """
    Entity Model Comment
    """
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    date_posted = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=1028)

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
            Owner(creator) of comment
        """
        return self.creator

    @property
    def short_text(self):
        """Used for pretty output in big lists

        Returns
        -------
        str
            comment text cut to 128 letters maximum
        """
        if len(self.text) < 128:
            return self.text
        return self.text[:128] + '...'

    @classmethod
    def get_all(cls) -> QuerySet:
        """Returns all objects of the class

        Returns
        -------
        QuerySet
            Set that contains all comments
        """
        return cls.objects.all()

    @classmethod
    def get_review_comment(cls, pk: int) -> QuerySet:
        """ Returns all comments for review

        Parameters
        ----------
        pk : int
            Review pk/id for filtering

        Returns
        -------
        QuerySet
            Set of comments, for provided review
        """
        return cls.objects.filter(review__pk=pk)

    @classmethod
    def get_user_comment(cls, pk: int) -> QuerySet:
        """ Returns all comments owned by user

        Parameters
        ----------
        pk : int
            User pk/id for filtering

        Returns
        -------
        QuerySet
            Set of comments, owned by provided user
        """
        return cls.objects.filter(creator__pk=pk)

    class Meta:
        """
        Class container with metadata
        """
        verbose_name = "Comment"
        ordering = ('-date_posted',)
