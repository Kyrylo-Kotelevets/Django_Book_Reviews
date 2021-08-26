from django.db import models


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
