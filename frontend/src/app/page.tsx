'use client'

import { useEffect, useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import Image from 'next/image'
import AuthModal from '@/components/AuthModal'
import { API_ENDPOINTS, apiCall } from '@/lib/api'
import { mockEvents } from '@/lib/mockData'

interface CrowdBoltEvent {
  id: string
  name: string
  category: string
  venue_name: string
  city: string
  state: string
  event_date: string
  image_url: string
  artist_lineup: string[]
  ticket_count: number
  lowest_price: number | null
}

interface EventsResponse {
  count: number
  results: CrowdBoltEvent[]
}

export default function Home() {
  const router = useRouter()
  const [events, setEvents] = useState<CrowdBoltEvent[]>([])
  const [trendingEvents, setTrendingEvents] = useState<CrowdBoltEvent[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState('date')
  const [loading, setLoading] = useState(true)
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [isPaused, setIsPaused] = useState(false)

  const fetchEvents = async () => {
    try {
      const response = await apiCall(API_ENDPOINTS.events)
      if (response.ok) {
        const data: EventsResponse = await response.json()
        setEvents(data.results)
      } else {
        throw new Error('Events API failed')
      }
    } catch (error) {
      console.error('Failed to fetch events:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const fetchTrendingEvents = async () => {
    try {
      const response = await apiCall(`${API_ENDPOINTS.trending}?limit=3`)
      if (response.ok) {
        const data = await response.json()
        setTrendingEvents(data.trending_events)
      } else {
        throw new Error('Trending events API failed')
      }
    } catch (error) {
      console.error('Failed to fetch trending events:', error)
      throw error
    }
  }

  const fetchEventsWithFallback = useCallback(async () => {
    try {
      await Promise.all([fetchEvents(), fetchTrendingEvents()])
    } catch (error) {
      console.error('API calls failed, falling back to mock data:', error)
      // Fallback to mock data
      const transformedEvents = mockEvents.map(event => ({
        id: event.id.toString(),
        name: event.title,
        category: event.category,
        venue_name: event.location,
        city: event.location.split(',')[0],
        state: event.location.split(',')[1]?.trim() || '',
        event_date: event.date,
        image_url: event.image_url,
        artist_lineup: [event.category],
        ticket_count: event.ticket_count,
        lowest_price: event.lowest_price
      }))

      setEvents(transformedEvents)
      setTrendingEvents(transformedEvents.filter((_, index) => index < 3))
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    const useMockData = process.env.NEXT_PUBLIC_USE_MOCK_DATA === 'true' ||
                       process.env.NODE_ENV === 'production' // Default to mock data in production

    if (useMockData) {
      // Use mock data for demo
      const transformedEvents = mockEvents.map(event => ({
        id: event.id.toString(),
        name: event.title,
        category: event.category,
        venue_name: event.location,
        city: event.location.split(',')[0],
        state: event.location.split(',')[1]?.trim() || '',
        event_date: event.date,
        image_url: event.image_url,
        artist_lineup: [event.category],
        ticket_count: event.ticket_count,
        lowest_price: event.lowest_price
      }))

      setEvents(transformedEvents)
      setTrendingEvents(transformedEvents.filter((_, index) => index < 3))
      setLoading(false)
    } else {
      // Try real API calls, fallback to mock data on failure
      fetchEventsWithFallback()
    }
  }, [fetchEventsWithFallback])


  const filteredEvents = events.filter(event =>
    event.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    event.city.toLowerCase().includes(searchQuery.toLowerCase()) ||
    event.artist_lineup.some(artist => artist.toLowerCase().includes(searchQuery.toLowerCase()))
  )

  const sortedEvents = [...filteredEvents].sort((a, b) => {
    switch (sortBy) {
      case 'date':
        return new Date(a.event_date).getTime() - new Date(b.event_date).getTime()
      case 'venue':
        return a.venue_name.localeCompare(b.venue_name)
      case 'popularity':
        return (b.ticket_count || 0) - (a.ticket_count || 0)
      default:
        return 0
    }
  })

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    const target = e.target as HTMLImageElement
    const fallbackImages = [
      'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?ixlib=rb-4.0.3&w=800&q=80', // Concert crowd
      'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?ixlib=rb-4.0.3&w=800&q=80', // Stage lights
      'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?ixlib=rb-4.0.3&w=800&q=80', // Music festival
      'https://via.placeholder.com/800x400/8B5CF6/FFFFFF?text=CrowdBolt+Event'
    ]

    if (!target.dataset.fallbackIndex) {
      target.dataset.fallbackIndex = '0'
    }

    const fallbackIndex = parseInt(target.dataset.fallbackIndex)
    if (fallbackIndex < fallbackImages.length - 1) {
      target.dataset.fallbackIndex = (fallbackIndex + 1).toString()
      target.src = fallbackImages[fallbackIndex + 1]
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-900 via-purple-800 to-black">
      {/* Header */}
      <header className="p-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between">
            {/* Logo with Lightning Bolt */}
            <div className="flex items-center space-x-3">
              <div className="relative">
                <div className="w-12 h-12 bg-black rounded-full flex items-center justify-center shadow-lg border-2 border-gray-800">
                  <svg className="w-7 h-7 text-purple-400" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M13 2L3 14h6l-2 8 10-12h-6l2-8z"/>
                  </svg>
                </div>
              </div>
              <h1 className="text-5xl font-black text-white font-bebas tracking-widest bg-gradient-to-r from-purple-300 to-pink-300 bg-clip-text text-transparent">
                CROWDBOLT
              </h1>
            </div>

            {/* Center - Search Bar */}
            <div className="flex-1 max-w-md mx-8">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search events, artists, venues..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-6 py-3 text-lg bg-white/10 backdrop-blur-sm border border-purple-400/30 rounded-2xl text-white placeholder-purple-200 focus:outline-none focus:border-purple-300 focus:bg-white/20 transition-all font-playfair"
                />
                <svg className="absolute right-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-purple-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>

            {/* Navigation */}
            <nav className="flex items-center space-x-8">
              <div className="relative">
                <span className="text-white font-cinzel font-semibold">Events</span>
                <div className="absolute -bottom-2 left-0 right-0 h-0.5 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full"></div>
              </div>
              <a href="/about" className="text-purple-200 hover:text-white transition-colors font-playfair">About</a>
              <a href="/help" className="text-purple-200 hover:text-white transition-colors font-playfair">Help</a>
              <button
                onClick={() => setShowAuthModal(true)}
                className="text-purple-200 hover:text-white transition-colors font-playfair"
              >
                Login
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="px-6 py-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between gap-6">
            {/* Left Side - Slogan */}
            <div className="flex-1 max-w-2xl space-y-6">
              <div className="space-y-3">
                <h2 className="text-4xl font-bold text-white font-playfair leading-tight">
                  <span className="bg-gradient-to-r from-purple-300 to-pink-300 bg-clip-text text-transparent">
                    Buy or Sell
                  </span>
                  <br />
                  <span className="bg-gradient-to-r from-purple-300 to-pink-300 bg-clip-text text-transparent">
                    EDM and Rave Tickets
                  </span>
                </h2>
                <p className="text-lg text-purple-200 font-cinzel font-medium leading-relaxed">
                  The ultimate marketplace for electronic music events
                </p>
              </div>

              {/* Join the Party Button */}
              <button
                onClick={() => setShowAuthModal(true)}
                className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-3 rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all font-bebas font-bold text-lg tracking-wider shadow-lg hover:shadow-xl transform hover:scale-105"
              >
                Join the Party
              </button>
            </div>

            {/* Right Side - Instagram Banner */}
            <div className="flex-1 max-w-lg">
              <div className="relative h-80 rounded-xl overflow-hidden group cursor-pointer shadow-2xl hover:shadow-purple-500/20 transition-all duration-500">
                {/* Background Image */}
                <Image
                  src="https://images.unsplash.com/photo-1470225620780-dba8ba36b745?ixlib=rb-4.0.3&w=800&q=80"
                  alt="CrowdBolt Instagram"
                  width={800}
                  height={320}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out"
                  onError={handleImageError}
                />

                {/* Gradient Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-purple-900/40 to-transparent group-hover:from-black/70 group-hover:via-purple-900/20 transition-all duration-500"></div>

                {/* Instagram Content Overlay */}
                <div className="absolute inset-0 flex flex-col justify-end p-6">
                  <div className="space-y-4">
                    {/* Instagram Icon */}
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-gradient-to-tr from-purple-500 via-pink-500 to-orange-400 rounded-lg p-0.5">
                        <div className="w-full h-full bg-black rounded-md flex items-center justify-center">
                          <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                          </svg>
                        </div>
                      </div>
                      <span className="text-white font-orbitron font-medium text-lg tracking-wider">@crowdbolt</span>
                    </div>

                    {/* Text Content */}
                    <div className="space-y-2">
                      <h3 className="text-2xl font-bold text-white font-bebas leading-tight tracking-wide">
                        Follow Us on Instagram
                      </h3>
                      <p className="text-gray-200 font-cinzel text-sm leading-relaxed">
                        Get exclusive drops & behind-the-scenes content from the hottest events
                      </p>
                    </div>

                    {/* Follow Button */}
                    <div className="pt-2">
                      <div className="inline-flex items-center space-x-2 bg-white/20 backdrop-blur-sm border border-white/30 rounded-lg px-6 py-3 group-hover:bg-white/40 group-hover:border-white/50 group-hover:scale-105 transition-all duration-300">
                        <span className="text-white font-bebas font-semibold text-sm group-hover:text-white tracking-wider">Follow</span>
                        <svg className="w-4 h-4 text-white group-hover:translate-x-2 transition-transform duration-300 ease-out" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Trending Events */}
      <section className="py-6 mt-4 overflow-hidden">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-white mb-6 font-playfair bg-gradient-to-r from-purple-300 to-pink-300 bg-clip-text text-transparent">
            Trending Events
          </h2>
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-300"></div>
          </div>
        ) : (
          <div className="relative">
            {/* Continuous Scrolling Container */}
            <div
              className="flex gap-6 w-fit"
              style={{
                animation: isPaused ? 'none' : 'scroll 60s linear infinite'
              }}
              onMouseEnter={() => setIsPaused(true)}
              onMouseLeave={() => setIsPaused(false)}
            >
              {/* Duplicate events to create seamless loop but only show 3 unique */}
              {[...trendingEvents, ...trendingEvents].map((event, index) => (
                <div
                  key={`${event.id}-${index}`}
                  onClick={() => router.push(`/events/${event.id}`)}
                  className="w-72 flex-shrink-0 rounded-xl overflow-hidden transition-all cursor-pointer hover:scale-105 duration-300"
                >
                  {/* Event Image */}
                  <div className="relative h-40">
                    <Image
                      src={event.image_url}
                      alt={event.name}
                      width={288}
                      height={160}
                      className="w-full h-full object-cover"
                      onError={handleImageError}
                    />
                    {/* Gradient overlay for better text readability */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                  </div>

                  {/* Event Details */}
                  <div className="p-4">
                    <h3 className="text-lg font-bold text-white mb-1 line-clamp-2 font-playfair">{event.name}</h3>
                    <p className="text-purple-200 mb-1 text-sm font-playfair">{event.venue_name}</p>
                    <p className="text-purple-300 text-xs mb-3 font-playfair">{formatDate(event.event_date)}</p>

                    {event.artist_lineup.length > 0 && (
                      <div className="flex flex-wrap gap-1 mb-3">
                        {event.artist_lineup.slice(0, 2).map((artist, artistIndex) => (
                          <span key={artistIndex} className="text-xs bg-purple-700/50 text-purple-100 px-2 py-1 rounded font-playfair">
                            {artist}
                          </span>
                        ))}
                      </div>
                    )}

                    <div className="flex justify-between items-center">
                      <span className="text-purple-200 text-xs font-playfair">{event.ticket_count} tickets</span>
                      {event.lowest_price && (
                        <span className="text-white font-bold text-sm font-playfair">From ${event.lowest_price}</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Add CSS animation for scrolling */}
        <style jsx>{`
          @keyframes scroll {
            0% {
              transform: translateX(0);
            }
            100% {
              transform: translateX(-50%);
            }
          }
        `}</style>
      </section>

      {/* All Events */}
      <section className="px-6 py-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-3xl font-bold text-white font-playfair bg-gradient-to-r from-purple-300 to-pink-300 bg-clip-text text-transparent">All Events</h2>

            {/* Sort Options */}
            <div className="flex items-center space-x-4">
              <span className="text-purple-200 font-playfair">Sort by:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="bg-white/10 backdrop-blur-sm border border-purple-400/30 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-300 font-playfair"
              >
                <option value="date" className="bg-gray-800">Date</option>
                <option value="venue" className="bg-gray-800">Venue</option>
                <option value="popularity" className="bg-gray-800">Popularity</option>
              </select>
            </div>
          </div>

          {loading ? (
            <div className="flex justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-300"></div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {sortedEvents.map((event) => (
                <div
                  key={event.id}
                  onClick={() => router.push(`/events/${event.id}`)}
                  className="rounded-xl overflow-hidden transition-all cursor-pointer hover:scale-105 duration-300"
                >
                  <div className="relative h-40">
                    <Image
                      src={event.image_url}
                      alt={event.name}
                      width={288}
                      height={160}
                      className="w-full h-full object-cover"
                      onError={handleImageError}
                    />
                  </div>

                  <div className="p-4">
                    <h3 className="text-base font-bold text-white mb-1 line-clamp-2 font-playfair">{event.name}</h3>
                    <p className="text-gray-300 mb-1 text-sm font-playfair">{event.venue_name}</p>
                    <p className="text-gray-400 text-xs mb-1 font-playfair">{event.city}, {event.state}</p>
                    <p className="text-gray-400 text-xs mb-3 font-playfair">{formatDate(event.event_date)}</p>

                    {event.artist_lineup.length > 0 && (
                      <div className="flex flex-wrap gap-1 mb-3">
                        {event.artist_lineup.slice(0, 2).map((artist, index) => (
                          <span key={index} className="text-xs bg-gray-700/50 text-gray-300 px-2 py-1 rounded font-playfair">
                            {artist}
                          </span>
                        ))}
                      </div>
                    )}

                    <div className="flex justify-between items-center">
                      <span className="text-gray-400 text-xs font-playfair">{event.ticket_count} tickets</span>
                      {event.lowest_price && (
                        <span className="text-white font-bold text-sm font-playfair">From ${event.lowest_price}</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {sortedEvents.length === 0 && !loading && (
            <div className="text-center py-12">
              <p className="text-gray-400 text-xl font-playfair">No events found</p>
              <p className="text-gray-500 mt-2 font-playfair">Try searching for something else</p>
            </div>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-12 border-t border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Tagline */}
            <div className="md:col-span-1">
              <p className="text-white text-sm font-light italic leading-relaxed">
                No more excuses,<br />
                you&apos;re coming out<br />
                tonight.
              </p>
            </div>

            {/* Company */}
            <div>
              <h3 className="text-white font-medium mb-4 text-sm">Company</h3>
              <ul className="space-y-2">
                <li><a href="/home" className="text-gray-300 hover:text-white text-sm font-light transition-colors">Home</a></li>
                <li><a href="/about" className="text-gray-300 hover:text-white text-sm font-light transition-colors">About</a></li>
                <li><a href="/faq" className="text-gray-300 hover:text-white text-sm font-light transition-colors">FAQ</a></li>
              </ul>
            </div>

            {/* Support */}
            <div>
              <h3 className="text-white font-medium mb-4 text-sm">Support</h3>
              <ul className="space-y-2">
                <li><a href="/support" className="text-gray-300 hover:text-white text-sm font-light transition-colors">Support</a></li>
                <li><a href="/request" className="text-gray-300 hover:text-white text-sm font-light transition-colors">Request an Event</a></li>
                <li><a href="/help" className="text-gray-300 hover:text-white text-sm font-light transition-colors">Help</a></li>
              </ul>
            </div>

            {/* Legal */}
            <div>
              <h3 className="text-white font-medium mb-4 text-sm">Legal</h3>
              <ul className="space-y-2">
                <li><a href="/privacy" className="text-gray-300 hover:text-white text-sm font-light transition-colors">Privacy Policy</a></li>
                <li><a href="/terms" className="text-gray-300 hover:text-white text-sm font-light transition-colors">Terms & Conditions</a></li>
              </ul>
            </div>
          </div>
        </div>
      </footer>

      {/* Authentication Modal */}
      <AuthModal isOpen={showAuthModal} onClose={() => setShowAuthModal(false)} />
    </div>
  );
}
