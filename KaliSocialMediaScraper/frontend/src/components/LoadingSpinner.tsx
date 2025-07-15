import React from 'react';
import { Box, CircularProgress, Typography, LinearProgress } from '@mui/material';

interface LoadingSpinnerProps {
  message?: string;
  variant?: 'circular' | 'linear';
  size?: number;
  fullScreen?: boolean;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message = 'Loading...',
  variant = 'circular',
  size = 40,
  fullScreen = false,
}) => {
  const content = (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 2,
        p: 3,
      }}
    >
      {variant === 'circular' ? (
        <CircularProgress size={size} />
      ) : (
        <Box sx={{ width: '100%', maxWidth: 400 }}>
          <LinearProgress />
        </Box>
      )}
      {message && (
        <Typography variant="body2" color="text.secondary">
          {message}
        </Typography>
      )}
    </Box>
  );

  if (fullScreen) {
    return (
      <Box
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          zIndex: 9999,
        }}
      >
        {content}
      </Box>
    );
  }

  return content;
}; 