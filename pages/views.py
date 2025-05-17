from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView
from django.contrib import messages
from .models import AboutPage
from .forms import AboutPageForm

# View for the contact page
def contact_page(request):
    return render(request, 'contact.html')

# View for the author page
def author_page(request):
    return render(request, 'author.html')

# View for the privacy policy page
def privacy_policy_page(request):
    return render(request, 'privacy-policy.html')

# View for the terms and conditions page
def terms_conditions_page(request):
    return render(request, 'terms-conditions.html')

class AboutPageView(TemplateView):
    template_name = 'about_editable.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about, created = AboutPage.objects.get_or_create(id=1)
        context['about'] = about
        
        # Add the form only if user is staff or superuser
        if self.request.user.is_staff or self.request.user.is_superuser:
            context['form'] = AboutPageForm(instance=about)
            
        return context
    
    def post(self, request, *args, **kwargs):
        # Only allow staff or superusers to edit
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "You don't have permission to edit this page.")
            return redirect('about')
        
        about, created = AboutPage.objects.get_or_create(id=1)
        form = AboutPageForm(request.POST, request.FILES, instance=about)
        
        if form.is_valid():
            form.save()
            messages.success(request, "About page updated successfully.")
            return redirect('about')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, self.template_name, context)