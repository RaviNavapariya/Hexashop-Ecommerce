from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm , UsernameField , UserChangeForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm


hobbies = [
    ('Football','Football'),
    ('Cricket','Cricket'),
    ('Basketball','Basketball'),
    ('Valleyball','Valleyball'),
    ]

gend = (
    ('male','Male'),
    ('female','Female'),
    )

typ = (
    ('buyer','Buyer'),
    ('seller','Seller'),
)


class SignupForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    hobby = forms.CharField(label='Select Hobbies',widget=forms.CheckboxSelectMultiple(choices=hobbies))
    gender = forms.CharField(label='Select Gender',widget=forms.RadioSelect(choices=gend))
    # user_type = forms.CharField(label='User type',widget=forms.RadioSelect(choices=typ))
    mob = forms.CharField(label='Contact Number',widget=forms.NumberInput(attrs={'class':'form-control'}))
    dob = forms.DateField(label = 'Date of Birth',widget=forms.DateInput(attrs={'class':'form-control'}))
    class Meta:
        model= User
        labels = {'username':'Username',
                   'first_name':'First Name',
                   'last_name':'Last Name',
                   'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
                    'first_name':forms.TextInput(attrs={'class':'form-control'}),
                    'last_name':forms.TextInput(attrs={'class':'form-control'}),
                    'email':forms.EmailInput(attrs={'class':'form-control'}),                    
                    }
        fields =['username','first_name','last_name','email','hobby','gender','dob','mob']
        

class LoginForm(AuthenticationForm):
    username = UsernameField(label='Username',widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Password',widget = forms.PasswordInput(attrs={'class':'form-control'}))

class UserEditForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'email':'Email'}

class AdminEditForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = "__all__"

class createproductform(ModelForm):
    class Meta:
        model=Product
        fields='__all__'
        labels = {'name':'Product Title','image':'Upload Product Image'}
