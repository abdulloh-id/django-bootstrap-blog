from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from articles.views import HomepageView  # Import HomepageView from articles app
from .views import AboutPageView

# Class-based views
urlpatterns = [
    path('', HomepageView.as_view(), name='home'),  # Use HomepageView for homepage
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('about/', AboutPageView.as_view(), name='about'),
]

# Function-based views
urlpatterns += [
    path('contact/', views.contact_page, name='contact'),  # Contact page
    path('author/', views.author_page, name='author'),  # Author page
    path('privacy-policy/', views.privacy_policy_page, name='privacy-policy'),  # Privacy policy
    path('terms-conditions/', views.terms_conditions_page, name='terms-conditions'),  # Terms and conditions
]