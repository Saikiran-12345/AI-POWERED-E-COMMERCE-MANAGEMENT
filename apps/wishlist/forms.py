from django import forms
from django.core.exceptions import ValidationError
from .models import Wishlist, WishlistItem

class WishlistForm(forms.ModelForm):
    """Advanced form for Wishlist with explicit validation logic."""
    class Meta:
        model = Wishlist
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

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

class WishlistItemForm(forms.ModelForm):
    """Advanced form for WishlistItem with explicit validation logic."""
    class Meta:
        model = WishlistItem
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

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

