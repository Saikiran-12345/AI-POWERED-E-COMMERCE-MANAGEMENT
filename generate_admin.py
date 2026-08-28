import os
import re

apps = [
    "audit", "cart", "wishlist", "orders", 
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
        admin_code = f"from django.contrib import admin\nfrom .models import {', '.join(models)}\n\n"
        for model in models:
            # Extract fields for this model to populate list_display
            model_block = re.search(fr"class {model}\(.*?Model\):(.*?)(?=\nclass |\Z)", content, re.DOTALL)
            fields = []
            if model_block:
                fields = re.findall(r"^\s+([a-z_]+)\s*=\s*models\.", model_block.group(1), re.MULTILINE)
            
            list_display = ["'id'"] + [f"'{f}'" for f in fields[:5]]
            search_fields = [f"'{f}'" for f in fields if 'name' in f or 'title' in f or 'email' in f]
            list_filter = [f"'{f}'" for f in fields if 'status' in f or 'is_' in f or 'type' in f]
            
            admin_code += f"@admin.register({model})\nclass {model}Admin(admin.ModelAdmin):\n"
            admin_code += f"    list_display = [{', '.join(list_display)}]\n"
            if search_fields:
                admin_code += f"    search_fields = [{', '.join(search_fields)}]\n"
            if list_filter:
                admin_code += f"    list_filter = [{', '.join(list_filter)}]\n"
            admin_code += f"    list_per_page = 50\n\n"
            
        with open(os.path.join(root_dir, "apps", app, "admin.py"), "w", encoding="utf-8") as f:
            f.write(admin_code)

print("Generated Admin configs successfully!")
