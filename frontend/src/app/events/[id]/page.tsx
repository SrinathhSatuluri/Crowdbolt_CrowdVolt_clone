'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import AuthModal from '@/components/AuthModal'
import { API_ENDPOINTS, apiCall } from '@/lib/api'
import { mockEvents, mockEventStats } from '@/lib/mockData'

interface EventDetails {
  id: string
  name: string
  category: string
  venue_name: string
  venue_address: string
  city: string
  state: string
  event_date: string
  doors_open: string
  image_url: string
  artist_lineup: string[]
  description: string
  ticket_count: number
  lowest_price: number | null
  highest_price: number | null
}

interface TicketStats {
  total_tickets: number
  interested_buyers: number
  avg_price: number
  last_sale_price: number | null
}

export default function EventDetailsPage() {
  const params = useParams()
  const router = useRouter()
  const [event, setEvent] = useState<EventDetails | null>(null)
  const [ticketStats, setTicketStats] = useState<TicketStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [activeSection, setActiveSection] = useState<'tickets' | 'buyers' | null>(null)

  useEffect(() => {
    if (params.id) {
      const useMockData = process.env.NEXT_PUBLIC_USE_MOCK_DATA === 'true'

      if (useMockData) {
        // Use mock data for demo
        const mockEvent = mockEvents.find(e => e.id.toString() === params.id)
        if (mockEvent) {
          const transformedEvent = {
            id: mockEvent.id.toString(),
            name: mockEvent.title,
            category: mockEvent.category,
            venue_name: mockEvent.location,
            venue_address: `${mockEvent.location} Venue`,
            city: mockEvent.location.split(',')[0],
            state: mockEvent.location.split(',')[1]?.trim() || '',
            event_date: mockEvent.date,
            doors_open: '7:00 PM',
            image_url: mockEvent.image_url,
            artist_lineup: [mockEvent.category],
            description: mockEvent.description,
            ticket_count: mockEvent.ticket_count,
            lowest_price: mockEvent.lowest_price,
            highest_price: mockEvent.highest_price
          }
          setEvent(transformedEvent)
          setTicketStats(mockEventStats)
        } else {
          router.push('/')
        }
        setLoading(false)
      } else {
        // Use real API calls
        fetchEventDetails()
        fetchTicketStats()
      }
    }
  }, [params.id, router])

  const fetchEventDetails = async () => {
    try {
      const response = await apiCall(API_ENDPOINTS.eventDetail(params.id as string))
      if (response.ok) {
        const data = await response.json()
        setEvent(data)
      } else {
        router.push('/')
      }
    } catch (error) {
      console.error('Failed to fetch event details:', error)
      router.push('/')
    } finally {
      setLoading(false)
    }
  }

  const fetchTicketStats = async () => {
    try {
      const response = await apiCall(API_ENDPOINTS.eventStats(params.id as string))
      if (response.ok) {
        const data = await response.json()
        setTicketStats(data)
      }
    } catch (error) {
      console.error('Failed to fetch ticket stats:', error)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const handleBuyClick = () => {
    setShowAuthModal(true)
  }

  const handleSellClick = () => {
    setShowAuthModal(true)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-300"></div>
      </div>
    )
  }

  if (!event) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-4">Event Not Found</h2>
          <button
            onClick={() => router.push('/')}
            className="bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600 transition-colors"
          >
            Back to Events
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black">
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

            {/* Center - Back Button */}
            <div className="flex-1 max-w-md mx-8 flex justify-center">
              <button
                onClick={() => router.push('/')}
                className="flex items-center space-x-2 text-purple-200 hover:text-white transition-colors font-playfair"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                <span>Back to Events</span>
              </button>
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

      <div className="max-w-6xl mx-auto px-6 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Side - Event Image and Info */}
          <div className="space-y-4">
            {/* Event Image */}
            <div className="relative rounded-xl overflow-hidden">
              <img
                src={event.image_url}
                alt={event.name}
                className="w-full h-64 object-cover"
              />
            </div>

            {/* Event Details */}
            <div className="space-y-3">
              <div>
                <h1 className="text-3xl font-bold text-white font-playfair mb-2">{event.name}</h1>
                <p className="text-gray-400 font-playfair uppercase text-sm tracking-wider">{event.category}</p>
              </div>

              <div className="space-y-1">
                <div className="flex items-center space-x-2 text-gray-300">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                  </svg>
                  <span className="font-playfair text-sm">{event.venue_name}</span>
                </div>
                <p className="text-gray-400 font-playfair ml-6 text-sm">{event.venue_address}</p>
                <p className="text-gray-400 font-playfair ml-6 text-sm">{event.city}, {event.state}</p>
              </div>

              <div className="flex items-center space-x-2 text-gray-300">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
                </svg>
                <span className="font-playfair text-sm">{formatDate(event.event_date)}</span>
              </div>

              {event.artist_lineup.length > 0 && (
                <div className="space-y-2">
                  <h3 className="text-base font-semibold text-white font-playfair">Lineup</h3>
                  <div className="flex flex-wrap gap-1">
                    {event.artist_lineup.map((artist, index) => (
                      <span key={index} className="bg-purple-900/30 text-purple-200 px-2 py-1 rounded-full text-xs font-playfair">
                        {artist}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="space-y-2">
                <h3 className="text-base font-semibold text-white font-playfair">Description</h3>
                <p className="text-gray-300 font-playfair text-sm leading-relaxed">{event.description}</p>
              </div>
            </div>
          </div>

          {/* Right Side - Ticket Trading */}
          <div className="space-y-4">
            {/* Trading Section */}
            <div className="space-y-4">
              {/* Buy and Sell Buttons */}
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={handleBuyClick}
                  className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-lg font-bebas text-lg tracking-wider transition-colors flex items-center justify-center"
                >
                  <span>BUY</span>
                  {event.lowest_price && (
                    <>
                      <div className="w-px h-4 bg-white/30 mx-3"></div>
                      <span>${event.lowest_price}</span>
                    </>
                  )}
                </button>
                <button
                  onClick={handleSellClick}
                  className="bg-white hover:bg-gray-200 text-black font-bold py-3 rounded-lg font-bebas text-lg tracking-wider transition-colors"
                >
                  SELL
                </button>
              </div>

              {/* Available Tickets and Interested Buyers */}
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={() => setActiveSection(activeSection === 'tickets' ? null : 'tickets')}
                  className={`text-center py-3 px-4 rounded-lg transition-colors cursor-pointer font-playfair ${
                    activeSection === 'tickets'
                      ? 'bg-purple-900/30 text-purple-300'
                      : 'hover:bg-gray-800/50 text-white'
                  }`}
                >
                  Available Tickets
                </button>
                <button
                  onClick={() => setActiveSection(activeSection === 'buyers' ? null : 'buyers')}
                  className={`text-center py-3 px-4 rounded-lg transition-colors cursor-pointer font-playfair ${
                    activeSection === 'buyers'
                      ? 'bg-purple-900/30 text-purple-300'
                      : 'hover:bg-gray-800/50 text-white'
                  }`}
                >
                  Interested Buyers
                </button>
              </div>

              {/* Inline Display Area */}
              {activeSection && (
                <div className="mt-4 space-y-3">
                  {activeSection === 'tickets' && (
                    <div className="space-y-2">
                      {[
                        { name: 'Sarah Johnson', section: 'VIP', price: 189, avatar: 'https://images.unsplash.com/photo-1494790108755-2616b612b743?w=150' },
                        { name: 'Mike Chen', section: 'GA', price: 145, avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150' },
                        { name: 'Alex Rivera', section: 'Section A', price: 167, avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150' },
                        { name: 'Jessica Park', section: 'VIP', price: 195, avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150' },
                      ].map((seller, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-black/20 rounded-lg">
                          <div className="flex items-center space-x-3">
                            <img
                              src={seller.avatar}
                              alt={seller.name}
                              className="w-8 h-8 rounded-full object-cover"
                            />
                            <div>
                              <p className="text-white text-sm font-playfair">{seller.name}</p>
                              <p className="text-gray-400 text-xs font-playfair">{seller.section}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-green-400 font-bold text-sm font-bebas">${seller.price}</p>
                            <button className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-xs font-bebas transition-colors">
                              BUY
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {activeSection === 'buyers' && (
                    <div className="space-y-2">
                      {[
                        { name: 'Emma Wilson', wantedPrice: 120, maxPrice: 150, avatar: 'https://images.unsplash.com/photo-1489424731084-a5d8b219a5bb?w=150' },
                        { name: 'James Thompson', wantedPrice: 135, maxPrice: 160, avatar: 'https://images.unsplash.com/photo-1507101105822-7472b28e22ac?w=150' },
                        { name: 'Lisa Martinez', wantedPrice: 175, maxPrice: 200, avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150' },
                        { name: 'Ryan Lee', wantedPrice: 110, maxPrice: 140, avatar: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150' },
                      ].map((buyer, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-black/20 rounded-lg">
                          <div className="flex items-center space-x-3">
                            <img
                              src={buyer.avatar}
                              alt={buyer.name}
                              className="w-8 h-8 rounded-full object-cover"
                            />
                            <div>
                              <p className="text-white text-sm font-playfair">{buyer.name}</p>
                              <p className="text-gray-400 text-xs font-playfair">Wants ${buyer.wantedPrice}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-blue-400 font-bold text-sm font-bebas">Max: ${buyer.maxPrice}</p>
                            <button className="bg-white hover:bg-gray-200 text-black px-3 py-1 rounded text-xs font-bebas transition-colors">
                              SELL
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Authentication Modal */}
      <AuthModal isOpen={showAuthModal} onClose={() => setShowAuthModal(false)} />
    </div>
  )
}