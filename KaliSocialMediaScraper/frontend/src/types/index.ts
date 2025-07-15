// Core Types
export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export interface Investigation {
  id: number;
  title: string;
  description?: string;
  target_type: 'domain' | 'email' | 'username' | 'phone' | 'ip_address' | 'organization' | 'person' | 'repository' | 'github_repository' | 'social_media';
  target_value: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  progress: number;
  created_at: string;
  updated_at?: string;
  results?: InvestigationResults;
}

export interface InvestigationResults {
  domain_analysis?: DomainAnalysis;
  github_analysis?: GitHubAnalysis;
  social_media_analysis?: SocialMediaAnalysis;
  threat_assessment?: ThreatAssessment;
  network_analysis?: NetworkAnalysis;
  timeline_analysis?: TimelineAnalysis;
}

// Domain Analysis Types
export interface DomainAnalysis {
  domain: string;
  ip_addresses: string[];
  subdomains: string[];
  dns_records: Record<string, string[]>;
  whois_data: Record<string, any>;
  ssl_certificate: Record<string, any>;
  technologies: string[];
  threat_indicators: string[];
  threat_assessment?: ThreatAssessment;
  reputation?: ReputationData;
  geolocation?: GeolocationData;
  risk_score: number;
}

export interface DNSRecord {
  type: string;
  name: string;
  value: string;
  ttl: number;
}

export interface WhoisData {
  registrar: string;
  creation_date: string;
  expiration_date: string;
  updated_date: string;
  status: string[];
  name_servers: string[];
}

export interface SSLCertificate {
  issuer: string;
  subject: string;
  valid_from: string;
  valid_until: string;
  serial_number: string;
  fingerprint: string;
}

export interface Technology {
  name: string;
  version?: string;
  category: string;
  confidence: number;
}

export interface ReputationData {
  score: number;
  category: string;
  details: string[];
}

export interface GeolocationData {
  country: string;
  region: string;
  city: string;
  latitude: number;
  longitude: number;
  isp: string;
}

// GitHub Analysis Types
export interface GitHubAnalysis {
  user?: GitHubUser;
  organization?: GitHubOrganization;
  repository?: GitHubRepository;
  activity: GitHubActivity[];
  threat_assessment?: ThreatAssessment;
}

export interface GitHubUser {
  username: string;
  name?: string;
  bio?: string;
  location?: string;
  company?: string;
  website?: string;
  public_repos: number;
  public_gists: number;
  followers: number;
  following: number;
  created_at: string;
  updated_at: string;
  avatar_url: string;
}

export interface GitHubOrganization {
  name: string;
  login: string;
  description?: string;
  location?: string;
  public_repos: number;
  public_gists: number;
  followers: number;
  following: number;
  created_at: string;
  updated_at: string;
  avatar_url: string;
}

export interface GitHubRepository {
  name: string;
  full_name: string;
  description?: string;
  language: string;
  stargazers_count: number;
  forks_count: number;
  watchers_count: number;
  open_issues_count: number;
  created_at: string;
  updated_at: string;
  pushed_at: string;
  topics: string[];
  license?: string;
  default_branch: string;
}

export interface GitHubActivity {
  type: 'commit' | 'issue' | 'pull_request' | 'release';
  id: string;
  title: string;
  description?: string;
  created_at: string;
  updated_at: string;
  author: string;
  url: string;
}

// Social Media Analysis Types
export interface SocialMediaAnalysis {
  platforms: PlatformAnalysis[];
  sherlock_results: SherlockResult[];
  threat_assessment?: ThreatAssessment;
  network_analysis?: NetworkAnalysis;
}

export interface PlatformAnalysis {
  platform: string;
  username: string;
  profile: SocialMediaProfile;
  posts: SocialMediaPost[];
  followers_count: number;
  following_count: number;
  threat_score: number;
}

export interface SocialMediaProfile {
  username: string;
  platform: string;
  display_name?: string;
  bio?: string;
  followers: number;
  following: number;
  verified: boolean;
  created_at: string;
  avatar_url?: string;
  cover_url?: string;
}

export interface SocialMediaPost {
  id: string;
  platform: string;
  author: string;
  content: string;
  timestamp: string;
  engagement: Record<string, number>;
  metadata: Record<string, any>;
  threat_indicators: string[];
}

export interface SherlockResult {
  platform: string;
  url: string;
  status: 'found' | 'not_found' | 'error';
  username: string;
  site_name: string;
  site_url: string;
}

// Threat Analysis Types
export interface ThreatAssessment {
  target: string;
  threat_level: 'low' | 'medium' | 'high' | 'critical';
  threat_score: number;
  indicators: string[];
  risk_factors: string[];
  recommendations: string[];
  confidence: number;
  created_at: string;
}

export interface ThreatIndicator {
  type: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
  evidence: string[];
}

