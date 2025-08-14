from django.shortcuts import render
from django.views.generic import TemplateView


class ListQuotationsView(TemplateView):
    template_name = 'quotations.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class CreateQuotationsView(TemplateView):
    template_name = 'quotations_create.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    # def post(self, request, *args, **kwargs):
    #     form = forms.AddProductForm(request.POST)
    #     if form.is_valid():
    #         product = form.save()
    #         messages.success(request, f'Quotation "{product.description}" created successfully!')
    #         return redirect('quotations')
    #     else:
    #         messages.error(request, 'Failed to create quotation. Please correct the errors below.')
    #         return render(request, self.template_name, {'form': form})
