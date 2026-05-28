from django.urls import path

from . import views

urlpatterns = [
    # Static Informational Pages
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('contact/', views.contact_view, name='contact'),
    
    # Legal / Compliance Pages
    path('privacy-policy/', views.privacy_policy_page, name='privacy-policy'),
    path('terms-conditions/', views.terms_conditions_page, name='terms-conditions'),
]