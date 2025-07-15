import React from 'react';
import { Box, Chip, Button } from '@mui/material';
import { CheckCircle as CheckIcon, Error as ErrorIcon, Refresh as RefreshIcon } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { healthCheck } from '../services/api';

export const BackendStatus: React.FC = () => {
  const { data: health, isLoading, error, refetch } = useQuery({
    queryKey: ['health-check'],
    queryFn: () => healthCheck(),
    retry: 1,
    refetchOnWindowFocus: false,
    refetchInterval: 30000, // Check every 30 seconds
  });

  const isError = error || health?.status === 'error';

  const handleRefresh = () => {
    refetch();
  };

  if (isLoading) {
    return (
      <Chip
        icon={<RefreshIcon />}
        label="Checking backend..."
        color="default"
        variant="outlined"
        size="small"
      />
    );
  }

  if (isError) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Chip
          icon={<ErrorIcon />}
          label="Backend offline"
          color="error"
          variant="outlined"
          size="small"
        />
        <Button
          size="small"
          startIcon={<RefreshIcon />}
          onClick={handleRefresh}
          sx={{ minWidth: 'auto', p: 0.5 }}
        >
          Retry
        </Button>
      </Box>
    );
  }

  return (
    <Chip
      icon={<CheckIcon />}
      label="Backend online"
      color="success"
      variant="outlined"
      size="small"
    />
  );
}; 