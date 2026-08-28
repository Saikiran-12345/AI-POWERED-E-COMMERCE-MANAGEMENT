from django import forms
from django.core.exceptions import ValidationError
from .models import AuditLog

class AuditLogForm(forms.ModelForm):
    """Advanced form for AuditLog with explicit validation logic."""
    class Meta:
        model = AuditLog
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

    def clean_action(self):
        data = self.cleaned_data.get('action')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_module(self):
        data = self.cleaned_data.get('module')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_description(self):
        data = self.cleaned_data.get('description')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_object_type(self):
        data = self.cleaned_data.get('object_type')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_object_id(self):
        data = self.cleaned_data.get('object_id')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_user_agent(self):
        data = self.cleaned_data.get('user_agent')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

