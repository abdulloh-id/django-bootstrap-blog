from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from .forms import AboutPageForm, ContactForm
from .models import AboutPage, ContactMessage

from django.contrib.auth import get_user_model

User = get_user_model()

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            messages.success(request, _("Message sent successfully!"))
            return redirect('contact')
        else:
            form_errors = []
            for field, errors in form.errors.items():
                for error in errors:
                    label = form.fields[field].label or field.capitalize()
                    form_errors.append(f"{label}: {error}")
            
            # ИСПРАВЛЕНО: добавлен префикс папки 'pages/'
            return render(request, 'pages/contact.html', {
                'form': request.POST,
                'form_errors': form_errors
            })
            
    # ИСПРАВЛЕНО: добавлен префикс папки 'pages/'
    return render(request, 'pages/contact.html')

# View for the privacy policy page.
def privacy_policy_page(request):
    return render(request, 'pages/privacy-policy.html')

# View for the terms and conditions page.
def terms_conditions_page(request):
    return render(request, 'pages/terms-conditions.html')

# View for the editable About page.
class AboutPageView(TemplateView):
    template_name = 'pages/about_editable.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about, created = AboutPage.objects.get_or_create(id=1)
        context['about'] = about
        context['blog_owner'] = User.objects.filter(is_superuser=True).first()

        if self.request.user.is_staff or self.request.user.is_superuser:
            context['form'] = AboutPageForm(instance=about)
        return context

    def post(self, request, *args, **kwargs):
        # Permission check for editing.
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, _("You don't have permission to edit this page."))
            return redirect('about')

        about, created = AboutPage.objects.get_or_create(id=1)
        form = AboutPageForm(request.POST, request.FILES, instance=about)

        if form.is_valid():
            form.save()
            messages.success(request, _("About page updated successfully."))
            return redirect('about')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form # Include invalid form in context.
            return render(request, self.template_name, context)