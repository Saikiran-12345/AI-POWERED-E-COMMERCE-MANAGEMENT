import os
import re

apps = [
    "accounts", "audit", "cart", "wishlist", "orders", 
    "inventory", "payments", "customers", "sellers", "reviews",
    "recommendations", "analytics", "forecasting", 
    "fraud_detection", "reports", "notifications", "products"
]

root_dir = r"d:\E-COMMERCE MANAGEMENT & RECOMMENDATION SAAS"

def generate_services_and_forms():
    for app in apps:
        models_file = os.path.join(root_dir, "apps", app, "models.py")
        if not os.path.exists(models_file):
            continue
            
        with open(models_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        models = re.findall(r"^class\s+([A-Za-z0-9_]+)\(.*?Model\):", content, re.MULTILINE)
        if not models:
            continue
            
        # 1. Generate Massive Forms (forms.py)
        forms_code = "from django import forms\nfrom django.core.exceptions import ValidationError\n"
        forms_code += f"from .models import {', '.join(models)}\n\n"
        
        for model in models:
            forms_code += f"class {model}Form(forms.ModelForm):\n"
            forms_code += f"    \"\"\"Advanced form for {model} with explicit validation logic.\"\"\"\n"
            forms_code += f"    class Meta:\n"
            forms_code += f"        model = {model}\n"
            forms_code += f"        fields = '__all__'\n"
            forms_code += f"        widgets = {{\n"
            forms_code += f"            # Provide default styling classes\n"
            forms_code += f"        }}\n\n"
            
            forms_code += f"    def __init__(self, *args, **kwargs):\n"
            forms_code += f"        super().__init__(*args, **kwargs)\n"
            forms_code += f"        for field_name, field in self.fields.items():\n"
            forms_code += f"            field.widget.attrs['class'] = 'form-control'\n"
            forms_code += f"            if field.required:\n"
            forms_code += f"                field.widget.attrs['required'] = 'required'\n\n"
            
            # Add explicit clean methods for all fields
            model_block = re.search(fr"class {model}\(.*?Model\):(.*?)(?=\nclass |\Z)", content, re.DOTALL)
            if model_block:
                fields = re.findall(r"^\s+([a-z_]+)\s*=\s*models\.(.*?)\(", model_block.group(1), re.MULTILINE)
                for field_name, field_type in fields:
                    if 'CharField' in field_type or 'TextField' in field_type:
                        forms_code += f"    def clean_{field_name}(self):\n"
                        forms_code += f"        data = self.cleaned_data.get('{field_name}')\n"
                        forms_code += f"        if data and len(str(data).strip()) == 0:\n"
                        forms_code += f"            raise ValidationError('This field cannot be empty or just whitespace.')\n"
                        forms_code += f"        return data\n\n"
                        
            forms_code += f"    def clean(self):\n"
            forms_code += f"        cleaned_data = super().clean()\n"
            forms_code += f"        # Add cross-field validation logic here\n"
            forms_code += f"        return cleaned_data\n\n"
            
        with open(os.path.join(root_dir, "apps", app, "forms.py"), "w", encoding="utf-8") as f:
            f.write(forms_code)
            
        # 2. Generate Service Layer (services.py)
        services_code = "import logging\nfrom django.db import transaction\nfrom django.core.exceptions import ObjectDoesNotExist\n"
        services_code += f"from .models import {', '.join(models)}\n\n"
        services_code += "logger = logging.getLogger(__name__)\n\n"
        
        for model in models:
            services_code += f"class {model}Service:\n"
            services_code += f"    \"\"\"Service layer for {model} to abstract business logic from views and serializers.\"\"\"\n\n"
            
            services_code += f"    @classmethod\n"
            services_code += f"    def get_by_id(cls, obj_id: int) -> {model}:\n"
            services_code += f"        try:\n"
            services_code += f"            return {model}.objects.get(id=obj_id)\n"
            services_code += f"        except {model}.DoesNotExist:\n"
            services_code += f"            logger.error(f'{model} with id {{obj_id}} not found.')\n"
            services_code += f"            raise ObjectDoesNotExist(f'{model} not found')\n\n"
            
            services_code += f"    @classmethod\n"
            services_code += f"    @transaction.atomic\n"
            services_code += f"    def create(cls, **kwargs) -> {model}:\n"
            services_code += f"        \"\"\"Create a new {model} instance securely.\"\"\"\n"
            services_code += f"        logger.info(f'Creating {model} with data: {{kwargs}}')\n"
            services_code += f"        instance = {model}(**kwargs)\n"
            services_code += f"        instance.full_clean()\n"
            services_code += f"        instance.save()\n"
            services_code += f"        return instance\n\n"
            
            services_code += f"    @classmethod\n"
            services_code += f"    @transaction.atomic\n"
            services_code += f"    def update(cls, instance: {model}, **kwargs) -> {model}:\n"
            services_code += f"        \"\"\"Update an existing {model} instance.\"\"\"\n"
            services_code += f"        logger.info(f'Updating {model} {{instance.id}} with data: {{kwargs}}')\n"
            services_code += f"        for key, value in kwargs.items():\n"
            services_code += f"            setattr(instance, key, value)\n"
            services_code += f"        instance.full_clean()\n"
            services_code += f"        instance.save()\n"
            services_code += f"        return instance\n\n"
            
            services_code += f"    @classmethod\n"
            services_code += f"    @transaction.atomic\n"
            services_code += f"    def delete(cls, instance: {model}) -> bool:\n"
            services_code += f"        \"\"\"Delete a {model} instance.\"\"\"\n"
            services_code += f"        logger.warning(f'Deleting {model} {{instance.id}}')\n"
            services_code += f"        instance.delete()\n"
            services_code += f"        return True\n\n"
            
            services_code += f"    @classmethod\n"
            services_code += f"    def get_all_active(cls):\n"
            services_code += f"        \"\"\"Retrieve all active {model} instances if applicable.\"\"\"\n"
            services_code += f"        if hasattr({model}, 'is_active'):\n"
            services_code += f"            return {model}.objects.filter(is_active=True)\n"
            services_code += f"        elif hasattr({model}, 'status'):\n"
            services_code += f"            return {model}.objects.filter(status='ACTIVE')\n"
            services_code += f"        return {model}.objects.all()\n\n"
            
        with open(os.path.join(root_dir, "apps", app, "services.py"), "w", encoding="utf-8") as f:
            f.write(services_code)

generate_services_and_forms()
print("Generated Forms and Services layer.")
