import type { PaletteOptions } from '@mui/material';

export const createPalette = (mode: 'light' | 'dark'): PaletteOptions => {
  const isLight = mode === 'light';

  const baseColors = {
    // Primary colors
    primary: {
      50: '#e3f2fd',
      100: '#bbdefb',
      200: '#90caf9',
      300: '#64b5f6',
      400: '#42a5f5',
      500: '#2196f3',
      600: '#1e88e5',
      700: '#1976d2',
      800: '#1565c0',
      900: '#0d47a1',
    },
    // Secondary colors
    secondary: {
      50: '#fce4ec',
      100: '#f8bbd9',
      200: '#f48fb1',
      300: '#f06292',
      400: '#ec407a',
      500: '#e91e63',
      600: '#d81b60',
      700: '#c2185b',
      800: '#ad1457',
      900: '#880e4f',
    },
    // Success colors
    success: {
      50: '#e8f5e8',
      100: '#c8e6c9',
      200: '#a5d6a7',
      300: '#81c784',
      400: '#66bb6a',
      500: '#4caf50',
      600: '#43a047',
      700: '#388e3c',
      800: '#2e7d32',
      900: '#1b5e20',
    },
    // Warning colors
    warning: {
      50: '#fff8e1',
      100: '#ffecb3',
      200: '#ffe082',
      300: '#ffd54f',
      400: '#ffca28',
      500: '#ffc107',
      600: '#ffb300',
      700: '#ffa000',
      800: '#ff8f00',
      900: '#ff6f00',
    },
    // Error colors
    error: {
      50: '#ffebee',
      100: '#ffcdd2',
      200: '#ef9a9a',
      300: '#e57373',
      400: '#ef5350',
      500: '#f44336',
      600: '#e53935',
      700: '#d32f2f',
      800: '#c62828',
      900: '#b71c1c',
    },
    // Info colors
    info: {
      50: '#e1f5fe',
      100: '#b3e5fc',
      200: '#81d4fa',
      300: '#4fc3f7',
      400: '#29b6f6',
      500: '#03a9f4',
      600: '#039be5',
      700: '#0288d1',
      800: '#0277bd',
      900: '#01579b',
    },
    // Neutral colors
    neutral: {
      50: '#fafafa',
      100: '#f5f5f5',
      200: '#eeeeee',
      300: '#e0e0e0',
      400: '#bdbdbd',
      500: '#9e9e9e',
      600: '#757575',
      700: '#616161',
      800: '#424242',
      900: '#212121',
    },
    // Threat level colors
    threat: {
      low: '#4caf50',
      medium: '#ff9800',
      high: '#f44336',
      critical: '#9c27b0',
    },
  };

  return {
    mode,
    primary: {
      main: baseColors.primary[500],
      light: baseColors.primary[300],
      dark: baseColors.primary[700],
      contrastText: isLight ? '#ffffff' : '#000000',
    },
    secondary: {
      main: baseColors.secondary[500],
      light: baseColors.secondary[300],
      dark: baseColors.secondary[700],
      contrastText: isLight ? '#ffffff' : '#000000',
    },
    success: {
      main: baseColors.success[500],
      light: baseColors.success[300],
      dark: baseColors.success[700],
      contrastText: isLight ? '#ffffff' : '#000000',
    },
    warning: {
      main: baseColors.warning[500],
      light: baseColors.warning[300],
      dark: baseColors.warning[700],
      contrastText: isLight ? '#000000' : '#ffffff',
    },
    error: {
      main: baseColors.error[500],
      light: baseColors.error[300],
      dark: baseColors.error[700],
      contrastText: isLight ? '#ffffff' : '#000000',
    },
    info: {
      main: baseColors.info[500],
      light: baseColors.info[300],
      dark: baseColors.info[700],
      contrastText: isLight ? '#ffffff' : '#000000',
    },
    neutral: {
      main: baseColors.neutral[500],
      light: baseColors.neutral[300],
      dark: baseColors.neutral[700],
      contrastText: isLight ? '#000000' : '#ffffff',
    },
    background: {
      default: isLight ? '#fafafa' : '#121212',
      paper: isLight ? '#ffffff' : '#1e1e1e',
    },
    text: {
      primary: isLight ? '#212121' : '#ffffff',
      secondary: isLight ? '#757575' : '#b0b0b0',
      disabled: isLight ? '#bdbdbd' : '#666666',
    },
    divider: isLight ? '#e0e0e0' : '#333333',
    action: {
      active: isLight ? '#757575' : '#b0b0b0',
      hover: isLight ? 'rgba(0, 0, 0, 0.04)' : 'rgba(255, 255, 255, 0.08)',
      selected: isLight ? 'rgba(0, 0, 0, 0.08)' : 'rgba(255, 255, 255, 0.16)',
      disabled: isLight ? 'rgba(0, 0, 0, 0.26)' : 'rgba(255, 255, 255, 0.3)',
      disabledBackground: isLight ? 'rgba(0, 0, 0, 0.12)' : 'rgba(255, 255, 255, 0.12)',
    },
  };
}; 