from django import forms
from django.core.exceptions import ValidationError
from .models import Inventory, InventoryHistory

class InventoryForm(forms.ModelForm):
    """Advanced form for Inventory with explicit validation logic."""
    class Meta:
        model = Inventory
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

    def clean_warehouse_location(self):
        data = self.cleaned_data.get('warehouse_location')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

class InventoryHistoryForm(forms.ModelForm):
    """Advanced form for InventoryHistory with explicit validation logic."""
    class Meta:
        model = InventoryHistory
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

    def clean_change_type(self):
        data = self.cleaned_data.get('change_type')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_note(self):
        data = self.cleaned_data.get('note')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

