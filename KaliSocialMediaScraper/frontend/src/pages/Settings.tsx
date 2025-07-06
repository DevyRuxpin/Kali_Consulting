import React, { useState, useEffect } from 'react';
import { 
  CogIcon, 
  ShieldCheckIcon, 
  GlobeAltIcon,
  ClockIcon,
  WifiIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  XCircleIcon
} from '@heroicons/react/24/outline';

interface ScrapingSettings {
  enableUserAgentRotation: boolean;
  enableProxyRotation: boolean;
  enableRandomDelays: boolean;
  defaultDelayMin: number;
  defaultDelayMax: number;
  maxRetries: number;
  timeoutSeconds: number;
}

interface ProxySettings {
  enabled: boolean;
  proxyList: string[];
  rotationInterval: number;
  authentication: {
    username: string;
    password: string;
  };
}

interface RateLimitSettings {
  requestsPerMinute: number;
  requestsPerHour: number;
  requestsPerDay: number;
  enableRateLimiting: boolean;
}

interface SecuritySettings {
  enableThreatDetection: boolean;
  enableAnomalyDetection: boolean;
  threatScoreThreshold: number;
  enableAutoBlocking: boolean;
}

interface NotificationSettings {
  emailNotifications: boolean;
  webhookNotifications: boolean;
  webhookUrl: string;
  notificationLevel: 'all' | 'high' | 'critical';
}

