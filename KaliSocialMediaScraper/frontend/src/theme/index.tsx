import { createTheme } from '@mui/material/styles';
import type { ThemeOptions, PaletteMode } from '@mui/material';
import { createPalette } from './palette';
import { createTypography } from './typography';
import { createComponents } from './components';

declare module '@mui/material/styles' {
  interface Palette {
    neutral: Palette['primary'];
  }
  interface PaletteOptions {
    neutral?: PaletteOptions['primary'];
  }
}

import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';

export const createAppTheme = (mode: PaletteMode = 'dark') => {
  const palette = createPalette(mode);
  const typography = createTypography();
  const components = createComponents();

  const themeOptions: ThemeOptions = {
    palette,
    typography,
    components,
    shape: {
      borderRadius: 12,
    },
    spacing: 8,
    breakpoints: {
      values: {
        xs: 0,
        sm: 600,
        md: 960,
        lg: 1280,
        xl: 1920,
      },
    },
  };

  return createTheme(themeOptions);
};

export const lightTheme = createAppTheme('light');
export const darkTheme = createAppTheme('dark');

// Theme context and hooks
interface ThemeContextType {
  mode: PaletteMode;
  toggleTheme: () => void;
  setMode: (mode: PaletteMode) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider = ({ children }: ThemeProviderProps) => {
  const [mode, setMode] = useState<PaletteMode>('dark');

  useEffect(() => {
    // Check for saved theme preference or system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme) {
      setMode(savedTheme as PaletteMode);
    } else if (systemPrefersDark) {
      setMode('dark');
    }
  }, []);

  const toggleTheme = () => {
    const newMode = mode === 'light' ? 'dark' : 'light';
    setMode(newMode);
    localStorage.setItem('theme', newMode);
  };

  const theme = createAppTheme(mode);

  return (
    <ThemeContext.Provider value={{ mode, toggleTheme, setMode }}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
}; 