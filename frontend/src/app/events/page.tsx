'use client'

import { useEffect, useState } from 'react'

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

export default function EventsPage() {
  const [events, setEvents] = useState<CrowdBoltEvent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchEvents()
  }, [])

  const fetchEvents = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/events/')
      if (!response.ok) {
        throw new Error('Failed to fetch events')
      }
      const data: EventsResponse = await response.json()
      setEvents(data.results)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getCategoryColor = (category: string) => {
    const colors = {
      concert: 'bg-blue-100 text-blue-800',
      festival: 'bg-purple-100 text-purple-800',
      rave: 'bg-pink-100 text-pink-800',
      comedy: 'bg-yellow-100 text-yellow-800',
      theater: 'bg-green-100 text-green-800',
      sports: 'bg-red-100 text-red-800',
      other: 'bg-gray-100 text-gray-800'
    }
    return colors[category as keyof typeof colors] || colors.other
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading awesome events...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 text-xl">Error: {error}</p>
          <p className="text-gray-600 mt-2">Make sure the Django server is running on port 8000</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">CrowdBolt Events</h1>
          <p className="text-gray-600 mt-2">Find and buy tickets to the hottest events</p>
        </div>
      </div>

      {/* Events Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {events.map((event) => (
            <div key={event.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              {/* Event Image */}
              <div className="relative h-48">
                <img
                  src={event.image_url}
                  alt={event.name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement
                    target.src = 'https://via.placeholder.com/400x200?text=Event+Image'
                  }}
                />
                <div className="absolute top-4 left-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(event.category)}`}>
                    {event.category.charAt(0).toUpperCase() + event.category.slice(1)}
                  </span>
                </div>
              </div>

              {/* Event Details */}
              <div className="p-6">
                <h3 className="font-bold text-lg text-gray-900 mb-2">{event.name}</h3>

                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center">
                    <span className="font-medium">📍</span>
                    <span className="ml-2">{event.venue_name}</span>
                  </div>
                  <div className="flex items-center">
                    <span className="font-medium">📅</span>
                    <span className="ml-2">{formatDate(event.event_date)}</span>
                  </div>
                  <div className="flex items-center">
                    <span className="font-medium">🌍</span>
                    <span className="ml-2">{event.city}, {event.state}</span>
                  </div>
                </div>

                {/* Artists */}
                {event.artist_lineup.length > 0 && (
                  <div className="mt-4">
                    <div className="flex flex-wrap gap-1">
                      {event.artist_lineup.slice(0, 3).map((artist, index) => (
                        <span key={index} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">
                          {artist}
                        </span>
                      ))}
                      {event.artist_lineup.length > 3 && (
                        <span className="text-gray-500 text-xs">+{event.artist_lineup.length - 3} more</span>
                      )}
                    </div>
                  </div>
                )}

                {/* Ticket Info */}
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="flex justify-between items-center">
                    <div>
                      <p className="text-sm text-gray-600">{event.ticket_count} tickets available</p>
                      {event.lowest_price && (
                        <p className="text-lg font-bold text-green-600">From ${event.lowest_price}</p>
                      )}
                    </div>
                    <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
                      View Tickets
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {events.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-600 text-xl">No events found</p>
            <p className="text-gray-500 mt-2">Check back later for new events!</p>
          </div>
        )}
      </div>
    </div>
  )
}