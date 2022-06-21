from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView,\
    PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,\
    PasswordResetCompleteView, logout_then_login
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


# LogoutView
# Logs a user out, then redirects to the login page.
class UserLogoutView(LogoutView):
    template_name = 'api/registration/logged_out.html'


# PasswordChangeView
# Allows a user to change their password.
class UserPasswordChangeView(PasswordChangeView):
    template_name = 'api/registration/password_change_form.html'
    success_url = reverse_lazy('api:password_change_done')


# PasswordChangeDoneView
# The page shown after a user changed their password.
# called by success_url in PasswordChangeView.
class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'api/registration/password_change_done.html'


# PasswordResetView
# Allows a user to reset their password, by generating a one-time use link, and sending that link to user email.
class UserPasswordResetView(PasswordResetView):
    template_name = 'api/registration/password_reset_form.html'
    success_url = reverse_lazy('api:password_reset_done')
    email_template_name = 'api/registration/password_reset_email.html'


# PasswordResetDoneView
# the page shown after a user reset their password in Password reset view.
# called by success_url in PasswordResetView
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'api/registration/password_reset_done.html'


# PasswordResetConfirmView
# called by a one-time use link in the email send by PasswordResetView.
# set new password for a user.
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'api/registration/password_reset_confirm.html'
    success_url = reverse_lazy('api:password_reset_complete')


# the page shown to confirm that user password is changed.
class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'api/registration/password_reset_complete.html'
