from django.contrib import admin
from .models import Recommendation
@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'score', 'reason', 'created_at')
    list_filter = ('reason',)
    search_fields = ('user__email', 'product__name')
