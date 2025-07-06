import React from 'react';
import { 
  MagnifyingGlassIcon, 
  ChartBarIcon, 
  DocumentTextIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  XCircleIcon,
  ArrowPathIcon,
  ExclamationCircleIcon
} from '@heroicons/react/24/outline';
import RealTimeDashboard from '../components/RealTimeDashboard';
import { useDashboardData } from '../hooks/useDashboardData';

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
    refreshInterval: 30000,
    enableRetry: true,
    maxRetries: 3
  });

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-success-500" />;
      case 'active':
        return <ClockIcon className="h-5 w-5 text-warning-500" />;
      case 'failed':
        return <XCircleIcon className="h-5 w-5 text-danger-500" />;
      default:
        return <ClockIcon className="h-5 w-5 text-gray-400" />;
    }
  };

  const getThreatScoreClass = (score: number) => {
    if (score >= 0.8) return 'threat-critical';
    if (score >= 0.6) return 'threat-high';
    if (score >= 0.4) return 'threat-medium';
    return 'threat-low';
  };

  const getThreatScoreText = (score: number) => {
    if (score >= 0.8) return 'Critical';
    if (score >= 0.6) return 'High';
    if (score >= 0.4) return 'Medium';
    return 'Low';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Overview of your OSINT investigations and findings
          </p>
        </div>
        <div className="flex items-center space-x-4">
          {/* Error Display */}
          {error && (
            <div className="flex items-center space-x-2 text-red-600">
              <ExclamationCircleIcon className="h-4 w-4" />
              <span className="text-sm">{error}</span>
            </div>
          )}
          
          {/* Loading Indicator */}
          {isLoading && (
            <div className="flex items-center space-x-2 text-blue-600">
              <ArrowPathIcon className="h-4 w-4 animate-spin" />
              <span className="text-sm">Loading...</span>
            </div>
          )}
          
          {/* Refresh Button */}
          <button
            onClick={refresh}
            disabled={isLoading}
            className="flex items-center space-x-2 px-3 py-2 text-sm bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors disabled:opacity-50"
          >
            <ArrowPathIcon className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
          
          <button className="btn-primary">
            <MagnifyingGlassIcon className="h-5 w-5 mr-2" />
            New Investigation
          </button>
        </div>
      </div>

      {/* Real-Time Intelligence Dashboard */}
      <RealTimeDashboard />

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="card">
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
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ChartBarIcon className="h-8 w-8 text-warning-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Active Investigations
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {stats?.activeInvestigations || 0}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ExclamationTriangleIcon className="h-8 w-8 text-danger-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  High Threat Findings
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {stats?.highThreatFindings || 0}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <DocumentTextIcon className="h-8 w-8 text-success-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Recent Reports
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {stats?.recentReports || 0}
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
                    <tr key={investigation.id}>
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
                        <span className={`status-${investigation.status}`}>
                          {investigation.status.charAt(0).toUpperCase() + investigation.status.slice(1)}
                        </span>
                      </td>
                      <td className="table-cell">
                        <div className="flex items-center">
                          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                            <div
                              className="bg-primary-600 h-2 rounded-full"
                              style={{ width: `${investigation.progress}%` }}
                            />
                          </div>
                          <span className="ml-2 text-sm text-gray-500 dark:text-gray-400">
                            {investigation.progress}%
                          </span>
                        </div>
                      </td>
                      <td className="table-cell">
                        <span className={getThreatScoreClass(investigation.threatScore)}>
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
        <div className="card">
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

        <div className="card">
          <div className="card-body">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
              System Status
            </h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  API Status
                </span>
                <span className="status-active">Online</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  Database
                </span>
                <span className="status-active">Connected</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  Scrapers
                </span>
                <span className="status-active">Running</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  Overall Health
                </span>
                <span className="status-active">{stats?.systemHealth || 'Unknown'}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
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