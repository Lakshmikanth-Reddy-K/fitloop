// API configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';
const AUTH_TOKEN = import.meta.env.VITE_AUTH_TOKEN || 'changeme123';

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = AUTH_TOKEN;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: {
        'X-Auth-Token': this.token,
        ...options.headers,
      },
      ...options,
    };

    // Don't add Content-Type for FormData
    if (!(options.body instanceof FormData) && options.body) {
      config.headers['Content-Type'] = 'application/json';
    }

    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.text();
      throw new Error(`HTTP ${response.status}: ${errorData}`);
    }

    // Handle different response types
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return response.json();
    } else if (contentType && contentType.includes('text/markdown')) {
      return response.blob();
    } else {
      return response.text();
    }
  }

  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  async post(endpoint, data) {
    const body = data instanceof FormData ? data : JSON.stringify(data);
    return this.request(endpoint, {
      method: 'POST',
      body,
    });
  }
}

export const api = new ApiClient();