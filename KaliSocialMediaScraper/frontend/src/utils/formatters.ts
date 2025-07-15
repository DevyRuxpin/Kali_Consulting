// Date and Time Formatting
export const formatDate = (date: string | Date, options?: Intl.DateTimeFormatOptions): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  const defaultOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  };
  
  return dateObj.toLocaleDateString('en-US', { ...defaultOptions, ...options });
};

export const formatRelativeTime = (date: string | Date): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - dateObj.getTime()) / 1000);

  if (diffInSeconds < 60) {
    return `${diffInSeconds} seconds ago`;
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  } else if (diffInSeconds < 2592000) {
    const days = Math.floor(diffInSeconds / 86400);
    return `${days} day${days > 1 ? 's' : ''} ago`;
  } else {
    return formatDate(dateObj, { year: 'numeric', month: 'short', day: 'numeric' });
  }
};

// Number Formatting
export const formatNumber = (num: number, options?: Intl.NumberFormatOptions): string => {
  const defaultOptions: Intl.NumberFormatOptions = {
    maximumFractionDigits: 2,
  };
  
  return num.toLocaleString('en-US', { ...defaultOptions, ...options });
};

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
};

export const formatPercentage = (value: number, total: number): string => {
  if (total === 0) return '0%';
  return `${Math.round((value / total) * 100)}%`;
};

// Text Formatting
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

export const capitalizeFirst = (text: string): string => {
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
};

export const formatCamelCase = (text: string): string => {
  return text
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, (str) => str.toUpperCase())
    .trim();
};

// URL and Domain Formatting
export const formatUrl = (url: string): string => {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname;
  } catch {
    return url;
  }
};

export const isValidUrl = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

export const extractDomain = (url: string): string => {
  try {
    const urlObj = new URL(url.startsWith('http') ? url : `https://${url}`);
    return urlObj.hostname;
  } catch {
    return url;
  }
};

// Status and State Formatting
export const formatStatus = (status: string): string => {
  return status
    .split('_')
    .map(word => capitalizeFirst(word))
    .join(' ');
};

export const getStatusColor = (status: string): 'success' | 'warning' | 'error' | 'info' => {
  const statusMap: Record<string, 'success' | 'warning' | 'error' | 'info'> = {
    completed: 'success',
    running: 'info',
    pending: 'warning',
    failed: 'error',
    healthy: 'success',
    warning: 'warning',
    critical: 'error',
  };
  
  return statusMap[status.toLowerCase()] || 'info';
};

// Threat Level Formatting
export const formatThreatLevel = (level: string): string => {
  const levelMap: Record<string, string> = {
    low: 'Low Risk',
    medium: 'Medium Risk',
    high: 'High Risk',
    critical: 'Critical Risk',
  };
  
  return levelMap[level.toLowerCase()] || level;
};

export const getThreatColor = (level: string): 'success' | 'warning' | 'error' => {
  const colorMap: Record<string, 'success' | 'warning' | 'error'> = {
    low: 'success',
    medium: 'warning',
    high: 'error',
    critical: 'error',
  };
  
  return colorMap[level.toLowerCase()] || 'warning';
};

// Investigation Formatting
export const formatTargetType = (type: string): string => {
  const typeMap: Record<string, string> = {
    domain: 'Domain Analysis',
    github: 'GitHub Analysis',
    social_media: 'Social Media Analysis',
    comprehensive: 'Comprehensive Analysis',
  };
  
  return typeMap[type] || formatCamelCase(type);
};

export const formatAnalysisDepth = (depth: string): string => {
  const depthMap: Record<string, string> = {
    basic: 'Basic Analysis',
    deep: 'Deep Analysis',
    comprehensive: 'Comprehensive Analysis',
  };
  
  return depthMap[depth] || formatCamelCase(depth);
};

// Currency and Financial Formatting
export const formatCurrency = (amount: number, currency: string = 'USD'): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
};

// Data Validation Formatting
export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validateDomain = (domain: string): boolean => {
  const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/;
  return domainRegex.test(domain);
};

// Time Duration Formatting
export const formatDuration = (seconds: number): string => {
  if (seconds < 60) {
    return `${seconds}s`;
  } else if (seconds < 3600) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
  } else {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  }
};

// Progress Formatting
export const formatProgress = (current: number, total: number): string => {
  const percentage = total > 0 ? (current / total) * 100 : 0;
  return `${Math.round(percentage)}%`;
};

// Hash and ID Formatting
export const formatHash = (hash: string, length: number = 8): string => {
  if (hash.length <= length) return hash;
  return `${hash.substring(0, length)}...`;
};

export const formatId = (id: string): string => {
  return id.replace(/-/g, '').substring(0, 8).toUpperCase();
}; 