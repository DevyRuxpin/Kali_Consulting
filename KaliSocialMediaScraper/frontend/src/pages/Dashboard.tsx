import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  Alert,
  Button,
  useTheme,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Security as SecurityIcon,
  Search as SearchIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { getDashboardStats } from '../services/api';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { TroubleshootingGuide } from '../components/TroubleshootingGuide';

export const Dashboard: React.FC = () => {
  const theme = useTheme();

  // Fetch dashboard stats
  const { data: stats, isLoading, error, refetch } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => getDashboardStats(),
    retry: 1,
    refetchOnWindowFocus: false,
  });

  const getSystemHealthIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircleIcon />;
      case 'warning':
        return <WarningIcon />;
      case 'critical':
        return <ErrorIcon />;
      default:
        return <WarningIcon />;
    }
  };

  const handleRefresh = () => {
    refetch();
  };

  // Show loading state
  if (isLoading) {
    return <LoadingSpinner message="Loading dashboard data..." />;
  }

  // Show error state
  if (error) {
    return (
      <Box>
        <Alert 
          severity="error" 
          sx={{ mb: 2 }}
          action={
            <Button color="inherit" size="small" onClick={handleRefresh}>
              Retry
            </Button>
          }
        >
          Failed to load dashboard data: {error instanceof Error ? error.message : 'Unknown error'}
        </Alert>
        
        {/* Show offline mode content */}
        <Box>
          <Typography variant="h4" component="h1" fontWeight={600} gutterBottom>
            Dashboard
          </Typography>
          <Alert severity="info" sx={{ mb: 3 }}>
            Running in offline mode. Some features may be limited.
          </Alert>
          
          {/* Offline statistics */}
          <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 3, mb: 3 }}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <SearchIcon sx={{ color: theme.palette.primary.main, mr: 1 }} />
                  <Typography variant="h6">Total Investigations</Typography>
                </Box>
                <Typography variant="h3" color="primary" fontWeight={600}>
                  0
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  0 currently active
                </Typography>
              </CardContent>
            </Card>

            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <SecurityIcon sx={{ color: theme.palette.warning.main, mr: 1 }} />
                  <Typography variant="h6">Threat Alerts</Typography>
                </Box>
                <Typography variant="h3" color="warning.main" fontWeight={600}>
                  0
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  No threats detected
                </Typography>
              </CardContent>
            </Card>

            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <TrendingUpIcon sx={{ color: theme.palette.success.main, mr: 1 }} />
                  <Typography variant="h6">Success Rate</Typography>
                </Box>
                <Typography variant="h3" color="success.main" fontWeight={600}>
                  0
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Investigations completed successfully
                </Typography>
              </CardContent>
            </Card>

            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <SearchIcon sx={{ color: theme.palette.info.main, mr: 1 }} />
                  <Typography variant="h6">Data Sources</Typography>
                </Box>
                <Typography variant="h3" color="info.main" fontWeight={600}>
                  0
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Profiles scraped
                </Typography>
              </CardContent>
            </Card>
          </Box>

          {/* Troubleshooting Guide */}
          <TroubleshootingGuide onRefresh={handleRefresh} />
        </Box>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" fontWeight={600}>
          Dashboard
        </Typography>
        <Button 
          variant="outlined" 
          startIcon={<RefreshIcon />}
          onClick={handleRefresh}
        >
          Refresh
        </Button>
      </Box>

      {/* Content */}
      <Box>
        {/* System Health Overview */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              System Health
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Chip
                icon={getSystemHealthIcon('healthy')}
                label="API Server"
                color="success"
                variant="outlined"
              />
              <Chip
                icon={getSystemHealthIcon('healthy')}
                label="Database"
                color="success"
                variant="outlined"
              />
              <Chip
                icon={getSystemHealthIcon('warning')}
                label="Scraping Services"
                color="warning"
                variant="outlined"
              />
              <Chip
                icon={getSystemHealthIcon('healthy')}
                label="Real-time Data"
                color="success"
                variant="outlined"
              />
            </Box>
          </CardContent>
        </Card>

        {/* Key Statistics */}
        <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 3, mb: 3 }}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SearchIcon sx={{ color: theme.palette.primary.main, mr: 1 }} />
                <Typography variant="h6">Total Investigations</Typography>
              </Box>
              <Typography variant="h3" color="primary" fontWeight={600}>
                {stats?.data?.total_investigations || 0}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {stats?.data?.active_investigations || 0} currently active
              </Typography>
            </CardContent>
          </Card>

          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SecurityIcon sx={{ color: theme.palette.warning.main, mr: 1 }} />
                <Typography variant="h6">Threat Alerts</Typography>
              </Box>
              <Typography variant="h3" color="warning.main" fontWeight={600}>
                {stats?.data?.high_priority_threats || 0}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                High threat level detected
              </Typography>
            </CardContent>
          </Card>

          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <TrendingUpIcon sx={{ color: theme.palette.success.main, mr: 1 }} />
                <Typography variant="h6">Success Rate</Typography>
              </Box>
              <Typography variant="h3" color="success.main" fontWeight={600}>
                {stats?.data?.completed_investigations || 0}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Investigations completed successfully
              </Typography>
            </CardContent>
          </Card>

          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SearchIcon sx={{ color: theme.palette.info.main, mr: 1 }} />
                <Typography variant="h6">Data Sources</Typography>
              </Box>
              <Typography variant="h3" color="info.main" fontWeight={600}>
                {stats?.data?.total_profiles_scraped || 0}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Profiles scraped
              </Typography>
            </CardContent>
          </Card>
        </Box>

        {/* Recent Activity */}
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Recent Activity
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {stats?.data?.recent_investigations?.map((activity: any, index: number) => (
                <Box
                  key={index}
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    p: 2,
                    border: `1px solid ${theme.palette.divider}`,
                    borderRadius: 1,
                  }}
                >
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="subtitle2" fontWeight={600}>
                      {activity.title}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {activity.description}
                    </Typography>
                  </Box>
                  <Chip
                    label={activity.status}
                    color={activity.status === 'completed' ? 'success' : 'primary'}
                    size="small"
                  />
                </Box>
              ))}
              {(!stats?.data?.recent_investigations || stats.data.recent_investigations.length === 0) && (
                <Typography variant="body2" color="textSecondary" align="center" sx={{ py: 3 }}>
                  No recent activity
                </Typography>
              )}
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
}; 