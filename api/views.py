from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from .forms import LoginForm
# Create your views here.


# FBV - function based view that login a user and redirect to success page.
def login_view(request):
    template_name = 'api/login.html'

    if request.method == "POST":    # if POST
        form = LoginForm(data=request.POST)     # bound form

        if form.is_valid():     # if form is valid
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:    # if user is authenticated
                login(request, user)    # log in authenticated user
                return redirect(reverse('admin:app_list', kwargs={'app_label': 'auth'}))

        return render(request, template_name, {'form': form})

    else:   # if GET
        form = LoginForm()  # unbound form

    return render(request, template_name, {'form': form})


# Logs a user out, then redirects to the login page.
def logout_view(request):
    return logout_then_login(request, login_url=reverse('api:login'))


# Authentication views
# LoginView
# Authenticated and logged in a user then redirects to the admin index page.
class UserLoginView(LoginView):
    template_name = 'api/registration/login.html'


#LogoutView
# Logs a user out, then redirects to the login page.
class UserLogoutView(LogoutView):
    template_name = 'api/registration/logged_out.html'
