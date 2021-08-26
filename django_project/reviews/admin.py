from django.contrib import admin
from .models import Post, Genre, Author, Book, Review, Comment


admin.site.register(Post)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Comment)
