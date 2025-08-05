// src/config.js
const API_CONFIG = {
  BASE_URL: process.env.NODE_ENV === 'development' 
    ? 'http://localhost:5000'  // Development
    : '/',                     // Production
  ENDPOINTS: {
    PRICES: '/api/prices',
    EVENTS: '/api/events',
    CHANGE_POINTS: '/api/change_points',
    INDICATORS: '/api/indicators'
  }
};

// Helper function to build full API URLs
export const getApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS[endpoint]}`;
};

export default API_CONFIG;