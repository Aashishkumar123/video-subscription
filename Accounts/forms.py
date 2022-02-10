from django import forms
from django_countries.widgets import CountrySelectWidget
from .models import Profile, phone_regex
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def email_exist(value):
    if User.objects.filter(email=value).exists():
        raise forms.ValidationError("Profile with this Email Address already exists")

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[email_exist],widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
    attrs={'class':'form-control','type':'password', 'name': 'password','placeholder':'Password'}),
    label='')
    password2 = forms.CharField(widget=forms.PasswordInput(
    attrs={'class':'form-control','type':'password', 'name': 'password','placeholder':'Confirm Password'}),
    label='')
    class Meta:
        model = User
        fields  =['username','email']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'username'}),
        }

    

class UserProfileForm(forms.ModelForm):
    def digit(value):
        if len(value) < 10:
            raise forms.ValidationError('Phone number should contains 10 digits')
    phone_number = forms.CharField(max_length=17,validators=[phone_regex,digit],widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Mobile number'}))
    
    class Meta:
        model = Profile
        fields = ['phone_number']

class CtryForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['country']
        widgets = {'country': CountrySelectWidget(attrs={'class':'form-select'})}

        