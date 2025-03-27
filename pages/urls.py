from django.urls import path
from . import views
from articles.views import HomepageView  # Import HomepageView from articles app

# Class-based views
urlpatterns = [
	 path('', HomepageView.as_view(), name='index-full'),  # Use HomepageView for homepage
]

# Function-based views
urlpatterns += [
    path('post-details-1/', views.post_details_1_page, name='post-details-1'),  # Post details
    path('post-details-2/', views.post_details_2_page, name='post-details-2'),  # Post details
    path('contact/', views.contact_page, name='contact'),  # Contact page
    path('about/', views.about_page, name='about'),  # About page
    path('author/', views.author_page, name='author'),  # Author page
    path('privacy-policy/', views.privacy_policy_page, name='privacy-policy'),  # Privacy policy
    path('terms-conditions/', views.terms_conditions_page, name='terms-conditions'),  # Terms and conditions
    path('post-elements/', views.post_elements_page, name='post-elements'),  # Development reference
    # Add other views here
]