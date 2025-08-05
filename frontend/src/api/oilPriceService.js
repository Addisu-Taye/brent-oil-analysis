
// src/api/oilPriceService.js
import axios from 'axios';
import { getApiUrl } from '../config';

// Create a custom axios instance with default settings
const api = axios.create({
  baseURL: process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: process.env.NODE_ENV === 'development' // Send cookies in dev
});

// Add request interceptor for logging
api.interceptors.request.use(config => {
  console.log(`Making ${config.method.toUpperCase()} request to ${config.url}`);
  return config;
}, error => {
  console.error('Request error:', error);
  return Promise.reject(error);
});

// Add response interceptor for error handling
api.interceptors.response.use(response => {
  return response;
}, error => {
  if (error.response) {
    // Server responded with a status code outside 2xx
    console.error('API Error:', {
      status: error.response.status,
      data: error.response.data,
      url: error.config.url
    });
  } else if (error.request) {
    // Request was made but no response received
    console.error('No response received:', error.request);
  } else {
    // Something happened in setting up the request
    console.error('Request setup error:', error.message);
  }
  return Promise.reject(error);
});

// Cache variables
const cache = {
  prices: null,
  events: null,
  changePoints: null,
  indicators: null,
  lastFetch: null
};

// Cache validity duration (5 minutes)
const CACHE_DURATION = 5 * 60 * 1000; 

/**
 * Fetches oil prices with caching support
 * @param {boolean} forceRefresh Bypass cache
 * @param {AbortSignal} signal Optional abort signal
 * @returns {Promise} Oil price data
 */
export const fetchOilPrices = async (forceRefresh = false, signal = null) => {
  if (!forceRefresh && cache.prices && Date.now() - cache.lastFetch < CACHE_DURATION) {
    return cache.prices;
  }

  try {
    const response = await api.get(getApiUrl('PRICES'), { signal });
    cache.prices = response.data;
    cache.lastFetch = Date.now();
    return response.data;
  } catch (error) {
    if (axios.isCancel(error)) {
      console.log('Request canceled:', error.message);
    } else {
      console.error('Error fetching oil prices:', error);
    }
    throw error;
  }
};

/**
 * Fetches oil market events
 * @param {AbortSignal} signal Optional abort signal
 * @returns {Promise} Events data
 */
export const fetchEvents = async (signal = null) => {
  try {
    const response = await api.get(getApiUrl('EVENTS'), { signal });
    return response.data;
  } catch (error) {
    if (axios.isCancel(error)) {
      console.log('Request canceled:', error.message);
    } else {
      console.error('Error fetching events:', error);
    }
    throw error;
  }
};

/**
 * Fetches change points data
 * @param {AbortSignal} signal Optional abort signal
 * @returns {Promise} Change points data
 */
export const fetchChangePoints = async (signal = null) => {
  try {
    const response = await api.get(getApiUrl('CHANGE_POINTS'), { signal });
    return response.data;
  } catch (error) {
    if (axios.isCancel(error)) {
      console.log('Request canceled:', error.message);
    } else {
      console.error('Error fetching change points:', error);
    }
    throw error;
  }
};

/**
 * Fetches market indicators
 * @param {AbortSignal} signal Optional abort signal
 * @returns {Promise} Indicators data
 */
export const fetchIndicators = async (signal = null) => {
  try {
    const response = await api.get(getApiUrl('INDICATORS'), { signal });
    return response.data;
  } catch (error) {
    if (axios.isCancel(error)) {
      console.log('Request canceled:', error.message);
    } else {
      console.error('Error fetching indicators:', error);
    }
    throw error;
  }
};

/**
 * Batch fetches all data with cancellation support
 * @param {Object} options Configuration options
 * @param {boolean} options.forceRefresh Bypass cache for prices
 * @param {AbortSignal} options.signal Abort signal for cancellation
 * @returns {Promise} Object containing all data
 */
export const fetchAllData = async ({ forceRefresh = false, signal = null } = {}) => {
  try {
    const [prices, events, changePoints, indicators] = await Promise.all([
      fetchOilPrices(forceRefresh, signal),
      fetchEvents(signal),
      fetchChangePoints(signal),
      fetchIndicators(signal)
    ]);
    
    return { 
      prices,
      events,
      changePoints,
      indicators,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    if (axios.isCancel(error)) {
      console.log('Batch request canceled:', error.message);
    } else {
      console.error('Error in batch data fetch:', error);
    }
    throw error;
  }
};

/**
 * Clears the API cache
 */
export const clearCache = () => {
  cache.prices = null;
  cache.events = null;
  cache.changePoints = null;
  cache.indicators = null;
  cache.lastFetch = null;
};