import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Chip,
  LinearProgress,
  Alert,
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
  Download as DownloadIcon,
  Visibility as ViewIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import toast from 'react-hot-toast';

// Mock data for reports
const mockReports = [
  {
    id: 1,
    title: 'Domain Analysis Report - example.com',
    type: 'domain_analysis',
    target: 'example.com',
    created_at: '2024-01-15T10:30:00Z',
    status: 'completed',
    file_size: '2.5 MB',
    format: 'PDF',
  },
  {
    id: 2,
    title: 'Social Media Scan Report - username123',
    type: 'social_media_scan',
    target: 'username123',
    created_at: '2024-01-14T15:45:00Z',
    status: 'completed',
    file_size: '1.8 MB',
    format: 'PDF',
  },
  {
    id: 3,
    title: 'Threat Assessment Report - suspicious.org',
    type: 'threat_assessment',
    target: 'suspicious.org',
    created_at: '2024-01-13T09:20:00Z',
    status: 'completed',
    file_size: '3.2 MB',
    format: 'PDF',
  },
  {
    id: 4,
    title: 'Comprehensive Investigation Report - target123',
    type: 'comprehensive',
    target: 'target123',
    created_at: '2024-01-12T14:15:00Z',
    status: 'processing',
    file_size: '0 MB',
    format: 'PDF',
  },
];

export const Reports: React.FC = () => {
  const [selectedReport, setSelectedReport] = useState<any>(null);

  // Mock query for reports
  const { data: reports, isLoading, error } = useQuery({
    queryKey: ['reports'],
    queryFn: () => Promise.resolve(mockReports),
  });

  const handleDownload = (report: any) => {
    toast.success(`Downloading ${report.title}`);
    // Mock download functionality
    const link = document.createElement('a');
    link.href = '#';
    link.download = `${report.title}.${report.format.toLowerCase()}`;
    link.click();
  };

  const handleView = (report: any) => {
    setSelectedReport(report);
    toast.success(`Opening ${report.title}`);
  };

  const getReportTypeColor = (type: string) => {
    switch (type) {
      case 'domain_analysis':
        return 'primary';
      case 'social_media_scan':
        return 'secondary';
      case 'threat_assessment':
        return 'error';
      case 'comprehensive':
        return 'info';
      default:
        return 'default';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'processing':
        return 'warning';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  if (error) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 2 }}>
          Failed to load reports: {error instanceof Error ? error.message : 'Unknown error'}
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" fontWeight={600}>
          Reports
        </Typography>
        <Button
          variant="contained"
          startIcon={<RefreshIcon />}
          onClick={() => window.location.reload()}
        >
          Refresh
        </Button>
      </Box>

      {/* Statistics Cards */}
      <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 3, mb: 3 }}>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Total Reports
            </Typography>
            <Typography variant="h4">
              {reports?.length || 0}
            </Typography>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Completed
            </Typography>
            <Typography variant="h4" color="success.main">
              {reports?.filter((r: any) => r.status === 'completed').length || 0}
            </Typography>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Processing
            </Typography>
            <Typography variant="h4" color="warning.main">
              {reports?.filter((r: any) => r.status === 'processing').length || 0}
            </Typography>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Total Size
            </Typography>
            <Typography variant="h4" color="info.main">
              {reports?.reduce((acc: number, r: any) => acc + parseFloat(r.file_size), 0).toFixed(1) || 0} MB
            </Typography>
          </CardContent>
        </Card>
      </Box>

      {/* Reports Table */}
      {isLoading ? (
        <LinearProgress />
      ) : (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Generated Reports
            </Typography>
            <TableContainer component={Paper} variant="outlined">
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Title</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Target</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Created</TableCell>
                    <TableCell>Size</TableCell>
                    <TableCell>Format</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {reports?.map((report: any) => (
                    <TableRow key={report.id}>
                      <TableCell>
                        <Typography variant="subtitle2" fontWeight={600}>
                          {report.title}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={report.type.replace(/_/g, ' ').toUpperCase()}
                          color={getReportTypeColor(report.type) as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">
                          {report.target}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={report.status}
                          color={getStatusColor(report.status) as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">
                          {new Date(report.created_at).toLocaleDateString()}
                        </Typography>
                        <Typography variant="caption" color="textSecondary">
                          {new Date(report.created_at).toLocaleTimeString()}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">
                          {report.file_size}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={report.format}
                          variant="outlined"
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', gap: 0.5 }}>
                          <IconButton
                            size="small"
                            onClick={() => handleView(report)}
                            disabled={report.status !== 'completed'}
                          >
                            <ViewIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleDownload(report)}
                            disabled={report.status !== 'completed'}
                          >
                            <DownloadIcon />
                          </IconButton>
                        </Box>
                      </TableCell>
                    </TableRow>
                  ))}
                  {(!reports || reports.length === 0) && (
                    <TableRow>
                      <TableCell colSpan={8} align="center">
                        <Typography variant="body2" color="textSecondary">
                          No reports found
                        </Typography>
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      )}

      {/* Report Preview Modal would go here */}
      {selectedReport && (
        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Report Preview: {selectedReport.title}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              This is a preview of the report. Click the download button to get the full report.
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
}; 