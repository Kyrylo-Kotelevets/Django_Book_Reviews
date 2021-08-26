from datetime import date

from PIL import Image
from authors.models import Author
from django.db import models
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
        if len(self.title) < 25:
            return self.title
        return self.title[:25] + '...'
