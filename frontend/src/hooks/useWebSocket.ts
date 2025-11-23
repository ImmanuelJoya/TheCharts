import { useEffect, useState, useCallback } from 'react';
import type { CryptoPair } from '../types';
import wsManager from '../services/websocketManager';

export const useWebSocket = (symbols: string[]) => {
    const [data, setData] = useState<Record<string, CryptoPair>>({});
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        wsManager.connect();

        const unsubscribe = wsManager.onMessage((newData) => {
            setData(prev => ({ ...prev, ...newData }));
        });

        wsManager.subscribe(symbols);
        setIsConnected(wsManager.isConnected());

        return () => {
            wsManager.unsubscribe(symbols);
            unsubscribe();
            wsManager.disconnect();
        };
    }, [symbols.join(',')]);

    const subscribe = useCallback((newSymbols: string[]) => {
        wsManager.subscribe(newSymbols);
    }, []);

    const unsubscribe = useCallback((symbolsToRemove: string[]) => {
        wsManager.unsubscribe(symbolsToRemove);
    }, []);

    return { data, isConnected, subscribe, unsubscribe };
};