from django.shortcuts import render, redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('index-full')  # Change 'home' to your desired URL

# View for post details 1
def post_details_1_page(request):
    return render(request, 'post-details-1.html')

# View for post details 2
def post_details_2_page(request):
    return render(request, 'post-details-2.html')

# View for the post elements page
def post_elements_page(request):
    return render(request, 'post-elements.html')

# View for the contact page
def contact_page(request):
    return render(request, 'contact.html')

# View for the about page
def about_page(request):
    return render(request, 'about.html')

# View for the author page
def author_page(request):
    return render(request, 'author.html')

# View for the privacy policy page
def privacy_policy_page(request):
    return render(request, 'privacy-policy.html')

# View for the terms and conditions page
def terms_conditions_page(request):
    return render(request, 'terms-conditions.html')