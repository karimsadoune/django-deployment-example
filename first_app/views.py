from django.shortcuts import render
from django.http import HttpResponse
from first_app.models import UserProfileInfo
from first_app.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'first_app/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def special(request):
    return HttpResponse("Your are logged in, Nice!")

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save user and hash password
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Save profile info
            profile = profile_form.save(commit=False)
            profile.user = user

            # Handle profile picture if uploaded
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'first_app/registration.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user:
            if user.is_active:
                # Log the user in
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account is not active.')
        else:
            # Avoid printing sensitive data for security reasons
            return HttpResponse('Invalid login details provided.')
    else:
        # Render the login page
        return render(request, 'first_app/login.html', {})