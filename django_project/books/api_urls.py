"""
Url Patterns for Books API
"""
from django.urls import path
from .api import BookList

urlpatterns = [
    path('', BookList.as_view(), name='api-book-list'),
]

