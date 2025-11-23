import { useState, useEffect } from 'react';
import { useWebSocket } from '../../hooks/useWebSocket';
import { marketApi } from '../../services/api';
import type { CryptoPair } from '../../types';

interface Props {
    symbols: string[];
}

export const PriceTicker = ({ symbols }: Props) => {
    const { data, isConnected } = useWebSocket(symbols);
    const [tickers, setTickers] = useState<Record<string, CryptoPair>>({});
    const [loading, setLoading] = useState(true);

    // Load initial data from API
    useEffect(() => {
        const loadInitialData = async () => {
            try {
                setLoading(true);
                const response = await marketApi.getCryptoData(symbols, 'USD');
                if (response.data) {
                    setTickers(response.data);
                }
            } catch (error) {
                console.error('Failed to load initial ticker data:', error);
            } finally {
                setLoading(false);
            }
        };

        loadInitialData();
    }, [symbols.join(',')]);

    // Update with WebSocket data when available
    useEffect(() => {
        if (Object.keys(data).length > 0) {
            setTickers(prev => ({ ...prev, ...data }));
        }
    }, [data]);

    return (
        <div className="bg-gray-900 text-white p-6 rounded-lg shadow-lg">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold">Live Prices</h2>
                <div className="flex items-center space-x-2">
                    {loading && (
                        <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
                    )}
                    <span className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                        isConnected
                            ? 'bg-green-600 text-white'
                            : 'bg-red-600 text-white'
                    }`}>
                        {isConnected ? '🟢 Live' : '🔴 Offline'}
                    </span>
                </div>
            </div>

            <div className="space-y-3">
                {symbols.map(symbol => {
                    const ticker = tickers[symbol];

                    if (loading && !ticker) {
                        return (
                            <div key={symbol} className="flex justify-between items-center p-3 bg-gray-800 rounded-lg animate-pulse">
                                <div>
                                    <div className="h-4 bg-gray-700 rounded w-16 mb-1"></div>
                                    <div className="h-3 bg-gray-700 rounded w-24"></div>
                                </div>
                                <div className="text-right">
                                    <div className="h-5 bg-gray-700 rounded w-20 mb-1"></div>
                                    <div className="h-4 bg-gray-700 rounded w-16"></div>
                                </div>
                            </div>
                        );
                    }

                    if (!ticker) {
                        return (
                            <div key={symbol} className="flex justify-between items-center p-3 bg-gray-800 rounded-lg opacity-50">
                                <div>
                                    <span className="font-semibold">{symbol}</span>
                                    <span className="text-gray-400 text-sm ml-2">No data</span>
                                </div>
                                <div className="text-right">
                                    <div className="text-gray-500">--</div>
                                    <div className="text-gray-500 text-sm">--%</div>
                                </div>
                            </div>
                        );
                    }

                    const changeClass = (ticker.change_24h || 0) >= 0 ? 'text-green-400' : 'text-red-400';
                    const changeSymbol = (ticker.change_24h || 0) >= 0 ? '↑' : '↓';

                    return (
                        <div key={symbol} className="flex justify-between items-center p-3 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors">
                            <div>
                                <span className="font-semibold text-lg">{symbol}</span>
                                <span className="text-gray-400 text-sm ml-2">{ticker.name || symbol}</span>
                            </div>
                            <div className="text-right">
                                <div className="font-mono text-lg font-semibold">
                                    ${ticker.price ? ticker.price.toFixed(2) : '0.00'}
                                </div>
                                <div className={`text-sm font-medium ${changeClass} flex items-center justify-end`}>
                                    <span className="mr-1">{changeSymbol}</span>
                                    {ticker.change_24h ? Math.abs(ticker.change_24h).toFixed(2) : '0.00'}%
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>

            {!isConnected && !loading && (
                <div className="mt-4 p-3 bg-yellow-900 bg-opacity-50 border border-yellow-700 rounded-lg text-yellow-200 text-sm">
                    ⚠️ Real-time updates are currently paused. Prices may be delayed.
                </div>
            )}
        </div>
    );
};