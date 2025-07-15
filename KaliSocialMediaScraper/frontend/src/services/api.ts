import axios from 'axios';
import type { AxiosInstance } from 'axios';
import type { 
  Investigation, 
  InvestigationFormData, 
  DashboardData, 
  ApiResponse, 
  SocialMediaScrapingFormData,
  DomainAnalysis,
  GitHubAnalysis,
  ThreatAssessment,
  AppSettings
} from '../types';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add any auth headers here if needed
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error);
        // Handle CORS errors
        if (error.code === 'ERR_NETWORK') {
          console.error('Network error - backend may not be running');
        }
        return Promise.reject(error);
      }
    );
  }

  // Health Check
  async healthCheck(): Promise<ApiResponse<any>> {
    try {
      const response = await this.client.get('/health/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      return {
        status: 'error',
        message: 'Backend service unavailable',
        timestamp: new Date().toISOString(),
      };
    }
  }

  // Authentication
  async login(username: string, password: string): Promise<ApiResponse<any>> {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await this.client.post('/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  }

  async register(userData: { username: string; email: string; password: string; full_name?: string }): Promise<ApiResponse<any>> {
    const response = await this.client.post('/auth/register', userData);
    return response.data;
  }

  async getCurrentUser(): Promise<ApiResponse<any>> {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  async refreshToken(): Promise<ApiResponse<any>> {
    const response = await this.client.post('/auth/refresh');
    return response.data;
  }

  async logout(): Promise<ApiResponse<any>> {
    const response = await this.client.post('/auth/logout');
    return response.data;
  }

  async updateProfile(userData: Partial<{ full_name: string; email: string }>): Promise<ApiResponse<any>> {
    const response = await this.client.put('/auth/me', userData);
    return response.data;
  }

  async changePassword(passwordData: { old_password: string; new_password: string }): Promise<ApiResponse<any>> {
    const response = await this.client.post('/auth/change-password', passwordData);
    return response.data;
  }

  // Dashboard
  async getDashboardData(): Promise<ApiResponse<DashboardData>> {
    try {
      const response = await this.client.get('/dashboard/data');
      return response.data;
    } catch (error) {
      console.error('Dashboard data fetch failed:', error);
      return {
        status: 'error',
        message: 'Failed to fetch dashboard data',
        timestamp: new Date().toISOString(),
      };
    }
  }

  async getDashboardStats(): Promise<ApiResponse<any>> {
    try {
      const response = await this.client.get('/dashboard/stats');
      return response.data;
    } catch (error) {
      console.error('Dashboard stats fetch failed:', error);
      // Return mock data when backend is not available
      return {
        status: 'success',
        data: {
          total_investigations: 0,
          active_investigations: 0,
          completed_investigations: 0,
          high_priority_threats: 0,
          total_profiles_scraped: 0,
          recent_investigations: []
        },
        timestamp: new Date().toISOString(),
      };
    }
  }

  // Investigations
  async createInvestigation(data: InvestigationFormData): Promise<ApiResponse<Investigation>> {
    const response = await this.client.post('/investigations/', data);
    return response.data;
  }

  async getInvestigations(
    skip: number = 0,
    limit: number = 100,
    status?: string,
    target_type?: string
  ): Promise<Investigation[]> {
    try {
      const params = new URLSearchParams();
      if (skip) params.append('skip', skip.toString());
      if (limit) params.append('limit', limit.toString());
      if (status) params.append('status', status);
      if (target_type) params.append('target_type', target_type);

      const response = await this.client.get(`/investigations/?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch investigations:', error);
      return [];
    }
  }

  async getInvestigation(id: string): Promise<Investigation> {
    const response = await this.client.get(`/investigations/${id}`);
    return response.data;
  }

  async deleteInvestigation(id: string): Promise<void> {
    await this.client.delete(`/investigations/${id}`);
  }

  // Social Media - Fixed endpoints to match backend
  async huntUsername(username: string, sites?: string[]): Promise<ApiResponse<any>> {
    const params = new URLSearchParams();
    params.append('username', username);
    if (sites) {
      sites.forEach(site => params.append('sites', site));
    }

    const response = await this.client.post(`/social-media/sherlock/hunt?${params.toString()}`);
    return response.data;
  }

  async getSherlockSites(): Promise<ApiResponse<any>> {
    const response = await this.client.get('/social-media/sherlock/sites');
    return response.data;
  }

  async scrapeSocialMedia(data: SocialMediaScrapingFormData): Promise<ApiResponse<any>> {
    const response = await this.client.post('/social-media/scrape', data);
    return response.data;
  }

  async comprehensiveHunt(
    username: string,
    includeDirectScraping: boolean = true,
    includeSherlock: boolean = true,
    platforms?: string[]
  ): Promise<ApiResponse<any>> {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('include_direct_scraping', includeDirectScraping.toString());
    params.append('include_sherlock', includeSherlock.toString());
    if (platforms) {
      platforms.forEach(platform => params.append('platforms', platform));
    }

    const response = await this.client.post(`/social-media/comprehensive-hunt?${params.toString()}`);
    return response.data;
  }

  async getSupportedPlatforms(): Promise<ApiResponse<any>> {
    const response = await this.client.get('/social-media/platforms');
    return response.data;
  }

  async getSocialMediaStatus(): Promise<ApiResponse<any>> {
    const response = await this.client.get('/social-media/status');
    return response.data;
  }

  // Domain Analysis - Fixed endpoint
  async analyzeDomain(domain: string): Promise<ApiResponse<DomainAnalysis>> {
    try {
      const response = await this.client.post('/domain/analyze', { domain });
      return response.data;
    } catch (error) {
      console.error('Domain analysis failed:', error);
      return {
        status: 'error',
        message: 'Failed to analyze domain',
        timestamp: new Date().toISOString(),
      };
    }
  }

  // GitHub Analysis - Fixed endpoint
  async analyzeGitHubTarget(target: string, targetType: 'user' | 'organization' | 'repository'): Promise<ApiResponse<GitHubAnalysis>> {
    const response = await this.client.post('/github/analyze', { target, target_type: targetType });
    return response.data;
  }

  // GitHub Analysis - New function for username analysis
  async analyzeGitHub(data: { username: string; analysis_depth: string }): Promise<ApiResponse<any>> {
    const response = await this.client.post('/github/analyze', data);
    return response.data;
  }

  // Analytics - New function
  async getAnalytics(): Promise<ApiResponse<any>> {
    const response = await this.client.get('/analytics/data');
    return response.data;
  }

  // Threat Analysis - Fixed endpoint
  async analyzeThreat(threatData: any): Promise<ApiResponse<ThreatAssessment>> {
    const response = await this.client.post('/threat/analyze', threatData);
    return response.data;
  }

  // Intelligence - Fixed endpoints
  async processIntelligence(data: any): Promise<ApiResponse<any>> {
    const response = await this.client.post('/intelligence/process', data);
    return response.data;
  }

  async generateIntelligenceReport(data: any): Promise<ApiResponse<any>> {
    const response = await this.client.post('/intelligence/report', data);
    return response.data;
  }

  // Analysis - Fixed endpoints
  async detectAnomalies(data: any): Promise<ApiResponse<any>> {
    const response = await this.client.post('/analysis/anomalies', data);
    return response.data;
  }

  async analyzePatterns(data: any): Promise<ApiResponse<any>> {
    const response = await this.client.post('/analysis/patterns', data);
    return response.data;
  }

  // Exports - Fixed endpoints
  async exportData(exportRequest: any): Promise<ApiResponse<any>> {
    const response = await this.client.post('/exports/data', exportRequest);
    return response.data;
  }

  async exportReport(reportRequest: any): Promise<ApiResponse<any>> {
    const response = await this.client.post('/exports/report', reportRequest);
    return response.data;
  }

  // Settings - Fixed endpoints
  async getSettings(): Promise<ApiResponse<AppSettings>> {
    const response = await this.client.get('/settings/');
    return response.data;
  }

  async updateSettings(settings: Partial<AppSettings>): Promise<ApiResponse<AppSettings>> {
    const response = await this.client.put('/settings/', settings);
    return response.data;
  }

  async getSystemInfo(): Promise<ApiResponse<any>> {
    const response = await this.client.get('/settings/system-info');
    return response.data;
  }

  // Real-time WebSocket connection
  createWebSocketConnection(): WebSocket {
    const wsUrl = API_BASE_URL.replace('http', 'ws') + '/ws';
    return new WebSocket(wsUrl);
  }

  // File upload
  async uploadFile(file: File, endpoint: string): Promise<ApiResponse<any>> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.client.post(endpoint, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  // Download file
  async downloadFile(endpoint: string, filename?: string): Promise<void> {
    const response = await this.client.get(endpoint, {
      responseType: 'blob',
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename || 'download');
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  }
}

// Export singleton instance
const apiClient = new ApiClient();
export default apiClient;

// Export individual functions for convenience
export const healthCheck = apiClient.healthCheck.bind(apiClient);
export const login = apiClient.login.bind(apiClient);
export const register = apiClient.register.bind(apiClient);
export const getCurrentUser = apiClient.getCurrentUser.bind(apiClient);
export const refreshToken = apiClient.refreshToken.bind(apiClient);
export const logout = apiClient.logout.bind(apiClient);
export const updateProfile = apiClient.updateProfile.bind(apiClient);
export const changePassword = apiClient.changePassword.bind(apiClient);
export const getDashboardData = apiClient.getDashboardData.bind(apiClient);
export const getDashboardStats = apiClient.getDashboardStats.bind(apiClient);
export const createInvestigation = apiClient.createInvestigation.bind(apiClient);
export const getInvestigations = apiClient.getInvestigations.bind(apiClient);
export const getInvestigation = apiClient.getInvestigation.bind(apiClient);
export const deleteInvestigation = apiClient.deleteInvestigation.bind(apiClient);
export const huntUsername = apiClient.huntUsername.bind(apiClient);
export const getSherlockSites = apiClient.getSherlockSites.bind(apiClient);
export const scrapeSocialMedia = apiClient.scrapeSocialMedia.bind(apiClient);
export const comprehensiveHunt = apiClient.comprehensiveHunt.bind(apiClient);
export const getSupportedPlatforms = apiClient.getSupportedPlatforms.bind(apiClient);
export const getSocialMediaStatus = apiClient.getSocialMediaStatus.bind(apiClient);
export const analyzeDomain = apiClient.analyzeDomain.bind(apiClient);
export const analyzeGitHubTarget = apiClient.analyzeGitHubTarget.bind(apiClient);
export const analyzeGitHub = apiClient.analyzeGitHub.bind(apiClient);
export const getAnalytics = apiClient.getAnalytics.bind(apiClient);
export const analyzeThreat = apiClient.analyzeThreat.bind(apiClient);
export const processIntelligence = apiClient.processIntelligence.bind(apiClient);
export const generateIntelligenceReport = apiClient.generateIntelligenceReport.bind(apiClient);
export const detectAnomalies = apiClient.detectAnomalies.bind(apiClient);
export const analyzePatterns = apiClient.analyzePatterns.bind(apiClient);
export const exportData = apiClient.exportData.bind(apiClient);
export const exportReport = apiClient.exportReport.bind(apiClient);
export const getSettings = apiClient.getSettings.bind(apiClient);
export const updateSettings = apiClient.updateSettings.bind(apiClient);
export const getSystemInfo = apiClient.getSystemInfo.bind(apiClient);
export const createWebSocketConnection = apiClient.createWebSocketConnection.bind(apiClient);
export const uploadFile = apiClient.uploadFile.bind(apiClient);
export const downloadFile = apiClient.downloadFile.bind(apiClient); 