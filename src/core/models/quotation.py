from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError


class Quotation(models.Model):

    class SystemTypeChoices(models.TextChoices):
        OFF_GRID = 'OFF_GRID', 'Off Grid'
        ON_GRID = 'ON_GRID', 'On Grid'
        HYBRID = 'HYBRID', 'Hybrid'

    class StructureType(models.TextChoices):
        ELEVATED = 'ELEVATED', 'Elevated'
        SURFACE_MOUNTED = 'SURFACE_MOUNTED', 'Surface Mounted'

    system_type = models.CharField(choices=SystemTypeChoices.choices, null=True, blank=True)
    structure_type = models.CharField(choices=StructureType.choices, null=True, blank=True)

    def __str__(self):
        return f'"{self.text}" - {self.author}'


class QuotationItem(models.Model):
    # Reference to the Quotation this item belongs to.
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='items', editable=False)

    # Reference to the original product.
    original_product = models.ForeignKey('core.Product', on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    # Product Related Information at the time of quotation. If the product is updated later,
    # this information will not change. This is to ensure that the quotation reflects the product
    # information at the time of quotation. All fields are allowed to be null or blank because the
    # product may be provided by client.
    description = models.CharField(max_length=255, editable=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=False)
    warranty_years = models.IntegerField(null=True, blank=True, editable=False)

    # Quantity of the product in this quotation item
    quantity = models.IntegerField(default=1, editable=False)

    # Indicates whether the product was provided by the client
    provided_by_client = models.BooleanField(default=False, editable=False)

    def clean(self):
        if not self.provided_by_client:
            if not self.unit_price:
                raise ValidationError("Unit price is required for products not provided by the client.")
        return super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    @property
    def product_type(self):
        return self.original_product.product_type

    def __str__(self):
        return f'{self.description} - {self.quantity} @ {self.unit_price}'
