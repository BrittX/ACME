from rest_framework import mixins, viewsets

from quotes.models import Quote
from quotes.serializers import QuoteSerializer


class QuoteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Quote API endpoint for creating, and retrieving quote objects."""

    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
