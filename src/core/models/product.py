from django.db import models


class Product(models.Model):

    class ProductTypeChoices(models.TextChoices):
        SOLAR_PANEL = 'SOLAR_PANEL', 'Solar Panel'
        INVERTER = 'INVERTER', 'Inverter'
        BATTERY = 'BATTERY', 'Battery'
        CABLE_TIE = 'CABLE_TIE', 'Cable Tie'
        AC_CABLE = 'AC_CABLE', 'AC Cable'
        DC_CABLE = 'DC_CABLE', 'DC Cable'
        LIGHTNING_ARRESTER = 'LIGHTNING_ARRESTER', 'Lightning Arrester'

        # Additional charges / services. Not necessarily a physical product.
        KE_FILE_SUBMISSION_CHARGE = 'KE_FILE_SUBMISSION', 'KE File Submission'
        INSTALLATION_CHARGE = 'INSTALLATION_CHARGE', 'Installation Charge'
        TRANSPORTATION_CHARGE = 'TRANSPORTATION_CHARGE', 'Transportation Charge'
        DC_AC_EARTHING_CHARGE = 'DC_AC_EARTHING', 'DC/AC Earthing'

    class BrandChoices(models.TextChoices):
        solar_max = 'SOLAR_MAX', 'SolarMax'

    # String description of the product
    description = models.CharField(max_length=100)

    # Price at which the product is sold
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Price at which the product can be purchased
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Warranty period in years
    # Some products may not have a warranty
    warranty_years = models.IntegerField(null=True, blank=True)

    # Type of product (e.g., Solar Panel, Inverter)
    product_type = models.CharField(choices=ProductTypeChoices.choices, editable=False)

    # Brand of the product (e.g., SolarMax)
    # Some products may not have a brand (e.g., Cable Tie)
    brand = models.CharField(choices=BrandChoices.choices, null=True, blank=True, editable=False)

    # Rating in Kilo-Watt
    # This is used for Inverters and Solar Panels and not all products will have a rating
    rating_kw = models.IntegerField(null=True, blank=True, editable=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if (self.product_type == self.ProductTypeChoices.INVERTER
            or self.product_type == self.ProductTypeChoices.SOLAR_PANEL
            or self.product_type == self.ProductTypeChoices.BATTERY
        ):
            if not self.rating_kw:
                raise ValueError("Rating is required for Inverters and Solar Panels")
            if not self.brand:
                raise ValueError("Brand is required for Inverters and Solar Panels")
        
        # For additional charges, rating_kw, brand, and warranty_years are not required
        elif self.product_type == self.ProductTypeChoices.KE_FILE_SUBMISSION_CHARGE:
            # Ensure that KE File Submission Charge is unique.
            if (Product.objects.filter(product_type=self.product_type).exists()):
                raise ValueError("KE File Submission Charge already exists. You can modify it instead.")
            if self.rating_kw or self.brand or self.warranty_years:
                raise ValueError("KE File Submission Charge can only have description, unit price and cost price")
        elif self.product_type == self.ProductTypeChoices.INSTALLATION_CHARGE:
            if self.rating_kw or self.brand or self.warranty_years:
                raise ValueError("Installation Charge can only have description, unit price and cost price")
        elif self.product_type == self.ProductTypeChoices.TRANSPORTATION_CHARGE:
            if self.rating_kw or self.brand or self.warranty_years:
                raise ValueError("Transportation Charge can only have description, unit price and cost price")
        elif self.product_type == self.ProductTypeChoices.DC_AC_EARTHING_CHARGE:
            if self.rating_kw or self.brand or self.warranty_years:
                raise ValueError("DC/AC Earthing Charge can only have description, unit price and cost price")

        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.description
