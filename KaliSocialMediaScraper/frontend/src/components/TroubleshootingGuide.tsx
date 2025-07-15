import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Button,
  Alert,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Refresh as RefreshIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';

interface TroubleshootingGuideProps {
  onRefresh?: () => void;
}

export const TroubleshootingGuide: React.FC<TroubleshootingGuideProps> = ({ onRefresh }) => {
  const commonIssues = [
    {
      title: 'Backend Service Not Running',
      description: 'The backend API server is not accessible',
      solutions: [
        'Start the backend server: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000',
        'Check if the backend is running on http://localhost:8000',
        'Verify the API_BASE_URL in your environment configuration',
      ],
    },
    {
      title: 'CORS Issues',
      description: 'Cross-origin requests are being blocked',
      solutions: [
        'Ensure the backend has CORS properly configured',
        'Check that the frontend is running on the correct port',
        'Verify the API_BASE_URL matches the backend URL',
      ],
    },
    {
      title: 'Database Connection Issues',
      description: 'Unable to connect to the database',
      solutions: [
        'Check if the database service is running',
        'Verify database connection settings in the backend',
        'Ensure database migrations have been applied',
      ],
    },
    {
      title: 'Network Connectivity',
      description: 'General network connectivity issues',
      solutions: [
        'Check your internet connection',
        'Verify firewall settings are not blocking requests',
        'Try accessing the backend directly in your browser',
      ],
    },
  ];

  const handleRefresh = () => {
    if (onRefresh) {
      onRefresh();
    } else {
      window.location.reload();
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Troubleshooting Guide
        </Typography>
        
        <Alert severity="info" sx={{ mb: 2 }}>
          <Typography variant="body2">
            If you're experiencing issues with the application, try these common solutions:
          </Typography>
        </Alert>

        <Box sx={{ mb: 2 }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={handleRefresh}
            sx={{ mr: 1 }}
          >
            Refresh Page
          </Button>
          <Button
            variant="outlined"
            startIcon={<SettingsIcon />}
            onClick={() => window.open('/settings', '_blank')}
          >
            Check Settings
          </Button>
        </Box>

        {commonIssues.map((issue, index) => (
          <Accordion key={index} sx={{ mb: 1 }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <ErrorIcon color="warning" />
                <Typography variant="subtitle1" fontWeight={600}>
                  {issue.title}
                </Typography>
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                {issue.description}
              </Typography>
              <List dense>
                {issue.solutions.map((solution, solutionIndex) => (
                  <ListItem key={solutionIndex} sx={{ py: 0.5 }}>
                    <ListItemIcon sx={{ minWidth: 32 }}>
                      <CheckIcon color="success" fontSize="small" />
                    </ListItemIcon>
                    <ListItemText
                      primary={solution}
                      primaryTypographyProps={{ variant: 'body2' }}
                    />
                  </ListItem>
                ))}
              </List>
            </AccordionDetails>
          </Accordion>
        ))}

        <Alert severity="warning" sx={{ mt: 2 }}>
          <Typography variant="body2">
            If the issue persists, check the browser console for detailed error messages 
            and contact support with the error details.
          </Typography>
        </Alert>
      </CardContent>
    </Card>
  );
}; 