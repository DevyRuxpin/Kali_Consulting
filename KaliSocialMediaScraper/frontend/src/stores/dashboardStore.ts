import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import type { DashboardData, SystemHealth, RealTimeMetrics } from '../types';

interface DashboardState {
  data: DashboardData | null;
  systemHealth: SystemHealth | null;
  realTimeMetrics: RealTimeMetrics | null;
  loading: boolean;
  error: string | null;
  lastUpdated: string | null;
}

interface DashboardActions {
  // State setters
  setDashboardData: (data: DashboardData) => void;
  setSystemHealth: (health: SystemHealth) => void;
  setRealTimeMetrics: (metrics: RealTimeMetrics) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setLastUpdated: (timestamp: string) => void;
  
  // Actions
  clearError: () => void;
  resetDashboard: () => void;
  
  // Computed
  getSystemStatus: () => 'healthy' | 'warning' | 'critical' | 'unknown';
  getActiveThreatsCount: () => number;
  getCompletedInvestigationsCount: () => number;
}

export const useDashboardStore = create<DashboardState & DashboardActions>()(
  devtools(
    (set, get) => ({
      // Initial state
      data: null,
      systemHealth: null,
      realTimeMetrics: null,
      loading: false,
      error: null,
      lastUpdated: null,

      // Actions
      setDashboardData: (data) => set({ data }),
      setSystemHealth: (health) => set({ systemHealth: health }),
      setRealTimeMetrics: (metrics) => set({ realTimeMetrics: metrics }),
      setLoading: (loading) => set({ loading }),
      setError: (error) => set({ error }),
      setLastUpdated: (timestamp) => set({ lastUpdated: timestamp }),

      clearError: () => set({ error: null }),
      resetDashboard: () => set({
        data: null,
        systemHealth: null,
        realTimeMetrics: null,
        loading: false,
        error: null,
        lastUpdated: null,
      }),

      // Computed
      getSystemStatus: () => {
        const { systemHealth } = get();
        return systemHealth?.status || 'unknown';
      },

      getActiveThreatsCount: () => {
        const { data } = get();
        return data?.statistics?.high_priority_threats || 0;
      },

      getCompletedInvestigationsCount: () => {
        const { data } = get();
        return data?.statistics?.completed_investigations || 0;
      },
    })
  )
); 