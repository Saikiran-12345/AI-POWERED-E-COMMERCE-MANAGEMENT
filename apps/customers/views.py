from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.permissions import AdminRequiredMixin
from django.views.generic import ListView
from .models import Customer

class CustomerListView(AdminRequiredMixin, ListView):
    model = Customer
    template_name = 'customers/list.html'
    context_object_name = 'customers'
    paginate_by = 25
    def get_queryset(self):
        return Customer.objects.select_related('user').order_by('-created_at')
