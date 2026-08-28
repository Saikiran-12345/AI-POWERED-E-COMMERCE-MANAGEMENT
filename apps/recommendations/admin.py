from django.contrib import admin
from .models import Recommendation

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'score', 'reason', 'created_at']
    list_per_page = 50

