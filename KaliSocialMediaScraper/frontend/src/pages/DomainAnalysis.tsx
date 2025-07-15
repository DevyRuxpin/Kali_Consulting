import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Chip,
  LinearProgress,
  Alert,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  Search as SearchIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import { useMutation } from '@tanstack/react-query';
import { analyzeDomain } from '../services/api';
import toast from 'react-hot-toast';

export const DomainAnalysis: React.FC = () => {
  const [domain, setDomain] = useState('');

  // Domain analysis mutation
  const analysisMutation = useMutation({
    mutationFn: (domain: string) => analyzeDomain(domain),
    onSuccess: () => {
      toast.success('Domain analysis completed successfully');
    },
    onError: (error) => {
      toast.error('Failed to analyze domain');
      console.error('Domain analysis error:', error);
    },
  });

  const handleAnalyze = () => {
    if (!domain.trim()) {
      toast.error('Please enter a domain');
      return;
    }
    analysisMutation.mutate(domain.trim());
  };

  const handleExport = () => {
    if (analysisMutation.data?.data) {
      const dataStr = JSON.stringify(analysisMutation.data.data, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `domain-analysis-${domain}-${new Date().toISOString().split('T')[0]}.json`;
      link.click();
      URL.revokeObjectURL(url);
    }
  };

  const analysisData = analysisMutation.data?.data;

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" fontWeight={600}>
          Domain Analysis
        </Typography>
      </Box>

      {/* Input Form */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Analyze Domain
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-end' }}>
            <TextField
              fullWidth
              label="Domain"
              placeholder="example.com"
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              disabled={analysisMutation.isPending}
            />
            <Button
              variant="contained"
              startIcon={<SearchIcon />}
              onClick={handleAnalyze}
              disabled={analysisMutation.isPending || !domain.trim()}
            >
              {analysisMutation.isPending ? 'Analyzing...' : 'Analyze'}
            </Button>
          </Box>
        </CardContent>
      </Card>

      {/* Loading State */}
      {analysisMutation.isPending && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Analyzing Domain
            </Typography>
            <LinearProgress />
            <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
              Gathering domain information, DNS records, and threat indicators...
            </Typography>
          </CardContent>
        </Card>
      )}

      {/* Results */}
      {analysisData && (
        <Box>
          {/* Export Button */}
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
            <Button
              variant="outlined"
              startIcon={<DownloadIcon />}
              onClick={handleExport}
            >
              Export Report
            </Button>
          </Box>

          {/* Domain Overview */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Domain Overview
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Domain
                  </Typography>
                  <Typography variant="body1" fontWeight={600}>
                    {analysisData.domain}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Risk Score
                  </Typography>
                  <Chip
                    label={`${analysisData.risk_score}/10`}
                    color={analysisData.risk_score > 7 ? 'error' : analysisData.risk_score > 4 ? 'warning' : 'success'}
                  />
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    IP Addresses
                  </Typography>
                  <Typography variant="body1">
                    {analysisData.ip_addresses?.length || 0} found
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Subdomains
                  </Typography>
                  <Typography variant="body1">
                    {analysisData.subdomains?.length || 0} found
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* IP Addresses */}
          {analysisData.ip_addresses && analysisData.ip_addresses.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  IP Addresses
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {analysisData.ip_addresses.map((ip: string, index: number) => (
                    <Chip key={index} label={ip} variant="outlined" />
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}

          {/* Subdomains */}
          {analysisData.subdomains && analysisData.subdomains.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Subdomains
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {analysisData.subdomains.map((subdomain: string, index: number) => (
                    <Chip key={index} label={subdomain} variant="outlined" />
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}

          {/* Technologies */}
          {analysisData.technologies && analysisData.technologies.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Technologies Detected
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {analysisData.technologies.map((tech: string, index: number) => (
                    <Chip key={index} label={tech} variant="outlined" />
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}

          {/* Threat Indicators */}
          {analysisData.threat_indicators && analysisData.threat_indicators.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom color="error">
                  Threat Indicators
                </Typography>
                <List>
                  {analysisData.threat_indicators.map((indicator: string, index: number) => (
                    <React.Fragment key={index}>
                      <ListItem>
                        <ListItemText
                          primary={indicator}
                          primaryTypographyProps={{ color: 'error' }}
                        />
                      </ListItem>
                      {index < analysisData.threat_indicators.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              </CardContent>
            </Card>
          )}

          {/* DNS Records */}
          {analysisData.dns_records && Object.keys(analysisData.dns_records).length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  DNS Records
                </Typography>
                {Object.entries(analysisData.dns_records).map(([type, records]) => (
                  <Box key={type} sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                      {type}
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {Array.isArray(records) && records.map((record: string, index: number) => (
                        <Chip key={index} label={record} size="small" variant="outlined" />
                      ))}
                    </Box>
                  </Box>
                ))}
              </CardContent>
            </Card>
          )}

          {/* WHOIS Data */}
          {analysisData.whois_data && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  WHOIS Information
                </Typography>
                <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
                  {Object.entries(analysisData.whois_data).map(([key, value]) => (
                    <Box key={key}>
                      <Typography variant="subtitle2" color="textSecondary">
                        {key.replace(/_/g, ' ').toUpperCase()}
                      </Typography>
                      <Typography variant="body2">
                        {Array.isArray(value) ? value.join(', ') : String(value)}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}

          {/* SSL Certificate */}
          {analysisData.ssl_certificate && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  SSL Certificate
                </Typography>
                <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
                  {Object.entries(analysisData.ssl_certificate).map(([key, value]) => (
                    <Box key={key}>
                      <Typography variant="subtitle2" color="textSecondary">
                        {key.replace(/_/g, ' ').toUpperCase()}
                      </Typography>
                      <Typography variant="body2">
                        {String(value)}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}
        </Box>
      )}

      {/* Error State */}
      {analysisMutation.isError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Failed to analyze domain. Please check the domain name and try again.
        </Alert>
      )}
    </Box>
  );
}; 