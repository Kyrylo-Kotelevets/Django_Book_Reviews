"""
Registering Models for Django Admin Panel
"""
from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class BookAdmin(admin.ModelAdmin):
    """
    Admin Model Settings
    """
    list_filter = ('date_posted', 'creator', 'review')
    search_fields = ('date_posted', 'creator', 'review')
    list_display = ('creator', 'review', 'date_posted')
