import React, { useState } from 'react';
import { Box, useTheme, useMediaQuery } from '@mui/material';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

interface LayoutProps {
  children: React.ReactNode;
}

const DRAWER_WIDTH = 280;
const HEADER_HEIGHT = 64;

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [sidebarOpen, setSidebarOpen] = useState(!isMobile);

  const handleSidebarToggle = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      {/* Sidebar */}
      <Sidebar
        open={sidebarOpen}
        onToggle={handleSidebarToggle}
        variant={isMobile ? 'temporary' : 'persistent'}
      />

      {/* Main Content Area */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          minHeight: '100vh',
          backgroundColor: theme.palette.background.default,
        }}
      >
        {/* Header */}
        <Header onSidebarToggle={handleSidebarToggle} />

        {/* Content */}
        <Box
          sx={{
            flex: 1,
            mt: `${HEADER_HEIGHT}px`,
            ml: { md: sidebarOpen ? `${DRAWER_WIDTH}px` : 0 },
            transition: theme.transitions.create(['margin'], {
              easing: theme.transitions.easing.sharp,
              duration: theme.transitions.duration.leavingScreen,
            }),
            p: { xs: 2, md: 3 },
            overflow: 'auto',
          }}
        >
          {children}
        </Box>
      </Box>
    </Box>
  );
}; 