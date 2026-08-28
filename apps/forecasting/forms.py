from django import forms
from django.core.exceptions import ValidationError
from .models import DemandForecast

class DemandForecastForm(forms.ModelForm):
    """Advanced form for DemandForecast with explicit validation logic."""
    class Meta:
        model = DemandForecast
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

    def clean_model_version(self):
        data = self.cleaned_data.get('model_version')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

