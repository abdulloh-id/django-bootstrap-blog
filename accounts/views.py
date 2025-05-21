from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from accounts.models import Profile
from .forms import CustomUserChangeForm, EditProfileForm
from .models import Profile


@login_required
def edit_profile_view(request):
    # Ensure a Profile exists for the logged-in user
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        # Initialize forms with POST data and instances
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)
        
        # Validate both forms
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:edit_profile')
        else:
            # Display form errors
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        # Initialize forms for GET request
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = EditProfileForm(instance=profile)
    
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    
@login_required  # Requires user to be logged in to access this view.
def change_password(request):
    if request.method == 'POST':
        # Handle form submission for changing the user's password.
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change.
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:edit_profile') # Redirect after successful password change.
        else:
            # Display any errors from the password change form.
            for error in form.errors.values():
                messages.error(request, error)
    return redirect('accounts:edit_profile') # Redirect to the edit profile page (GET request or form errors).