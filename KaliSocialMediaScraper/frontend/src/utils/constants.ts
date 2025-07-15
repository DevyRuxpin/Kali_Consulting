// API Configuration
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  TIMEOUT: 30000,
  RETRY_ATTEMPTS: 3,
  REFETCH_INTERVAL: 30000, // 30 seconds
} as const;

// Application Configuration
export const APP_CONFIG = {
  NAME: 'Kali OSINT Platform',
  VERSION: '1.0.0',
  DESCRIPTION: 'Advanced Open Source Intelligence Platform',
  AUTHOR: 'Kali OSINT Team',
  SUPPORT_EMAIL: 'support@kaliosint.com',
} as const;

// Theme Configuration
export const THEME_CONFIG = {
  DEFAULT_MODE: 'dark' as const,
  STORAGE_KEY: 'theme',
  TRANSITION_DURATION: 300,
} as const;

// Navigation Configuration
export const NAVIGATION_CONFIG = {
  ITEMS: [
    {
      text: 'Dashboard',
      path: '/dashboard',
      icon: 'Dashboard',
      description: 'Overview and system status',
    },
    {
      text: 'Investigations',
      path: '/investigations',
      icon: 'Search',
      description: 'Manage OSINT investigations',
    },
    {
      text: 'Social Media',
      path: '/social-media',
      icon: 'Public',
      description: 'Social media intelligence',
    },
    {
      text: 'Domain Analysis',
      path: '/domain-analysis',
      icon: 'Public',
      description: 'Domain and DNS analysis',
    },
    {
      text: 'GitHub Analysis',
      path: '/github-analysis',
      icon: 'Code',
      description: 'GitHub user and repository analysis',
    },
    {
      text: 'Threat Analysis',
      path: '/threat-analysis',
      icon: 'Security',
      description: 'Threat detection and analysis',
    },
    {
      text: 'Analytics',
      path: '/analytics',
      icon: 'Analytics',
      description: 'Advanced analytics and insights',
    },
    {
      text: 'Reports',
      path: '/reports',
      icon: 'Assessment',
      description: 'Generate intelligence reports',
    },
    {
      text: 'Settings',
      path: '/settings',
      icon: 'Settings',
      description: 'Platform configuration',
    },
  ],
} as const;

// Investigation Configuration
export const INVESTIGATION_CONFIG = {
  TARGET_TYPES: [
    { value: 'domain', label: 'Domain', description: 'Domain analysis and DNS lookup' },
    { value: 'github', label: 'GitHub', description: 'GitHub user and repository analysis' },
    { value: 'social_media', label: 'Social Media', description: 'Social media profile analysis' },
    { value: 'comprehensive', label: 'Comprehensive', description: 'Full OSINT investigation' },
  ],
  ANALYSIS_DEPTHS: [
    { value: 'basic', label: 'Basic', description: 'Quick analysis with essential data' },
    { value: 'deep', label: 'Deep', description: 'Comprehensive analysis with detailed insights' },
    { value: 'comprehensive', label: 'Comprehensive', description: 'Full analysis with all available data' },
  ],
  STATUSES: [
    { value: 'pending', label: 'Pending', color: 'warning' },
    { value: 'running', label: 'Running', color: 'info' },
    { value: 'completed', label: 'Completed', color: 'success' },
    { value: 'failed', label: 'Failed', color: 'error' },
  ],
} as const;

// Social Media Configuration
export const SOCIAL_MEDIA_CONFIG = {
  SUPPORTED_PLATFORMS: [
    'twitter',
    'instagram',
    'facebook',
    'linkedin',
    'github',
    'youtube',
    'tiktok',
    'reddit',
    'discord',
    'telegram',
  ],
  SHERLOCK_SITES: [
    'twitter',
    'instagram',
    'facebook',
    'linkedin',
    'github',
    'youtube',
    'tiktok',
    'reddit',
    'discord',
    'telegram',
  ],
} as const;

// Threat Analysis Configuration
export const THREAT_CONFIG = {
  SEVERITY_LEVELS: [
    { value: 'low', label: 'Low', color: 'success', score: 1 },
    { value: 'medium', label: 'Medium', color: 'warning', score: 2 },
    { value: 'high', label: 'High', color: 'error', score: 3 },
    { value: 'critical', label: 'Critical', color: 'error', score: 4 },
  ],
  THREAT_TYPES: [
    'malware',
    'phishing',
    'social_engineering',
    'data_breach',
    'cyber_attack',
    'disinformation',
    'radicalization',
    'extremism',
  ],
} as const;

// Export Configuration
export const EXPORT_CONFIG = {
  FORMATS: [
    { value: 'pdf', label: 'PDF', description: 'Portable Document Format' },
    { value: 'csv', label: 'CSV', description: 'Comma Separated Values' },
    { value: 'json', label: 'JSON', description: 'JavaScript Object Notation' },
    { value: 'excel', label: 'Excel', description: 'Microsoft Excel Format' },
  ],
  DEFAULT_OPTIONS: {
    include_charts: true,
    include_data: true,
    date_range: null,
  },
} as const;

// Notification Configuration
export const NOTIFICATION_CONFIG = {
  TYPES: [
    { value: 'info', label: 'Information', color: 'info' },
    { value: 'success', label: 'Success', color: 'success' },
    { value: 'warning', label: 'Warning', color: 'warning' },
    { value: 'error', label: 'Error', color: 'error' },
  ],
  DEFAULT_SETTINGS: {
    enabled: true,
    sound: true,
    desktop: true,
    autoClear: true,
    clearAfter: 30, // minutes
  },
} as const;

// System Configuration
export const SYSTEM_CONFIG = {
  HEALTH_STATUSES: [
    { value: 'healthy', label: 'Healthy', color: 'success' },
    { value: 'warning', label: 'Warning', color: 'warning' },
    { value: 'critical', label: 'Critical', color: 'error' },
  ],
  METRICS: {
    CPU_THRESHOLD: 80,
    MEMORY_THRESHOLD: 85,
    DISK_THRESHOLD: 90,
  },
} as const; 