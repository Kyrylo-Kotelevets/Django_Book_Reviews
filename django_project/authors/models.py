"""
The module is used to describe database Author model
"""
from django.db import models
from django.db.models import QuerySet


class Author(models.Model):
    """
    Entity Model Author
    """
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    def __str__(self) -> str:
        """
        Function for line display of the model
        """
        return "{} {}".format(self.first_name, self.last_name)

    @classmethod
    def get_all(cls) -> QuerySet:
        """Returns all objects of the class

        Returns
        -------
        QuerySet
            set that contains all authors
        """
        return cls.objects.all()

    class Meta:
        """
        Class container with metadata
        """
        verbose_name = "Author"
        unique_together = ('first_name', 'last_name',)
        ordering = ('last_name', 'first_name',)
