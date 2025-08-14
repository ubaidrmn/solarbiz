from django.contrib import admin
from core.models import User, SalesRepresentative, Product, Quotation, QuotationItem, Customer

admin.site.register(User)
admin.site.register(SalesRepresentative)
admin.site.register(Product)
admin.site.register(Quotation)
admin.site.register(QuotationItem)
admin.site.register(Customer)
