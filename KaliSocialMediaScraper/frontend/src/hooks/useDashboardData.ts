import { useState, useEffect, useCallback } from 'react';
import { DashboardService, retryRequest } from '../services/api';
import { InvestigationService } from '../services/api';

interface DashboardStats {
  totalInvestigations: number;
  activeInvestigations: number;
  completedInvestigations: number;
  failedInvestigations: number;
  totalFindings: number;
  highThreatFindings: number;
  recentReports: number;
  systemHealth: string;
  successRate: number;
  totalProfiles: number;
  highThreatProfiles: number;
  newInvestigationsToday?: number;
  failureRate?: number;
  newProfilesToday?: number;
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
  title?: string;
  status?: string;
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
      const [statsData, investigationsData, activityData] = await Promise.all([
        DashboardService.getDashboardStats(),
        InvestigationService.getInvestigations(), // Fetch actual investigations
        DashboardService.getRecentActivity()
      ]);

      // Map backend data to frontend format
      const mappedStats: DashboardStats = {
        totalInvestigations: statsData.total_investigations || 0,
        activeInvestigations: statsData.active_investigations || 0,
        completedInvestigations: statsData.completed_investigations || 0,
        failedInvestigations: statsData.failed_investigations || 0,
        totalFindings: 0, // Not provided by backend yet
        highThreatFindings: statsData.high_threat_profiles || 0,
        recentReports: 0, // Not provided by backend yet
        systemHealth: 'operational',
        successRate: statsData.success_rate || 0,
        totalProfiles: statsData.total_profiles || 0,
        highThreatProfiles: statsData.high_threat_profiles || 0,
        newInvestigationsToday: statsData.new_investigations_today || 0,
        failureRate: statsData.failure_rate || 0,
        newProfilesToday: statsData.new_profiles_today || 0
      };

      // Map investigations data
      const mappedInvestigations: Investigation[] = investigationsData.map((inv: any) => ({
        id: inv.id?.toString() || '',
        title: inv.title || inv.target_value || 'Unknown',
        target: inv.target_value || inv.target || 'Unknown',
        status: inv.status || 'pending',
        progress: inv.progress || 0,
        createdAt: inv.created_at || new Date().toISOString(),
        threatScore: inv.threat_score || 0.1
      }));

      // Map activity data - handle both array and object responses
      const mappedActivity: Activity[] = activityData.map((item: any) => ({
        id: item.id?.toString() || '',
        type: item.type || 'investigation',
        description: item.description || '',
        timestamp: item.timestamp || '',
        severity: item.status === 'failed' ? 'high' : 'low',
        title: item.title || '',
        status: item.status || ''
      }));

      setStats(mappedStats);
      setRecentInvestigations(mappedInvestigations);
      setRecentActivity(mappedActivity);
      setLastUpdate(new Date());

      console.log('Dashboard data:', {
        stats: mappedStats,
        investigations: mappedInvestigations,
        activity: mappedActivity
      }); // Debug log
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