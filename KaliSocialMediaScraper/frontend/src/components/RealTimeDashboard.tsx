import React from 'react';
import { 
  ChartBarIcon, 
  ExclamationTriangleIcon, 
  GlobeAltIcon,
  UserGroupIcon,
  ShieldExclamationIcon,
  EyeIcon,
  ArrowPathIcon,
  ExclamationCircleIcon
} from '@heroicons/react/24/outline';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useRealTimeData } from '../hooks/useRealTimeData';

const RealTimeDashboard: React.FC = () => {
  const {
    data: realTimeData,
    threatAlerts,
    entityActivity,
    isConnected,
    isLoading,
    error,
    lastUpdate,
    reconnect
  } = useRealTimeData({
    enableWebSocket: true,
    pollingInterval: 5000,
    maxDataPoints: 50,
    autoReconnect: true,
    reconnectDelay: 3000
  });

  // Placeholder: fetch real data from backend API
  // Example: useEffect(() => { fetch('/api/real-time/dashboard') ... }, [])

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getThreatScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-red-600';
    if (score >= 0.6) return 'text-orange-600';
    if (score >= 0.4) return 'text-yellow-600';
    return 'text-green-600';
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Real-Time Intelligence Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Live monitoring and threat intelligence
          </p>
        </div>
        <div className="flex items-center space-x-4">
          {/* Connection Status */}
          <div className={`flex items-center space-x-2 ${isConnected ? 'text-green-600' : 'text-red-600'}`}>
            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm font-medium">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
          
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
          
          {/* Reconnect Button */}
          {!isConnected && !isLoading && (
            <button
              onClick={reconnect}
              className="flex items-center space-x-2 px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              <ArrowPathIcon className="h-4 w-4" />
              <span>Reconnect</span>
            </button>
          )}
          
          <div className="text-sm text-gray-500">
            Last update: {lastUpdate.toLocaleTimeString()}
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="card">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ChartBarIcon className="h-8 w-8 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Active Investigations
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {realTimeData[realTimeData.length - 1]?.activeInvestigations || 0}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ExclamationTriangleIcon className="h-8 w-8 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Threats Detected
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {realTimeData[realTimeData.length - 1]?.threatsDetected || 0}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <UserGroupIcon className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Entities Monitored
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {realTimeData[realTimeData.length - 1]?.entitiesMonitored || 0}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-body">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <GlobeAltIcon className="h-8 w-8 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  Network Activity
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {realTimeData[realTimeData.length - 1]?.networkActivity || 0}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Activity Trend */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">
              Activity Trend
            </h3>
          </div>
          <div className="card-body">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={realTimeData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="activeInvestigations" 
                  stroke="#3B82F6" 
                  strokeWidth={2}
                  name="Investigations"
                />
                <Line 
                  type="monotone" 
                  dataKey="threatsDetected" 
                  stroke="#EF4444" 
                  strokeWidth={2}
                  name="Threats"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Anomaly Score */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">
              Anomaly Score
            </h3>
          </div>
          <div className="card-body">
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={realTimeData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis domain={[0, 1]} />
                <Tooltip />
                <Area 
                  type="monotone" 
                  dataKey="anomalyScore" 
                  stroke="#8B5CF6" 
                  fill="#8B5CF6" 
                  fillOpacity={0.3}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Threat Alerts and Entity Activity */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Threat Alerts */}
        <div className="card">
          <div className="card-header">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                Threat Alerts
              </h3>
              <ShieldExclamationIcon className="h-5 w-5 text-red-600" />
            </div>
          </div>
          <div className="card-body">
            <div className="space-y-4">
              {threatAlerts.map((alert) => (
                <div key={alert.id} className="border-l-4 border-red-500 pl-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="text-sm font-medium text-gray-900 dark:text-white">
                        {alert.title}
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        {alert.description}
                      </p>
                      <div className="flex items-center space-x-4 mt-2">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getSeverityColor(alert.severity)}`}>
                          {alert.severity.toUpperCase()}
                        </span>
                        <span className="text-xs text-gray-500">
                          {formatTime(alert.timestamp)}
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-900 dark:text-white">
                        {Math.round(alert.confidence * 100)}%
                      </div>
                      <div className="text-xs text-gray-500">Confidence</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Entity Activity */}
        <div className="card">
          <div className="card-header">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                Entity Activity
              </h3>
              <EyeIcon className="h-5 w-5 text-blue-600" />
            </div>
          </div>
          <div className="card-body">
            <div className="space-y-4">
              {entityActivity.map((entity) => (
                <div key={entity.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
                        <span className="text-sm font-medium text-blue-600 dark:text-blue-400">
                          {entity.name.charAt(0).toUpperCase()}
                        </span>
                      </div>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-900 dark:text-white">
                        {entity.name}
                      </h4>
                      <p className="text-xs text-gray-500">
                        {entity.platform} • {formatTime(entity.lastSeen)}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`text-sm font-medium ${getThreatScoreColor(entity.threatScore)}`}>
                      {Math.round(entity.threatScore * 100)}%
                    </div>
                    <div className="text-xs text-gray-500">Threat Score</div>
                    <div className="text-xs text-gray-500">
                      Activity: {entity.activityLevel}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Network Activity Chart */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
            Network Activity Overview
          </h3>
        </div>
        <div className="card-body">
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={realTimeData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="entitiesMonitored" fill="#10B981" name="Entities" />
              <Bar dataKey="networkActivity" fill="#3B82F6" name="Network Activity" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default RealTimeDashboard; 