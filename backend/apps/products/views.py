from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Min, Max, Avg, Count
from django.utils import timezone

from .models import Event, Ticket, TicketListing
from .serializers import (
    EventSerializer,
    EventListSerializer,
    TicketSerializer,
    TicketListSerializer,
    TicketCreateSerializer,
    TicketListingSerializer,
)


class EventListView(generics.ListCreateAPIView):
    """List and create events."""

    permission_classes = [AllowAny]  # Anyone can view events

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EventListSerializer
        return EventSerializer

    def get_queryset(self):
        queryset = Event.objects.filter(status='upcoming')

        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        # Filter by city
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)

        # Search in name and description
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(artist_lineup__icontains=search)
            )

        return queryset.order_by('event_date')

    def perform_create(self, serializer):
        # Set creator to current user if authenticated
        if self.request.user.is_authenticated:
            serializer.save(created_by=self.request.user)
        else:
            serializer.save()


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific event."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # Anyone can view

    def get_permissions(self):
        # Only authenticated users can modify
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]


class TicketListView(generics.ListCreateAPIView):
    """List and create tickets."""

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TicketCreateSerializer
        return TicketListSerializer

    def get_permissions(self):
        # Anyone can view tickets, auth required to create
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = Ticket.objects.filter(status='available')

        # Filter by event
        event_id = self.request.query_params.get('event')
        if event_id:
            queryset = queryset.filter(event=event_id)

        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(listing_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(listing_price__lte=max_price)

        # Filter by section
        section = self.request.query_params.get('section')
        if section:
            queryset = queryset.filter(section__icontains=section)

        # Sort options
        sort_by = self.request.query_params.get('sort', 'price')
        if sort_by == 'price':
            queryset = queryset.order_by('listing_price')
        elif sort_by == 'date':
            queryset = queryset.order_by('listed_at')
        elif sort_by == 'section':
            queryset = queryset.order_by('section', 'row')

        return queryset

    def perform_create(self, serializer):
        ticket = serializer.save()
        # Automatically create a listing for the ticket
        TicketListing.objects.create(ticket=ticket)


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific ticket."""

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        # Anyone can view, only seller can modify
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_object(self):
        obj = super().get_object()
        # Only seller can modify their own tickets
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.seller != self.request.user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You can only modify your own tickets.")
        return obj


class MyTicketsView(generics.ListAPIView):
    """Get current user's tickets."""

    serializer_class = TicketListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(seller=self.request.user).order_by('-listed_at')


@api_view(['GET'])
@permission_classes([AllowAny])
def trending_events(request):
    """Get trending events based on popularity metrics."""

    limit = int(request.query_params.get('limit', 3))
    events = Event.get_trending_events(limit=limit)

    serializer = EventListSerializer(events, many=True)
    return Response({
        'trending_events': serializer.data,
        'count': len(serializer.data)
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def market_stats(request):
    """Get marketplace statistics."""

    total_events = Event.objects.filter(status='upcoming').count()
    total_tickets = Ticket.objects.filter(status='available').count()

    # Average prices
    avg_price = Ticket.objects.filter(status='available').aggregate(
        avg_price=Avg('listing_price')
    )['avg_price']

    # Popular categories
    popular_categories = Event.objects.filter(status='upcoming').values('category').annotate(
        count=Count('category')
    ).order_by('-count')[:5]

    return Response({
        'total_events': total_events,
        'total_tickets': total_tickets,
        'average_ticket_price': round(float(avg_price) if avg_price else 0, 2),
        'popular_categories': list(popular_categories)
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def event_tickets(request, event_id):
    """Get all available tickets for a specific event."""

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    tickets = Ticket.objects.filter(
        event=event,
        status='available'
    ).order_by('listing_price')

    # Get price statistics
    price_stats = tickets.aggregate(
        min_price=Min('listing_price'),
        max_price=Max('listing_price'),
        avg_price=Avg('listing_price')
    )

    serializer = TicketListSerializer(tickets, many=True)

    return Response({
        'event': EventSerializer(event).data,
        'tickets': serializer.data,
        'stats': {
            'total_available': tickets.count(),
            'min_price': price_stats['min_price'],
            'max_price': price_stats['max_price'],
            'avg_price': round(float(price_stats['avg_price']) if price_stats['avg_price'] else 0, 2)
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def event_stats(request, event_id):
    """Get marketplace statistics for a specific event."""

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    # Get all tickets for this event
    tickets = Ticket.objects.filter(event=event, status='available')

    # Get price statistics
    price_stats = tickets.aggregate(
        min_price=Min('listing_price'),
        max_price=Max('listing_price'),
        avg_price=Avg('listing_price')
    )

    # Simulate interested buyers (in a real app, this would track actual user interest)
    import random
    interested_buyers = random.randint(10, 50) if tickets.count() > 0 else 0

    # Get last sale price (simulate for now)
    last_sale_price = None
    if price_stats['avg_price']:
        # Simulate a recent sale price close to average
        last_sale_price = round(float(price_stats['avg_price']) * random.uniform(0.9, 1.1), 2)

    return Response({
        'total_tickets': tickets.count(),
        'interested_buyers': interested_buyers,
        'avg_price': round(float(price_stats['avg_price']) if price_stats['avg_price'] else 0, 2),
        'last_sale_price': last_sale_price,
        'min_price': price_stats['min_price'],
        'max_price': price_stats['max_price']
    })
