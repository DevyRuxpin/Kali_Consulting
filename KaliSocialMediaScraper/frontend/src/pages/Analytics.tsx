import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Chip,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Security as SecurityIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Download as DownloadIcon,
  Refresh as RefreshIcon,
  Visibility as ViewIcon,
  Assessment as AssessmentIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { getAnalytics } from '../services/api';
import toast from 'react-hot-toast';

export const Analytics: React.FC = () => {
  // Analytics query
  const { data: analytics, isLoading, error } = useQuery({
    queryKey: ['analytics'],
    queryFn: getAnalytics,
  });

  const handleExport = () => {
    toast.success('Exporting analytics data...');
    // Mock export functionality
    const link = document.createElement('a');
    link.href = '#';
    link.download = `analytics-report-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
  };

  if (error) {
    return (
      <Box>
        <Typography variant="h4" component="h1" fontWeight={600} gutterBottom>
          Analytics
        </Typography>
        <Card>
          <CardContent>
            <Typography color="error">
              Failed to load analytics: {error instanceof Error ? error.message : 'Unknown error'}
            </Typography>
          </CardContent>
        </Card>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" fontWeight={600}>
          Analytics
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={() => window.location.reload()}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<DownloadIcon />}
            onClick={handleExport}
          >
            Export
          </Button>
        </Box>
      </Box>

      {/* Loading State */}
      {isLoading && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <LinearProgress />
            <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
              Loading analytics data...
            </Typography>
          </CardContent>
        </Card>
      )}

      {/* Analytics Content */}
      {analytics && (
        <Box>
          {/* Key Metrics */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Key Metrics
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 3 }}>
                <Box sx={{ textAlign: 'center' }}>
                  <SecurityIcon color="primary" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h4" fontWeight={600}>
                    {analytics.data?.total_investigations || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Total Investigations
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <TrendingUpIcon color="success" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h4" fontWeight={600} color="success.main">
                    {analytics.data?.completed_investigations || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Completed
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <WarningIcon color="warning" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h4" fontWeight={600} color="warning.main">
                    {analytics.data?.high_threat_findings || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    High Threat Findings
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Threat Analysis */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Threat Analysis Overview
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 3 }}>
                <Box sx={{ textAlign: 'center' }}>
                  <ErrorIcon color="error" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h4" fontWeight={600} color="error.main">
                    {analytics.data?.critical_threats || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Critical Threats
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <WarningIcon color="warning" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h4" fontWeight={600} color="warning.main">
                    {analytics.data?.high_threats || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    High Threats
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <AssessmentIcon color="info" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h4" fontWeight={600} color="info.main">
                    {analytics.data?.medium_threats || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Medium Threats
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <CheckCircleIcon color="success" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h4" fontWeight={600} color="success.main">
                    {analytics.data?.low_threats || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Low Threats
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Platform Statistics */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Platform Statistics
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 3 }}>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                    Social Media Scans
                  </Typography>
                  <Typography variant="h4" color="primary">
                    {analytics.data?.social_media_scans || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Total profiles analyzed
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                    Domain Analysis
                  </Typography>
                  <Typography variant="h4" color="primary">
                    {analytics.data?.domain_analysis || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Domains investigated
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Recent Activity */}
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Type</TableCell>
                      <TableCell>Target</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Threat Level</TableCell>
                      <TableCell>Date</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {(analytics.data?.recent_activity || []).map((activity: any, index: number) => (
                      <TableRow key={index}>
                        <TableCell>
                          <Chip
                            label={activity.type}
                            size="small"
                            color={
                              activity.type === 'domain_analysis'
                                ? 'primary'
                                : activity.type === 'social_media_scan'
                                ? 'secondary'
                                : 'default'
                            }
                          />
                        </TableCell>
                        <TableCell>{activity.target}</TableCell>
                        <TableCell>
                          <Chip
                            label={activity.status}
                            size="small"
                            color={
                              activity.status === 'completed'
                                ? 'success'
                                : activity.status === 'processing'
                                ? 'warning'
                                : 'error'
                            }
                          />
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={activity.threat_level}
                            size="small"
                            color={
                              activity.threat_level === 'critical'
                                ? 'error'
                                : activity.threat_level === 'high'
                                ? 'warning'
                                : activity.threat_level === 'medium'
                                ? 'info'
                                : 'success'
                            }
                          />
                        </TableCell>
                        <TableCell>
                          {new Date(activity.created_at).toLocaleDateString()}
                        </TableCell>
                        <TableCell>
                          <IconButton size="small">
                            <ViewIcon />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Box>
      )}
    </Box>
  );
}; 