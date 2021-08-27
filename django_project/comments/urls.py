"""
Url Patterns for Comments App
"""

from django.urls import path

from . import views
from .views import (
    CommentListView,
    CommentDetailView,
    CommentUpdateView,
    CommentDeleteView,
    UserCommentListView,
)

urlpatterns = [
    path('all/', CommentListView.as_view(), name='comment-list'),
    path('review/<int:pk>/add', views.CommentCreateView.as_view(), name='comment-add'),
    path('<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('user/<str:username>', UserCommentListView.as_view(), name='user-comment'),
]
