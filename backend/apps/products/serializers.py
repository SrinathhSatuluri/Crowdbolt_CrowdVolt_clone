from rest_framework import serializers
from .models import Event, Ticket, TicketListing


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""

    ticket_count = serializers.SerializerMethodField()
    lowest_price = serializers.SerializerMethodField()
    highest_price = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'category', 'status',
            'venue_name', 'venue_address', 'city', 'state', 'country',
            'event_date', 'doors_open', 'event_end',
            'image_url', 'artist_lineup',
            'ticket_count', 'lowest_price', 'highest_price',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_ticket_count(self, obj):
        return obj.tickets.filter(status='available').count()

    def get_lowest_price(self, obj):
        tickets = obj.tickets.filter(status='available')
        if tickets.exists():
            return tickets.order_by('listing_price').first().listing_price
        return None

    def get_highest_price(self, obj):
        tickets = obj.tickets.filter(status='available')
        if tickets.exists():
            return tickets.order_by('-listing_price').first().listing_price
        return None


class EventListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for event listings."""

    ticket_count = serializers.SerializerMethodField()
    lowest_price = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'category', 'venue_name', 'city', 'state',
            'event_date', 'image_url', 'artist_lineup',
            'ticket_count', 'lowest_price'
        ]

    def get_ticket_count(self, obj):
        return obj.tickets.filter(status='available').count()

    def get_lowest_price(self, obj):
        tickets = obj.tickets.filter(status='available')
        if tickets.exists():
            return tickets.order_by('listing_price').first().listing_price
        return None


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket model."""

    event_name = serializers.CharField(source='event.name', read_only=True)
    seller_email = serializers.CharField(source='seller.email', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'event', 'event_name', 'seller', 'seller_email',
            'section', 'row', 'seat_number', 'quantity',
            'original_price', 'listing_price',
            'condition', 'status', 'notes', 'transfer_method',
            'listed_at', 'updated_at', 'expires_at'
        ]
        read_only_fields = ['id', 'seller', 'listed_at', 'updated_at']


class TicketListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for ticket listings."""

    event_name = serializers.CharField(source='event.name', read_only=True)
    event_date = serializers.DateTimeField(source='event.event_date', read_only=True)
    markup_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'event_name', 'event_date',
            'section', 'row', 'quantity',
            'original_price', 'listing_price', 'markup_percentage',
            'condition', 'status'
        ]

    def get_markup_percentage(self, obj):
        return round(obj.markup_percentage(), 1)


class TicketCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tickets."""

    class Meta:
        model = Ticket
        fields = [
            'event', 'section', 'row', 'seat_number', 'quantity',
            'original_price', 'listing_price',
            'condition', 'notes', 'transfer_method', 'expires_at'
        ]

    def create(self, validated_data):
        # Set seller to current user
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        # Ensure listing price is reasonable
        if data['listing_price'] < data['original_price'] * 0.5:
            raise serializers.ValidationError(
                "Listing price cannot be less than 50% of original price."
            )

        if data['listing_price'] > data['original_price'] * 5:
            raise serializers.ValidationError(
                "Listing price cannot be more than 500% of original price."
            )

        return data


class TicketListingSerializer(serializers.ModelSerializer):
    """Serializer for TicketListing model."""

    ticket = TicketSerializer(read_only=True)
    total_fees = serializers.SerializerMethodField()
    seller_payout = serializers.SerializerMethodField()

    class Meta:
        model = TicketListing
        fields = [
            'id', 'ticket', 'status', 'views', 'saves',
            'platform_fee_percentage', 'payment_processing_fee',
            'total_fees', 'seller_payout',
            'created_at', 'updated_at'
        ]

    def get_total_fees(self, obj):
        return obj.total_fees()

    def get_seller_payout(self, obj):
        return obj.seller_payout()