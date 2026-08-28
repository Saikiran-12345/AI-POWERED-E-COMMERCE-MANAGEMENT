import os
import re

apps = [
    "accounts", "audit", "cart", "wishlist", "orders", 
    "inventory", "payments", "customers", "sellers", "reviews",
    "recommendations", "analytics", "forecasting", 
    "fraud_detection", "reports", "notifications", "products"
]

root_dir = r"d:\E-COMMERCE MANAGEMENT & RECOMMENDATION SAAS"

for app in apps:
    models_file = os.path.join(root_dir, "apps", app, "models.py")
    if not os.path.exists(models_file):
        continue
        
    with open(models_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    models = re.findall(r"^class\s+([A-Za-z0-9_]+)\(.*?Model\):", content, re.MULTILINE)
    
    if models:
        factories_code = f"import factory\nfrom django.utils import timezone\nfrom faker import Faker\nfrom .models import {', '.join(models)}\n\nfake = Faker()\n\n"
        for model in models:
            factories_code += f"class {model}Factory(factory.django.DjangoModelFactory):\n"
            factories_code += f"    class Meta:\n"
            factories_code += f"        model = {model}\n\n"
            
            # Simple attribute mocks
            model_block = re.search(fr"class {model}\(.*?Model\):(.*?)(?=\nclass |\Z)", content, re.DOTALL)
            if model_block:
                fields = re.findall(r"^\s+([a-z_]+)\s*=\s*models\.(.*?)\(", model_block.group(1), re.MULTILINE)
                for field_name, field_type in fields:
                    if 'CharField' in field_type:
                        if 'email' in field_name:
                            factories_code += f"    {field_name} = factory.LazyAttribute(lambda _: fake.email())\n"
                        elif 'name' in field_name:
                            factories_code += f"    {field_name} = factory.LazyAttribute(lambda _: fake.name())\n"
                        else:
                            factories_code += f"    {field_name} = factory.LazyAttribute(lambda _: fake.word())\n"
                    elif 'TextField' in field_type:
                        factories_code += f"    {field_name} = factory.LazyAttribute(lambda _: fake.text())\n"
                    elif 'IntegerField' in field_type or 'DecimalField' in field_type or 'FloatField' in field_type:
                        factories_code += f"    {field_name} = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=1000))\n"
                    elif 'BooleanField' in field_type:
                        factories_code += f"    {field_name} = factory.LazyAttribute(lambda _: fake.boolean())\n"
                    elif 'DateTimeField' in field_type or 'DateField' in field_type:
                        factories_code += f"    {field_name} = factory.LazyFunction(timezone.now)\n"
            factories_code += "\n"
            
        with open(os.path.join(root_dir, "apps", app, "factories.py"), "w", encoding="utf-8") as f:
            f.write(factories_code)

print("Generated Factories successfully!")
