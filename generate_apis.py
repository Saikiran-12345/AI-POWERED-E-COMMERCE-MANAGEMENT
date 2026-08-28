import os
import re

apps = [
    "accounts", "audit", "cart", "wishlist", "orders", 
    "inventory", "payments", "customers", "sellers", "reviews",
    "recommendations", "analytics", "forecasting", 
    "fraud_detection", "reports", "notifications"
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
        # Generate serializers
        serializers_code = f"from rest_framework import serializers\nfrom .models import {', '.join(models)}\n\n"
        for model in models:
            serializers_code += f"class {model}Serializer(serializers.ModelSerializer):\n    class Meta:\n        model = {model}\n        fields = '__all__'\n\n"
            
        with open(os.path.join(root_dir, "apps", app, "serializers.py"), "w", encoding="utf-8") as f:
            f.write(serializers_code)
            
        # Generate API ViewSets
        serializers_list = ", ".join([f"{m}Serializer" for m in models])
        api_code = f"from rest_framework import viewsets, filters\nfrom django_filters.rest_framework import DjangoFilterBackend\nfrom .models import {', '.join(models)}\nfrom .serializers import {serializers_list}\n\n"
        for model in models:
            api_code += f"class {model}ViewSet(viewsets.ModelViewSet):\n    queryset = {model}.objects.all()\n    serializer_class = {model}Serializer\n    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]\n    ordering_fields = '__all__'\n\n"
            
        with open(os.path.join(root_dir, "apps", app, "api.py"), "w", encoding="utf-8") as f:
            f.write(api_code)
            
        # Generate API URLs
        viewsets_list = ", ".join([f"{m}ViewSet" for m in models])
        urls_code = f"from django.urls import path, include\nfrom rest_framework.routers import DefaultRouter\nfrom .api import {viewsets_list}\n\nrouter = DefaultRouter()\n"
        for model in models:
            urls_code += f"router.register(r'{model.lower()}s', {model}ViewSet)\n"
        urls_code += f"\napp_name = 'api_{app}'\nurlpatterns = [\n    path('', include(router.urls)),\n]\n"
        
        with open(os.path.join(root_dir, "apps", app, "api_urls.py"), "w", encoding="utf-8") as f:
            f.write(urls_code)

print("Generated APIs successfully!")
