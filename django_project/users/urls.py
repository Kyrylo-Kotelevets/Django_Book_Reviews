from django.urls import path

from .views import user_login, register, profile, user_logout

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
