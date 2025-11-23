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
        <div className="bg-gray-900 text-white p-4 rounded-lg shadow-lg">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Live Prices</h2>
                <span className={`px-2 py-1 rounded text-xs ${isConnected ? 'bg-green-600' : 'bg-red-600'
                    }`}>
                    {isConnected ? 'Connected' : 'Disconnected'}
                </span>
            </div>

            <div className="space-y-2">
                {symbols.map(symbol => {
                    const ticker = tickers[symbol];
                    if (!ticker) return null;

                    const changeClass = (ticker.change_24h || 0) >= 0 ? 'text-green-500' : 'text-red-500';

                    return (
                        <div key={symbol} className="flex justify-between items-center p-2 bg-gray-800 rounded">
                            <div>
                                <span className="font-semibold">{symbol}</span>
                                <span className="text-gray-400 text-sm ml-2">{ticker.name}</span>
                            </div>
                            <div className="text-right">
                                <div className="font-mono">${ticker.price.toFixed(2)}</div>
                                <div className={`text-sm ${changeClass}`}>
                                    {ticker.change_24h?.toFixed(2)}%
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};