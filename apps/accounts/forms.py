"""
Forms for the accounts application.

Includes registration, login, profile update, and password change forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, UserRole


class UserRegistrationForm(forms.ModelForm):
    """
    Form for user registration.
    Validates email uniqueness, password strength, and role selection.
    """

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'autocomplete': 'new-password',
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password',
        }),
        help_text=_('Enter the same password as before, for verification.'),
    )
    role = forms.ChoiceField(
        choices=[
            (UserRole.CUSTOMER, 'Customer - Shop products'),
            (UserRole.SELLER, 'Seller - Sell your products'),
        ],
        initial=UserRole.CUSTOMER,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text=_('Select your account type.'),
    )
    terms_accepted = forms.BooleanField(
        required=True,
        label=_('I accept the Terms and Conditions'),
        error_messages={'required': _('You must accept the terms and conditions.')},
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'role')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number (optional)',
            }),
        }

    def clean_email(self) -> str:
        """Validate that email is unique."""
        email = self.cleaned_data.get('email', '').lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _('An account with this email address already exists.')
            )
        return email

    def clean_password2(self) -> str:
        """Validate that both passwords match."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('The two password fields didn\'t match.'))
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit: bool = True) -> User:
        """Save user with hashed password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Custom login form with email-based authentication.
    """

    username = forms.EmailField(
        label=_('Email Address'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'current-password',
        }),
    )
    remember_me = forms.BooleanField(
        required=False,
        label=_('Remember me'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    error_messages = {
        'invalid_login': _(
            'Please enter a correct email address and password. '
            'Note that both fields may be case-sensitive.'
        ),
        'inactive': _('This account is inactive. Please contact support.'),
    }


class UserProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user basic information.
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'avatar')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class UserProfileDetailForm(forms.ModelForm):
    """
    Form for updating extended profile details.
    """

    class Meta:
        model = UserProfile
        fields = (
            'bio', 'date_of_birth', 'gender',
            'address_line1', 'address_line2', 'city',
            'state', 'pincode', 'country',
            'newsletter_subscribed', 'email_notifications',
        )
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address_line1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street address',
            }),
            'address_line2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apartment, suite, etc.',
            }),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PIN code'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'newsletter_subscribed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Custom password change form with styled widgets.
    """

    old_password = forms.CharField(
        label=_('Current password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Current password',
        }),
    )
    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'New password',
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_('Confirm new password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'Confirm new password',
        }),
    )
