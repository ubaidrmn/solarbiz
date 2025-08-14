from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.db.models import Q
from core import forms
from core.models import Product


class ListProductsView(TemplateView):
    template_name = 'products.html'

    def _get_filters(self, request):
        return {
            'q': request.GET.get('q') or '',
            'price_min': request.GET.get('price_min') or '',
            'price_max': request.GET.get('price_max') or '',
            'product_type': request.GET.get('product_type') or '',
            'brand': request.GET.get('brand') or '',
            'warranty_min': request.GET.get('warranty_min') or '',
            'warranty_max': request.GET.get('warranty_max') or '',
        }

    def _apply_filters(self, qs, filters):
        if filters['q']:
            q = filters['q']
            qs = qs.filter(Q(description__icontains=q))
        if filters['price_min'] != '':
            try:
                qs = qs.filter(price__gte=float(filters['price_min']))
            except ValueError:
                pass
        if filters['price_max'] != '':
            try:
                qs = qs.filter(price__lte=float(filters['price_max']))
            except ValueError:
                pass
        if filters['product_type']:
            qs = qs.filter(product_type=filters['product_type'])
        if filters['brand']:
            qs = qs.filter(brand=filters['brand'])
        if filters['warranty_min'] != '':
            try:
                qs = qs.filter(warranty_years__gte=int(filters['warranty_min']))
            except ValueError:
                pass
        if filters['warranty_max'] != '':
            try:
                qs = qs.filter(warranty_years__lte=int(filters['warranty_max']))
            except ValueError:
                pass
        return qs

    def get(self, request, *args, **kwargs):
        form = forms.AddProductForm()
        filters = self._get_filters(request)
        products = Product.objects.all()
        products = self._apply_filters(products, filters).order_by('-id')
        return render(request, self.template_name, {
            'form': form,
            'products': products,
            'filters': filters,
            'product_type_choices': Product.ProductTypeChoices.choices,
            'brand_choices': Product.BrandChoices.choices,
        })

    def post(self, request, *args, **kwargs):
        form = forms.AddProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.description}" added successfully!')
            return redirect('products')
        else:
            messages.error(request, 'Failed to add product. Please correct the errors below.')
            products = Product.objects.all().order_by('-id')
            return render(request, self.template_name, {
                'form': form,
                'products': products,
                'filters': self._get_filters(request),
                'product_type_choices': Product.ProductTypeChoices.choices,
                'brand_choices': Product.BrandChoices.choices,
            })
