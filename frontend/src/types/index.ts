// Common types used across the application

export interface User {
  id: string
  email: string
  firstName: string
  lastName: string
  avatar?: string
  createdAt: string
  updatedAt: string
}

export interface Product {
  id: string
  name: string
  brand: string
  category: string
  description: string
  imageUrl: string
  sizes: string[]
  price: number
  createdAt: string
  updatedAt: string
}

export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  totalPages: number
}