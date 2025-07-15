import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Badge,
  Menu,
  MenuItem,
  Avatar,
  Divider,
  useTheme,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications as NotificationsIcon,
  Brightness4 as DarkModeIcon,
  Brightness7 as LightModeIcon,
  AccountCircle as AccountIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon,
} from '@mui/icons-material';
import { useTheme as useAppTheme } from '../../theme';
import { BackendStatus } from '../BackendStatus';

interface HeaderProps {
  onSidebarToggle: () => void;
  title?: string;
}

export const Header: React.FC<HeaderProps> = ({ 
  onSidebarToggle, 
  title = 'Kali OSINT Platform' 
}) => {
  const theme = useTheme();
  const { mode, toggleTheme } = useAppTheme();
  
  const [notificationsAnchor, setNotificationsAnchor] = useState<null | HTMLElement>(null);
  const [userMenuAnchor, setUserMenuAnchor] = useState<null | HTMLElement>(null);

  const handleNotificationsOpen = (event: React.MouseEvent<HTMLElement>) => {
    setNotificationsAnchor(event.currentTarget);
  };

  const handleNotificationsClose = () => {
    setNotificationsAnchor(null);
  };

  const handleUserMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setUserMenuAnchor(event.currentTarget);
  };

  const handleUserMenuClose = () => {
    setUserMenuAnchor(null);
  };

  const mockNotifications = [
    {
      id: 1,
      title: 'New investigation completed',
      message: 'Domain analysis for example.com has finished',
      time: '2 minutes ago',
      type: 'success' as const,
    },
    {
      id: 2,
      title: 'High threat detected',
      message: 'Threat score 0.85 for user @suspicious_user',
      time: '5 minutes ago',
      type: 'warning' as const,
    },
    {
      id: 3,
      title: 'System update',
      message: 'New OSINT tools have been added',
      time: '1 hour ago',
      type: 'info' as const,
    },
  ];

  const unreadCount = mockNotifications.length;

  return (
    <AppBar
      position="fixed"
      sx={{
        zIndex: theme.zIndex.drawer + 1,
        backgroundColor: theme.palette.background.paper,
        color: theme.palette.text.primary,
        borderBottom: `1px solid ${theme.palette.divider}`,
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
      }}
    >
      <Toolbar sx={{ minHeight: 64 }}>
        {/* Sidebar Toggle */}
        <IconButton
          color="inherit"
          aria-label="open drawer"
          edge="start"
          onClick={onSidebarToggle}
          sx={{ mr: 2, display: { md: 'none' } }}
        >
          <MenuIcon />
        </IconButton>

        {/* App Title */}
        <Typography
          variant="h6"
          component="div"
          sx={{
            flexGrow: 1,
            fontWeight: 600,
            color: theme.palette.primary.main,
            display: { xs: 'none', sm: 'block' },
          }}
        >
          {title}
        </Typography>

        {/* Right Side Actions */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {/* Backend Status */}
          <BackendStatus />

          {/* Theme Toggle */}
          <IconButton
            color="inherit"
            onClick={toggleTheme}
            sx={{
              p: 1,
              borderRadius: 2,
              '&:hover': {
                backgroundColor: theme.palette.action.hover,
              },
            }}
          >
            {mode === 'dark' ? <LightModeIcon /> : <DarkModeIcon />}
          </IconButton>

          {/* Notifications */}
          <IconButton
            color="inherit"
            onClick={handleNotificationsOpen}
            sx={{
              p: 1,
              borderRadius: 2,
              '&:hover': {
                backgroundColor: theme.palette.action.hover,
              },
            }}
          >
            <Badge badgeContent={unreadCount} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>

          {/* User Menu */}
          <IconButton
            color="inherit"
            onClick={handleUserMenuOpen}
            sx={{
              p: 1,
              borderRadius: 2,
              '&:hover': {
                backgroundColor: theme.palette.action.hover,
              },
            }}
          >
            <Avatar
              sx={{
                width: 32,
                height: 32,
                backgroundColor: theme.palette.primary.main,
                fontSize: '0.875rem',
              }}
            >
              A
            </Avatar>
          </IconButton>
        </Box>
      </Toolbar>

      {/* Notifications Menu */}
      <Menu
        anchorEl={notificationsAnchor}
        open={Boolean(notificationsAnchor)}
        onClose={handleNotificationsClose}
        PaperProps={{
          sx: {
            width: 320,
            maxHeight: 400,
            mt: 1,
          },
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <Box sx={{ p: 2, borderBottom: `1px solid ${theme.palette.divider}` }}>
          <Typography variant="h6" fontWeight={600}>
            Notifications
          </Typography>
        </Box>
        {mockNotifications.map((notification) => (
          <MenuItem
            key={notification.id}
            onClick={handleNotificationsClose}
            sx={{
              py: 1.5,
              px: 2,
              borderBottom: `1px solid ${theme.palette.divider}`,
              '&:last-child': {
                borderBottom: 'none',
              },
            }}
          >
            <Box sx={{ width: '100%' }}>
              <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                {notification.title}
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {notification.message}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {notification.time}
              </Typography>
            </Box>
          </MenuItem>
        ))}
        {mockNotifications.length === 0 && (
          <MenuItem disabled>
            <Typography variant="body2" color="text.secondary">
              No notifications
            </Typography>
          </MenuItem>
        )}
      </Menu>

      {/* User Menu */}
      <Menu
        anchorEl={userMenuAnchor}
        open={Boolean(userMenuAnchor)}
        onClose={handleUserMenuClose}
        PaperProps={{
          sx: {
            width: 200,
            mt: 1,
          },
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <Box sx={{ p: 2, borderBottom: `1px solid ${theme.palette.divider}` }}>
          <Typography variant="subtitle1" fontWeight={600}>
            Admin User
          </Typography>
          <Typography variant="body2" color="text.secondary">
            admin@example.com
          </Typography>
        </Box>
        <MenuItem onClick={handleUserMenuClose}>
          <AccountIcon sx={{ mr: 2 }} />
          Profile
        </MenuItem>
        <MenuItem onClick={handleUserMenuClose}>
          <SettingsIcon sx={{ mr: 2 }} />
          Settings
        </MenuItem>
        <Divider />
        <MenuItem onClick={handleUserMenuClose}>
          <LogoutIcon sx={{ mr: 2 }} />
          Logout
        </MenuItem>
      </Menu>
    </AppBar>
  );
}; 