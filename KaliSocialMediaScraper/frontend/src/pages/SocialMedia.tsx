import React, { useState, useEffect } from 'react';
import { 
  MagnifyingGlassIcon, 
  UserIcon, 
  CheckCircleIcon,
  ClockIcon,
  XCircleIcon,
  PlusIcon,
  EyeIcon,
  TrashIcon,
  ArrowPathIcon,
  GlobeAltIcon,
  ExclamationTriangleIcon,
  DocumentTextIcon,
  FunnelIcon,
  CalendarIcon
} from '@heroicons/react/24/outline';
import { SocialMediaService } from '../services/api';

interface SocialMediaProfile {
  id: string;
  platform: string;
  username: string;
  displayName: string;
  bio: string;
  followersCount: number;
  followingCount: number;
  postsCount: number;
  isVerified: boolean;
  isPrivate: boolean;
  threatScore: number;
  sentimentScore: number;
  collectedAt: string;
}

interface ScrapingJob {
  id: string;
  platform: string;
  target: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  createdAt: string;
  result?: any;
}

interface DateRange {
  startDate: string;
  endDate: string;
}

const SocialMedia: React.FC = () => {
  const [profiles, setProfiles] = useState<SocialMediaProfile[]>([]);
  const [scrapingJobs, setScrapingJobs] = useState<ScrapingJob[]>([]);
  const [filteredScrapingJobs, setFilteredScrapingJobs] = useState<ScrapingJob[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showScrapingForm, setShowScrapingForm] = useState(false);
  const [isScraping, setIsScraping] = useState(false);
  const [selectedPlatform, setSelectedPlatform] = useState('github');
  const [targetValue, setTargetValue] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [dateRange, setDateRange] = useState<DateRange>({
    startDate: '',
    endDate: ''
  });
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [platformFilter, setPlatformFilter] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState<string>('');

  useEffect(() => {
    fetchProfiles();
  }, []);

  const fetchProfiles = async () => {
    try {
      setIsLoading(true);
      const data = await SocialMediaService.scrapePlatform('profiles', 'list');
      setProfiles(data);
    } catch (error) {
      console.error('Failed to fetch profiles:', error);
      setError('Failed to fetch profiles');
    } finally {
      setIsLoading(false);
    }
  };

  const handleScrapeProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!targetValue.trim()) {
      setError('Please enter a target value');
      return;
    }

    try {
      setIsScraping(true);
      setError(null);

      // Create new scraping job
      const newJob: ScrapingJob = {
        id: Date.now().toString(),
        platform: selectedPlatform,
        target: targetValue,
        status: 'running',
        progress: 0,
        createdAt: new Date().toISOString()
      };

      setScrapingJobs(prev => [newJob, ...prev]);

      // Call the actual scraping API
      const result = await SocialMediaService.scrapePlatform(selectedPlatform, targetValue);

      // Update job status
      setScrapingJobs(prev => prev.map(job => 
        job.id === newJob.id 
          ? { ...job, status: 'completed', progress: 100, result }
          : job
      ));

      // Add new profile if successful
      if (result && result.data) {
        const newProfile: SocialMediaProfile = {
          id: Date.now().toString(),
          platform: selectedPlatform,
          username: targetValue,
          displayName: result.data.display_name || targetValue,
          bio: result.data.bio || '',
          followersCount: result.data.followers_count || 0,
          followingCount: result.data.following_count || 0,
          postsCount: result.data.public_repos || 0,
          isVerified: result.data.is_verified || false,
          isPrivate: result.data.is_private || false,
          threatScore: 0.1, // Calculate based on analysis
          sentimentScore: 0.5, // Calculate based on analysis
          collectedAt: new Date().toISOString()
        };

        setProfiles(prev => [newProfile, ...prev]);
      }

      setShowScrapingForm(false);
      setTargetValue('');

    } catch (error) {
      console.error('Failed to scrape profile:', error);
      setError('Failed to scrape profile');
      
      // Update job status to failed
      setScrapingJobs(prev => prev.map(job => 
        job.id === Date.now().toString()
          ? { ...job, status: 'failed', progress: 0 }
          : job
      ));
    } finally {
      setIsScraping(false);
    }
  };

  const deleteProfile = async (profileId: string) => {
    try {
      setProfiles(prev => prev.filter(profile => profile.id !== profileId));
    } catch (error) {
      console.error('Failed to delete profile:', error);
    }
  };

  const getThreatScoreClass = (score: number) => {
    if (score >= 0.8) return 'text-red-600 bg-red-100';
    if (score >= 0.6) return 'text-orange-600 bg-orange-100';
    if (score >= 0.4) return 'text-yellow-600 bg-yellow-100';
    return 'text-green-600 bg-green-100';
  };

  const getThreatScoreText = (score: number) => {
    if (score >= 0.8) return 'Critical';
    if (score >= 0.6) return 'High';
    if (score >= 0.4) return 'Medium';
    return 'Low';
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'running':
        return <ClockIcon className="h-5 w-5 text-yellow-500 animate-spin" />;
      case 'failed':
        return <XCircleIcon className="h-5 w-5 text-red-500" />;
      default:
        return <ClockIcon className="h-5 w-5 text-gray-400" />;
    }
  };

  useEffect(() => {
    fetchProfiles();
  }, []);

  // Filter scraping jobs based on current filters
  useEffect(() => {
    let filtered = [...scrapingJobs];

    // Date range filter
    if (dateRange.startDate || dateRange.endDate) {
      filtered = filtered.filter(job => {
        const createdDate = new Date(job.createdAt);
        const startDate = dateRange.startDate ? new Date(dateRange.startDate) : null;
        const endDate = dateRange.endDate ? new Date(dateRange.endDate) : null;
        
        if (startDate && endDate) {
          return createdDate >= startDate && createdDate <= endDate;
        } else if (startDate) {
          return createdDate >= startDate;
        } else if (endDate) {
          return createdDate <= endDate;
        }
        return true;
      });
    }

    // Status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter(job => job.status === statusFilter);
    }

    // Platform filter
    if (platformFilter !== 'all') {
      filtered = filtered.filter(job => job.platform === platformFilter);
    }

    // Search term filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(job => 
        job.target.toLowerCase().includes(term) ||
        job.platform.toLowerCase().includes(term)
      );
    }

    setFilteredScrapingJobs(filtered);
  }, [scrapingJobs, dateRange, statusFilter, platformFilter, searchTerm]);

  const clearFilters = () => {
    setDateRange({ startDate: '', endDate: '' });
    setStatusFilter('all');
    setPlatformFilter('all');
    setSearchTerm('');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Social Media Analysis
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Analyze social media profiles and posts
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center px-3 py-2 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600"
          >
            <FunnelIcon className="h-4 w-4 mr-2" />
            Filters
          </button>
          <button
            onClick={() => setShowScrapingForm(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
          >
            <PlusIcon className="h-5 w-5" />
            <span>Scrape Profile</span>
          </button>
        </div>
      </div>

      {/* Filters Section */}
      {showFilters && (
        <div className="card">
          <div className="card-body">
            <h3 className="text-lg font-semibold mb-4">Filter Social Media Data</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Date Range */}
              <div>
                <label className="block text-sm font-medium mb-1">Date Range</label>
                <div className="flex space-x-2">
                  <input
                    type="date"
                    value={dateRange.startDate}
                    onChange={(e) => setDateRange({...dateRange, startDate: e.target.value})}
                    className="flex-1 p-2 border rounded-md text-sm"
                  />
                  <span className="text-gray-500 self-center">to</span>
                  <input
                    type="date"
                    value={dateRange.endDate}
                    onChange={(e) => setDateRange({...dateRange, endDate: e.target.value})}
                    className="flex-1 p-2 border rounded-md text-sm"
                  />
                </div>
              </div>

              {/* Status Filter */}
              <div>
                <label className="block text-sm font-medium mb-1">Status</label>
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="all">All Status</option>
                  <option value="pending">Pending</option>
                  <option value="running">Running</option>
                  <option value="completed">Completed</option>
                  <option value="failed">Failed</option>
                </select>
              </div>

              {/* Platform Filter */}
              <div>
                <label className="block text-sm font-medium mb-1">Platform</label>
                <select
                  value={platformFilter}
                  onChange={(e) => setPlatformFilter(e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="all">All Platforms</option>
                  <option value="github">GitHub</option>
                  <option value="twitter">Twitter</option>
                  <option value="instagram">Instagram</option>
                  <option value="linkedin">LinkedIn</option>
                  <option value="reddit">Reddit</option>
                </select>
              </div>

              {/* Search */}
              <div>
                <label className="block text-sm font-medium mb-1">Search</label>
                <div className="relative">
                  <MagnifyingGlassIcon className="h-4 w-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                  <input
                    type="text"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="Search profiles..."
                    className="w-full pl-10 pr-4 p-2 border rounded-md"
                  />
                </div>
              </div>
            </div>

            <div className="flex justify-between items-center mt-4">
              <div className="text-sm text-gray-600 dark:text-gray-400">
                Showing {filteredScrapingJobs.length} of {scrapingJobs.length} scraping jobs
              </div>
              <button
                onClick={clearFilters}
                className="text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
              >
                Clear Filters
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Scraping Form */}
      {showScrapingForm && (
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">
              Scrape Social Media Profile
            </h3>
          </div>
          <div className="card-body">
            <form onSubmit={handleScrapeProfile} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Platform
                  </label>
                  <select
                    value={selectedPlatform}
                    onChange={(e) => setSelectedPlatform(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="github">GitHub</option>
                    <option value="twitter">Twitter</option>
                    <option value="instagram">Instagram</option>
                    <option value="linkedin">LinkedIn</option>
                    <option value="reddit">Reddit</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Target Username/Profile
                  </label>
                  <input
                    type="text"
                    value={targetValue}
                    onChange={(e) => setTargetValue(e.target.value)}
                    placeholder="Enter username or profile URL"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    required
                  />
                </div>
              </div>

              {error && (
                <div className="text-red-600 text-sm">{error}</div>
              )}

              <div className="flex space-x-2">
                <button
                  type="submit"
                  disabled={isScraping}
                  className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
                >
                  {isScraping ? (
                    <>
                      <ArrowPathIcon className="h-4 w-4 animate-spin" />
                      <span>Scraping...</span>
                    </>
                  ) : (
                    <>
                      <MagnifyingGlassIcon className="h-4 w-4" />
                      <span>Start Scraping</span>
                    </>
                  )}
                </button>
                <button
                  type="button"
                  onClick={() => setShowScrapingForm(false)}
                  className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Scraping Jobs */}
      {scrapingJobs.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">
              Active Scraping Jobs
            </h3>
          </div>
          <div className="card-body">
            <div className="space-y-4">
              {filteredScrapingJobs.map((job) => (
                <div key={job.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center space-x-4">
                    {getStatusIcon(job.status)}
                    <div>
                      <p className="font-medium">{job.platform}: {job.target}</p>
                      <p className="text-sm text-gray-600">
                        {job.status === 'running' ? `Progress: ${job.progress}%` : job.status}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {job.status === 'running' && (
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${job.progress}%` }}
                        />
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Profiles List */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
            Scraped Profiles
          </h3>
        </div>
        <div className="card-body">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <ArrowPathIcon className="h-6 w-6 animate-spin text-primary-600" />
              <span className="ml-2 text-gray-600">Loading profiles...</span>
            </div>
          ) : profiles.length === 0 ? (
            <div className="text-center py-8">
              <UserIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">No profiles scraped yet</p>
            </div>
          ) : (
            <div className="overflow-hidden">
              <table className="table">
                <thead className="table-header">
                  <tr>
                    <th className="table-header-cell">Profile</th>
                    <th className="table-header-cell">Platform</th>
                    <th className="table-header-cell">Followers</th>
                    <th className="table-header-cell">Posts</th>
                    <th className="table-header-cell">Threat Score</th>
                    <th className="table-header-cell">Status</th>
                    <th className="table-header-cell">Collected</th>
                    <th className="table-header-cell">Actions</th>
                  </tr>
                </thead>
                <tbody className="table-body">
                  {profiles.map((profile) => (
                    <tr key={profile.id} className="table-row">
                      <td className="table-cell">
                        <div className="flex items-center">
                          <UserIcon className="h-5 w-5 text-primary-600 mr-2" />
                          <div>
                            <p className="font-medium">{profile.displayName}</p>
                            <p className="text-sm text-gray-600">@{profile.username}</p>
                          </div>
                        </div>
                      </td>
                      <td className="table-cell">
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          {profile.platform}
                        </span>
                      </td>
                      <td className="table-cell">
                        <span className="text-sm">{profile.followersCount.toLocaleString()}</span>
                      </td>
                      <td className="table-cell">
                        <span className="text-sm">{profile.postsCount.toLocaleString()}</span>
                      </td>
                      <td className="table-cell">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getThreatScoreClass(profile.threatScore)}`}>
                          {getThreatScoreText(profile.threatScore)}
                        </span>
                      </td>
                      <td className="table-cell">
                        <div className="flex items-center">
                          {profile.isVerified ? (
                            <CheckCircleIcon className="h-4 w-4 text-green-500 mr-1" />
                          ) : (
                            <XCircleIcon className="h-4 w-4 text-gray-400 mr-1" />
                          )}
                          <span className="text-sm">
                            {profile.isVerified ? 'Verified' : 'Unverified'}
                          </span>
                        </div>
                      </td>
                      <td className="table-cell">
                        <span className="text-sm text-gray-600">
                          {new Date(profile.collectedAt).toLocaleDateString()}
                        </span>
                      </td>
                      <td className="table-cell">
                        <div className="flex items-center space-x-2">
                          <button
                            className="text-primary-600 hover:text-primary-700"
                            title="View Details"
                          >
                            <EyeIcon className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => deleteProfile(profile.id)}
                            className="text-red-600 hover:text-red-700"
                            title="Delete"
                          >
                            <TrashIcon className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SocialMedia; 