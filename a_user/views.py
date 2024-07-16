from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import ProfileForm, EmailForm
from django.contrib.auth.models import User
from django.contrib import messages
from allauth.account.utils import send_email_confirmation

def profile_view(request):
    context = {
        'profile': request.user.profile
    }
    return render(request, 'a_user/profile.html', context)

@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
        
    if request.path == reverse('profile_onboarding'):
        onboarding = True
    else:
        onboarding = False
    return render(request, 'a_user/profile_edit.html', {'form': form, 'onboarding': onboarding})

@login_required
def profile_settings_view(request):
    return render(request, 'a_user/profile_settings.html')

@login_required
def profile_emailchange(request):
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form': form})
    
    if request.method == "POST":
        form = EmailForm(request.POST, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('profile_settings_view')
            form.save()

            # Then Signal updates email address and set verified to False

            # Then send confirmation email
            send_email_confirmation(request, request.user)
            return redirect('profile_settings_view')
        else:
            messages.warning(request, 'Form is not valid')
            return redirect('profile_settings_view')

    return redirect('index')

@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect('profile_settings_view')

@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted')
        return redirect('index')
    return render(request, 'a_user/profile_delete.html')