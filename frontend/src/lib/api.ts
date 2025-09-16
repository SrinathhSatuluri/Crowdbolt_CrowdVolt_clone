// API configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const API_ENDPOINTS = {
  events: `${API_BASE_URL}/api/events/`,
  trending: `${API_BASE_URL}/api/trending/`,
  eventDetail: (id: string) => `${API_BASE_URL}/api/events/${id}/`,
  eventStats: (id: string) => `${API_BASE_URL}/api/events/${id}/stats/`,
  tickets: `${API_BASE_URL}/api/tickets/`,
  auth: {
    login: `${API_BASE_URL}/api/auth/login/`,
    register: `${API_BASE_URL}/api/auth/register/`,
    refresh: `${API_BASE_URL}/api/auth/refresh/`,
  }
}

// Helper function for API calls
export const apiCall = async (url: string, options?: RequestInit) => {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    })
    return response
  } catch (error) {
    console.error('API call failed:', error)
    throw error
  }
}