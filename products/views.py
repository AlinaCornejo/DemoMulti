
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from .models import Product, Order
from tenant_schemas.utils import tenant_context

class ProductListView(ListView):
    model = Product
    template_name = 'tenant/product_list.html'
    context_object_name = 'products'

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'price']
    template_name = 'tenant/product_form.html'
    def get_success_url(self):
        return reverse('tenant-dashboard', kwargs={'tenant_id': self.request.tenant.id})

    def form_valid(self, form):
        with tenant_context(self.request.tenant):
            return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'price']
    template_name = 'tenant/product_form.html'
    def get_success_url(self):
        return reverse('tenant-dashboard', kwargs={'tenant_id': self.request.tenant.id})

    def get_object(self):
        with tenant_context(self.request.tenant):
            return get_object_or_404(Product, pk=self.kwargs['pk'])

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'tenant/product_confirm_delete.html'
    def get_success_url(self):
        return reverse('tenant-dashboard', kwargs={'tenant_id': self.request.tenant.id})
    def get_object(self):
        with tenant_context(self.request.tenant):
            return get_object_or_404(Product, pk=self.kwargs['pk'])



class OrderListView(ListView):
    model = Order
    template_name = 'tenant/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        with tenant_context(self.request.tenant):
            return Order.objects.select_related('product').all()

class OrderCreateView(CreateView):
    model = Order
    fields = ['product', 'quantity']
    template_name = 'tenant/order_form.html'
    def get_success_url(self):
        return reverse('tenant-dashboard', kwargs={'tenant_id': self.request.tenant.id})

    def get_form(self, form_class=None):
        with tenant_context(self.request.tenant):
            form = super().get_form(form_class)
            form.fields['product'].queryset = Product.objects.all()
            return form

    def form_valid(self, form):
        with tenant_context(self.request.tenant):
            return super().form_valid(form)

class OrderDetailView(DetailView):
    model = Order
    template_name = 'tenant/order_detail.html'

    def get_object(self):
        with tenant_context(self.request.tenant):
            return get_object_or_404(Order.objects.select_related('product'), pk=self.kwargs['pk'])