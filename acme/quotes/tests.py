import faker
from django.test import TestCase

from quotes.models import Quote

_faker = faker.Faker()

# Create your tests here.


class QuotesTests(TestCase):
    """Testing Quotes app."""

    def setUp(self):
        """Reusable variables for the various tests."""
        # Quote object
        quote_one = Quote.objects.create(
            first_name=_faker.first_name(),
            last_name=_faker.last_name(),
            state="CA",
            pet=True,
            coverage_type="Basic",
            flood_coverage=True,
        )
        quote_two = Quote.objects.create(
            first_name=_faker.first_name(),
            last_name=_faker.last_name(),
            state="CA",
            pet=True,
            coverage_type="Premium",
            flood_coverage=True,
        )
        quote_three = Quote.objects.create(
            first_name=_faker.first_name(),
            last_name=_faker.last_name(),
            state="NY",
            pet=True,
            coverage_type="Premium",
        )
        quote_four = Quote.objects.create(
            first_name=_faker.first_name(),
            last_name=_faker.last_name(),
            state="TX",
            coverage_type="Basic",
            flood_coverage=True,
        )
        self.quotes = [quote_one, quote_two, quote_three, quote_four]
        self.expected_prices = {
            quote_one: {"subtotal": 40.80, "monthly_tax": 0.41, "total": 41.21},
            quote_two: {"subtotal": 61.20, "monthly_tax": 0.61, "total": 61.81},
            quote_three: {"subtotal": 60, "monthly_tax": 1.20, "total": 61.20},
            quote_four: {"subtotal": 30, "monthly_tax": 0.15, "total": 30.15},
        }

    def test_name(self):
        """Tests the name property."""
        for quote in self.quotes:
            expected_name = f"{quote.first_name} {quote.last_name}"
            self.assertEqual(quote.name, expected_name)

    def test_calculate_subtotal(self):
        """Tests the calculate subtotal function."""
        for quote in self.quotes:
            expected_subtotal = self.expected_prices[quote]["subtotal"]
            self.assertEqual(quote.calculate_subtotal(), expected_subtotal)

    def test_monthly_tax(self):
        """Tests the calculate monthly tax function."""
        for quote in self.quotes:
            expected_tax = self.expected_prices[quote]["monthly_tax"]
            self.assertEqual(quote.calculate_monthly_tax(), expected_tax)

    def test_calculate_total(self):
        """Tests the calculate total function."""
        for quote in self.quotes:
            expected_total = self.expected_prices[quote]["total"]
            self.assertEqual(quote.calculate_total(), expected_total)

    def test_flood_coverage_amount(self):
        """Tests the flood coverage amount function."""
        quote = self.quotes[0]
        quote_subtotal = 40
        expected_amount = 40.8
        self.assertEqual(quote.flood_coverage_amount(quote_subtotal), expected_amount)

    def test_flood_coverage_amount_dne(self):
        """Tests the flood coverage amount returns original subtotal."""
        quote = self.quotes[2]
        quote_subtotal = expected_amount = 60
        self.assertEqual(quote.flood_coverage_amount(quote_subtotal), expected_amount)

    def test_pet_coverage_amount(self):
        """Tests the pet coverage amount function."""
        quote = self.quotes[0]
        quote_subtotal = 20
        expected_amount = 20
        self.assertEqual(quote.pet_coverage_amount(quote_subtotal), expected_amount)

    def test_pet_coverage_amount_dne(self):
        """Tests the pet coverage amount returns 0."""
        quote = self.quotes[3]
        quote_subtotal = 20
        expected_amount = 0
        self.assertEqual(quote.pet_coverage_amount(quote_subtotal), expected_amount)

    def test_save(self):
        """Tests the overwritten save method."""
        quote = Quote(
            first_name=_faker.first_name,
            last_name=_faker.last_name,
            state="TX",
            coverage_type="Premium",
        )
        # Before saving, prices not set
        self.assertIsNone(quote.subtotal)
        self.assertIsNone(quote.monthly_tax)
        self.assertIsNone(quote.total)

        quote.save()

        self.assertIsNotNone(quote.subtotal)
        self.assertIsNotNone(quote.monthly_tax)
        self.assertIsNotNone(quote.total)
