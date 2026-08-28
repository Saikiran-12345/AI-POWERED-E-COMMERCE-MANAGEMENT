from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.permissions import SellerRequiredMixin, AdminRequiredMixin
from django.views.generic import ListView
from .models import SellerProfile

class SellerListView(AdminRequiredMixin, ListView):
    model = SellerProfile
    template_name = 'sellers/list.html'
    context_object_name = 'sellers'
    paginate_by = 25
