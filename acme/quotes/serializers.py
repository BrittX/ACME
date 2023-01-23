from rest_framework import serializers

from quotes.models import Quote


class QuoteSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for validating fields on the Quote object."""

    id = serializers.ReadOnlyField()
    subtotal = serializers.ReadOnlyField()
    monthly_tax = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()

    class Meta:
        """Setting additional options for the QuoteSerializer."""

        model = Quote
        fields = "__all__"
