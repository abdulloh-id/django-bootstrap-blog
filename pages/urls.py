from django.contrib.auth.views import LogoutView
from django.urls import path

from articles.views import HomepageView  # Import HomepageView from articles app
from .views import AboutPageView
from . import views


# URL patterns for class-based views.
urlpatterns = [
    path('', HomepageView.as_view(), name='home'),  # Use HomepageView for the main homepage.
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'), # Logout functionality.
    path('about/', AboutPageView.as_view(), name='about'), # About page.
]

# URL patterns for function-based views (appending to urlpatterns).
urlpatterns += [
    path('contact/', views.contact_page, name='contact'),  # Contact page.
    path('author/', views.author_page, name='author'),  # Author information page.
    path('privacy-policy/', views.privacy_policy_page, name='privacy-policy'),  # Privacy policy page.
    path('terms-conditions/', views.terms_conditions_page, name='terms-conditions'),  # Terms and conditions page.
]