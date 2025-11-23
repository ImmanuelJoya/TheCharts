import { useState, useEffect } from 'react';
import { PriceTicker } from './components/market/PriceTicker';
import { marketApi } from './services/api';
import type { TopCrypto, FearGreedResponse } from './types';

function App() {
  const [fearGreed, setFearGreed] = useState<FearGreedResponse | null>(null);
  const [topCryptos, setTopCryptos] = useState<TopCrypto[]>([]);

  useEffect(() => {
    // Load initial data
    marketApi.getFearGreed().then(setFearGreed);
    marketApi.getTopCryptos(10).then(setTopCryptos);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">CryptoCarts Dashboard</h1>
        <p className="text-gray-600 mt-2">Real-time cryptocurrency monitoring platform</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Live Price Ticker */}
        <div className="lg:col-span-2">
          <PriceTicker symbols={['BTC', 'ETH', 'ADA', 'SOL', 'DOT']} />
        </div>

        {/* Fear & Greed Index */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Fear & Greed Index</h2>
          {fearGreed ? (
            <div>
              <div className="text-3xl font-bold text-center mb-2">{fearGreed.value}</div>
              <div className="text-center px-4 py-2 bg-gray-100 rounded">
                {fearGreed.classification}
              </div>
            </div>
          ) : (
            <div className="animate-pulse bg-gray-200 h-20 rounded"></div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;