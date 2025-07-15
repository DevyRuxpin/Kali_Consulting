import type { Components, Theme } from '@mui/material/styles';

export const createComponents = (): Components<Theme> => {
  return {
    MuiCssBaseline: {
      styleOverrides: {
        '*': {
          boxSizing: 'border-box',
        },
        html: {
          WebkitFontSmoothing: 'antialiased',
          MozOsxFontSmoothing: 'grayscale',
          height: '100%',
          width: '100%',
        },
        body: {
          height: '100%',
          width: '100%',
        },
        '#root': {
          height: '100%',
          width: '100%',
        },
        'input:-webkit-autofill': {
          WebkitBoxShadow: '0 0 0 1000px "#ffffff" inset',
          WebkitTextFillColor: '#000000',
        },
        'input:-webkit-autofill:focus': {
          WebkitBoxShadow: '0 0 0 1000px "#ffffff" inset',
          WebkitTextFillColor: '#000000',
        },
        'input:-webkit-autofill:hover': {
          WebkitBoxShadow: '0 0 0 1000px "#ffffff" inset',
          WebkitTextFillColor: '#000000',
        },
        'input:-webkit-autofill:active': {
          WebkitBoxShadow: '0 0 0 1000px "#ffffff" inset',
          WebkitTextFillColor: '#000000',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
          boxShadow: 'none',
          '&:hover': {
            boxShadow: 'none',
          },
        },
        contained: {
          '&:hover': {
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
          },
        },
        outlined: {
          borderWidth: 2,
          '&:hover': {
            borderWidth: 2,
          },
        },
        sizeLarge: {
          padding: '12px 24px',
          fontSize: '1rem',
        },
        sizeSmall: {
          padding: '6px 16px',
          fontSize: '0.875rem',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          '&:hover': {
            boxShadow: '0 4px 16px rgba(0, 0, 0, 0.15)',
          },
        },
      },
    },
    MuiCardContent: {
      styleOverrides: {
        root: {
          padding: 24,
          '&:last-child': {
            paddingBottom: 24,
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
            '&:hover .MuiOutlinedInput-notchedOutline': {
              borderColor: "#2196f3",
            },
            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
              borderColor: "#2196f3",
              borderWidth: 2,
            },
          },
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          '&:hover .MuiOutlinedInput-notchedOutline': {
            borderColor: "#2196f3",
          },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderColor: "#2196f3",
            borderWidth: 2,
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
        elevation1: {
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
        },
        elevation2: {
          boxShadow: '0 4px 16px rgba(0, 0, 0, 0.1)',
        },
        elevation3: {
          boxShadow: '0 8px 24px rgba(0, 0, 0, 0.12)',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRight: 'none',
          boxShadow: '2px 0 8px rgba(0, 0, 0, 0.1)',
        },
      },
    },
    MuiListItem: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          margin: '4px 8px',
          '&:hover': {
            backgroundColor: 'rgba(0, 0, 0, 0.04)',
          },
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          margin: '4px 8px',
          '&:hover': {
            backgroundColor: 'rgba(0, 0, 0, 0.04)',
          },
          '&.Mui-selected': {
            backgroundColor: "#2196f3",
            color: "#ffffff",
            '&:hover': {
              backgroundColor: "#1976d2",
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          fontWeight: 500,
        },
        filled: {
          '&.MuiChip-colorPrimary': {
            backgroundColor: "#2196f3",
            color: "#ffffff",
          },
          '&.MuiChip-colorSecondary': {
            backgroundColor: "#e91e63",
            color: "#ffffff",
          },
          '&.MuiChip-colorSuccess': {
            backgroundColor: "#4caf50",
            color: "#ffffff",
          },
          '&.MuiChip-colorWarning': {
            backgroundColor: "#ff9800",
            color: "#000000",
          },
          '&.MuiChip-colorError': {
            backgroundColor: "#f44336",
            color: "#ffffff",
          },
        },
      },
    },
    MuiAlert: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
        },
      },
    },
    MuiSnackbar: {
      styleOverrides: {
        root: {
          '& .MuiAlert-root': {
            borderRadius: 8,
          },
        },
      },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          '& .MuiTableCell-root': {
            fontWeight: 600,
            backgroundColor: '#ffffff',
          },
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: {
          borderBottom: '1px solid #e0e0e0',
          padding: '16px',
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          '&:hover': {
            backgroundColor: 'rgba(0, 0, 0, 0.04)',
          },
        },
      },
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          height: 8,
        },
      },
    },
    MuiCircularProgress: {
      styleOverrides: {
        root: {
          '&.MuiCircularProgress-colorPrimary': {
            color: "#2196f3",
          },
        },
      },
    },
    MuiSkeleton: {
      styleOverrides: {
        root: {
          borderRadius: 4,
        },
      },
    },
    MuiTooltip: {
      styleOverrides: {
        tooltip: {
          backgroundColor: '#ffffff',
          color: '#212121',
          border: '1px solid #e0e0e0',
          borderRadius: 8,
          fontSize: '0.875rem',
          boxShadow: '0 4px 16px rgba(0, 0, 0, 0.15)',
        },
        arrow: {
          color: '#ffffff',
          '&::before': {
            border: '1px solid #e0e0e0',
          },
        },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: {
          borderRadius: 12,
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
        },
      },
    },
    MuiDialogTitle: {
      styleOverrides: {
        root: {
          padding: '24px 24px 16px 24px',
        },
      },
    },
    MuiDialogContent: {
      styleOverrides: {
        root: {
          padding: '16px 24px',
        },
      },
    },
    MuiDialogActions: {
      styleOverrides: {
        root: {
          padding: '16px 24px 24px 24px',
        },
      },
    },
    MuiMenu: {
      styleOverrides: {
        paper: {
          borderRadius: 8,
          boxShadow: '0 4px 16px rgba(0, 0, 0, 0.15)',
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          margin: '2px 8px',
          '&:hover': {
            backgroundColor: 'rgba(0, 0, 0, 0.04)',
          },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
    MuiAutocomplete: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
          },
        },
        paper: {
          borderRadius: 8,
          boxShadow: '0 4px 16px rgba(0, 0, 0, 0.15)',
        },
      },
    },
    MuiSwitch: {
      styleOverrides: {
        root: {
          '& .MuiSwitch-track': {
            borderRadius: 12,
          },
          '& .MuiSwitch-thumb': {
            borderRadius: 10,
          },
        },
      },
    },
    MuiCheckbox: {
      styleOverrides: {
        root: {
          '&.Mui-checked': {
            color: "#2196f3",
          },
        },
      },
    },
    MuiRadio: {
      styleOverrides: {
        root: {
          '&.Mui-checked': {
            color: "#2196f3",
          },
        },
      },
    },
    MuiSlider: {
      styleOverrides: {
        root: {
          '& .MuiSlider-track': {
            borderRadius: 4,
          },
          '& .MuiSlider-thumb': {
            borderRadius: 8,
          },
        },
      },
    },
  };
}; 