import React, { useEffect, useState } from 'react';
import { 
  MagnifyingGlassIcon, 
  ChartBarIcon, 
  DocumentTextIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  XCircleIcon,
  UserGroupIcon,
  ShieldCheckIcon,
  PlayIcon,
  SignalIcon,
  WifiIcon,
  ServerIcon,
  BoltIcon
} from '@heroicons/react/24/outline';
import RealTimeDashboard from '../components/RealTimeDashboard';
import { useDashboardData } from '../hooks/useDashboardData';
import { useRealTimeData } from '../hooks/useRealTimeData';
import { InvestigationService } from '../services/api';

const Dashboard: React.FC = () => {
  const {
    stats,
    recentInvestigations,
    recentActivity,
    isLoading,
    error,
    lastUpdate,
    refresh
  } = useDashboardData({
    autoRefresh: true,
    refreshInterval: 5000 // More frequent updates
  });

  const { data: realTimeData } = useRealTimeData();
  
  // Real-time investigation tracking
  const [runningInvestigations, setRunningInvestigations] = useState<any[]>([]);
  const [systemStatus, setSystemStatus] = useState({
    api: 'online',
    database: 'connected',
    scrapers: 'running',
    overall: 'healthy'
  });

  // Auto-refresh running investigations
  useEffect(() => {
    const updateRunningInvestigations = async () => {
      try {
        const investigations = await InvestigationService.getInvestigations();
        const running = investigations.filter(inv => inv.status === 'running');
        setRunningInvestigations(running);
      } catch (error) {
        console.error('Error updating running investigations:', error);
      }
    };

    updateRunningInvestigations();
    const interval = setInterval(updateRunningInvestigations, 3000); // Update every 3 seconds

    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-8 w-8 text-green-500" />;
      case 'running':
        return <PlayIcon className="h-8 w-8 text-blue-500 animate-pulse" />;
      case 'failed':
        return <XCircleIcon className="h-8 w-8 text-red-500" />;
      case 'pending':
        return <ClockIcon className="h-8 w-8 text-yellow-500" />;
      default:
        return <ClockIcon className="h-8 w-8 text-gray-400" />;
    }
  };

  const getThreatScoreClass = (score: number) => {
    if (score >= 0.8) return 'text-red-600 bg-red-100 dark:bg-red-900 dark:text-red-200';
    if (score >= 0.6) return 'text-orange-600 bg-orange-100 dark:bg-orange-900 dark:text-orange-200';
    if (score >= 0.4) return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900 dark:text-yellow-200';
    return 'text-green-600 bg-green-100 dark:bg-green-900 dark:text-green-200';
  };

  const getThreatScoreText = (score: number) => {
    if (score >= 0.8) return 'Critical';
    if (score >= 0.6) return 'High';
    if (score >= 0.4) return 'Medium';
    return 'Low';
  };

  const getSystemStatusIcon = (status: string) => {
    switch (status) {
      case 'online':
      case 'connected':
      case 'running':
      case 'healthy':
        return <CheckCircleIcon className="h-4 w-4 text-green-500" />;
      case 'offline':
      case 'disconnected':
      case 'stopped':
      case 'error':
        return <XCircleIcon className="h-4 w-4 text-red-500" />;
      default:
        return <ClockIcon className="h-4 w-4 text-yellow-500" />;
    }
  };

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <ExclamationTriangleIcon className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            Error Loading Dashboard
          </h3>
          <p className="text-gray-500 dark:text-gray-400 mb-4">{error}</p>
          <button
            onClick={refresh}
            className="btn-primary"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            OSINT Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Real-time threat intelligence and investigation monitoring
          </p>
        </div>
        <div className="flex items-center space-x-4">
          {/* Real-time indicator */}
          {runningInvestigations.length > 0 && (
            <div className="flex items-center bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg px-3 py-2">
              <PlayIcon className="h-4 w-4 text-blue-500 mr-2 animate-pulse" />
              <span className="text-sm text-blue-700 dark:text-blue-300 font-medium">
                {runningInvestigations.length} active investigation(s)
              </span>
            </div>
          )}
          <div className="text-sm text-gray-500 dark:text-gray-400">
            Last updated: {lastUpdate.toLocaleTimeString()}
          </div>
          <button
            onClick={refresh}
            disabled={isLoading}
            className="btn-secondary flex items-center"
          >
            {isLoading ? (
              <>
                <ClockIcon className="h-4 w-4 mr-2 animate-spin" />
                Refreshing...
              </>
            ) : (
              <>
                <BoltIcon className="h-4 w-4 mr-2" />
                Refresh
              </>
            )}
          </button>
        </div>
      </div>

      {/* Real-Time Intelligence Dashboard */}
      <RealTimeDashboard />

      {/* Live Progress Tracking */}
      {runningInvestigations.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white flex items-center">
              <PlayIcon className="h-5 w-5 text-blue-500 mr-2 animate-pulse" />
              Live Investigations
            </h3>
          </div>
          <div className="card-body">
            <div className="space-y-4">
              {runningInvestigations.map((investigation) => (
                <div key={investigation.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center">
                      <PlayIcon className="h-5 w-5 text-blue-500 mr-2 animate-pulse" />
                      <div>
                        <h4 className="font-medium text-gray-900 dark:text-white">
                          {investigation.title}
                        </h4>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {investigation.target_type}: {investigation.target_value}
                        </p>
                      </div>
                    </div>
                    <span className="text-sm text-blue-600 dark:text-blue-400 font-medium">
                      {investigation.progress}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                    <div
                      className="bg-blue-600 h-3 rounded-full transition-all duration-500"
                      style={{ width: `${investigation.progress}%` }}
                    />
                  </div>
                  <div className="flex items-center justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
                    <span>Started: {new Date(investigation.created_at).toLocaleTimeString()}</span>
                    <span>ETA: {investigation.progress < 50 ? 'Calculating...' : 'Soon'}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="card hover:shadow-lg transition-shadow">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <MagnifyingGlassIcon className="h-8 w-8 text-primary-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Total Investigations
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {stats?.totalInvestigations || 0}
                </p>
                <p className="text-xs text-green-600 dark:text-green-400">
                  +{stats?.newInvestigationsToday || 0} today
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="card hover:shadow-lg transition-shadow">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CheckCircleIcon className="h-8 w-8 text-success-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Completed
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {stats?.completedInvestigations || 0}
                </p>
                <p className="text-xs text-green-600 dark:text-green-400">
                  {stats?.successRate ? `${stats.successRate.toFixed(1)}%` : '0%'} success rate
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="card hover:shadow-lg transition-shadow">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <PlayIcon className="h-8 w-8 text-blue-500 animate-pulse" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Active
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {runningInvestigations.length}
                </p>
                <p className="text-xs text-blue-600 dark:text-blue-400">
                  Real-time tracking
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="card hover:shadow-lg transition-shadow">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ShieldCheckIcon className="h-8 w-8 text-danger-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  High Threat Profiles
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {stats?.highThreatProfiles || 0}
                </p>
                <p className="text-xs text-red-600 dark:text-red-400">
                  Requires attention
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Additional Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <div className="card hover:shadow-lg transition-shadow">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <XCircleIcon className="h-8 w-8 text-danger-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Failed Investigations
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {stats?.failedInvestigations || 0}
                </p>
                <p className="text-xs text-red-600 dark:text-red-400">
                  {stats?.failureRate ? `${stats.failureRate.toFixed(1)}%` : '0%'} failure rate
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="card hover:shadow-lg transition-shadow">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ChartBarIcon className="h-8 w-8 text-info-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Success Rate
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {stats?.successRate ? `${stats.successRate.toFixed(1)}%` : '0%'}
                </p>
                <p className="text-xs text-green-600 dark:text-green-400">
                  Excellent performance
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="card hover:shadow-lg transition-shadow">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <UserGroupIcon className="h-8 w-8 text-success-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Total Profiles
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {stats?.totalProfiles || 0}
                </p>
                <p className="text-xs text-green-600 dark:text-green-400">
                  +{stats?.newProfilesToday || 0} today
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Investigations */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
            Recent Investigations
          </h3>
        </div>
        <div className="card-body">
          <div className="overflow-hidden">
            <table className="table">
              <thead className="table-header">
                <tr>
                  <th className="table-header-cell">Investigation</th>
                  <th className="table-header-cell">Target</th>
                  <th className="table-header-cell">Status</th>
                  <th className="table-header-cell">Progress</th>
                  <th className="table-header-cell">Threat Score</th>
                  <th className="table-header-cell">Created</th>
                </tr>
              </thead>
              <tbody className="table-body">
                {recentInvestigations.length > 0 ? (
                  recentInvestigations.map((investigation) => (
                    <tr key={investigation.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                      <td className="table-cell">
                        <div className="flex items-center">
                          <div className="flex-shrink-0 h-10 w-10">
                            {getStatusIcon(investigation.status)}
                          </div>
                          <div className="ml-4">
                            <div className="text-sm font-medium text-gray-900 dark:text-white">
                              {investigation.title}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="table-cell">
                        <div className="text-sm text-gray-900 dark:text-white">
                          {investigation.target}
                        </div>
                      </td>
                      <td className="table-cell">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          investigation.status === 'completed' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                          investigation.status === 'running' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' :
                          investigation.status === 'failed' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' :
                          'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
                        }`}>
                          {investigation.status.charAt(0).toUpperCase() + investigation.status.slice(1)}
                        </span>
                      </td>
                      <td className="table-cell">
                        <div className="flex items-center">
                          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                            <div
                              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${investigation.progress}%` }}
                            />
                          </div>
                          <span className="ml-2 text-sm text-gray-500 dark:text-gray-400">
                            {investigation.progress}%
                          </span>
                        </div>
                      </td>
                      <td className="table-cell">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getThreatScoreClass(investigation.threatScore)}`}>
                          {getThreatScoreText(investigation.threatScore)}
                        </span>
                      </td>
                      <td className="table-cell">
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          {new Date(investigation.createdAt).toLocaleDateString()}
                        </div>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={6} className="table-cell text-center text-gray-500 dark:text-gray-400 py-8">
                      {isLoading ? 'Loading investigations...' : 'No recent investigations found'}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <div className="card hover:shadow-lg transition-shadow">
          <div className="card-body">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
              Quick Actions
            </h3>
            <div className="space-y-3">
              <button className="w-full btn-primary">
                <MagnifyingGlassIcon className="h-5 w-5 mr-2" />
                Start New Investigation
              </button>
              <button className="w-full btn-secondary">
                <ChartBarIcon className="h-5 w-5 mr-2" />
                View Analytics
              </button>
              <button className="w-full btn-secondary">
                <DocumentTextIcon className="h-5 w-5 mr-2" />
                Generate Report
              </button>
            </div>
          </div>
        </div>

        <div className="card hover:shadow-lg transition-shadow">
          <div className="card-body">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
              System Status
            </h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400 flex items-center">
                  <SignalIcon className="h-4 w-4 mr-2" />
                  API Status
                </span>
                <span className="flex items-center text-sm">
                  {getSystemStatusIcon(systemStatus.api)}
                  <span className="ml-1 status-active">Online</span>
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400 flex items-center">
                  <ServerIcon className="h-4 w-4 mr-2" />
                  Database
                </span>
                <span className="flex items-center text-sm">
                  {getSystemStatusIcon(systemStatus.database)}
                  <span className="ml-1 status-active">Connected</span>
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400 flex items-center">
                  <WifiIcon className="h-4 w-4 mr-2" />
                  Scrapers
                </span>
                <span className="flex items-center text-sm">
                  {getSystemStatusIcon(systemStatus.scrapers)}
                  <span className="ml-1 status-active">Running</span>
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400 flex items-center">
                  <ShieldCheckIcon className="h-4 w-4 mr-2" />
                  Overall Health
                </span>
                <span className="flex items-center text-sm">
                  {getSystemStatusIcon(systemStatus.overall)}
                  <span className="ml-1 status-active">{stats?.systemHealth || 'Healthy'}</span>
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="card hover:shadow-lg transition-shadow">
          <div className="card-body">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
              Recent Activity
            </h3>
            <div className="space-y-3">
              {recentActivity.length > 0 ? (
                recentActivity.slice(0, 5).map((activity) => (
                  <div key={activity.id} className="flex items-center space-x-3">
                    <div className="flex-shrink-0">
                      <div className={`h-2 w-2 rounded-full ${
                        activity.severity === 'critical' ? 'bg-red-400' :
                        activity.severity === 'high' ? 'bg-orange-400' :
                        activity.severity === 'medium' ? 'bg-yellow-400' :
                        'bg-green-400'
                      }`}></div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-900 dark:text-white">
                        {activity.description}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        {new Date(activity.timestamp).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center text-gray-500 dark:text-gray-400 py-4">
                  {isLoading ? 'Loading activity...' : 'No recent activity'}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 