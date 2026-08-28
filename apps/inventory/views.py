from django.views.generic import ListView
from apps.accounts.permissions import SellerOrAdminRequiredMixin
from .models import Inventory

class InventoryListView(SellerOrAdminRequiredMixin, ListView):
    model = Inventory
    template_name = 'inventory/list.html'
    context_object_name = 'inventory_items'
    paginate_by = 25
    def get_queryset(self):
        user = self.request.user
        qs = Inventory.objects.select_related('product', 'product__seller')
        if user.is_seller:
            qs = qs.filter(product__seller=user)
        return qs.order_by('quantity')
