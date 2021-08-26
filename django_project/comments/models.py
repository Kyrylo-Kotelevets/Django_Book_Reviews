from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from reviews.models import Review


class Comment(models.Model):
    """
    Comment Model
    """
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    date_posted = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=1028)

    class Meta:
        ordering = ['-date_posted']

    def __repr__(self):
        """
        repr method overriding
        """
        return self.creator.username + " : " + str(self.review.pk)

    def __str__(self):
        """
        str method overriding
        """
        return self.text[:100]

    @property
    def owner(self):
        """
        Returns owner(creator) of comment
        Added for permission checks
        """
        return self.creator

    @property
    def short_text(self):
        """
        Returns short text
        Added for more pretty output on site
        """
        if len(self.text) < 128:
            return self.text
        return self.text[:128] + '...'

    @classmethod
    def get_review_comment(cls, pk: int):
        """
        Returns all review comments
        """
        return cls.objects.filter(review__pk=pk)

    @classmethod
    def get_user_comment(cls, pk: int):
        """
        Returns all user comments
        """
        return cls.objects.filter(creator__pk=pk)
