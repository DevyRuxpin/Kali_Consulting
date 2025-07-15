import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Chip,
  LinearProgress,
  Alert,
  Checkbox,
  FormControlLabel,
} from '@mui/material';
import {
  Search as SearchIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import { useMutation } from '@tanstack/react-query';
import { comprehensiveHunt } from '../services/api';
import toast from 'react-hot-toast';
import { useTheme } from '@mui/material/styles';

const SUPPORTED_PLATFORMS = [
  'twitter',
  'instagram',
  'facebook',
  'linkedin',
  'github',
  'youtube',
  'tiktok',
  'reddit',
  'discord',
  'telegram',
];

export const SocialMedia: React.FC = () => {
  const [username, setUsername] = useState('');
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [includeDirectScraping, setIncludeDirectScraping] = useState(true);
  const [includeSherlock, setIncludeSherlock] = useState(true);

  // Social media scan mutation
  const scanMutation = useMutation({
    mutationFn: (data: {
      username: string;
      includeDirectScraping: boolean;
      includeSherlock: boolean;
      platforms?: string[];
    }) => comprehensiveHunt(
      data.username,
      data.includeDirectScraping,
      data.includeSherlock,
      data.platforms
    ),
    onSuccess: () => {
      toast.success('Social media scan completed successfully');
    },
    onError: (error) => {
      toast.error('Failed to scan social media');
      console.error('Social media scan error:', error);
    },
  });

  const handleScan = () => {
    if (!username.trim()) {
      toast.error('Please enter a username');
      return;
    }
    scanMutation.mutate({
      username: username.trim(),
      includeDirectScraping,
      includeSherlock,
      platforms: selectedPlatforms.length > 0 ? selectedPlatforms : undefined,
    });
  };

  const handleExport = () => {
    if (scanMutation.data?.data) {
      const dataStr = JSON.stringify(scanMutation.data.data, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `social-media-scan-${username}-${new Date().toISOString().split('T')[0]}.json`;
      link.click();
      URL.revokeObjectURL(url);
    }
  };

  const scanData = scanMutation.data?.data;

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" fontWeight={600}>
          Social Media Scan
        </Typography>
      </Box>

      {/* Input Form */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Scan Social Media Profiles
          </Typography>
          
          {/* Username Input */}
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-end', mb: 3 }}>
            <TextField
              fullWidth
              label="Username"
              placeholder="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={scanMutation.isPending}
            />
            <Button
              variant="contained"
              startIcon={<SearchIcon />}
              onClick={handleScan}
              disabled={scanMutation.isPending || !username.trim()}
            >
              {scanMutation.isPending ? 'Scanning...' : 'Scan'}
            </Button>
          </Box>

          {/* Platform Selection */}
          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle1" gutterBottom>
              Select Platforms
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {SUPPORTED_PLATFORMS.map((platform) => (
                <Chip
                  key={platform}
                  label={platform}
                  onClick={() => {
                    if (selectedPlatforms.includes(platform)) {
                      setSelectedPlatforms(selectedPlatforms.filter(p => p !== platform));
                    } else {
                      setSelectedPlatforms([...selectedPlatforms, platform]);
                    }
                  }}
                  color={selectedPlatforms.includes(platform) ? 'primary' : 'default'}
                  variant={selectedPlatforms.includes(platform) ? 'filled' : 'outlined'}
                  clickable
                />
              ))}
            </Box>
            <Typography variant="caption" color="textSecondary">
              Leave empty to scan all platforms
            </Typography>
          </Box>

          {/* Scan Options */}
          <Box sx={{ display: 'flex', gap: 3 }}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={includeDirectScraping}
                  onChange={(e) => setIncludeDirectScraping(e.target.checked)}
                  disabled={scanMutation.isPending}
                />
              }
              label="Include Direct Scraping"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={includeSherlock}
                  onChange={(e) => setIncludeSherlock(e.target.checked)}
                  disabled={scanMutation.isPending}
                />
              }
              label="Include Sherlock Search"
            />
          </Box>
        </CardContent>
      </Card>

      {/* Loading State */}
      {scanMutation.isPending && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Scanning Social Media
            </Typography>
            <LinearProgress />
            <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
              Searching for {username} across {selectedPlatforms.length > 0 ? selectedPlatforms.length : 'all'} platforms...
            </Typography>
          </CardContent>
        </Card>
      )}

      {/* Results */}
      {scanData && (
        <Box>
          {/* Export Button */}
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
            <Button
              variant="outlined"
              startIcon={<DownloadIcon />}
              onClick={handleExport}
            >
              Export Results
            </Button>
          </Box>

          {/* Summary */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Scan Summary
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Username
                  </Typography>
                  <Typography variant="body1" fontWeight={600}>
                    {username}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Platforms Found
                  </Typography>
                  <Typography variant="body1">
                    {scanData.platforms?.length || 0}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Sherlock Results
                  </Typography>
                  <Typography variant="body1">
                    {scanData.sherlock_results?.length || 0}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Threat Score
                  </Typography>
                  <Chip
                    label={`${scanData.threat_assessment?.threat_score || 0}/10`}
                    color={scanData.threat_assessment?.threat_score > 7 ? 'error' : scanData.threat_assessment?.threat_score > 4 ? 'warning' : 'success'}
                  />
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Platform Results */}
          {scanData.platforms && scanData.platforms.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Platform Analysis
                </Typography>
                {scanData.platforms.map((platform: any, index: number) => (
                  <Box key={index} sx={{ mb: 2, p: 2, border: `1px solid ${useTheme().palette.divider}`, borderRadius: 1 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                      <Typography variant="subtitle1" fontWeight={600}>
                        {platform.platform}
                      </Typography>
                      <Chip
                        label={`Threat: ${platform.threat_score}/10`}
                        color={platform.threat_score > 7 ? 'error' : platform.threat_score > 4 ? 'warning' : 'success'}
                        size="small"
                      />
                    </Box>
                    <Typography variant="body2" color="textSecondary" gutterBottom>
                      Username: {platform.username}
                    </Typography>
                    {platform.profile && (
                      <Box sx={{ mt: 1 }}>
                        <Typography variant="body2">
                          Followers: {platform.profile.followers || 0} | Following: {platform.profile.following || 0}
                        </Typography>
                        {platform.profile.bio && (
                          <Typography variant="body2" color="textSecondary" sx={{ mt: 0.5 }}>
                            Bio: {platform.profile.bio}
                          </Typography>
                        )}
                      </Box>
                    )}
                  </Box>
                ))}
              </CardContent>
            </Card>
          )}

          {/* Sherlock Results */}
          {scanData.sherlock_results && scanData.sherlock_results.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Sherlock Search Results
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {scanData.sherlock_results.map((result: any, index: number) => (
                    <Chip
                      key={index}
                      label={result.site_name}
                      color={result.status === 'found' ? 'success' : 'default'}
                      variant="outlined"
                      onClick={() => window.open(result.url, '_blank')}
                      clickable={result.status === 'found'}
                    />
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}

          {/* Threat Assessment */}
          {scanData.threat_assessment && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom color="error">
                  Threat Assessment
                </Typography>
                <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2, mb: 2 }}>
                  <Box>
                    <Typography variant="subtitle2" color="textSecondary">
                      Threat Level
                    </Typography>
                    <Chip
                      label={scanData.threat_assessment.threat_level.toUpperCase()}
                      color={scanData.threat_assessment.threat_level === 'high' || scanData.threat_assessment.threat_level === 'critical' ? 'error' : 'warning'}
                    />
                  </Box>
                  <Box>
                    <Typography variant="subtitle2" color="textSecondary">
                      Threat Score
                    </Typography>
                    <Typography variant="h6">
                      {scanData.threat_assessment.threat_score}/10
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="subtitle2" color="textSecondary">
                      Confidence
                    </Typography>
                    <Typography variant="h6">
                      {Math.round(scanData.threat_assessment.confidence * 100)}%
                    </Typography>
                  </Box>
                </Box>
                
                {scanData.threat_assessment.indicators && scanData.threat_assessment.indicators.length > 0 && (
                  <Box>
                    <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                      Threat Indicators
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {scanData.threat_assessment.indicators.map((indicator: string, index: number) => (
                        <Chip key={index} label={indicator} color="error" size="small" />
                      ))}
                    </Box>
                  </Box>
                )}

                {scanData.threat_assessment.recommendations && scanData.threat_assessment.recommendations.length > 0 && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                      Recommendations
                    </Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                      {scanData.threat_assessment.recommendations.map((recommendation: string, index: number) => (
                        <Typography key={index} variant="body2">
                          • {recommendation}
                        </Typography>
                      ))}
                    </Box>
                  </Box>
                )}
              </CardContent>
            </Card>
          )}
        </Box>
      )}

      {/* Error State */}
      {scanMutation.isError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Failed to scan social media. Please check the username and try again.
        </Alert>
      )}
    </Box>
  );
}; 