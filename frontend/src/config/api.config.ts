/**
 * API Configuration
 * 
 * Frontend configuration for API communication
 */

export const config = {
  apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:3000/api',
  apiTimeout: 10000,
  enableMockData: process.env.REACT_APP_USE_MOCK === 'true',
  features: {
    analytics: true,
    marketing: true,
    support: true,
  },
};

export default config;
