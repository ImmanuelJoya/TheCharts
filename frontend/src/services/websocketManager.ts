import { io, Socket } from 'socket.io-client';
import type { CryptoPair } from '../types';

class WebSocketManager {
    private socket: Socket | null = null;
    private subscribedSymbols: Set<string> = new Set();
    private messageHandlers: Array<(data: Record<string, CryptoPair>) => void> = [];

    connect(url = 'http://localhost:8000') {
        if (this.socket?.connected) return;

        this.socket = io(url, {
            transports: ['websocket'],
            reconnection: true,
            reconnectionAttempts: 5,
            reconnectionDelay: 1000,
        });

        this.socket.on('connect', () => {
            console.log('✓ Connected to WebSocket server');
            this.resubscribeAll();
        });

        this.socket.on('disconnect', () => {
            console.log('✗ Disconnected from WebSocket server');
        });

        this.socket.on('crypto_update', (message) => {
            if (message.type === 'update') {
                this.messageHandlers.forEach(handler => handler(message.data));
            }
        });

        this.socket.on('error', (error) => {
            console.error('WebSocket error:', error);
        });
    }

    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
        }
    }

    subscribe(symbols: string[]) {
        if (!this.socket?.connected) return;

        symbols.forEach(symbol => this.subscribedSymbols.add(symbol));

        this.socket.emit('subscribe', {
            action: 'subscribe',
            symbols: Array.from(this.subscribedSymbols),
        });
    }

    unsubscribe(symbols: string[]) {
        if (!this.socket?.connected) return;

        symbols.forEach(symbol => this.subscribedSymbols.delete(symbol));

        this.socket.emit('unsubscribe', {
            action: 'unsubscribe',
            symbols,
        });
    }

    private resubscribeAll() {
        if (this.subscribedSymbols.size > 0) {
            this.socket?.emit('subscribe', {
                action: 'subscribe',
                symbols: Array.from(this.subscribedSymbols),
            });
        }
    }

    onMessage(handler: (data: Record<string, CryptoPair>) => void) {
        this.messageHandlers.push(handler);
        return () => {
            this.messageHandlers = this.messageHandlers.filter(h => h !== handler);
        };
    }

    isConnected(): boolean {
        return this.socket?.connected || false;
    }
}

export default new WebSocketManager();