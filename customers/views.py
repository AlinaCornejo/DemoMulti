from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .models import Client
from products.models import Product, Order
from tenant_schemas.utils import tenant_context

class ClientListView(ListView):
    model = Client
    template_name = 'customers/client_list.html'
    def get_queryset(self):
        return Client.objects.exclude(schema_name='public')

class ClientCreateView(CreateView):
    model = Client
    fields = ['name', 'schema_name', 'paid_until', 'on_trial']
    template_name = 'customers/client_form.html'
    success_url = '/clients/'

def tenant_dashboard(request, tenant_id):
    tenant = Client.objects.get(id=tenant_id)
    with tenant_context(tenant):
        # Este código se ejecutará en el esquema del tenant
        products = Product.objects.all()
        orders = Order.objects.all()
        return render(request, 'tenant/dashboard.html', {
            'tenant': tenant,
            'products': products,
            'orders': orders,
        })
