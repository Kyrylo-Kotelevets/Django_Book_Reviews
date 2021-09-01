"""
Url Patterns for Authors api
"""
from django.urls import path
from .api import AuthorList

urlpatterns = [
    path('', AuthorList.as_view(), name='api-author-list'),
]
