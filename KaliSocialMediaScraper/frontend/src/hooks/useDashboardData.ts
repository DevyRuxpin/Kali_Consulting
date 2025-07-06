import { useState, useEffect, useCallback } from 'react';
import { DashboardService, retryRequest } from '../services/api';

interface DashboardStats {
  totalInvestigations: number;
  activeInvestigations: number;
  completedInvestigations: number;
  failedInvestigations: number;
  totalFindings: number;
  highThreatFindings: number;
  recentReports: number;
  systemHealth: string;
}

interface Investigation {
  id: string;
  title: string;
  target: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  progress: number;
  createdAt: string;
  threatScore: number;
}

interface Activity {
  id: string;
  type: string;
  description: string;
  timestamp: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
}

interface UseDashboardDataOptions {
  autoRefresh?: boolean;
  refreshInterval?: number;
  enableRetry?: boolean;
  maxRetries?: number;
}

interface UseDashboardDataReturn {
  stats: DashboardStats | null;
  recentInvestigations: Investigation[];
  recentActivity: Activity[];
  isLoading: boolean;
  error: string | null;
  lastUpdate: Date;
  refresh: () => Promise<void>;
}

export const useDashboardData = (options: UseDashboardDataOptions = {}): UseDashboardDataReturn => {
  const {
    autoRefresh = true,
    refreshInterval = 30000, // 30 seconds
    enableRetry = true,
    maxRetries = 3
  } = options;

  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentInvestigations, setRecentInvestigations] = useState<Investigation[]>([]);
  const [recentActivity, setRecentActivity] = useState<Activity[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // Fetch dashboard data
  const fetchDashboardData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Fetch all dashboard data in parallel
      const [statsData, activityData] = await Promise.all([
        DashboardService.getDashboardStats(),
        DashboardService.getRecentActivity()
      ]);

      setStats(statsData);
      setRecentActivity(activityData);
      setLastUpdate(new Date());
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch dashboard data';
      setError(errorMessage);
      console.error('Error fetching dashboard data:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Fetch with retry logic
  const fetchWithRetry = useCallback(async () => {
    if (enableRetry) {
      return retryRequest(fetchDashboardData, maxRetries, 1000);
    }
    return fetchDashboardData();
  }, [fetchDashboardData, enableRetry, maxRetries]);

  // Manual refresh function
  const refresh = useCallback(async () => {
    await fetchWithRetry();
  }, [fetchWithRetry]);

  // Initialize data fetching
  useEffect(() => {
    fetchWithRetry();

    // Set up auto-refresh
    if (autoRefresh) {
      const interval = setInterval(() => {
        fetchWithRetry();
      }, refreshInterval);

      return () => clearInterval(interval);
    }
  }, [fetchWithRetry, autoRefresh, refreshInterval]);

  return {
    stats,
    recentInvestigations,
    recentActivity,
    isLoading,
    error,
    lastUpdate,
    refresh
  };
}; 