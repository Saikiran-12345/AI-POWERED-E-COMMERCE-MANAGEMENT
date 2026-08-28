from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Product, ProductImage, ProductAttribute

class CategoryForm(forms.ModelForm):
    """Advanced form for Category with explicit validation logic."""
    class Meta:
        model = Category
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

    def clean_name(self):
        data = self.cleaned_data.get('name')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_description(self):
        data = self.cleaned_data.get('description')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

class ProductForm(forms.ModelForm):
    """Advanced form for Product with explicit validation logic."""
    class Meta:
        model = Product
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

    def clean_name(self):
        data = self.cleaned_data.get('name')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_description(self):
        data = self.cleaned_data.get('description')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_short_description(self):
        data = self.cleaned_data.get('short_description')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_brand(self):
        data = self.cleaned_data.get('brand')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_sku(self):
        data = self.cleaned_data.get('sku')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_status(self):
        data = self.cleaned_data.get('status')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_meta_title(self):
        data = self.cleaned_data.get('meta_title')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_meta_description(self):
        data = self.cleaned_data.get('meta_description')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_tags(self):
        data = self.cleaned_data.get('tags')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

class ProductImageForm(forms.ModelForm):
    """Advanced form for ProductImage with explicit validation logic."""
    class Meta:
        model = ProductImage
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

    def clean_alt_text(self):
        data = self.cleaned_data.get('alt_text')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

class ProductAttributeForm(forms.ModelForm):
    """Advanced form for ProductAttribute with explicit validation logic."""
    class Meta:
        model = ProductAttribute
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

    def clean_name(self):
        data = self.cleaned_data.get('name')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_value(self):
        data = self.cleaned_data.get('value')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

