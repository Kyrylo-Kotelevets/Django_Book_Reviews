"""
Registering Models for Django Admin Panel
"""
from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin Model Settings
    """
    list_filter = ('publication_year', 'authors', 'genres')
    search_fields = ('authors', 'genres', 'title')
    list_display = ('title', 'publication_year')