// Network Analysis Types
export interface NetworkAnalysis {
  nodes: NetworkNode[];
  edges: NetworkEdge[];
  communities: NetworkCommunity[];
  centrality_scores: CentralityScores;
}

export interface NetworkNode {
  id: string;
  label: string;
  type: string;
  properties: Record<string, any>;
  threat_level?: 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
}

export interface NetworkEdge {
  source: string;
  target: string;
  type: string;
  properties: Record<string, any>;
  strength: number;
}

export interface NetworkCommunity {
  id: string;
  nodes: string[];
  threat_score: number;
  description: string;
}

export interface CentralityScores {
  degree: Record<string, number>;
  betweenness: Record<string, number>;
  closeness: Record<string, number>;
  eigenvector: Record<string, number>;
}

// Timeline Analysis Types
export interface TimelineAnalysis {
  events: TimelineEvent[];
  patterns: TimelinePattern[];
  anomalies: TimelineAnomaly[];
}

export interface TimelineEvent {
  timestamp: string;
  event_type: string;
  description: string;
  source: string;
  platform?: string;
  properties: Record<string, any>;
  threat_level?: 'low' | 'medium' | 'high' | 'critical';
}

export interface TimelinePattern {
  id: string;
  pattern_type: string;
  description: string;
  frequency: number;
  time_range: {
    start: string;
    end: string;
  };
  events: string[];
}

export interface TimelineAnomaly {
  id: string;
  anomaly_type: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  timestamp: string;
  related_events: string[];
}

// Dashboard Types
export interface DashboardData {
  statistics: DashboardStatistics;
  recent_investigations: Investigation[];
  active_threats: ThreatAssessment[];
  system_health: SystemHealth;
  real_time_metrics: RealTimeMetrics;
}

export interface DashboardStatistics {
  total_investigations: number;
  active_investigations: number;
  completed_investigations: number;
  total_threats: number;
  high_priority_threats: number;
  total_profiles_scraped: number;
  total_posts_analyzed: number;
}

export interface SystemHealth {
  status: 'healthy' | 'warning' | 'critical';
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  database_status: string;
  redis_status: string;
  celery_status: string;
}

export interface RealTimeMetrics {
  investigations_per_minute: number;
  threats_detected: number;
  data_processed: number;
  active_scrapers: number;
}

// API Response Types
export interface ApiResponse<T> {
  status: 'success' | 'error';
  data?: T;
  message?: string;
  timestamp: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Form Data Types
export interface InvestigationFormData {
  target_type: 'domain' | 'email' | 'username' | 'phone' | 'ip_address' | 'organization' | 'person' | 'repository' | 'github_repository' | 'social_media';
  target_value: string;
  analysis_depth: 'basic' | 'standard' | 'deep' | 'comprehensive';
  platforms: string[];
  include_network_analysis: boolean;
  include_timeline_analysis: boolean;
  include_threat_assessment: boolean;
  analysis_options: Record<string, any>;
  search_timeframe: string;
  date_range_start?: string;
  date_range_end?: string;
}

export interface SocialMediaScrapingFormData {
  platform: string;
  target: string;
  include_metadata: boolean;
  include_media: boolean;
  max_posts: number;
}

// App State Types
export interface AppState {
  theme: 'light' | 'dark' | 'system';
  sidebarOpen: boolean;
  notifications: Notification[];
  user: User | null;
  loading: boolean;
  error: string | null;
}

export interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  timestamp: string;
  read: boolean;
}

// Chart Types
export interface ChartData {
  labels: string[];
  datasets: ChartDataset[];
}

export interface ChartDataset {
  label: string;
  data: number[];
  backgroundColor?: string;
  borderColor?: string;
  borderWidth?: number;
}

// Export Types
export interface ExportOptions {
  format: 'pdf' | 'csv' | 'json' | 'excel';
  include_charts: boolean;
  include_data: boolean;
  date_range?: {
    start: string;
    end: string;
  };
}

// Settings Types
export interface AppSettings {
  max_concurrent_scrapers: number;
  rate_limiting_enabled: boolean;
  proxy_rotation_enabled: boolean;
  data_retention_days: number;
  threat_detection_sensitivity: 'low' | 'medium' | 'high';
  auto_export_enabled: boolean;
  notification_enabled: boolean;
  dark_web_monitoring: boolean;
  ml_analysis_enabled: boolean;
  max_investigations_per_user: number;
  scraping_timeout_seconds: number;
  max_profiles_per_investigation: number;
  threat_score_threshold: number;
  auto_cleanup_enabled: boolean;
  backup_enabled: boolean;
}

// WebSocket Types
export interface RealTimeData {
  type: 'investigation_update' | 'threat_alert' | 'system_status' | 'metric_update';
  data: any;
  timestamp: string;
}

export interface WebSocketOptions {
  url: string;
  onMessage?: (data: any) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (event: Event) => void;
  reconnectAttempts?: number;
  reconnectInterval?: number;
  autoReconnect?: boolean;
} 