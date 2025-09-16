from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Events
    path('events/', views.EventListView.as_view(), name='event-list'),
    path('events/<uuid:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('events/<uuid:event_id>/tickets/', views.event_tickets, name='event-tickets'),
    path('events/<uuid:event_id>/stats/', views.event_stats, name='event-stats'),

    # Tickets
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('tickets/<uuid:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('my-tickets/', views.MyTicketsView.as_view(), name='my-tickets'),

    # Stats and trending
    path('stats/', views.market_stats, name='market-stats'),
    path('trending/', views.trending_events, name='trending-events'),
]