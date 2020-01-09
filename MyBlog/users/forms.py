from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea

from .models import Profile


class UserRegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter the username'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter the first name'}))
    email = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter the email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter the password'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter the password'}))


    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if User.objects.filter(username=username).exists():
            self.add_error('username', "Username already exists")
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already exists')
        if password != repeat_password:
            self.add_error('password', 'password mismatch')
            self.add_error('repeat_password', 'password mismatch')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        labels = {
            'first_name': 'Name'
        }


class ProfileUpdateFrom(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'about']
        widgets = {
            'about': Textarea(attrs={'cols': 30, 'rows': 5}),
        }


class ForgetPasswordForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'placeholder':'Enter the email'}))


class ResetPasswordForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    repeatpassword = forms.CharField(max_length=32, widget=forms.PasswordInput)
    otp = forms.CharField(max_length=10)

