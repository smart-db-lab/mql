import axios from 'axios';
import Cookies from 'js-cookie';
import { getToken,setToken,removeToken,getRefreshToken } from '../services/apiServices';
const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const refreshAccessToken = async () => {
  try {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await api.post('/auth/token/refresh/', {
      refresh: refreshToken,
    });
    if (!response.data || !response.data.access) {
      throw new Error('Invalid response from token refresh endpoint');
    }
    setToken(response.data.access, refreshToken);
    // Cookies.set('access_token', response.data.access);
    return response.data.access;
  } catch (error) {
    console.error('Error refreshing token:', error.response?.data || error.message);
    throw error;
  }
};

const apiRequest = async (endpoint, method, token = null, data = null, params = null) => {
  try {
    console.log(`API Request: ${method.toUpperCase()} ${endpoint}`, { token, data, params });
    const config = {
      url: endpoint,
      method: method.toUpperCase(),
      headers: {
        'Content-Type': data instanceof FormData ? 'multipart/form-data' : 'application/json',
      },
    };

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    if (data && ['POST', 'PUT', 'PATCH'].includes(method.toUpperCase())) {
      config.data = data;
    }

    if (params) {
      const query = new URLSearchParams(params).toString();
      config.url = `${endpoint}?${query}`;
    }

    const response = await api(config);
    return response.data;
  } catch (error) {
    if (error.response?.status === 401 || error.response?.data?.code === 'token_not_valid') {
      try {
        const newAccessToken = await refreshAccessToken();
        return await apiRequest(endpoint, method, newAccessToken, data, params);
      } catch (refreshError) {
        removeToken();
        window.location.href = `${import.meta.env.VITE_BASE_PATH}signin`;
        throw refreshError;
      }
    }
    throw error.response?.data || error;
  }
};

export default apiRequest;
