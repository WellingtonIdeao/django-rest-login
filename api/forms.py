from django import forms


# login form
class LoginForm(forms.Form):
    username = forms.CharField(label='Name', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
