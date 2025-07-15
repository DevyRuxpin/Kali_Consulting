import { useState, useCallback, useMemo } from 'react';
import { toast } from 'react-hot-toast';
import { detectAnomalies, analyzePatterns, processIntelligence, generateIntelligenceReport } from '../services/api';
import { handleApiError } from '../utils/errorHandler';
import { useMutation } from '@tanstack/react-query';

export interface AnalyticsData {
  id: string;
  timestamp: string;
  value: number;
  category: string;
  metadata?: Record<string, any>;
}

export interface AnomalyResult {
  id: string;
  timestamp: string;
  score: number;
  type: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
}

export interface PatternResult {
  id: string;
  pattern_type: string;
  description: string;
  confidence: number;
  frequency: number;
  entities: string[];
}

export interface IntelligenceResult {
  insights: string[];
  correlations: Array<{ source: string; target: string; strength: number }>;
  recommendations: string[];
  risk_score: number;
}

export interface AnalyticsOptions {
  timeRange?: {
    start: string;
    end: string;
  };
  categories?: string[];
  threshold?: number;
  includeMetadata?: boolean;
}

export const useAnalytics = (options: AnalyticsOptions = {}) => {
  const [selectedData, setSelectedData] = useState<AnalyticsData[]>([]);
  const [analysisResults, setAnalysisResults] = useState<{
    anomalies: AnomalyResult[];
    patterns: PatternResult[];
    intelligence: IntelligenceResult | null;
  }>({
    anomalies: [],
    patterns: [],
    intelligence: null,
  });

  // Anomaly detection mutation
  const anomalyMutation = useMutation({
    mutationFn: async (data: AnalyticsData[]) => {
      const response = await detectAnomalies({
        data: data.map(item => ({
          timestamp: item.timestamp,
          value: item.value,
          category: item.category,
          metadata: item.metadata,
        })),
        threshold: options.threshold || 0.5,
      });
      return response;
    },
    onSuccess: (response: any) => {
      if (response.status === 'success') {
        setAnalysisResults(prev => ({
          ...prev,
          anomalies: response.data?.anomalies || [],
        }));
        toast.success('Anomaly detection completed');
      }
    },
    onError: (error: any) => {
      const errorInfo = handleApiError(error, { component: 'useAnalytics', action: 'anomaly_detection' });
      toast.error(errorInfo.message);
    },
  });

  // Pattern analysis mutation
  const patternMutation = useMutation({
    mutationFn: async (data: AnalyticsData[]) => {
      const response = await analyzePatterns({
        data: data.map(item => ({
          timestamp: item.timestamp,
          value: item.value,
          category: item.category,
          metadata: item.metadata,
        })),
        pattern_types: ['temporal', 'behavioral', 'correlation'],
      });
      return response;
    },
    onSuccess: (response: any) => {
      if (response.status === 'success') {
        setAnalysisResults(prev => ({
          ...prev,
          patterns: response.data?.patterns || [],
        }));
        toast.success('Pattern analysis completed');
      }
    },
    onError: (error: any) => {
      const errorInfo = handleApiError(error, { component: 'useAnalytics', action: 'pattern_analysis' });
      toast.error(errorInfo.message);
    },
  });

  // Intelligence processing mutation
  const intelligenceMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await processIntelligence(data);
      return response;
    },
    onSuccess: (response: any) => {
      if (response.status === 'success') {
        setAnalysisResults(prev => ({
          ...prev,
          intelligence: response.data || null,
        }));
        toast.success('Intelligence analysis completed');
      }
    },
    onError: (error: any) => {
      const errorInfo = handleApiError(error, { component: 'useAnalytics', action: 'intelligence_processing' });
      toast.error(errorInfo.message);
    },
  });

  // Report generation mutation
  const reportMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await generateIntelligenceReport(data);
      return response;
    },
    onSuccess: (response: any) => {
      if (response.status === 'success') {
        toast.success('Report generated successfully');
      }
    },
    onError: (error: any) => {
      const errorInfo = handleApiError(error, { component: 'useAnalytics', action: 'report_generation' });
      toast.error(errorInfo.message);
    },
  });

  // Detect anomalies
  const detectAnomaliesHandler = useCallback(async (data: AnalyticsData[]) => {
    setSelectedData(data);
    await anomalyMutation.mutateAsync(data);
  }, [anomalyMutation]);

  // Analyze patterns
  const analyzePatternsHandler = useCallback(async (data: AnalyticsData[]) => {
    setSelectedData(data);
    await patternMutation.mutateAsync(data);
  }, [patternMutation]);

  // Process intelligence
  const processIntelligenceHandler = useCallback(async (data: any) => {
    await intelligenceMutation.mutateAsync(data);
  }, [intelligenceMutation]);

  // Generate report
  const generateReportHandler = useCallback(async (data: any) => {
    await reportMutation.mutateAsync(data);
  }, [reportMutation]);

  // Computed analytics
  const analytics = useMemo(() => {
    if (selectedData.length === 0) return null;

    const values = selectedData.map(d => d.value);
    const categories = [...new Set(selectedData.map(d => d.category))];
    
    const stats = {
      count: selectedData.length,
      sum: values.reduce((a, b) => a + b, 0),
      mean: values.reduce((a, b) => a + b, 0) / values.length,
      min: Math.min(...values),
      max: Math.max(...values),
      categories: categories.length,
    };

    const variance = values.reduce((acc, val) => acc + Math.pow(val - stats.mean, 2), 0) / values.length;
    (stats as any)['std'] = Math.sqrt(variance);

    return stats;
  }, [selectedData]);

  // Filter data by time range
  const filterByTimeRange = useCallback((data: AnalyticsData[], start: string, end: string) => {
    return data.filter(item => {
      const timestamp = new Date(item.timestamp);
      const startDate = new Date(start);
      const endDate = new Date(end);
      return timestamp >= startDate && timestamp <= endDate;
    });
  }, []);

  // Filter data by category
  const filterByCategory = useCallback((data: AnalyticsData[], categories: string[]) => {
    return data.filter(item => categories.includes(item.category));
  }, []);

  // Group data by category
  const groupByCategory = useCallback((data: AnalyticsData[]) => {
    return data.reduce((acc, item) => {
      if (!acc[item.category]) {
        acc[item.category] = [];
      }
      acc[item.category].push(item);
      return acc;
    }, {} as Record<string, AnalyticsData[]>);
  }, []);

  // Calculate trends
  const calculateTrends = useCallback((data: AnalyticsData[]) => {
    if (data.length < 2) return null;

    const sortedData = data.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
    const values = sortedData.map(d => d.value);
    
    // Simple linear regression
    const n = values.length;
    const x = Array.from({ length: n }, (_, i) => i);
    const sumX = x.reduce((a, b) => a + b, 0);
    const sumY = values.reduce((a, b) => a + b, 0);
    const sumXY = x.reduce((acc, xi, i) => acc + xi * values[i], 0);
    const sumXX = x.reduce((acc, xi) => acc + xi * xi, 0);
    
    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;
    
    return {
      slope,
      intercept,
      trend: slope > 0 ? 'increasing' : slope < 0 ? 'decreasing' : 'stable',
      strength: Math.abs(slope),
    };
  }, []);

  return {
    // State
    selectedData,
    analysisResults,
    analytics,
    
    // Actions
    detectAnomalies: detectAnomaliesHandler,
    analyzePatterns: analyzePatternsHandler,
    processIntelligence: processIntelligenceHandler,
    generateReport: generateReportHandler,
    
    // Utilities
    filterByTimeRange,
    filterByCategory,
    groupByCategory,
    calculateTrends,
    
    // Mutation states
    isDetectingAnomalies: anomalyMutation.isPending,
    isAnalyzingPatterns: patternMutation.isPending,
    isProcessingIntelligence: intelligenceMutation.isPending,
    isGeneratingReport: reportMutation.isPending,
  };
}; 