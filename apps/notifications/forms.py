from django import forms
from django.core.exceptions import ValidationError
from .models import Notification

class NotificationForm(forms.ModelForm):
    """Advanced form for Notification with explicit validation logic."""
    class Meta:
        model = Notification
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

    def clean_notification_type(self):
        data = self.cleaned_data.get('notification_type')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_title(self):
        data = self.cleaned_data.get('title')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_message(self):
        data = self.cleaned_data.get('message')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_link(self):
        data = self.cleaned_data.get('link')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

