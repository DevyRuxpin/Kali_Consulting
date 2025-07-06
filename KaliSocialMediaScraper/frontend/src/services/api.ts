import axios, { AxiosInstance, AxiosResponse } from 'axios';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default configuration
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for authentication and logging
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Log requests in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    // Handle different types of errors
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      
      switch (status) {
        case 401:
          // Unauthorized - redirect to login
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
          break;
        case 403:
          // Forbidden
          console.error('Access forbidden:', data);
          break;
        case 404:
          // Not found
          console.error('Resource not found:', data);
          break;
        case 429:
          // Rate limited
          console.error('Rate limited:', data);
          break;
        case 500:
          // Server error
          console.error('Server error:', data);
          break;
        default:
          console.error(`HTTP ${status}:`, data);
      }
    } else if (error.request) {
      // Network error
      console.error('Network error:', error.request);
    } else {
      // Other error
      console.error('Request error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// API Service Classes
export class InvestigationService {
  static async getInvestigations(): Promise<any[]> {
    try {
      const response = await api.get('/api/v1/investigations/');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch investigations:', error);
      throw error;
    }
  }

  static async createInvestigation(data: any): Promise<any> {
    try {
      const response = await api.post('/api/v1/investigations/', data);
      return response.data;
    } catch (error) {
      console.error('Failed to create investigation:', error);
      throw error;
    }
  }

  static async getInvestigation(id: string): Promise<any> {
    try {
      const response = await api.get(`/api/v1/investigations/${id}`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch investigation:', error);
      throw error;
    }
  }

  static async updateInvestigation(id: string, data: any): Promise<any> {
    try {
      const response = await api.put(`/api/v1/investigations/${id}`, data);
      return response.data;
    } catch (error) {
      console.error('Failed to update investigation:', error);
      throw error;
    }
  }

  static async deleteInvestigation(id: string): Promise<void> {
    try {
      await api.delete(`/api/v1/investigations/${id}`);
    } catch (error) {
      console.error('Failed to delete investigation:', error);
      throw error;
    }
  }
}

export class SocialMediaService {
  static async scrapePlatform(platform: string, target: string, options: any = {}): Promise<any> {
    try {
      const response = await api.post('/api/v1/social-media/scrape', {
        platform,
        target,
        ...options
      });
      return response.data;
    } catch (error) {
      console.error('Failed to scrape social media:', error);
      throw error;
    }
  }

  static async analyzeProfile(platform: string, username: string): Promise<any> {
    try {
      const response = await api.post('/api/v1/social-media/analyze', {
        platform,
        username
      });
      return response.data;
    } catch (error) {
      console.error('Failed to analyze profile:', error);
      throw error;
    }
  }

  static async searchContent(platform: string, query: string, maxResults: number = 50): Promise<any> {
    try {
      const response = await api.post('/api/v1/social-media/search', {
        platform,
        query,
        max_results: maxResults
      });
      return response.data;
    } catch (error) {
      console.error('Failed to search content:', error);
      throw error;
    }
  }
}

export class AnalysisService {
  static async getAnalysisResults(investigationId: string): Promise<any> {
    try {
      const response = await api.get(`/api/v1/analysis/${investigationId}`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch analysis results:', error);
      throw error;
    }
  }

  static async runAnalysis(data: any): Promise<any> {
    try {
      const response = await api.post('/api/v1/analysis/run', data);
      return response.data;
    } catch (error) {
      console.error('Failed to run analysis:', error);
      throw error;
    }
  }
}

export class IntelligenceService {
  static async getThreatIntelligence(): Promise<any> {
    try {
      const response = await api.get('/api/v1/intelligence/threats');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch threat intelligence:', error);
      throw error;
    }
  }

  static async getNetworkAnalysis(investigationId: string): Promise<any> {
    try {
      const response = await api.get(`/api/v1/intelligence/network/${investigationId}`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch network analysis:', error);
      throw error;
    }
  }
}

export class DashboardService {
  static async getDashboardStats(): Promise<any> {
    try {
      const response = await api.get('/api/v1/dashboard/stats');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch dashboard stats:', error);
      throw error;
    }
  }

  static async getRealTimeData(): Promise<any> {
    try {
      const response = await api.get('/api/v1/dashboard/real-time');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch real-time data:', error);
      throw error;
    }
  }

  static async getRecentActivity(): Promise<any[]> {
    try {
      const response = await api.get('/api/v1/dashboard/activity');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch recent activity:', error);
      throw error;
    }
  }
}

export class HealthService {
  static async checkHealth(): Promise<any> {
    try {
      const response = await api.get('/api/v1/health');
      return response.data;
    } catch (error) {
      console.error('Failed to check health:', error);
      throw error;
    }
  }
}

// Utility functions
export const retryRequest = async <T>(
  requestFn: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> => {
  let lastError: any;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await requestFn();
    } catch (error) {
      lastError = error;
      
      if (attempt === maxRetries) {
        throw error;
      }
      
      // Wait before retrying
      await new Promise(resolve => setTimeout(resolve, delay * attempt));
    }
  }
  
  throw lastError;
};

export const createWebSocketConnection = (url: string): WebSocket => {
  const ws = new WebSocket(url);
  
  ws.onopen = () => {
    console.log('WebSocket connected');
  };
  
  ws.onclose = () => {
    console.log('WebSocket disconnected');
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
  
  return ws;
};

export default api; 