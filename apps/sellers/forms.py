from django import forms
from django.core.exceptions import ValidationError
from .models import SellerProfile

class SellerProfileForm(forms.ModelForm):
    """Advanced form for SellerProfile with explicit validation logic."""
    class Meta:
        model = SellerProfile
        fields = '__all__'
        widgets = {
            # Provide default styling classes
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field.required:
                field.widget.attrs['required'] = 'required'

    def clean_business_name(self):
        data = self.cleaned_data.get('business_name')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_business_phone(self):
        data = self.cleaned_data.get('business_phone')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_business_address(self):
        data = self.cleaned_data.get('business_address')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_gst_number(self):
        data = self.cleaned_data.get('gst_number')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_pan_number(self):
        data = self.cleaned_data.get('pan_number')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_bank_account(self):
        data = self.cleaned_data.get('bank_account')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_ifsc_code(self):
        data = self.cleaned_data.get('ifsc_code')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_verification_status(self):
        data = self.cleaned_data.get('verification_status')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_bio(self):
        data = self.cleaned_data.get('bio')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

