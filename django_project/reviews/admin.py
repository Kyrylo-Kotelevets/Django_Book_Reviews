"""
Registering Models for Django Admin Panel
"""
from django.contrib import admin
from .models import Review


@admin.register(Review)
class BookAdmin(admin.ModelAdmin):
    """
    Admin Model Settings
    """
    list_filter = ('date_posted', 'creator', 'rating', 'book')
    search_fields = ('title', 'text', 'creator')
    list_display = ('creator', 'book', 'date_posted')
