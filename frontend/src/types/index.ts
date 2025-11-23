export interface CryptoPair {
    symbol: string;
    name: string;
    currency: string;
    price: number;
    market_cap?: number;
    volume_24h?: number;
    change_24h?: number;
}

export interface CryptoDataResponse {
    data: Record<string, CryptoPair>;
}

export interface TopCrypto extends CryptoPair {
    rank: number;
}

export interface FearGreedResponse {
    value: number;
    classification: string;
    timestamp: string;
}

export interface WSMessage {
    type: 'update';
    data: Record<string, CryptoPair>;
}

export interface WSSubscribe {
    action: 'subscribe';
    symbols: string[];
}

export interface WSUnsubscribe {
    action: 'unsubscribe';
    symbols: string[];
}