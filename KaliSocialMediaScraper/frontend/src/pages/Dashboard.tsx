import React from 'react';
import { 
  MagnifyingGlassIcon, 
  ChartBarIcon, 
  DocumentTextIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  XCircleIcon
} from '@heroicons/react/24/outline';

const Dashboard: React.FC = () => {
  // Mock data - in real app this would come from API
  const stats = {
    totalInvestigations: 156,
    activeInvestigations: 23,
    completedInvestigations: 128,
    failedInvestigations: 5,
    totalFindings: 1247,
    highThreatFindings: 89,
    recentReports: 12,
    systemHealth: 'Good'
  };

  const recentInvestigations = [
    {
      id: 1,
      title: 'GitHub Repository Analysis',
      target: 'github.com/suspicious/repo',
      status: 'completed',
      progress: 100,
      createdAt: '2024-01-15T10:30:00Z',
      threatScore: 0.8
    },
    {
      id: 2,
      title: 'Social Media Profile Investigation',
      target: '@suspicious_user',
      status: 'active',
      progress: 65,
      createdAt: '2024-01-15T09:15:00Z',
      threatScore: 0.6
    },
    {
      id: 3,
      title: 'Domain Analysis',
      target: 'suspicious-domain.com',
      status: 'pending',
      progress: 0,
      createdAt: '2024-01-15T08:45:00Z',
      threatScore: 0.3
    }
  ];

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
        <button className="btn-primary">
          <MagnifyingGlassIcon className="h-5 w-5 mr-2" />
          New Investigation
        </button>
      </div>

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
                  {stats.totalInvestigations}
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
                  {stats.activeInvestigations}
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
                  {stats.highThreatFindings}
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
                  {stats.recentReports}
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
                {recentInvestigations.map((investigation) => (
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
                ))}
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
                <span className="status-active">{stats.systemHealth}</span>
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
              <div className="flex items-center space-x-3">
                <div className="flex-shrink-0">
                  <div className="h-2 w-2 bg-success-400 rounded-full"></div>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900 dark:text-white">
                    Investigation completed
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    2 minutes ago
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <div className="flex-shrink-0">
                  <div className="h-2 w-2 bg-warning-400 rounded-full"></div>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900 dark:text-white">
                    New finding detected
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    5 minutes ago
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <div className="flex-shrink-0">
                  <div className="h-2 w-2 bg-primary-400 rounded-full"></div>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900 dark:text-white">
                    Report generated
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    10 minutes ago
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 