const Settings: React.FC = () => {
  const [activeTab, setActiveTab] = useState('scraping');
  const [isLoading, setIsLoading] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'success' | 'error'>('idle');

  // Settings state
  const [scrapingSettings, setScrapingSettings] = useState<ScrapingSettings>({
    enableUserAgentRotation: true,
    enableProxyRotation: false,
    enableRandomDelays: true,
    defaultDelayMin: 2,
    defaultDelayMax: 5,
    maxRetries: 3,
    timeoutSeconds: 30
  });

  const [proxySettings, setProxySettings] = useState<ProxySettings>({
    enabled: false,
    proxyList: [],
    rotationInterval: 60,
    authentication: {
      username: '',
      password: ''
    }
  });

  const [rateLimitSettings, setRateLimitSettings] = useState<RateLimitSettings>({
    requestsPerMinute: 60,
    requestsPerHour: 1000,
    requestsPerDay: 10000,
    enableRateLimiting: true
  });

  const [securitySettings, setSecuritySettings] = useState<SecuritySettings>({
    enableThreatDetection: true,
    enableAnomalyDetection: true,
    threatScoreThreshold: 0.7,
    enableAutoBlocking: false
  });

  const [notificationSettings, setNotificationSettings] = useState<NotificationSettings>({
    emailNotifications: false,
    webhookNotifications: false,
    webhookUrl: '',
    notificationLevel: 'high'
  });

  const tabs = [
    { id: 'scraping', name: 'Scraping', icon: GlobeAltIcon },
    { id: 'proxy', name: 'Proxy', icon: WifiIcon },
    { id: 'rate-limits', name: 'Rate Limits', icon: ClockIcon },
    { id: 'security', name: 'Security', icon: ShieldCheckIcon },
    { id: 'notifications', name: 'Notifications', icon: ExclamationTriangleIcon }
  ];

  const handleSave = async () => {
    setIsLoading(true);
    setSaveStatus('saving');

    try {
      // Simulate API call to save settings
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setSaveStatus('success');
      setTimeout(() => setSaveStatus('idle'), 3000);
    } catch (error) {
      setSaveStatus('error');
      setTimeout(() => setSaveStatus('idle'), 3000);
    } finally {
      setIsLoading(false);
    }
  };

  const getSaveStatusIcon = () => {
    switch (saveStatus) {
      case 'saving':
        return <ClockIcon className="h-5 w-5 animate-spin" />;
      case 'success':
        return <CheckCircleIcon className="h-5 w-5 text-green-600" />;
      case 'error':
        return <XCircleIcon className="h-5 w-5 text-red-600" />;
      default:
        return null;
    }
  };

  const getSaveStatusText = () => {
    switch (saveStatus) {
      case 'saving':
        return 'Saving...';
      case 'success':
        return 'Settings saved!';
      case 'error':
        return 'Failed to save settings';
      default:
        return 'Save Settings';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Settings
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Configure platform behavior and preferences
          </p>
        </div>
        <button
          onClick={handleSave}
          disabled={isLoading}
          className="btn-primary flex items-center space-x-2"
        >
          {getSaveStatusIcon()}
          <span>{getSaveStatusText()}</span>
        </button>
      </div>

      {/* Settings Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-700">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="h-5 w-5" />
                <span>{tab.name}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Settings Content */}
      <div className="space-y-6">
        {/* Scraping Settings */}
        {activeTab === 'scraping' && (
          <div className="space-y-6">
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                  Anti-Detection Settings
                </h3>
              </div>
              <div className="card-body space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      User Agent Rotation
                    </label>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Rotate user agents to avoid detection
                    </p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={scrapingSettings.enableUserAgentRotation}
                      onChange={(e) => setScrapingSettings(prev => ({
                        ...prev,
                        enableUserAgentRotation: e.target.checked
                      }))}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Random Delays
                    </label>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Add random delays between requests
                    </p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={scrapingSettings.enableRandomDelays}
                      onChange={(e) => setScrapingSettings(prev => ({
                        ...prev,
                        enableRandomDelays: e.target.checked
                      }))}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                {scrapingSettings.enableRandomDelays && (
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Min Delay (seconds)
                      </label>
                      <input
                        type="number"
                        value={scrapingSettings.defaultDelayMin}
                        onChange={(e) => setScrapingSettings(prev => ({
                          ...prev,
                          defaultDelayMin: parseInt(e.target.value)
                        }))}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Max Delay (seconds)
                      </label>
                      <input
                        type="number"
                        value={scrapingSettings.defaultDelayMax}
                        onChange={(e) => setScrapingSettings(prev => ({
                          ...prev,
                          defaultDelayMax: parseInt(e.target.value)
                        }))}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                  Request Settings
                </h3>
              </div>
              <div className="card-body space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Max Retries
                    </label>
                    <input
                      type="number"
                      value={scrapingSettings.maxRetries}
                      onChange={(e) => setScrapingSettings(prev => ({
                        ...prev,
                        maxRetries: parseInt(e.target.value)
                      }))}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Timeout (seconds)
                    </label>
                    <input
                      type="number"
                      value={scrapingSettings.timeoutSeconds}
                      onChange={(e) => setScrapingSettings(prev => ({
                        ...prev,
                        timeoutSeconds: parseInt(e.target.value)
                      }))}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Proxy Settings */}
        {activeTab === 'proxy' && (
          <div className="space-y-6">
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                  Proxy Configuration
                </h3>
              </div>
              <div className="card-body space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Enable Proxy Rotation
                    </label>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Use proxy servers to avoid IP blocking
                    </p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={proxySettings.enabled}
                      onChange={(e) => setProxySettings(prev => ({
                        ...prev,
                        enabled: e.target.checked
                      }))}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                {proxySettings.enabled && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Proxy List (one per line)
                      </label>
                      <textarea
                        value={proxySettings.proxyList.join('\n')}
                        onChange={(e) => setProxySettings(prev => ({
                          ...prev,
                          proxyList: e.target.value.split('\n').filter(line => line.trim())
                        }))}
                        rows={4}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                        placeholder="http://proxy1:port&#10;http://proxy2:port"
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                          Username
                        </label>
                        <input
                          type="text"
                          value={proxySettings.authentication.username}
                          onChange={(e) => setProxySettings(prev => ({
                            ...prev,
                            authentication: {
                              ...prev.authentication,
                              username: e.target.value
                            }
                          }))}
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                          Password
                        </label>
                        <input
                          type="password"
                          value={proxySettings.authentication.password}
                          onChange={(e) => setProxySettings(prev => ({
                            ...prev,
                            authentication: {
                              ...prev.authentication,
                              password: e.target.value
                            }
                          }))}
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                        />
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Rate Limit Settings */}
        {activeTab === 'rate-limits' && (
          <div className="space-y-6">
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                  Rate Limiting
                </h3>
              </div>
              <div className="card-body space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Enable Rate Limiting
                    </label>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Limit requests to avoid being blocked
                    </p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={rateLimitSettings.enableRateLimiting}
                      onChange={(e) => setRateLimitSettings(prev => ({
                        ...prev,
                        enableRateLimiting: e.target.checked
                      }))}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                {rateLimitSettings.enableRateLimiting && (
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Requests per Minute
                      </label>
                      <input
                        type="number"
                        value={rateLimitSettings.requestsPerMinute}
                        onChange={(e) => setRateLimitSettings(prev => ({
                          ...prev,
                          requestsPerMinute: parseInt(e.target.value)
                        }))}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Requests per Hour
                      </label>
                      <input
                        type="number"
                        value={rateLimitSettings.requestsPerHour}
                        onChange={(e) => setRateLimitSettings(prev => ({
                          ...prev,
                          requestsPerHour: parseInt(e.target.value)
                        }))}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Requests per Day
                      </label>
                      <input
                        type="number"
                        value={rateLimitSettings.requestsPerDay}
                        onChange={(e) => setRateLimitSettings(prev => ({
                          ...prev,
                          requestsPerDay: parseInt(e.target.value)
                        }))}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Security Settings */}
        {activeTab === 'security' && (
          <div className="space-y-6">
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                  Threat Detection
                </h3>
              </div>
              <div className="card-body space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Enable Threat Detection
                    </label>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Automatically detect and flag suspicious content
                    </p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={securitySettings.enableThreatDetection}
                      onChange={(e) => setSecuritySettings(prev => ({
                        ...prev,
                        enableThreatDetection: e.target.checked
                      }))}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Enable Anomaly Detection
                    </label>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Detect unusual patterns in scraped data
                    </p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={securitySettings.enableAnomalyDetection}
                      onChange={(e) => setSecuritySettings(prev => ({
                        ...prev,
                        enableAnomalyDetection: e.target.checked
                      }))}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Threat Score Threshold
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={securitySettings.threatScoreThreshold}
                    onChange={(e) => setSecuritySettings(prev => ({
                      ...prev,
                      threatScoreThreshold: parseFloat(e.target.value)
                    }))}
                    className="mt-1 block w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>0.0 (Low)</span>
                    <span>{securitySettings.threatScoreThreshold}</span>
                    <span>1.0 (High)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Notification Settings */}
        {activeTab === 'notifications' && (
          <div className="space-y-6">
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                  Notification Preferences
                </h3>
              </div>
              <div className="card-body space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Email Notifications
                    </label>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Receive notifications via email
                    </p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={notificationSettings.emailNotifications}
                      onChange={(e) => setNotificationSettings(prev => ({
                        ...prev,
                        emailNotifications: e.target.checked
                      }))}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Webhook Notifications
                    </label>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Send notifications to external webhook
                    </p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={notificationSettings.webhookNotifications}
                      onChange={(e) => setNotificationSettings(prev => ({
                        ...prev,
                        webhookNotifications: e.target.checked
                      }))}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                {notificationSettings.webhookNotifications && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Webhook URL
                    </label>
                    <input
                      type="url"
                      value={notificationSettings.webhookUrl}
                      onChange={(e) => setNotificationSettings(prev => ({
                        ...prev,
                        webhookUrl: e.target.value
                      }))}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                      placeholder="https://your-webhook-url.com/notifications"
                    />
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Notification Level
                  </label>
                  <select
                    value={notificationSettings.notificationLevel}
                    onChange={(e) => setNotificationSettings(prev => ({
                      ...prev,
                      notificationLevel: e.target.value as 'all' | 'high' | 'critical'
                    }))}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  >
                    <option value="all">All notifications</option>
                    <option value="high">High priority only</option>
                    <option value="critical">Critical only</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Settings; 