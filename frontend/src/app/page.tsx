export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            CrowdBolt
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            The premier marketplace for authentic sneakers, streetwear, and collectibles.
            Buy and sell with confidence.
          </p>

          <div className="flex gap-4 justify-center mb-16">
            <button className="bg-black text-white px-8 py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors">
              Shop Now
            </button>
            <button className="border border-gray-300 text-gray-700 px-8 py-3 rounded-lg font-medium hover:bg-gray-50 transition-colors">
              Start Selling
            </button>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mt-16">
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-green-600 text-2xl">✓</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">100% Authentic</h3>
              <p className="text-gray-600">Every item is verified by our team of experts</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-blue-600 text-2xl">🚀</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Fast Shipping</h3>
              <p className="text-gray-600">Get your items delivered quickly and safely</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-purple-600 text-2xl">💎</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Premium Experience</h3>
              <p className="text-gray-600">Curated selection of the most sought-after items</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
