from django.urls import path, include
from core.views import customer_views, quotation_views, product_views, dashboard_views, documentation_views

urlpatterns = [
    path('', dashboard_views.DashboardView.as_view(), name='dashboard'),
    path('customers/', customer_views.ListCustomersView.as_view(), name='customers'),
    path('quotations/', quotation_views.ListQuotationsView.as_view(), name='quotations'),
    path('quotations/create/', quotation_views.CreateQuotationsView.as_view(), name='quotations_create'),
    path('products/', product_views.ListProductsView.as_view(), name='products'),
]
