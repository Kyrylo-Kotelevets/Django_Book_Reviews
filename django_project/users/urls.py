from django.urls import path

from .views import user_login, user_register, user_profile, user_logout

urlpatterns = [
    path('register/', user_register, name='register'),
    path('profile/', user_profile, name='profile'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
