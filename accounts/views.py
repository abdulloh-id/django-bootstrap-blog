from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from accounts.models import Profile


@login_required  # Requires user to be logged in to access this view.
def edit_profile_view(request):
    # Ensure a Profile exists for the logged-in user. Creates one if it doesn't.
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        # Handle form submission for updating profile information.
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.birthdate = request.POST.get('birthdate')

        # Update user's avatar if a new one was uploaded.
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']

        # Save the updated user and profile information to the database.
        user.save()
        profile.save()

        messages.success(request, 'Your profile has been updated!')
        return redirect('accounts:edit_profile')  # Redirect to the edit profile page.

    return render(request, 'accounts/edit_profile.html')  # Render the edit profile form.

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