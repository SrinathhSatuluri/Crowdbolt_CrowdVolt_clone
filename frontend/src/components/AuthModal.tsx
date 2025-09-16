'use client'

import { useState } from 'react'

interface AuthModalProps {
  isOpen: boolean
  onClose: () => void
}

export default function AuthModal({ isOpen, onClose }: AuthModalProps) {
  const [step, setStep] = useState<'phone' | 'verification'>('phone')
  const [phoneNumber, setPhoneNumber] = useState('')
  const [verificationCode, setVerificationCode] = useState('')
  const [loading, setLoading] = useState(false)

  const handlePhoneSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    // Simulate API call
    setTimeout(() => {
      setStep('verification')
      setLoading(false)
    }, 1500)
  }

  const handleVerificationSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    // Simulate verification
    setTimeout(() => {
      setLoading(false)
      onClose()
      // Here you would typically store the auth token and redirect
      alert('Welcome to CrowdBolt! 🎉')
    }, 1500)
  }

  const resetModal = () => {
    setStep('phone')
    setPhoneNumber('')
    setVerificationCode('')
    setLoading(false)
  }

  const handleClose = () => {
    resetModal()
    onClose()
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gradient-to-b from-purple-900 via-purple-800 to-gray-900 rounded-2xl border border-purple-400/30 p-8 max-w-md w-full relative">
        {/* Close Button */}
        <button
          onClick={handleClose}
          className="absolute top-4 right-4 text-purple-200 hover:text-white transition-colors"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Logo */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <div className="relative">
              <div className="w-12 h-12 bg-black rounded-full flex items-center justify-center shadow-lg border-2 border-gray-800">
                <svg className="w-7 h-7 text-purple-400" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M13 2L3 14h6l-2 8 10-12h-6l2-8z"/>
                </svg>
              </div>
            </div>
            <h1 className="text-3xl font-bold text-white font-cinzel bg-gradient-to-r from-purple-300 to-pink-300 bg-clip-text text-transparent">
              CrowdBolt
            </h1>
          </div>
          <h2 className="text-2xl font-bold text-white font-playfair">Join the Party</h2>
          <p className="text-purple-200 mt-2 font-playfair">
            {step === 'phone' ? 'Enter your phone number to get started' : 'Enter the verification code sent to your phone'}
          </p>
        </div>

        {step === 'phone' ? (
          <form onSubmit={handlePhoneSubmit} className="space-y-6">
            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-purple-200 mb-2 font-playfair">
                Phone Number
              </label>
              <input
                type="tel"
                id="phone"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                placeholder="+1 (555) 123-4567"
                className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border border-purple-400/30 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:border-purple-300 focus:bg-white/20 transition-all font-playfair"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading || !phoneNumber}
              className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-playfair"
            >
              {loading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Sending Code...</span>
                </div>
              ) : (
                'Send Verification Code'
              )}
            </button>
          </form>
        ) : (
          <form onSubmit={handleVerificationSubmit} className="space-y-6">
            <div>
              <label htmlFor="code" className="block text-sm font-medium text-purple-200 mb-2 font-playfair">
                Verification Code
              </label>
              <input
                type="text"
                id="code"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value)}
                placeholder="123456"
                className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border border-purple-400/30 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:border-purple-300 focus:bg-white/20 transition-all text-center text-2xl tracking-widest font-playfair"
                maxLength={6}
                required
              />
              <p className="text-sm text-purple-300 mt-2 font-playfair">
                Sent to {phoneNumber}
              </p>
            </div>
            <button
              type="submit"
              disabled={loading || verificationCode.length < 6}
              className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-playfair"
            >
              {loading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Verifying...</span>
                </div>
              ) : (
                'Verify & Join'
              )}
            </button>
            <button
              type="button"
              onClick={() => setStep('phone')}
              className="w-full py-2 text-purple-300 hover:text-white transition-colors text-sm font-playfair"
            >
              Back to phone number
            </button>
          </form>
        )}
      </div>
    </div>
  )
}