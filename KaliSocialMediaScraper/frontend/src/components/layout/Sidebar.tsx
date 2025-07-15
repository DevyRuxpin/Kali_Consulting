import React from 'react';
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Search as SearchIcon,
  Language as LanguageIcon,
  SocialDistance as SocialIcon,
  Security as SecurityIcon,
  Assessment as AssessmentIcon,
  Settings as SettingsIcon,
  Close as CloseIcon,
} from '@mui/icons-material';
import { useLocation, useNavigate } from 'react-router-dom';

interface SidebarProps {
  open: boolean;
  onToggle: () => void;
  variant?: 'permanent' | 'persistent' | 'temporary';
}

const DRAWER_WIDTH = 280;

const navigationItems = [
  {
    title: 'Dashboard',
    path: '/dashboard',
    icon: DashboardIcon,
    description: 'Overview and system health',
  },
  {
    title: 'Investigations',
    path: '/investigations',
    icon: SearchIcon,
    description: 'Manage OSINT investigations',
  },
  {
    title: 'Domain Analysis',
    path: '/domain-analysis',
    icon: LanguageIcon,
    description: 'Analyze domains and infrastructure',
  },
  {
    title: 'Social Media Scan',
    path: '/social-media',
    icon: SocialIcon,
    description: 'Scan social media profiles',
  },
  {
    title: 'Threat Analysis',
    path: '/threat-analysis',
    icon: SecurityIcon,
    description: 'Assess threat levels and indicators',
  },
  {
    title: 'Reports',
    path: '/reports',
    icon: AssessmentIcon,
    description: 'View and export reports',
  },
  {
    title: 'Settings',
    path: '/settings',
    icon: SettingsIcon,
    description: 'System configuration',
  },
];

export const Sidebar: React.FC<SidebarProps> = ({ 
  open, 
  onToggle, 
  variant = 'persistent' 
}) => {
  const theme = useTheme();
  const location = useLocation();
  const navigate = useNavigate();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const handleNavigation = (path: string) => {
    navigate(path);
    if (isMobile) {
      onToggle();
    }
  };

  const isActive = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  const drawerContent = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box
        sx={{
          p: 2,
          borderBottom: `1px solid ${theme.palette.divider}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <SecurityIcon 
            sx={{ 
              color: theme.palette.primary.main, 
              mr: 1,
              fontSize: 28 
            }} 
          />
          <Typography variant="h6" fontWeight={600} color="primary">
            Kali OSINT
          </Typography>
        </Box>
        {isMobile && (
          <Box
            component="button"
            onClick={onToggle}
            sx={{
              border: 'none',
              background: 'none',
              cursor: 'pointer',
              p: 0.5,
              borderRadius: 1,
              '&:hover': {
                backgroundColor: theme.palette.action.hover,
              },
            }}
          >
            <CloseIcon />
          </Box>
        )}
      </Box>

      {/* Navigation */}
      <Box sx={{ flex: 1, overflow: 'auto' }}>
        <List sx={{ pt: 1 }}>
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.path);
            
            return (
              <ListItem key={item.path} disablePadding>
                <ListItemButton
                  onClick={() => handleNavigation(item.path)}
                  sx={{
                    mx: 1,
                    mb: 0.5,
                    borderRadius: 2,
                    backgroundColor: active ? theme.palette.primary.main : 'transparent',
                    color: active ? theme.palette.primary.contrastText : theme.palette.text.primary,
                    '&:hover': {
                      backgroundColor: active 
                        ? theme.palette.primary.dark 
                        : theme.palette.action.hover,
                    },
                    transition: 'all 0.2s ease-in-out',
                  }}
                >
                  <ListItemIcon
                    sx={{
                      color: active ? theme.palette.primary.contrastText : theme.palette.text.secondary,
                      minWidth: 40,
                    }}
                  >
                    <Icon />
                  </ListItemIcon>
                  <ListItemText
                    primary={item.title}
                    secondary={item.description}
                    primaryTypographyProps={{
                      fontWeight: active ? 600 : 400,
                      fontSize: '0.95rem',
                    }}
                    secondaryTypographyProps={{
                      fontSize: '0.75rem',
                      color: active ? 'rgba(255, 255, 255, 0.7)' : theme.palette.text.secondary,
                    }}
                  />
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>
      </Box>

      {/* Footer */}
      <Box sx={{ p: 2, borderTop: `1px solid ${theme.palette.divider}` }}>
        <Typography variant="caption" color="text.secondary" align="center">
          Version 1.0.0
        </Typography>
      </Box>
    </Box>
  );

  if (variant === 'permanent') {
    return (
      <Drawer
        variant="permanent"
        sx={{
          width: DRAWER_WIDTH,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: DRAWER_WIDTH,
            boxSizing: 'border-box',
            borderRight: `1px solid ${theme.palette.divider}`,
            backgroundColor: theme.palette.background.paper,
          },
        }}
      >
        {drawerContent}
      </Drawer>
    );
  }

  return (
    <Drawer
      variant={variant}
      open={open}
      onClose={onToggle}
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: DRAWER_WIDTH,
          boxSizing: 'border-box',
          borderRight: `1px solid ${theme.palette.divider}`,
          backgroundColor: theme.palette.background.paper,
        },
      }}
      ModalProps={{
        keepMounted: true, // Better open performance on mobile.
      }}
    >
      {drawerContent}
    </Drawer>
  );
}; 