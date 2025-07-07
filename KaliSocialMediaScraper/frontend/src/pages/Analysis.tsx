import React, { useState, useEffect } from 'react';
import { 
  MagnifyingGlassIcon, 
  ChartBarIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  XCircleIcon,
  PlusIcon,
  EyeIcon,
  GlobeAltIcon,
  ShieldCheckIcon,
  CircleStackIcon,
  DocumentTextIcon,
  FunnelIcon,
  CalendarIcon
} from '@heroicons/react/24/outline';
import { AnalysisService } from '../services/api';

interface AnalysisResult {
  id: string;
  type: 'domain' | 'threat' | 'network' | 'social';
  target: string;
  status: 'running' | 'completed' | 'failed';
  progress: number;
  createdAt: string;
  result?: any;
}

interface ThreatAssessment {
  target: string;
  threatLevel: 'low' | 'medium' | 'high' | 'critical';
  threatScore: number;
  indicators: string[];
  riskFactors: string[];
  recommendations: string[];
  confidence: number;
}

interface DateRange {
  startDate: string;
  endDate: string;
}

const Analysis: React.FC = () => {
  const [analysisJobs, setAnalysisJobs] = useState<AnalysisResult[]>([]);
  const [filteredAnalysisJobs, setFilteredAnalysisJobs] = useState<AnalysisResult[]>([]);
  const [threatAssessments, setThreatAssessments] = useState<ThreatAssessment[]>([]);
  const [filteredThreatAssessments, setFilteredThreatAssessments] = useState<ThreatAssessment[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showAnalysisForm, setShowAnalysisForm] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [selectedType, setSelectedType] = useState<'domain' | 'threat' | 'network' | 'social'>('domain');
  const [targetValue, setTargetValue] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [dateRange, setDateRange] = useState<DateRange>({
    startDate: '',
    endDate: ''
  });
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState<string>('');

  useEffect(() => {
    fetchAnalysisResults();
  }, []);

  // Filter analysis jobs and threat assessments
  useEffect(() => {
    // Filter analysis jobs
    let filteredJobs = [...analysisJobs];

    // Date range filter
    if (dateRange.startDate || dateRange.endDate) {
      filteredJobs = filteredJobs.filter(job => {
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
      filteredJobs = filteredJobs.filter(job => job.status === statusFilter);
    }

    // Type filter
    if (typeFilter !== 'all') {
      filteredJobs = filteredJobs.filter(job => job.type === typeFilter);
    }

    // Search term filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filteredJobs = filteredJobs.filter(job => 
        job.target.toLowerCase().includes(term) ||
        job.type.toLowerCase().includes(term)
      );
    }

    setFilteredAnalysisJobs(filteredJobs);

    // Filter threat assessments (use same filters)
    let filteredAssessments = [...threatAssessments];
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filteredAssessments = filteredAssessments.filter(assessment => 
        assessment.target.toLowerCase().includes(term)
      );
    }
    setFilteredThreatAssessments(filteredAssessments);
  }, [analysisJobs, threatAssessments, dateRange, statusFilter, typeFilter, searchTerm]);

  const clearFilters = () => {
    setDateRange({ startDate: '', endDate: '' });
    setStatusFilter('all');
    setTypeFilter('all');
    setSearchTerm('');
  };

  const fetchAnalysisResults = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Fetch real analysis results from backend
      const [threatData, networkData] = await Promise.all([
        AnalysisService.getAnalysisResults('threat'),
        AnalysisService.getAnalysisResults('network-graph/summary')
      ]);

      // Process threat assessments
      const threatAssessments = threatData.threat_assessments || [];
      const mappedThreatAssessments: ThreatAssessment[] = threatAssessments.map((assessment: any) => ({
        target: assessment.target || 'Unknown',
        threatLevel: assessment.threat_level || 'low',
        threatScore: assessment.threat_score || 0.1,
        indicators: assessment.indicators || [],
        riskFactors: assessment.risk_factors || [],
        recommendations: assessment.recommendations || [],
        confidence: assessment.confidence || 0.8
      }));

      // Process analysis jobs
      const analysisJobs: AnalysisResult[] = [];
      
      // Add threat analysis job
      if (threatData.threat_assessments && threatData.threat_assessments.length > 0) {
        analysisJobs.push({
          id: 'threat-analysis',
          type: 'threat',
          target: 'System-wide threat assessment',
          status: 'completed',
          progress: 100,
          createdAt: new Date().toISOString(),
          result: threatData
        });
      }

      // Add network analysis job
      if (networkData && networkData.nodes) {
        analysisJobs.push({
          id: 'network-analysis',
          type: 'network',
          target: 'Network graph analysis',
          status: networkData.nodes.length > 0 ? 'completed' : 'failed',
          progress: networkData.nodes.length > 0 ? 100 : 0,
          createdAt: new Date().toISOString(),
          result: networkData
        });
      }

      setAnalysisJobs(analysisJobs);
      setThreatAssessments(mappedThreatAssessments);
    } catch (error) {
      console.error('Failed to fetch analysis results:', error);
      setError('Failed to fetch analysis results');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRunAnalysis = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!targetValue.trim()) {
      setError('Please enter a target value');
      return;
    }

    try {
      setIsAnalyzing(true);
      setError(null);

      // Create new analysis job
      const newJob: AnalysisResult = {
        id: Date.now().toString(),
        type: selectedType,
        target: targetValue,
        status: 'running',
        progress: 0,
        createdAt: new Date().toISOString()
      };

      setAnalysisJobs(prev => [newJob, ...prev]);

      // Call the actual analysis API
      const result: any = await AnalysisService.runAnalysis({
        type: selectedType,
        target: targetValue
      });

      // Update job status
      setAnalysisJobs(prev => prev.map(job => 
        job.id === newJob.id 
          ? { ...job, status: 'completed', progress: 100, result }
          : job
      ));

      // Add threat assessment if completed
      if (result && result.threat_assessments && result.threat_assessments.length > 0) {
        const assessment = result.threat_assessments[0];
        const newAssessment: ThreatAssessment = {
          target: targetValue,
          threatLevel: assessment.threat_level || 'low',
          threatScore: assessment.threat_score || 0.1,
          indicators: assessment.indicators || [],
          riskFactors: assessment.risk_factors || [],
          recommendations: assessment.recommendations || [],
          confidence: assessment.confidence || 0.8
        };

        setThreatAssessments(prev => [newAssessment, ...prev]);
      }

      setShowAnalysisForm(false);
      setTargetValue('');

    } catch (error) {
      console.error('Failed to run analysis:', error);
      setError('Failed to run analysis');
      
      // Update job status to failed
      setAnalysisJobs(prev => prev.map(job => 
        job.id === Date.now().toString()
          ? { ...job, status: 'failed', progress: 0 }
          : job
      ));
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getThreatLevelClass = (level: string) => {
    switch (level) {
      case 'critical':
        return 'text-red-600 bg-red-100';
      case 'high':
        return 'text-orange-600 bg-orange-100';
      case 'medium':
        return 'text-yellow-600 bg-yellow-100';
      case 'low':
        return 'text-green-600 bg-green-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
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

  const getAnalysisTypeIcon = (type: string) => {
    switch (type) {
      case 'domain':
        return <GlobeAltIcon className="h-5 w-5" />;
      case 'threat':
        return <ShieldCheckIcon className="h-5 w-5" />;
      case 'network':
        return <CircleStackIcon className="h-5 w-5" />;
      case 'social':
        return <ChartBarIcon className="h-5 w-5" />;
      default:
        return <DocumentTextIcon className="h-5 w-5" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Analysis
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Advanced threat analysis and intelligence
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
            onClick={() => setShowAnalysisForm(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
          >
            <PlusIcon className="h-5 w-5" />
            <span>New Analysis</span>
          </button>
        </div>
      </div>

      {/* Filters Section */}
      {showFilters && (
        <div className="card">
          <div className="card-body">
            <h3 className="text-lg font-semibold mb-4">Filter Analysis</h3>
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
                  <option value="running">Running</option>
                  <option value="completed">Completed</option>
                  <option value="failed">Failed</option>
                </select>
              </div>

              {/* Type Filter */}
              <div>
                <label className="block text-sm font-medium mb-1">Analysis Type</label>
                <select
                  value={typeFilter}
                  onChange={(e) => setTypeFilter(e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="all">All Types</option>
                  <option value="domain">Domain</option>
                  <option value="threat">Threat</option>
                  <option value="network">Network</option>
                  <option value="social">Social</option>
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
                    placeholder="Search analysis..."
                    className="w-full pl-10 pr-4 p-2 border rounded-md"
                  />
                </div>
              </div>
            </div>

            <div className="flex justify-between items-center mt-4">
              <div className="text-sm text-gray-600 dark:text-gray-400">
                Showing {filteredAnalysisJobs.length} of {analysisJobs.length} analysis jobs
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

      {/* Analysis Form */}
      {showAnalysisForm && (
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">
              Run New Analysis
            </h3>
          </div>
          <div className="card-body">
            <form onSubmit={handleRunAnalysis} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Analysis Type
                  </label>
                  <select
                    value={selectedType}
                    onChange={(e) => setSelectedType(e.target.value as any)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="domain">Domain Analysis</option>
                    <option value="threat">Threat Assessment</option>
                    <option value="network">Network Analysis</option>
                    <option value="social">Social Media Analysis</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Target
                  </label>
                  <input
                    type="text"
                    value={targetValue}
                    onChange={(e) => setTargetValue(e.target.value)}
                    placeholder="Enter domain, IP, or target"
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
                  disabled={isAnalyzing}
                  className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
                >
                  {isAnalyzing ? (
                    <>
                      <ClockIcon className="h-4 w-4 animate-spin" />
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <MagnifyingGlassIcon className="h-4 w-4" />
                      <span>Start Analysis</span>
                    </>
                  )}
                </button>
                <button
                  type="button"
                  onClick={() => setShowAnalysisForm(false)}
                  className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Analysis Jobs */}
      {analysisJobs.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">
              Analysis Jobs
            </h3>
          </div>
          <div className="card-body">
            <div className="space-y-4">
                              {filteredAnalysisJobs.map((job) => (
                <div key={job.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center space-x-4">
                    {getStatusIcon(job.status)}
                    <div className="flex items-center space-x-2">
                      {getAnalysisTypeIcon(job.type)}
                      <div>
                        <p className="font-medium">{(job.type || 'unknown').toUpperCase()}: {job.target}</p>
                        <p className="text-sm text-gray-600">
                          {job.status === 'running' ? `Progress: ${job.progress}%` : job.status}
                        </p>
                      </div>
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
                    {job.status === 'completed' && (
                      <button className="text-primary-600 hover:text-primary-700">
                        <EyeIcon className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Threat Assessments */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
            Threat Assessments
          </h3>
        </div>
        <div className="card-body">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <ClockIcon className="h-6 w-6 animate-spin text-primary-600" />
              <span className="ml-2 text-gray-600">Loading assessments...</span>
            </div>
          ) : filteredThreatAssessments.length === 0 ? (
            <div className="text-center py-8">
              <ShieldCheckIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">No threat assessments found matching your filters</p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredThreatAssessments.map((assessment, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-2">
                      <ExclamationTriangleIcon className="h-5 w-5 text-primary-600" />
                      <h4 className="font-medium">{assessment.target}</h4>
                    </div>
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getThreatLevelClass(assessment.threatLevel)}`}>
                      {(assessment.threatLevel || 'low').toUpperCase()}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div>
                      <p className="text-sm font-medium text-gray-600">Threat Score</p>
                      <p className="text-lg font-semibold">{(assessment.threatScore * 100).toFixed(1)}%</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-600">Confidence</p>
                      <p className="text-lg font-semibold">{(assessment.confidence * 100).toFixed(1)}%</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-600">Risk Level</p>
                      <p className="text-lg font-semibold">{assessment.threatLevel}</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h5 className="font-medium mb-2">Threat Indicators</h5>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {assessment.indicators.map((indicator, i) => (
                          <li key={i} className="flex items-center">
                            <ExclamationTriangleIcon className="h-3 w-3 text-red-500 mr-2" />
                            {indicator}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h5 className="font-medium mb-2">Recommendations</h5>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {assessment.recommendations.map((rec, i) => (
                          <li key={i} className="flex items-center">
                            <CheckCircleIcon className="h-3 w-3 text-green-500 mr-2" />
                            {rec}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Analysis; 