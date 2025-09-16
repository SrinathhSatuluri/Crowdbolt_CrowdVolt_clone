from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

User = get_user_model()


class Event(models.Model):
    """Event model for concerts, raves, festivals."""

    CATEGORY_CHOICES = [
        ('concert', 'Concert'),
        ('festival', 'Festival'),
        ('rave', 'Rave/Club'),
        ('theater', 'Theater'),
        ('sports', 'Sports'),
        ('comedy', 'Comedy'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('live', 'Live/Happening'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')

    # Event details
    venue_name = models.CharField(max_length=200)
    venue_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default='US')

    # Timing
    event_date = models.DateTimeField()
    doors_open = models.DateTimeField(null=True, blank=True)
    event_end = models.DateTimeField(null=True, blank=True)

    # Media
    image_url = models.URLField(blank=True)
    artist_lineup = models.JSONField(default=list, blank=True)  # ['Artist 1', 'Artist 2']

    # Popularity tracking
    view_count = models.PositiveIntegerField(default=0)
    search_count = models.PositiveIntegerField(default=0)
    ticket_sales_count = models.PositiveIntegerField(default=0)
    is_trending = models.BooleanField(default=False)
    trending_score = models.FloatField(default=0.0)  # Calculated score for trending

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_events')

    class Meta:
        db_table = 'events'
        ordering = ['event_date']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['city']),
            models.Index(fields=['event_date']),
            models.Index(fields=['trending_score']),
            models.Index(fields=['is_trending']),
        ]

    def __str__(self):
        return f"{self.name} - {self.event_date.strftime('%Y-%m-%d')}"

    def is_upcoming(self):
        return self.status == 'upcoming' and self.event_date > timezone.now()

    def is_past(self):
        return self.event_date < timezone.now()

    def calculate_trending_score(self):
        """Calculate trending score based on recent activity."""
        # Weight factors for different metrics
        view_weight = 1.0
        search_weight = 2.0
        sales_weight = 5.0

        # Calculate base score
        score = (self.view_count * view_weight +
                self.search_count * search_weight +
                self.ticket_sales_count * sales_weight)

        # Boost for upcoming events
        if self.is_upcoming():
            score *= 1.5

        return score

    @classmethod
    def get_trending_events(cls, limit=3):
        """Get top trending events."""
        return cls.objects.filter(
            status='upcoming'
        ).order_by('-trending_score')[:limit]


class Ticket(models.Model):
    """Ticket model for event tickets being resold."""

    CONDITION_CHOICES = [
        ('digital', 'Digital/Mobile'),
        ('physical', 'Physical Ticket'),
        ('pdf', 'PDF Ticket'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending Sale'),
        ('sold', 'Sold'),
        ('transferred', 'Transferred'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_selling')

    # Ticket details
    section = models.CharField(max_length=100, blank=True)
    row = models.CharField(max_length=20, blank=True)
    seat_number = models.CharField(max_length=20, blank=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])

    # Pricing
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    listing_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Status and condition
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='digital')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    # Additional info
    notes = models.TextField(blank=True, help_text='Additional notes about the tickets')
    transfer_method = models.CharField(max_length=200, blank=True, help_text='How tickets will be transferred')

    # Metadata
    listed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tickets'
        ordering = ['listing_price']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['event', 'status']),
            models.Index(fields=['seller']),
            models.Index(fields=['listing_price']),
        ]

    def __str__(self):
        return f"{self.event.name} - {self.section} - ${self.listing_price}"

    def is_available(self):
        return self.status == 'available' and (not self.expires_at or self.expires_at > timezone.now())

    def markup_percentage(self):
        if self.original_price > 0:
            return ((self.listing_price - self.original_price) / self.original_price) * 100
        return 0


class TicketListing(models.Model):
    """Represents a ticket listing transaction."""

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('sold', 'Sold'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='listing')

    # Listing details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    views = models.PositiveIntegerField(default=0)
    saves = models.PositiveIntegerField(default=0)  # Users who saved/favorited

    # Platform fees
    platform_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    payment_processing_fee = models.DecimalField(max_digits=5, decimal_places=2, default=2.90)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ticket_listings'

    def __str__(self):
        return f"Listing: {self.ticket}"

    def total_fees(self):
        """Calculate total platform fees."""
        base_price = self.ticket.listing_price
        platform_fee = base_price * (self.platform_fee_percentage / 100)
        return platform_fee + self.payment_processing_fee

    def seller_payout(self):
        """Calculate how much seller receives after fees."""
        return self.ticket.listing_price - self.total_fees()
