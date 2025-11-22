import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const marketApi = {
    getCryptoList: async () => {
        const response = await api.get('/market/list');
        return response.data;
    },

    getTopCryptos: async (limit = 100) => {
        const response = await api.get(`/market/top?limit=${limit}`);
        return response.data;
    },

    getCryptoData: async (symbols: string[], currency = 'USD') => {
        const response = await api.post('/market/data', { symbols, currency });
        return response.data;
    },

    getFearGreed: async (): Promise<FearGreedResponse> => {
        const response = await api.get('/market/fear-greed');
        return response.data;
    },
};

export default api;