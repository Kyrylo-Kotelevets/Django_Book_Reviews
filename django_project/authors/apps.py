"""
App settings
"""
from django.apps import AppConfig


class AuthorsConfig(AppConfig):
    """
    App Config
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authors'
