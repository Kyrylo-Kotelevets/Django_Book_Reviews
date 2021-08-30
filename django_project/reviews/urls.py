"""
Url Patterns for Reviews App
"""

from django.urls import path, include

from .views import (
    about,
    ReviewListView,
    ReviewDetailView,
    ReviewCreateView,
    ReviewUpdateView,
    ReviewDeleteView,
    UserReviewListView,
)

urlpatterns = [
    path('', include('books.urls')),
    path('comments/', include('comments.urls')),

    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('book/<int:pk>/review/add', ReviewCreateView.as_view(), name='review-add'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),

    path('user/<str:username>/reviews', UserReviewListView.as_view(), name='user-review'),
    path('about/', about, name='blog-about'),
]
