from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .forms import AboutPageForm
from .models import AboutPage


# View for the contact page.
def contact_page(request):
    return render(request, 'contact.html')

# View for the author page.
def author_page(request):
    return render(request, 'author.html')

# View for the privacy policy page.
def privacy_policy_page(request):
    return render(request, 'privacy-policy.html')

# View for the terms and conditions page.
def terms_conditions_page(request):
    return render(request, 'terms-conditions.html')

# View for the editable About page.
class AboutPageView(TemplateView):
    template_name = 'about_editable.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about, _ = AboutPage.objects.get_or_create(id=1) # Get or create AboutPage instance.
        context['about'] = about

        # Add the form for staff/superusers.
        if self.request.user.is_staff or self.request.user.is_superuser:
            context['form'] = AboutPageForm(instance=about)
        return context

    def post(self, request, *args, **kwargs):
        # Permission check for editing.
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "You don't have permission to edit this page.")
            return redirect('about')

        about, _ = AboutPage.objects.get_or_create(id=1)
        form = AboutPageForm(request.POST, request.FILES, instance=about)

        if form.is_valid():
            form.save()
            messages.success(request, "About page updated successfully.")
            return redirect('about')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form # Include invalid form in context.
            return render(request, self.template_name, context)