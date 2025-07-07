import React, { useState, useEffect } from 'react';
import { 
  DocumentTextIcon, 
  ArrowDownTrayIcon, 
  TrashIcon,
  PlusIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  FunnelIcon,
  MagnifyingGlassIcon,
  ChevronDownIcon,
  ChevronUpIcon
} from '@heroicons/react/24/outline';
import { InvestigationService, ExportService } from '../services/api';

interface Report {
  id: string;
  title: string;
  investigation_id: string;
  report_type: 'pdf' | 'html' | 'json' | 'csv';
  status: 'generating' | 'completed' | 'failed';
  created_at: string;
  file_path?: string;
  file_size?: number;
  completed_at?: string;
}

interface ReportContent {
  content_type: string;
  content?: string;
  file_path?: string;
  file_size?: number;
  message?: string;
}

interface DateRange {
  startDate: string;
  endDate: string;
}

const Reports: React.FC = () => {
  const [reports, setReports] = useState<Report[]>([]);
  const [filteredReports, setFilteredReports] = useState<Report[]>([]);
  const [investigations, setInvestigations] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedInvestigation, setSelectedInvestigation] = useState('');
  const [selectedFormat, setSelectedFormat] = useState<'pdf' | 'html' | 'json' | 'csv'>('pdf');
  const [isGenerating, setIsGenerating] = useState(false);

  const [reportContent, setReportContent] = useState<ReportContent | null>(null);
  const [isLoadingContent, setIsLoadingContent] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [expandedReports, setExpandedReports] = useState<Set<string>>(new Set());
  const [dateRange, setDateRange] = useState<DateRange>({
    startDate: '',
    endDate: ''
  });
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [reportTypeFilter, setReportTypeFilter] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState<string>('');

  useEffect(() => {
    fetchReports();
    fetchInvestigations();
  }, []);

  // Filter reports based on current filters
  useEffect(() => {
    let filtered = [...reports];

    // Date range filter
    if (dateRange.startDate || dateRange.endDate) {
      filtered = filtered.filter(report => {
        const createdDate = new Date(report.created_at);
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
      filtered = filtered.filter(report => report.status === statusFilter);
    }

    // Report type filter
    if (reportTypeFilter !== 'all') {
      filtered = filtered.filter(report => report.report_type === reportTypeFilter);
    }

    // Search term filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(report => 
        report.title.toLowerCase().includes(term) ||
        report.investigation_id.toString().includes(term)
      );
    }

    setFilteredReports(filtered);
  }, [reports, dateRange, statusFilter, reportTypeFilter, searchTerm]);

  const fetchReports = async () => {
    try {
      setIsLoading(true);
      const data = await ExportService.listReports();
      setReports(data);
    } catch (error) {
      console.error('Failed to fetch reports:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchInvestigations = async () => {
    try {
      const data = await InvestigationService.getInvestigations();
      setInvestigations(data);
    } catch (error) {
      console.error('Failed to fetch investigations:', error);
    }
  };

  const generateReport = async () => {
    if (!selectedInvestigation) {
      alert('Please select an investigation');
      return;
    }

    try {
      setIsGenerating(true);
      const payload = {
        investigation_id: selectedInvestigation,
        report_type: selectedFormat
      };
      await ExportService.generateReport(payload);
      await fetchReports();
      setIsGenerating(false);
    } catch (error) {
      console.error('Failed to generate report:', error);
      setIsGenerating(false);
    }
  };

  const downloadReport = async (report: Report) => {
    if (!report.id) return;
    try {
      const blob = await ExportService.downloadReport(report.id);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${report.title}.${report.report_type}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Failed to download report:', error);
    }
  };

  const deleteReport = async (reportId: string) => {
    if (!window.confirm('Are you sure you want to delete this report?')) return;
    
    try {
      await ExportService.deleteReport(reportId);
      setReports(prev => prev.filter(report => report.id !== reportId));
      // Remove from expanded reports if it was expanded
      setExpandedReports(prev => {
        const newSet = new Set(prev);
        newSet.delete(reportId);
        return newSet;
      });
    } catch (error) {
      console.error('Failed to delete report:', error);
      alert('Failed to delete report');
    }
  };

  const deleteInvestigation = async (investigationId: string) => {
    if (!window.confirm('Are you sure you want to delete this investigation? This will also delete all associated reports.')) return;
    
    try {
      await InvestigationService.deleteInvestigation(investigationId);
      // Refresh both investigations and reports
      await fetchInvestigations();
      await fetchReports();
    } catch (error) {
      console.error('Failed to delete investigation:', error);
      alert('Failed to delete investigation');
    }
  };

  const toggleReportExpansion = async (report: Report) => {
    const isExpanded = expandedReports.has(report.id);
    
    if (isExpanded) {
      // Collapse
      setExpandedReports(prev => {
        const newSet = new Set(prev);
        newSet.delete(report.id);
        return newSet;
      });
      setReportContent(null);
    } else {
      // Expand and load content
      setExpandedReports(prev => new Set(Array.from(prev).concat(report.id)));
      
      if (report.status === 'completed') {
        try {
          setIsLoadingContent(true);
          const content = await ExportService.getReportContent(report.id);
          setReportContent(content);
        } catch (error) {
          console.error('Failed to load report content:', error);
          setReportContent({
            content_type: 'error',
            message: 'Failed to load report content'
          });
        } finally {
          setIsLoadingContent(false);
        }
      }
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'generating':
        return <ClockIcon className="h-5 w-5 text-yellow-500 animate-spin" />;
      case 'failed':
        return <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />;
      default:
        return <ClockIcon className="h-5 w-5 text-gray-400" />;
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
        return 'Completed';
      case 'generating':
        return 'Generating';
      case 'failed':
        return 'Failed';
      default:
        return 'Unknown';
    }
  };

  const clearFilters = () => {
    setDateRange({ startDate: '', endDate: '' });
    setStatusFilter('all');
    setReportTypeFilter('all');
    setSearchTerm('');
  };

  const getInvestigationTitle = (investigationId: string) => {
    const investigation = investigations.find(inv => inv.id.toString() === investigationId);
    return investigation?.title || `Investigation ${investigationId}`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Reports
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Generate and manage investigation reports
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
        </div>
      </div>

      {/* Filters Section */}
      {showFilters && (
        <div className="card">
          <div className="card-body">
            <h3 className="text-lg font-semibold mb-4">Filter Reports</h3>
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
                  <option value="generating">Generating</option>
                  <option value="completed">Completed</option>
                  <option value="failed">Failed</option>
                </select>
              </div>

              {/* Report Type Filter */}
              <div>
                <label className="block text-sm font-medium mb-1">Report Type</label>
                <select
                  value={reportTypeFilter}
                  onChange={(e) => setReportTypeFilter(e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="all">All Types</option>
                  <option value="pdf">PDF</option>
                  <option value="html">HTML</option>
                  <option value="json">JSON</option>
                  <option value="csv">CSV</option>
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
                    placeholder="Search reports..."
                    className="w-full pl-10 pr-4 p-2 border rounded-md"
                  />
                </div>
              </div>
            </div>

            <div className="flex justify-between items-center mt-4">
              <div className="text-sm text-gray-600 dark:text-gray-400">
                Showing {filteredReports.length} of {reports.length} reports
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

      {/* Generate Report Section */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
            Generate New Report
          </h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Investigation
              </label>
              <select
                value={selectedInvestigation}
                onChange={(e) => setSelectedInvestigation(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Select an investigation</option>
                {investigations.map((investigation) => (
                  <option key={investigation.id} value={investigation.id}>
                    {investigation.title}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Format
              </label>
              <select
                value={selectedFormat}
                onChange={(e) => setSelectedFormat(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="pdf">PDF</option>
                <option value="html">HTML</option>
                <option value="json">JSON</option>
                <option value="csv">CSV</option>
              </select>
            </div>

            <div className="flex items-end">
              <button
                onClick={generateReport}
                disabled={!selectedInvestigation || isGenerating}
                className="w-full flex items-center justify-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGenerating ? (
                  <>
                    <ClockIcon className="h-4 w-4 mr-2 animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <PlusIcon className="h-4 w-4 mr-2" />
                    Generate Report
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Reports List - Compact View */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
            Generated Reports
          </h3>
        </div>
        <div className="card-body">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <ClockIcon className="h-6 w-6 animate-spin text-primary-600" />
              <span className="ml-2 text-gray-600">Loading reports...</span>
            </div>
          ) : filteredReports.length === 0 ? (
            <div className="text-center py-8">
              <DocumentTextIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">No reports found matching your filters</p>
            </div>
          ) : (
            <div className="space-y-2">
              {filteredReports.map((report) => {
                const isExpanded = expandedReports.has(report.id);
                return (
                  <div key={report.id} className="border border-gray-200 dark:border-gray-700 rounded-lg">
                    {/* Report Header - Clickable */}
                    <div 
                      className="p-4 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                      onClick={() => toggleReportExpansion(report)}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <DocumentTextIcon className="h-5 w-5 text-primary-600" />
                          <div>
                            <h4 className="font-medium text-gray-900 dark:text-white">
                              {report.title}
                            </h4>
                            <p className="text-sm text-gray-500 dark:text-gray-400">
                              {getInvestigationTitle(report.investigation_id)} • {report.report_type.toUpperCase()}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-4">
                          <div className="flex items-center space-x-2">
                            {getStatusIcon(report.status)}
                            <span className="text-sm text-gray-600 dark:text-gray-400">
                              {getStatusText(report.status)}
                            </span>
                          </div>
                          <div className="flex items-center space-x-2">
                            {report.status === 'completed' && (
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  downloadReport(report);
                                }}
                                className="text-primary-600 hover:text-primary-700 p-1"
                                title="Download"
                              >
                                <ArrowDownTrayIcon className="h-4 w-4" />
                              </button>
                            )}
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                deleteReport(report.id);
                              }}
                              className="text-red-600 hover:text-red-700 p-1"
                              title="Delete Report"
                            >
                              <TrashIcon className="h-4 w-4" />
                            </button>
                            {isExpanded ? (
                              <ChevronUpIcon className="h-4 w-4 text-gray-500" />
                            ) : (
                              <ChevronDownIcon className="h-4 w-4 text-gray-500" />
                            )}
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Expanded Content */}
                    {isExpanded && (
                      <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-900">
                        {isLoadingContent ? (
                          <div className="flex items-center justify-center py-8">
                            <ClockIcon className="h-6 w-6 animate-spin text-primary-600" />
                            <span className="ml-2 text-gray-600 dark:text-gray-400">Loading report content...</span>
                          </div>
                        ) : reportContent ? (
                          <div>
                            {reportContent.content_type === 'pdf' ? (
                              <div className="text-center py-8">
                                <DocumentTextIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                                <p className="text-gray-600 dark:text-gray-400 mb-4">
                                  {reportContent.message || 'PDF content cannot be displayed directly.'}
                                </p>
                                <button
                                  onClick={() => downloadReport(report)}
                                  className="btn-primary"
                                >
                                  <ArrowDownTrayIcon className="h-4 w-4 mr-2" />
                                  Download PDF
                                </button>
                              </div>
                            ) : (
                              <div>
                                <div className="mb-4 flex items-center justify-between">
                                  <span className="text-sm text-gray-500 dark:text-gray-400">
                                    File size: {reportContent.file_size} bytes
                                  </span>
                                  <button
                                    onClick={() => downloadReport(report)}
                                    className="text-primary-600 hover:text-primary-700 text-sm"
                                  >
                                    <ArrowDownTrayIcon className="h-4 w-4 inline mr-1" />
                                    Download
                                  </button>
                                </div>
                                
                                {reportContent.content_type === 'html' ? (
                                  <div 
                                    className="border border-gray-200 dark:border-gray-700 rounded-md p-4 bg-white dark:bg-gray-800 overflow-auto max-h-96"
                                    dangerouslySetInnerHTML={{ __html: reportContent.content || '' }}
                                  />
                                ) : (
                                  <pre className="border border-gray-200 dark:border-gray-700 rounded-md p-4 bg-white dark:bg-gray-800 overflow-auto max-h-96 text-sm">
                                    {reportContent.content || 'No content available'}
                                  </pre>
                                )}
                              </div>
                            )}
                          </div>
                        ) : (
                          <div className="text-center py-8">
                            <ExclamationTriangleIcon className="h-12 w-12 text-red-400 mx-auto mb-4" />
                            <p className="text-gray-600 dark:text-gray-400">Failed to load report content</p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Investigations Management */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
            Investigations Management
          </h3>
        </div>
        <div className="card-body">
          {investigations.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500 dark:text-gray-400">No investigations found</p>
            </div>
          ) : (
            <div className="space-y-2">
              {investigations.map((investigation) => (
                <div key={investigation.id} className="flex items-center justify-between p-3 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-white">
                      {investigation.title}
                    </h4>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {investigation.target_type}: {investigation.target_value} • Status: {investigation.status}
                    </p>
                  </div>
                  <button
                    onClick={() => deleteInvestigation(investigation.id.toString())}
                    className="text-red-600 hover:text-red-700 p-2"
                    title="Delete Investigation"
                  >
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Reports; 