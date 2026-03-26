from django.urls import path
from . import views

urlpatterns = [
    # Static Informational Pages
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('author/', views.author_page, name='author'),
    
    # Legal / Compliance Pages
    path('privacy-policy/', views.privacy_policy_page, name='privacy-policy'),
    path('terms-conditions/', views.terms_conditions_page, name='terms-conditions'),
]