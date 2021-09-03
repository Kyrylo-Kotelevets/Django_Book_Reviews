"""
Url Patterns for Genres API
"""
from django.urls import path
from .api import GenreList

urlpatterns = [
    path('', GenreList.as_view(), name='api-genre-list'),
]

