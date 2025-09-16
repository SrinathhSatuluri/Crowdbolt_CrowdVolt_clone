from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random

from products.models import Event, Ticket, TicketListing

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with demo events and tickets'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo data for CrowdBolt marketplace...')

        # Create demo users
        demo_users = self.create_demo_users()

        # Create demo events
        events = self.create_demo_events()

        # Create demo tickets for events
        self.create_demo_tickets(events, demo_users)

        # Update trending scores for top 3 events
        self.update_trending_scores(events)

        self.stdout.write(
            self.style.SUCCESS('Demo data created successfully!')
        )

    def create_demo_users(self):
        """Create demo users as ticket sellers."""
        users = []
        demo_users_data = [
            {'email': 'seller1@crowdbolt.com', 'first_name': 'Alice', 'last_name': 'Johnson'},
            {'email': 'seller2@crowdbolt.com', 'first_name': 'Bob', 'last_name': 'Smith'},
            {'email': 'seller3@crowdbolt.com', 'first_name': 'Carol', 'last_name': 'Davis'},
        ]

        for user_data in demo_users_data:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'role': 'seller'
                }
            )
            if created:
                user.set_password('DemoPass123!')
                user.save()
                self.stdout.write(f'Created user: {user.email}')
            users.append(user)

        return users

    def create_demo_events(self):
        """Create exciting demo events."""
        events_data = [
            {
                'name': 'Electric Nights Festival 2024',
                'description': 'The biggest electronic music festival featuring top DJs from around the world. Three days of non-stop beats, amazing visuals, and unforgettable experiences.',
                'category': 'festival',
                'venue_name': 'Brooklyn Mirage',
                'venue_address': '140 Stewart Ave, Brooklyn, NY 11237',
                'city': 'Brooklyn',
                'state': 'NY',
                'event_date': timezone.now() + timedelta(days=30),
                'doors_open': timezone.now() + timedelta(days=30, hours=-2),
                'image_url': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1065&q=80',
                'artist_lineup': ['Calvin Harris', 'Skrillex', 'Deadmau5', 'Diplo']
            },
            {
                'name': 'Neon Rave Underground',
                'description': 'Underground techno experience in an abandoned warehouse. Pure vibes, minimal commercial interference, maximum music.',
                'category': 'rave',
                'venue_name': 'Secret Warehouse',
                'venue_address': 'Location revealed 24h before event',
                'city': 'Los Angeles',
                'state': 'CA',
                'event_date': timezone.now() + timedelta(days=15),
                'doors_open': timezone.now() + timedelta(days=15, hours=-1),
                'image_url': 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
                'artist_lineup': ['Charlotte de Witte', 'Ben Klock', 'Paula Temple']
            },
            {
                'name': 'Summer Vibes Concert',
                'description': 'Chill outdoor concert featuring indie and alternative rock bands. Perfect for a relaxed evening under the stars.',
                'category': 'concert',
                'venue_name': 'Central Park SummerStage',
                'venue_address': 'Rumsey Playfield, Central Park, NYC',
                'city': 'New York',
                'state': 'NY',
                'event_date': timezone.now() + timedelta(days=45),
                'doors_open': timezone.now() + timedelta(days=45, hours=-1),
                'image_url': 'https://images.unsplash.com/photo-1506157786151-b8491531f063?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
                'artist_lineup': ['Arctic Monkeys', 'Tame Impala', 'Glass Animals']
            },
            {
                'name': 'Bass Drop Madness',
                'description': 'Heavy dubstep and bass music showcase. Bring ear protection and prepare for the bass to drop!',
                'category': 'concert',
                'venue_name': 'Red Rocks Amphitheatre',
                'venue_address': '18300 W Alameda Pkwy, Morrison, CO',
                'city': 'Morrison',
                'state': 'CO',
                'event_date': timezone.now() + timedelta(days=60),
                'doors_open': timezone.now() + timedelta(days=60, hours=-1),
                'image_url': 'https://images.unsplash.com/photo-1571266028243-1d815fb80e25?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
                'artist_lineup': ['Excision', 'Subtronics', 'Svdden Death']
            },
            {
                'name': 'Comedy Night Extravaganza',
                'description': 'Stand-up comedy show featuring the hottest comedians. Prepare to laugh until your sides hurt!',
                'category': 'comedy',
                'venue_name': 'The Comedy Cellar',
                'venue_address': '117 MacDougal St, New York, NY',
                'city': 'New York',
                'state': 'NY',
                'event_date': timezone.now() + timedelta(days=20),
                'doors_open': timezone.now() + timedelta(days=20, hours=-1),
                'image_url': 'https://images.unsplash.com/photo-1606135142146-8c5e6e35b71b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
                'artist_lineup': ['Dave Chappelle', 'Kevin Hart', 'Amy Schumer']
            },
            {
                'name': 'Jazz & Blues Night',
                'description': 'Intimate evening of smooth jazz and blues featuring legendary musicians. Perfect for a sophisticated night out.',
                'category': 'concert',
                'venue_name': 'Blue Note',
                'venue_address': '131 W 3rd St, New York, NY',
                'city': 'New York',
                'state': 'NY',
                'event_date': timezone.now() + timedelta(days=35),
                'doors_open': timezone.now() + timedelta(days=35, hours=-1),
                'image_url': 'https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
                'artist_lineup': ['Wynton Marsalis', 'Diana Krall', 'Brad Mehldau']
            },
            {
                'name': 'EDM Warehouse Party',
                'description': 'High-energy electronic dance music party in a converted warehouse. Massive sound system and incredible light show.',
                'category': 'rave',
                'venue_name': 'Industrial Complex',
                'venue_address': '2847 Industrial Blvd, Chicago, IL',
                'city': 'Chicago',
                'state': 'IL',
                'event_date': timezone.now() + timedelta(days=25),
                'doors_open': timezone.now() + timedelta(days=25, hours=-2),
                'image_url': 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
                'artist_lineup': ['Martin Garrix', 'Marshmello', 'Zedd', 'Tiësto']
            },
            {
                'name': 'Hip-Hop Block Party',
                'description': 'Old school meets new school in this epic hip-hop celebration. Street food, breakdancing, and legendary MCs.',
                'category': 'festival',
                'venue_name': 'Brooklyn Bridge Park',
                'venue_address': '334 Furman St, Brooklyn, NY',
                'city': 'Brooklyn',
                'state': 'NY',
                'event_date': timezone.now() + timedelta(days=50),
                'doors_open': timezone.now() + timedelta(days=50, hours=-1),
                'image_url': 'https://images.unsplash.com/photo-1571019613831-39f3c0e2b5c9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
                'artist_lineup': ['Kendrick Lamar', 'J. Cole', 'Tyler The Creator', 'Childish Gambino']
            },
            {
                'name': 'Country Music Fest',
                'description': 'Boots, hats, and great music under the open sky. Three days of the best country music with camping available.',
                'category': 'festival',
                'venue_name': 'Fair Grounds',
                'venue_address': '1751 Gentilly Blvd, New Orleans, LA',
                'city': 'New Orleans',
                'state': 'LA',
                'event_date': timezone.now() + timedelta(days=75),
                'doors_open': timezone.now() + timedelta(days=75, hours=-3),
                'image_url': 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
                'artist_lineup': ['Luke Bryan', 'Carrie Underwood', 'Blake Shelton', 'Keith Urban']
            },
            {
                'name': 'Theater Spectacular',
                'description': 'Broadway-style musical theater performance featuring award-winning actors and stunning choreography.',
                'category': 'theater',
                'venue_name': 'Majestic Theatre',
                'venue_address': '245 W 44th St, New York, NY',
                'city': 'New York',
                'state': 'NY',
                'event_date': timezone.now() + timedelta(days=40),
                'doors_open': timezone.now() + timedelta(days=40, hours=-1),
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
                'artist_lineup': ['Lin-Manuel Miranda', 'Idina Menzel', 'Hugh Jackman']
            }
        ]

        events = []
        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                name=event_data['name'],
                defaults=event_data
            )
            if created:
                self.stdout.write(f'Created event: {event.name}')
            events.append(event)

        return events

    def create_demo_tickets(self, events, users):
        """Create demo tickets for events."""
        sections = ['GA', 'VIP', 'Section A', 'Section B', 'Floor', 'Balcony']

        for event in events:
            # Create 3-8 tickets per event
            num_tickets = random.randint(3, 8)

            for i in range(num_tickets):
                seller = random.choice(users)
                section = random.choice(sections)

                # Price based on section type
                if 'VIP' in section:
                    original_price = random.randint(150, 300)
                elif 'GA' in section:
                    original_price = random.randint(80, 150)
                else:
                    original_price = random.randint(100, 200)

                # Listing price with some markup/discount
                markup_factor = random.uniform(0.8, 2.5)  # Can be discounted or marked up
                listing_price = round(original_price * markup_factor, 2)

                ticket_data = {
                    'event': event,
                    'seller': seller,
                    'section': section,
                    'row': random.choice(['A', 'B', 'C', 'GA', '']) if section != 'GA' else '',
                    'seat_number': str(random.randint(1, 50)) if section not in ['GA', 'Floor'] else '',
                    'quantity': random.choice([1, 1, 1, 2, 2, 4]),  # Mostly 1-2 tickets
                    'original_price': original_price,
                    'listing_price': listing_price,
                    'condition': random.choice(['digital', 'digital', 'physical', 'pdf']),
                    'notes': random.choice([
                        'Great seats with amazing view!',
                        'Can\'t make it anymore, selling at face value',
                        'Bought extra tickets, selling to a good home',
                        'Moving sale - need to sell quickly',
                        ''
                    ]),
                    'transfer_method': random.choice([
                        'Ticketmaster Transfer',
                        'StubHub Instant Download',
                        'AXS Mobile Transfer',
                        'PDF Email',
                        'Meet in person'
                    ])
                }

                ticket, created = Ticket.objects.get_or_create(
                    event=event,
                    seller=seller,
                    section=section,
                    row=ticket_data['row'],
                    seat_number=ticket_data['seat_number'],
                    defaults=ticket_data
                )

                if created:
                    # Create listing for the ticket
                    TicketListing.objects.create(ticket=ticket)
                    self.stdout.write(f'Created ticket: {ticket}')

        total_events = Event.objects.count()
        total_tickets = Ticket.objects.count()
        self.stdout.write(
            f'Database now has {total_events} events and {total_tickets} tickets!'
        )

    def update_trending_scores(self, events):
        """Set trending scores to make specific events popular."""

        # Define which events should be trending with high scores and unique images
        trending_events = {
            'Electric Nights Festival 2024': {
                'view_count': 3500,
                'search_count': 650,
                'ticket_sales_count': 120,
                'trending_score': 2000.0,
                'is_trending': True,
                'image_url': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1065&q=80'
            },
            'Neon Rave Underground': {
                'view_count': 2800,
                'search_count': 520,
                'ticket_sales_count': 95,
                'trending_score': 1800.0,
                'is_trending': True,
                'image_url': 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
            },
            'EDM Warehouse Party': {
                'view_count': 2200,
                'search_count': 380,
                'ticket_sales_count': 75,
                'trending_score': 1600.0,
                'is_trending': True,
                'image_url': 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
            }
        }

        # Update events with trending data
        for event in events:
            if event.name in trending_events:
                trending_data = trending_events[event.name]
                event.view_count = trending_data['view_count']
                event.search_count = trending_data['search_count']
                event.ticket_sales_count = trending_data['ticket_sales_count']
                event.trending_score = trending_data['trending_score']
                event.is_trending = trending_data['is_trending']
                event.image_url = trending_data['image_url']  # Update image URL
                event.save()
                self.stdout.write(f'Updated trending data and image for: {event.name}')
            else:
                # Set lower scores for non-trending events
                event.view_count = random.randint(50, 500)
                event.search_count = random.randint(10, 100)
                event.ticket_sales_count = random.randint(2, 25)
                event.trending_score = event.calculate_trending_score()
                event.save()