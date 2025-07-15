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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  Search as SearchIcon,
  Download as DownloadIcon,
  Security as SecurityIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { useMutation } from '@tanstack/react-query';
import { analyzeThreat } from '../services/api';
import toast from 'react-hot-toast';
import { useTheme } from '@mui/material/styles';

const ENTITY_TYPES = [
  'domain',
  'email',
  'username',
  'phone',
  'ip_address',
  'organization',
  'person',
  'cryptocurrency_address',
  'social_media_profile',
];

export const ThreatAnalysis: React.FC = () => {
  const [entity, setEntity] = useState('');
  const [entityType, setEntityType] = useState('domain');

  // Threat analysis mutation
  const analysisMutation = useMutation({
    mutationFn: (data: { entity: string; entityType: string }) => analyzeThreat({
      target: data.entity,
      target_type: data.entityType,
      analysis_depth: 'comprehensive',
    }),
    onSuccess: () => {
      toast.success('Threat analysis completed successfully');
    },
    onError: (error) => {
      toast.error('Failed to analyze threat');
      console.error('Threat analysis error:', error);
    },
  });

  const handleAnalyze = () => {
    if (!entity.trim()) {
      toast.error('Please enter an entity to analyze');
      return;
    }
    analysisMutation.mutate({
      entity: entity.trim(),
      entityType,
    });
  };

  const handleExport = () => {
    if (analysisMutation.data?.data) {
      const dataStr = JSON.stringify(analysisMutation.data.data, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `threat-analysis-${entity}-${new Date().toISOString().split('T')[0]}.json`;
      link.click();
      URL.revokeObjectURL(url);
    }
  };

  const analysisData = analysisMutation.data?.data;

  const getThreatLevelColor = (level: string) => {
    switch (level) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  const getThreatLevelIcon = (level: string) => {
    switch (level) {
      case 'critical':
      case 'high':
        return <WarningIcon color="error" />;
      case 'medium':
        return <WarningIcon color="warning" />;
      case 'low':
        return <CheckCircleIcon color="success" />;
      default:
        return <SecurityIcon />;
    }
  };

  const theme = useTheme();

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" fontWeight={600}>
          Threat Analysis
        </Typography>
      </Box>

      {/* Input Form */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Analyze Threat Level
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-end', mb: 3 }}>
            <FormControl sx={{ minWidth: 200 }}>
              <InputLabel>Entity Type</InputLabel>
              <Select
                value={entityType}
                label="Entity Type"
                onChange={(e) => setEntityType(e.target.value)}
                disabled={analysisMutation.isPending}
              >
                {ENTITY_TYPES.map((type) => (
                  <MenuItem key={type} value={type}>
                    {type.replace(/_/g, ' ').toUpperCase()}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Entity"
              placeholder={`Enter ${entityType.replace(/_/g, ' ')}`}
              value={entity}
              onChange={(e) => setEntity(e.target.value)}
              disabled={analysisMutation.isPending}
            />
            <Button
              variant="contained"
              startIcon={<SearchIcon />}
              onClick={handleAnalyze}
              disabled={analysisMutation.isPending || !entity.trim()}
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
              Analyzing Threat
            </Typography>
            <LinearProgress />
            <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
              Gathering threat intelligence, analyzing patterns, and assessing risk factors...
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

          {/* Threat Overview */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Threat Assessment Overview
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Target
                  </Typography>
                  <Typography variant="body1" fontWeight={600}>
                    {analysisData.target}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Threat Level
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    {getThreatLevelIcon(analysisData.threat_level)}
                    <Chip
                      label={analysisData.threat_level.toUpperCase()}
                      color={getThreatLevelColor(analysisData.threat_level) as any}
                    />
                  </Box>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Threat Score
                  </Typography>
                  <Typography variant="h4" color={getThreatLevelColor(analysisData.threat_level)}>
                    {analysisData.threat_score}/10
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Confidence
                  </Typography>
                  <Typography variant="h6">
                    {Math.round(analysisData.confidence * 100)}%
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Threat Indicators */}
          {analysisData.indicators && analysisData.indicators.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom color="error">
                  Threat Indicators
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {analysisData.indicators.map((indicator: string, index: number) => (
                    <Chip
                      key={index}
                      label={indicator}
                      color="error"
                      variant="outlined"
                      icon={<WarningIcon />}
                    />
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}

          {/* Risk Factors */}
          {analysisData.risk_factors && analysisData.risk_factors.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom color="warning">
                  Risk Factors
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  {analysisData.risk_factors.map((factor: string, index: number) => (
                    <Box
                      key={index}
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 1,
                        p: 1,
                        border: `1px solid ${theme.palette.warning.light}`,
                        borderRadius: 1,
                        backgroundColor: theme.palette.warning.light + '20',
                      }}
                    >
                      <WarningIcon color="warning" fontSize="small" />
                      <Typography variant="body2">{factor}</Typography>
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}

          {/* Recommendations */}
          {analysisData.recommendations && analysisData.recommendations.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom color="primary">
                  Recommendations
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {analysisData.recommendations.map((recommendation: string, index: number) => (
                    <Box
                      key={index}
                      sx={{
                        display: 'flex',
                        alignItems: 'flex-start',
                        gap: 1,
                        p: 2,
                        border: `1px solid ${theme.palette.primary.light}`,
                        borderRadius: 1,
                        backgroundColor: theme.palette.primary.light + '20',
                      }}
                    >
                      <CheckCircleIcon color="primary" fontSize="small" sx={{ mt: 0.25 }} />
                      <Typography variant="body2">{recommendation}</Typography>
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}

          {/* Detailed Analysis */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Analysis Details
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 2 }}>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                    Analysis Timestamp
                  </Typography>
                  <Typography variant="body2">
                    {new Date(analysisData.created_at).toLocaleString()}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                    Analysis Method
                  </Typography>
                  <Typography variant="body2">
                    Comprehensive Threat Intelligence Analysis
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                    Data Sources
                  </Typography>
                  <Typography variant="body2">
                    Multiple threat intelligence feeds, dark web monitoring, and behavioral analysis
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Box>
      )}

      {/* Error State */}
      {analysisMutation.isError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Failed to analyze threat. Please check the entity and try again.
        </Alert>
      )}
    </Box>
  );
}; 