from django.db import models


class Genre(models.Model):
    """
    Book genre model
    """
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
