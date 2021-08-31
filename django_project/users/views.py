from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


def user_register(request):
    """
    User Registration
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            Profile.objects.create(user=User.objects.get(username=form.cleaned_data.get('username')))

            messages.success(request, 'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """
    Login View
    """

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:  # If user account available
                login(request, user)  # Save user in session

                messages.success(request, 'Welcome, {}'.format(user.username))
                return redirect('blog-home')
            else:
                messages.error(request, 'Login Failed')
        else:
            messages.error(request, 'Invalid login or password')

    return render(request, 'users/login.html')


@login_required
def user_profile(request):
    """
    User Profile Updating and Displaying
    """

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,
                                instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


@login_required
def user_logout(request):
    logout(request)  # Delete user from session
    return render(request, 'users/logout.html')
