import { configureStore, createSlice } from '@reduxjs/toolkit'
import authReducer from './authSlice'

// Simple placeholder slice for now
const appSlice = createSlice({
  name: 'app',
  initialState: {
    loading: false,
  },
  reducers: {
    setLoading: (state, action) => {
      state.loading = action.payload
    },
  },
})

export const store = configureStore({
  reducer: {
    app: appSlice.reducer,
    auth: authReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch