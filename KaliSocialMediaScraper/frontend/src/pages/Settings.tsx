import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Switch,
  FormControlLabel,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider,
  Alert,
} from '@mui/material';
import {
  Save as SaveIcon,
  Refresh as RefreshIcon,
  Security as SecurityIcon,
  Notifications as NotificationsIcon,
  Storage as StorageIcon,
} from '@mui/icons-material';
import { useMutation, useQuery } from '@tanstack/react-query';
import { getSettings, updateSettings } from '../services/api';
import toast from 'react-hot-toast';

export const Settings: React.FC = () => {
  const [settings, setSettings] = useState<any>(null);
  const [hasChanges, setHasChanges] = useState(false);

  // Fetch settings
  const { data: currentSettings, isLoading, error } = useQuery({
    queryKey: ['settings'],
    queryFn: () => getSettings(),
  });

  // Set settings when data is loaded
  React.useEffect(() => {
    if (currentSettings?.data) {
      setSettings(currentSettings.data);
    }
  }, [currentSettings]);

  // Update settings mutation
  const updateMutation = useMutation({
    mutationFn: (newSettings: any) => updateSettings(newSettings),
    onSuccess: () => {
      toast.success('Settings updated successfully');
      setHasChanges(false);
    },
    onError: (error) => {
      toast.error('Failed to update settings');
      console.error('Settings update error:', error);
    },
  });

  const handleSettingChange = (key: string, value: any) => {
    setSettings((prev: any) => ({
      ...prev,
      [key]: value,
    }));
    setHasChanges(true);
  };

  const handleSave = () => {
    if (settings) {
      updateMutation.mutate(settings);
    }
  };

  const handleReset = () => {
    if (currentSettings?.data) {
      setSettings(currentSettings.data);
      setHasChanges(false);
    }
  };

  if (error) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 2 }}>
          Failed to load settings: {error instanceof Error ? error.message : 'Unknown error'}
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" fontWeight={600}>
          Settings
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={handleReset}
            disabled={!hasChanges}
          >
            Reset
          </Button>
          <Button
            variant="contained"
            startIcon={<SaveIcon />}
            onClick={handleSave}
            disabled={!hasChanges || updateMutation.isPending}
          >
            {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
          </Button>
        </Box>
      </Box>

      {isLoading ? (
        <Typography>Loading settings...</Typography>
      ) : (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          {/* System Settings */}
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <StorageIcon color="primary" />
                <Typography variant="h6">System Settings</Typography>
              </Box>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 3 }}>
                <TextField
                  label="Max Concurrent Scrapers"
                  type="number"
                  value={settings?.max_concurrent_scrapers || 5}
                  onChange={(e) => handleSettingChange('max_concurrent_scrapers', parseInt(e.target.value))}
                  inputProps={{ min: 1, max: 20 }}
                  helperText="Maximum number of simultaneous scraping operations"
                />
                <TextField
                  label="Scraping Timeout (seconds)"
                  type="number"
                  value={settings?.scraping_timeout_seconds || 300}
                  onChange={(e) => handleSettingChange('scraping_timeout_seconds', parseInt(e.target.value))}
                  inputProps={{ min: 60, max: 3600 }}
                  helperText="Timeout for individual scraping operations"
                />
                <TextField
                  label="Max Investigations Per User"
                  type="number"
                  value={settings?.max_investigations_per_user || 100}
                  onChange={(e) => handleSettingChange('max_investigations_per_user', parseInt(e.target.value))}
                  inputProps={{ min: 1, max: 1000 }}
                  helperText="Maximum investigations a user can create"
                />
                <TextField
                  label="Data Retention (days)"
                  type="number"
                  value={settings?.data_retention_days || 90}
                  onChange={(e) => handleSettingChange('data_retention_days', parseInt(e.target.value))}
                  inputProps={{ min: 1, max: 365 }}
                  helperText="How long to keep investigation data"
                />
              </Box>
            </CardContent>
          </Card>

          {/* Scraping Settings */}
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <SecurityIcon color="primary" />
                <Typography variant="h6">Scraping Configuration</Typography>
              </Box>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 3 }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings?.rate_limiting_enabled || false}
                      onChange={(e) => handleSettingChange('rate_limiting_enabled', e.target.checked)}
                    />
                  }
                  label="Enable Rate Limiting"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings?.proxy_rotation_enabled || false}
                      onChange={(e) => handleSettingChange('proxy_rotation_enabled', e.target.checked)}
                    />
                  }
                  label="Enable Proxy Rotation"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings?.dark_web_monitoring || false}
                      onChange={(e) => handleSettingChange('dark_web_monitoring', e.target.checked)}
                    />
                  }
                  label="Dark Web Monitoring"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings?.ml_analysis_enabled || false}
                      onChange={(e) => handleSettingChange('ml_analysis_enabled', e.target.checked)}
                    />
                  }
                  label="ML Analysis Enabled"
                />
              </Box>
              <Divider sx={{ my: 2 }} />
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 3 }}>
                <FormControl fullWidth>
                  <InputLabel>Threat Detection Sensitivity</InputLabel>
                  <Select
                    value={settings?.threat_detection_sensitivity || 'medium'}
                    label="Threat Detection Sensitivity"
                    onChange={(e) => handleSettingChange('threat_detection_sensitivity', e.target.value)}
                  >
                    <MenuItem value="low">Low</MenuItem>
                    <MenuItem value="medium">Medium</MenuItem>
                    <MenuItem value="high">High</MenuItem>
                  </Select>
                </FormControl>
                <TextField
                  label="Threat Score Threshold"
                  type="number"
                  value={settings?.threat_score_threshold || 7}
                  onChange={(e) => handleSettingChange('threat_score_threshold', parseInt(e.target.value))}
                  inputProps={{ min: 1, max: 10 }}
                  helperText="Minimum score to trigger threat alerts"
                />
                <TextField
                  label="Max Profiles Per Investigation"
                  type="number"
                  value={settings?.max_profiles_per_investigation || 1000}
                  onChange={(e) => handleSettingChange('max_profiles_per_investigation', parseInt(e.target.value))}
                  inputProps={{ min: 1, max: 10000 }}
                  helperText="Maximum profiles to scrape per investigation"
                />
              </Box>
            </CardContent>
          </Card>

          {/* Notification Settings */}
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <NotificationsIcon color="primary" />
                <Typography variant="h6">Notification Settings</Typography>
              </Box>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 3 }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings?.notification_enabled || false}
                      onChange={(e) => handleSettingChange('notification_enabled', e.target.checked)}
                    />
                  }
                  label="Enable Notifications"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings?.auto_export_enabled || false}
                      onChange={(e) => handleSettingChange('auto_export_enabled', e.target.checked)}
                    />
                  }
                  label="Auto Export Reports"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings?.auto_cleanup_enabled || false}
                      onChange={(e) => handleSettingChange('auto_cleanup_enabled', e.target.checked)}
                    />
                  }
                  label="Auto Cleanup Old Data"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings?.backup_enabled || false}
                      onChange={(e) => handleSettingChange('backup_enabled', e.target.checked)}
                    />
                  }
                  label="Enable Automatic Backups"
                />
              </Box>
            </CardContent>
          </Card>

          {/* Advanced Settings */}
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Advanced Configuration
              </Typography>
              <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                These settings affect system performance and behavior. Modify with caution.
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 3 }}>
                <TextField
                  label="WebSocket Reconnect Interval (ms)"
                  type="number"
                  value={settings?.websocket_reconnect_interval || 5000}
                  onChange={(e) => handleSettingChange('websocket_reconnect_interval', parseInt(e.target.value))}
                  inputProps={{ min: 1000, max: 30000 }}
                  helperText="Interval between WebSocket reconnection attempts"
                />
                <TextField
                  label="API Rate Limit (requests/min)"
                  type="number"
                  value={settings?.api_rate_limit || 100}
                  onChange={(e) => handleSettingChange('api_rate_limit', parseInt(e.target.value))}
                  inputProps={{ min: 10, max: 1000 }}
                  helperText="Maximum API requests per minute"
                />
                <TextField
                  label="Cache TTL (seconds)"
                  type="number"
                  value={settings?.cache_ttl_seconds || 3600}
                  onChange={(e) => handleSettingChange('cache_ttl_seconds', parseInt(e.target.value))}
                  inputProps={{ min: 60, max: 86400 }}
                  helperText="Time to live for cached data"
                />
              </Box>
            </CardContent>
          </Card>
        </Box>
      )}
    </Box>
  );
}; 