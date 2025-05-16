
from django.urls import path
from .views import (ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
                    OrderListView, OrderCreateView, OrderDetailView)

urlpatterns = [
    # Productos
    path('', ProductListView.as_view(), name='product-list'),
    path('add/', ProductCreateView.as_view(), name='product-add'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='product-edit'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    
    # Órdenes
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/add/', OrderCreateView.as_view(), name='order-add'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]