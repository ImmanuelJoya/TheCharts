import { useState, useEffect } from 'react';
import { PriceTicker } from './components/market/PriceTicker';
import { marketApi } from './services/api';
import type { TopCrypto, FearGreedResponse } from './types';

function App() {
  const [fearGreed, setFearGreed] = useState<FearGreedResponse | null>(null);
  const [topCryptos, setTopCryptos] = useState<TopCrypto[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        // Load initial data
        const [fearGreedData, topCryptosData] = await Promise.all([
          marketApi.getFearGreed(),
          marketApi.getTopCryptos(10)
        ]);

        setFearGreed(fearGreedData);
        setTopCryptos(topCryptosData || []);
      } catch (error) {
        console.error('Failed to load market data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const getFearGreedColor = (value: number) => {
    if (value < 25) return 'bg-red-500';
    if (value < 45) return 'bg-orange-500';
    if (value < 55) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-900 bg-opacity-50 backdrop-blur-sm border-b border-gray-700 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
                TheCharts
              </h1>
              <p className="text-gray-400 mt-2">Real-time cryptocurrency monitoring platform</p>
            </div>
            {loading && (
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
                <span className="text-gray-400">Loading...</span>
              </div>
            )}
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          {/* Live Price Ticker - Takes 2 columns on XL screens */}
          <div className="xl:col-span-2">
            <PriceTicker symbols={['BTC', 'ETH', 'ADA', 'SOL', 'DOT', 'MATIC', 'LINK']} />
          </div>

          {/* Right Sidebar */}
          <div className="space-y-6">
            {/* Fear & Greed Index */}
            <div className="bg-gray-800 bg-opacity-50 backdrop-blur-sm rounded-xl shadow-xl border border-gray-700">
              <div className="p-6">
                <h2 className="text-xl font-semibold mb-4 flex items-center">
                  <span className="mr-2">📊</span>
                  Fear & Greed Index
                </h2>
                {fearGreed ? (
                  <div>
                    <div className="text-5xl font-bold text-center mb-4">{fearGreed.value}</div>
                    <div className={`text-center px-4 py-3 rounded-lg font-medium text-white ${getFearGreedColor(fearGreed.value)}`}>
                      {fearGreed.classification}
                    </div>
                    <div className="mt-4 text-center text-sm text-gray-400">
                      Market sentiment indicator (0-100)
                    </div>
                  </div>
                ) : (
                  <div className="animate-pulse">
                    <div className="h-20 bg-gray-700 rounded-lg mb-4"></div>
                    <div className="h-6 bg-gray-700 rounded"></div>
                  </div>
                )}
              </div>
            </div>

            {/* Top Cryptos */}
            <div className="bg-gray-800 bg-opacity-50 backdrop-blur-sm rounded-xl shadow-xl border border-gray-700">
              <div className="p-6">
                <h2 className="text-xl font-semibold mb-4 flex items-center">
                  <span className="mr-2">🏆</span>
                  Top Cryptocurrencies
                </h2>
                {topCryptos.length > 0 ? (
                  <div className="space-y-3">
                    {topCryptos.slice(0, 5).map((crypto, index) => (
                      <div key={crypto.symbol} className="flex items-center justify-between p-3 bg-gray-700 bg-opacity-50 rounded-lg hover:bg-opacity-70 transition-colors">
                        <div className="flex items-center">
                          <span className="text-2xl font-bold text-gray-500 mr-3 w-8">#{crypto.rank || index + 1}</span>
                          <div>
                            <div className="font-semibold">{crypto.symbol}</div>
                            <div className="text-sm text-gray-400">{crypto.name}</div>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="font-mono text-sm">
                            ${crypto.price ? crypto.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : '0.00'}
                          </div>
                          <div className={`text-xs ${crypto.change_24h >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {crypto.change_24h >= 0 ? '+' : ''}{crypto.change_24h?.toFixed(2)}%
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="space-y-3">
                    {[1, 2, 3, 4, 5].map((i) => (
                      <div key={i} className="animate-pulse">
                        <div className="h-12 bg-gray-700 rounded-lg mb-2"></div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Market Stats */}
            <div className="bg-gray-800 bg-opacity-50 backdrop-blur-sm rounded-xl shadow-xl border border-gray-700 p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <span className="mr-2">📈</span>
                Market Overview
              </h2>
              <div className="space-y-3">
                <div className="flex justify-between items-center p-3 bg-gray-700 bg-opacity-50 rounded-lg">
                  <span className="text-gray-300">Market Status</span>
                  <span className="px-2 py-1 bg-green-600 bg-opacity-20 text-green-400 rounded text-sm">Active</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-700 bg-opacity-50 rounded-lg">
                  <span className="text-gray-300">Data Source</span>
                  <span className="text-blue-400">FreeCryptoAPI</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-700 bg-opacity-50 rounded-lg">
                  <span className="text-gray-300">Update Mode</span>
                  <span className="text-purple-400">Real-time</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 py-6 border-t border-gray-700 text-center text-gray-400">
          <p>© 2024 TheCharts - Real-time Crypto Monitoring Platform</p>
          <p className="text-sm mt-2">Powered by FastAPI & React</p>
        </div>
      </div>
    </div>
  );
}

export default App;