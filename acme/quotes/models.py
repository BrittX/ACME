# DB model definitions for the quote object.
from uuid import uuid4

from django.db import models

from quotes.constants import (
    COVERAGE_RATES,
    COVERAGE_TYPE,
    MONTHLY_TAX,
    STATES,
    STATE_FLOOD_RATE,
)


class Quote(models.Model):
    """Quote ."""

    id = models.UUIDField(
        verbose_name="Quote ID",
        unique=True,
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    first_name = models.CharField(verbose_name="First Name", max_length=50, null=False)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, null=False)
    coverage_type = models.CharField(
        choices=COVERAGE_TYPE, verbose_name="Coverage Type", max_length=7
    )
    state = models.CharField(
        choices=STATES,
        max_length=2,
        verbose_name="State",
    )
    pet = models.BooleanField(
        default=False,
    )
    flood_coverage = models.BooleanField(
        default=False,
        verbose_name="Flood Coverage",
    )
    total = models.DecimalField(verbose_name="Total", decimal_places=2, max_digits=5)
    monthly_tax = models.DecimalField(
        verbose_name="Monthly Tax", decimal_places=2, max_digits=5
    )
    subtotal = models.DecimalField(
        verbose_name="Subtotal", decimal_places=2, max_digits=5
    )

    def save(self, *args, **kwargs):
        """Overrides the save function to store quote pricing.

        Returns:
            None.
        """
        self.subtotal = self.calculate_subtotal()
        self.monthly_tax = self.calculate_monthly_tax()
        self.total = self.calculate_total()

        super(Quote, self).save(*args, **kwargs)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def pet_coverage_amount(self, subtotal):
        """The additional amount of pet coverate is selected.

        Returns:
            int. The pet coverage amount or 0.
        """
        if self.pet:
            return COVERAGE_RATES["Pet"]
        return 0

    def flood_coverage_amount(self, subtotal):
        """The subtotal including flood coverage (if applicable).

        Returns:
            int. The subtotal with flood coverage added (if it exists).
        """
        if self.flood_coverage:
            return round(subtotal + (subtotal * STATE_FLOOD_RATE[self.state]), 2)

        return subtotal

    def calculate_total(self):
        """The quote total based on coverage selections.

        Returns:
            int. The total quote price.
        """
        total = round(self.calculate_subtotal() + self.calculate_monthly_tax(), 2)
        return total

    def calculate_subtotal(self):
        """The quote subtotal based on coverage options and excluding taxes.

        Returns:
            int. The quote subtotal amount.
        """
        subtotal = COVERAGE_RATES[self.coverage_type]

        # Add additional insurance options
        subtotal += self.pet_coverage_amount(subtotal)
        subtotal = self.flood_coverage_amount(subtotal)

        return subtotal

    def calculate_monthly_tax(self):
        """The monthly tax of the quote object based on the subtotal.

        Returns:
            int. The monthly tax amount.
        """
        monthly_tax = round(self.calculate_subtotal() * MONTHLY_TAX[self.state], 2)
        return monthly_tax
