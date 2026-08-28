from django import forms
from django.core.exceptions import ValidationError
from .models import Payment

class PaymentForm(forms.ModelForm):
    """Advanced form for Payment with explicit validation logic."""
    class Meta:
        model = Payment
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

    def clean_method(self):
        data = self.cleaned_data.get('method')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_status(self):
        data = self.cleaned_data.get('status')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_transaction_reference(self):
        data = self.cleaned_data.get('transaction_reference')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_failure_reason(self):
        data = self.cleaned_data.get('failure_reason')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_card_type(self):
        data = self.cleaned_data.get('card_type')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_upi_id(self):
        data = self.cleaned_data.get('upi_id')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

