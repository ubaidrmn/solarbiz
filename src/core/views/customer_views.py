from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.db.models import Q
from core import forms
from core.models import Customer


class ListCustomersView(TemplateView):
    template_name = 'customers.html'

    def _get_filters(self, request):
        return {
            'city': request.GET.get('city') or '',
            'system_type': request.GET.get('system_type') or '',
            'structure_type': request.GET.get('structure_type') or '',
            'rating_min': request.GET.get('rating_min') or '',
            'rating_max': request.GET.get('rating_max') or '',
            'has_notes': (request.GET.get('has_notes') == 'on') or False,
            'q': request.GET.get('q') or '',
        }

    def _apply_filters(self, qs, filters):
        if filters['city']:
            qs = qs.filter(city=filters['city'])
        if filters['has_notes']:
            qs = qs.exclude(notes__isnull=True).exclude(notes__exact='')
        if filters['q']:
            q = filters['q']
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(phone__icontains=q) |
                Q(address__icontains=q) |
                Q(notes__icontains=q)
            )
        return qs

    def get(self, request, *args, **kwargs):
        form = forms.AddCustomerForm()
        filters = self._get_filters(request)
        customers = Customer.objects.all()
        customers = self._apply_filters(customers, filters).order_by('-id')
        return render(request, self.template_name, {
            'form': form,
            'customers': customers,
            'filters': filters,
            'city_choices': Customer.CityChoices.choices,
        })

    def post(self, request, *args, **kwargs):
        form = forms.AddCustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer "{customer.name}" added successfully!')
            return redirect('customers')
        else:
            messages.error(request, 'Failed to add customer. Please correct the errors below.')
            customers = Customer.objects.all().order_by('-id')
            return render(request, self.template_name, {
                'form': form,
                'customers': customers,
                'filters': self._get_filters(request),
                'city_choices': Customer.CityChoices.choices,
                'system_type_choices': Customer.SystemTypeChoices.choices,
                'structure_type_choices': Customer.StructureType.choices,
            })
