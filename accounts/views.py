# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import Profile

@login_required
def edit_profile_view(request):
    # First, make sure the user has a profile
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        # Update user information
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.birthdate = request.POST.get('birthdate')
        
        # Update profile information
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        # Save changes
        user.save()
        profile.save()
        
        messages.success(request, 'Your profile has been updated!')
        return redirect('accounts:edit_profile')
        
    return render(request, 'accounts/edit_profile.html')  # (fixed path here too!)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return redirect('accounts:edit_profile')