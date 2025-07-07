import React, { useEffect, useState } from 'react';
import { InvestigationService } from '../services/api';
import { CalendarIcon, MagnifyingGlassIcon, FunnelIcon, EyeIcon, TrashIcon, PlayIcon, CheckCircleIcon, XCircleIcon, ClockIcon } from '@heroicons/react/24/outline';

interface Investigation {
  id: number;
  title: string;
  description?: string;
  target_type: string;
  target_value: string;
  status: string;
  progress: number;
  created_at: string;
  updated_at?: string;
}

interface CreateInvestigationForm {
  target_type: string;
  target_value: string;
  analysis_depth: string;
  include_network_analysis: boolean;
  include_timeline_analysis: boolean;
  include_threat_assessment: boolean;
  platforms: string[];
  date_range_start?: string;
  date_range_end?: string;
  search_timeframe: string;
}

interface DateRange {
  startDate: string;
  endDate: string;
}

const Investigations: React.FC = () => {
  const [investigations, setInvestigations] = useState<Investigation[]>([]);
  const [filteredInvestigations, setFilteredInvestigations] = useState<Investigation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [creating, setCreating] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [dateRange, setDateRange] = useState<DateRange>({
    startDate: '',
    endDate: ''
  });
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [targetTypeFilter, setTargetTypeFilter] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [formData, setFormData] = useState<CreateInvestigationForm>({
    target_type: 'domain',
    target_value: '',
    analysis_depth: 'standard',
    include_network_analysis: true,
    include_timeline_analysis: true,
    include_threat_assessment: true,
    platforms: [],
    search_timeframe: 'all',
  });

  // Real-time progress tracking
  const [progressIntervals, setProgressIntervals] = useState<{[key: number]: NodeJS.Timeout}>({});

  useEffect(() => {
    loadInvestigations();
    
    // Set up real-time updates for running investigations
    const interval = setInterval(() => {
      updateRunningInvestigations();
    }, 2000); // Update every 2 seconds

    return () => {
      clearInterval(interval);
      // Clear all progress intervals
      Object.values(progressIntervals).forEach(clearInterval);
    };
  }, []);

  const loadInvestigations = async () => {
    try {
      const data = await InvestigationService.getInvestigations();
      setInvestigations(data);
      setLoading(false);
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  const updateRunningInvestigations = async () => {
    const runningInvestigations = investigations.filter(inv => inv.status === 'running');
    if (runningInvestigations.length === 0) return;

    try {
      for (const investigation of runningInvestigations) {
        const status = await InvestigationService.getInvestigationStatus(investigation.id.toString());
        setInvestigations(prev => 
          prev.map(inv => 
            inv.id === investigation.id 
              ? { ...inv, status: status.status, progress: status.progress }
              : inv
          )
        );
      }
    } catch (error) {
      console.error('Error updating investigation status:', error);
    }
  };

  // Filter investigations based on current filters
  useEffect(() => {
    let filtered = [...investigations];

    // Date range filter
    if (dateRange.startDate || dateRange.endDate) {
      filtered = filtered.filter(inv => {
        const createdDate = new Date(inv.created_at);
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
      filtered = filtered.filter(inv => inv.status === statusFilter);
    }

    // Target type filter
    if (targetTypeFilter !== 'all') {
      filtered = filtered.filter(inv => inv.target_type === targetTypeFilter);
    }

    // Search term filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(inv => 
        inv.title.toLowerCase().includes(term) ||
        inv.target_value.toLowerCase().includes(term) ||
        (inv.description && inv.description.toLowerCase().includes(term))
      );
    }

    setFilteredInvestigations(filtered);
  }, [investigations, dateRange, statusFilter, targetTypeFilter, searchTerm]);

  const clearFilters = () => {
    setDateRange({ startDate: '', endDate: '' });
    setStatusFilter('all');
    setTargetTypeFilter('all');
    setSearchTerm('');
  };

  const handleCreateInvestigation = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    setError(null);

    try {
      // Prepare the request data with date range parameters
      const requestData = {
        target_type: formData.target_type,
        target_value: formData.target_value,
        analysis_depth: formData.analysis_depth,
        include_network_analysis: formData.include_network_analysis,
        include_timeline_analysis: formData.include_timeline_analysis,
        include_threat_assessment: formData.include_threat_assessment,
        platforms: formData.platforms,
        search_timeframe: formData.search_timeframe,
        date_range_start: formData.search_timeframe === 'custom' ? formData.date_range_start : undefined,
        date_range_end: formData.search_timeframe === 'custom' ? formData.date_range_end : undefined,
        analysis_options: {}
      };

      console.log('Creating investigation with data:', requestData);

      const result = await InvestigationService.createInvestigation(requestData);
      
      console.log('Investigation created:', result);
      
      // Reset form
      setFormData({
        target_type: 'domain',
        target_value: '',
        analysis_depth: 'standard',
        include_network_analysis: true,
        include_timeline_analysis: true,
        include_threat_assessment: true,
        platforms: [],
        search_timeframe: 'all',
      });
      
      setShowCreateForm(false);
      
      // Refresh investigations list
      await loadInvestigations();
      
    } catch (err: any) {
      console.error('Error creating investigation:', err);
      setError(err.message || 'Failed to create investigation');
    } finally {
      setCreating(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'running':
        return <PlayIcon className="h-5 w-5 text-blue-500 animate-pulse" />;
      case 'failed':
        return <XCircleIcon className="h-5 w-5 text-red-500" />;
      case 'pending':
        return <ClockIcon className="h-5 w-5 text-yellow-500" />;
      default:
        return <ClockIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'running':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'failed':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
    }
  };

  const handleViewFindings = async (investigationId: number) => {
    try {
      const findings = await InvestigationService.getInvestigationFindings(investigationId.toString());
      // For now, just log the findings - we'll implement a modal later
      console.log('Findings:', findings);
      alert('View findings functionality coming soon!');
    } catch (error) {
      console.error('Error fetching findings:', error);
      alert('Error fetching findings');
    }
  };

  const handleDeleteInvestigation = async (investigationId: number) => {
    if (!window.confirm('Are you sure you want to delete this investigation? This will also delete all associated reports.')) return;
    
    try {
      await InvestigationService.deleteInvestigation(investigationId.toString());
      // Refresh the investigations list
      await loadInvestigations();
    } catch (error) {
      console.error('Error deleting investigation:', error);
      alert('Error deleting investigation');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Investigations
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage and monitor your OSINT investigations
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
            onClick={() => setShowCreateForm(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md flex items-center"
          >
            <PlayIcon className="h-4 w-4 mr-2" />
            Create Investigation
          </button>
        </div>
      </div>

      {/* Real-time status indicator */}
      {investigations.some(inv => inv.status === 'running') && (
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <div className="flex items-center">
            <PlayIcon className="h-5 w-5 text-blue-500 mr-2 animate-pulse" />
            <span className="text-blue-700 dark:text-blue-300 font-medium">
              Real-time updates enabled - {investigations.filter(inv => inv.status === 'running').length} investigation(s) running
            </span>
          </div>
        </div>
      )}

      {/* Filters Section */}
      {showFilters && (
        <div className="card">
          <div className="card-body">
            <h3 className="text-lg font-semibold mb-4">Filter Investigations</h3>
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

              {/* Target Type Filter */}
              <div>
                <label className="block text-sm font-medium mb-1">Target Type</label>
                <select
                  value={targetTypeFilter}
                  onChange={(e) => setTargetTypeFilter(e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="all">All Types</option>
                  <option value="domain">Domain</option>
                  <option value="email">Email</option>
                  <option value="username">Username</option>
                  <option value="phone">Phone</option>
                  <option value="ip_address">IP Address</option>
                  <option value="organization">Organization</option>
                  <option value="person">Person</option>
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
                    placeholder="Search investigations..."
                    className="w-full pl-10 pr-4 p-2 border rounded-md"
                  />
                </div>
              </div>
            </div>

            <div className="flex justify-between items-center mt-4">
              <div className="text-sm text-gray-600 dark:text-gray-400">
                Showing {filteredInvestigations.length} of {investigations.length} investigations
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

      {showCreateForm && (
        <div className="card">
          <div className="card-body">
            <h3 className="text-lg font-semibold mb-4">Create New Investigation</h3>
            <form onSubmit={handleCreateInvestigation} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Target Type</label>
                <select
                  value={formData.target_type}
                  onChange={(e) => setFormData({...formData, target_type: e.target.value})}
                  className="w-full p-2 border rounded-md"
                  required
                >
                  <option value="domain">Domain</option>
                  <option value="email">Email</option>
                  <option value="username">Username</option>
                  <option value="github_repository">GitHub Repository</option>
                  <option value="social_media">Social Media</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Target Value</label>
                <input
                  type="text"
                  value={formData.target_value}
                  onChange={(e) => setFormData({...formData, target_value: e.target.value})}
                  className="w-full p-2 border rounded-md"
                  placeholder="Enter target value..."
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Analysis Depth</label>
                <select
                  value={formData.analysis_depth}
                  onChange={(e) => setFormData({...formData, analysis_depth: e.target.value})}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="basic">Basic</option>
                  <option value="standard">Standard</option>
                  <option value="deep">Deep</option>
                  <option value="comprehensive">Comprehensive</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Search Timeframe</label>
                <select
                  value={formData.search_timeframe}
                  onChange={(e) => setFormData({...formData, search_timeframe: e.target.value})}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="all">All Time</option>
                  <option value="last_24h">Last 24 Hours</option>
                  <option value="last_7d">Last 7 Days</option>
                  <option value="last_30d">Last 30 Days</option>
                  <option value="last_90d">Last 90 Days</option>
                  <option value="last_year">Last Year</option>
                  <option value="custom">Custom Date Range</option>
                </select>
              </div>
              
              {formData.search_timeframe === 'custom' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Start Date</label>
                    <input
                      type="date"
                      value={formData.date_range_start || ''}
                      onChange={(e) => setFormData({...formData, date_range_start: e.target.value})}
                      className="w-full p-2 border rounded-md"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">End Date</label>
                    <input
                      type="date"
                      value={formData.date_range_end || ''}
                      onChange={(e) => setFormData({...formData, date_range_end: e.target.value})}
                      className="w-full p-2 border rounded-md"
                    />
                  </div>
                </div>
              )}
              
              <div className="space-y-2">
                <label className="block text-sm font-medium">Analysis Options</label>
                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.include_network_analysis}
                      onChange={(e) => setFormData({...formData, include_network_analysis: e.target.checked})}
                      className="mr-2"
                    />
                    Include Network Analysis
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.include_timeline_analysis}
                      onChange={(e) => setFormData({...formData, include_timeline_analysis: e.target.checked})}
                      className="mr-2"
                    />
                    Include Timeline Analysis
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.include_threat_assessment}
                      onChange={(e) => setFormData({...formData, include_threat_assessment: e.target.checked})}
                      className="mr-2"
                    />
                    Include Threat Assessment
                  </label>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Platforms</label>
                <div className="flex flex-wrap gap-2">
                  {["github", "twitter", "instagram", "telegram", "discord", "reddit", "facebook", "linkedin", "youtube", "tiktok"].map((platform) => (
                    <label key={platform} className="flex items-center">
                      <input
                        type="checkbox"
                        checked={formData.platforms.includes(platform)}
                        onChange={(e) => {
                          setFormData({
                            ...formData,
                            platforms: e.target.checked
                              ? [...formData.platforms, platform]
                              : formData.platforms.filter((p) => p !== platform),
                          });
                        }}
                        className="mr-2"
                      />
                      {platform.charAt(0).toUpperCase() + platform.slice(1)}
                    </label>
                  ))}
                </div>
              </div>
              
              <div className="flex space-x-2">
                <button
                  type="submit"
                  disabled={creating}
                  className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md disabled:opacity-50 flex items-center"
                >
                  {creating ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Creating...
                    </>
                  ) : (
                    <>
                      <PlayIcon className="h-4 w-4 mr-2" />
                      Create Investigation
                    </>
                  )}
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-md"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="card">
        <div className="card-body">
          {loading && (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="ml-2 text-gray-600 dark:text-gray-400">Loading investigations...</span>
            </div>
          )}
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
              <p className="text-red-700 dark:text-red-300">Error: {error}</p>
            </div>
          )}
          {!loading && !error && filteredInvestigations.length === 0 && (
            <div className="text-center py-8">
              <p className="text-gray-500 dark:text-gray-400">No investigations found matching your filters.</p>
            </div>
          )}
          {!loading && !error && filteredInvestigations.length > 0 && (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Title</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Target</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Progress</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Created</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                  {filteredInvestigations.map((inv) => (
                    <tr key={inv.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900 dark:text-white">{inv.title}</div>
                        {inv.description && (
                          <div className="text-sm text-gray-500 dark:text-gray-400">{inv.description}</div>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900 dark:text-white">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                            {inv.target_type}
                          </span>
                          <span className="ml-2">{inv.target_value}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          {getStatusIcon(inv.status)}
                          <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(inv.status)}`}>
                            {inv.status}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mr-2">
                            <div 
                              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${inv.progress}%` }}
                            ></div>
                          </div>
                          <span className="text-sm text-gray-500 dark:text-gray-400">{inv.progress}%</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {new Date(inv.created_at).toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleViewFindings(inv.id)}
                            className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300"
                            title="View Findings"
                          >
                            <EyeIcon className="h-4 w-4" />
                          </button>
                          {inv.status === 'completed' && (
                            <button
                              onClick={() => window.open(`/api/v1/exports/investigation/${inv.id}/pdf`, '_blank')}
                              className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300"
                              title="Export Report"
                            >
                              <CalendarIcon className="h-4 w-4" />
                            </button>
                          )}
                          <button
                            onClick={() => handleDeleteInvestigation(inv.id)}
                            className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                            title="Delete Investigation"
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

export default Investigations; 