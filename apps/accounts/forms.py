from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User, UserProfile

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=20, required=False)
    terms_accepted = forms.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'role')

class UserLoginForm(forms.Form):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    remember_me = forms.BooleanField(required=False)

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address_line1', 'address_line2', 'city', 'state', 'pincode', 'country')

class UserProfileDetailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number')

class CustomPasswordChangeForm(PasswordChangeForm):
    pass
