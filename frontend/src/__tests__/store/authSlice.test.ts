import { configureStore } from '@reduxjs/toolkit'
import authReducer, {
  setUser,
  clearAuth,
  setTokens,
  setLoading,
  setError,
  updateUser,
  User
} from '../../store/authSlice'

// Create a typed store for testing
const createTestStore = () => configureStore({
  reducer: {
    auth: authReducer
  }
})

type TestStore = ReturnType<typeof createTestStore>

// Mock user data
const mockUser: User = {
  id: '1',
  email: 'test@crowdbolt.com',
  username: 'testuser',
  role: 'buyer',
  isVerified: true,
  identityVerified: false
}

const mockTokens = {
  token: 'mock-access-token',
  refreshToken: 'mock-refresh-token'
}

describe('authSlice', () => {
  let store: TestStore

  beforeEach(() => {
    store = createTestStore()
  })

  describe('initial state', () => {
    it('should have correct initial state', () => {
      const state = store.getState().auth

      expect(state.user).toBeNull()
      expect(state.token).toBeNull()
      expect(state.refreshToken).toBeNull()
      expect(state.isAuthenticated).toBe(false)
      expect(state.isLoading).toBe(false)
      expect(state.error).toBeNull()
    })
  })

  describe('setLoading action', () => {
    it('should handle setLoading', () => {
      store.dispatch(setLoading(true))
      const state = store.getState().auth

      expect(state.isLoading).toBe(true)
    })
  })

  describe('setError action', () => {
    it('should handle setError', () => {
      const errorMessage = 'Something went wrong'
      store.dispatch(setError(errorMessage))
      const state = store.getState().auth

      expect(state.error).toBe(errorMessage)
    })
  })

  describe('setUser action', () => {
    it('should handle setUser', () => {
      store.dispatch(setUser(mockUser))
      const state = store.getState().auth

      expect(state.user).toEqual(mockUser)
      expect(state.isAuthenticated).toBe(true)
      expect(state.error).toBeNull()
    })
  })

  describe('setTokens action', () => {
    it('should handle setTokens', () => {
      store.dispatch(setTokens(mockTokens))
      const state = store.getState().auth

      expect(state.token).toBe(mockTokens.token)
      expect(state.refreshToken).toBe(mockTokens.refreshToken)
    })
  })

  describe('clearAuth action', () => {
    it('should handle clearAuth', () => {
      // First set some auth data
      store.dispatch(setUser(mockUser))
      store.dispatch(setTokens(mockTokens))

      // Then clear it
      store.dispatch(clearAuth())
      const state = store.getState().auth

      expect(state.user).toBeNull()
      expect(state.token).toBeNull()
      expect(state.refreshToken).toBeNull()
      expect(state.isAuthenticated).toBe(false)
      expect(state.error).toBeNull()
    })
  })

  describe('updateUser action', () => {
    it('should handle updateUser', () => {
      // First set a user
      store.dispatch(setUser(mockUser))

      // Then update some fields
      const updates = { isVerified: false, identityVerified: true }
      store.dispatch(updateUser(updates))
      const state = store.getState().auth

      expect(state.user?.isVerified).toBe(false)
      expect(state.user?.identityVerified).toBe(true)
      expect(state.user?.email).toBe(mockUser.email) // Other fields should remain
    })

    it('should not update user if no user exists', () => {
      const updates = { isVerified: false }
      store.dispatch(updateUser(updates))
      const state = store.getState().auth

      expect(state.user).toBeNull()
    })
  })
})