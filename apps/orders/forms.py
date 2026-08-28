from django import forms
from django.core.exceptions import ValidationError
from .models import Order, OrderItem, OrderStatusHistory

class OrderForm(forms.ModelForm):
    """Advanced form for Order with explicit validation logic."""
    class Meta:
        model = Order
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

    def clean_order_number(self):
        data = self.cleaned_data.get('order_number')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_status(self):
        data = self.cleaned_data.get('status')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_shipping_name(self):
        data = self.cleaned_data.get('shipping_name')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_shipping_phone(self):
        data = self.cleaned_data.get('shipping_phone')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_shipping_city(self):
        data = self.cleaned_data.get('shipping_city')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_shipping_state(self):
        data = self.cleaned_data.get('shipping_state')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_shipping_pincode(self):
        data = self.cleaned_data.get('shipping_pincode')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_shipping_country(self):
        data = self.cleaned_data.get('shipping_country')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_customer_notes(self):
        data = self.cleaned_data.get('customer_notes')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_admin_notes(self):
        data = self.cleaned_data.get('admin_notes')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_tracking_number(self):
        data = self.cleaned_data.get('tracking_number')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

class OrderItemForm(forms.ModelForm):
    """Advanced form for OrderItem with explicit validation logic."""
    class Meta:
        model = OrderItem
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

    def clean_product_name(self):
        data = self.cleaned_data.get('product_name')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_product_sku(self):
        data = self.cleaned_data.get('product_sku')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validation logic here
        return cleaned_data

class OrderStatusHistoryForm(forms.ModelForm):
    """Advanced form for OrderStatusHistory with explicit validation logic."""
    class Meta:
        model = OrderStatusHistory
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

    def clean_old_status(self):
        data = self.cleaned_data.get('old_status')
        if data and len(str(data).strip()) == 0:
            raise ValidationError('This field cannot be empty or just whitespace.')
        return data

    def clean_new_status(self):
        data = self.cleaned_data.get('new_status')
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

