"""
The module is used to describe database Genre model
"""
from django.db import models


class Genre(models.Model):
    """
    Entity Genre model
    """
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        """
        Function for line display of the model
        """
        return self.name

    @classmethod
    def get_all(cls):
        """
        The function returns all objects of the class
        """
        return cls.objects.all()

    class Meta:
        """
        Class container with metadata
        """
        verbose_name = "Genre"
        ordering = ('name',)
