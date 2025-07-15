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
} from '@mui/material';
import {
  Search as SearchIcon,
  Download as DownloadIcon,
  GitHub as GitHubIcon,
  Person as PersonIcon,
  Code as CodeIcon,
  Star as StarIcon,
  CallSplit as ForkIcon,
  CalendarToday as CalendarIcon,
  Language as LanguageIcon,
} from '@mui/icons-material';
import { useMutation } from '@tanstack/react-query';
import { analyzeGitHub } from '../services/api';
import toast from 'react-hot-toast';

interface GitHubAnalysisResult {
  username: string;
  threat_level: string;
  threat_score: number;
  followers_count: number;
  public_repos_count: number;
  total_stars: number;
  total_forks: number;
  top_language: string;
  repos_with_issues: number;
  repos_with_pull_requests: number;
  repos_with_wiki: number;
  repos_with_pages: number;
  account_age_days: number;
  recent_commits: number;
  recent_issues: number;
  recent_pull_requests: number;
  recent_releases: number;
  threat_indicators?: Array<{
    type: string;
    description: string;
    severity?: string;
  }>;
  recommendations?: Array<{
    category: string;
    description: string;
    priority?: string;
  }>;
}

export const GitHubAnalysis: React.FC = () => {
  const [username, setUsername] = useState('');
  const [analysisResults, setAnalysisResults] = useState<GitHubAnalysisResult | null>(null);

  // GitHub analysis mutation
  const analysisMutation = useMutation({
    mutationFn: (data: { username: string }) => analyzeGitHub({
      username: data.username,
      analysis_depth: 'comprehensive',
    }),
    onSuccess: (data) => {
      setAnalysisResults(data.data);
      toast.success('GitHub analysis completed successfully');
    },
    onError: (error) => {
      toast.error('Failed to analyze GitHub profile');
      console.error('GitHub analysis error:', error);
    },
  });

  const handleAnalyze = () => {
    if (!username.trim()) {
      toast.error('Please enter a GitHub username');
      return;
    }
    analysisMutation.mutate({
      username: username.trim(),
    });
  };

  const handleExport = () => {
    if (analysisResults) {
      const dataStr = JSON.stringify(analysisResults, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `github-analysis-${username}-${new Date().toISOString().split('T')[0]}.json`;
      link.click();
      URL.revokeObjectURL(url);
    }
  };

  const getThreatLevelColor = (level: string) => {
    switch (level) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" fontWeight={600}>
          GitHub Analysis
        </Typography>
      </Box>

      {/* Input Form */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Analyze GitHub Profile
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-end', mb: 3 }}>
            <TextField
              fullWidth
              label="GitHub Username"
              placeholder="Enter GitHub username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={analysisMutation.isPending}
            />
            <Button
              variant="contained"
              startIcon={<SearchIcon />}
              onClick={handleAnalyze}
              disabled={analysisMutation.isPending || !username.trim()}
            >
              {analysisMutation.isPending ? 'Analyzing...' : 'Analyze'}
            </Button>
          </Box>
        </CardContent>
      </Card>

      {/* Loading State */}
      {analysisMutation.isPending && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Analyzing GitHub Profile
            </Typography>
            <LinearProgress />
            <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
              Gathering profile data, analyzing repositories, and assessing activity patterns...
            </Typography>
          </CardContent>
        </Card>
      )}

      {/* Results */}
      {analysisResults && (
        <Box>
          {/* Export Button */}
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
            <Button
              variant="outlined"
              startIcon={<DownloadIcon />}
              onClick={handleExport}
            >
              Export Report
            </Button>
          </Box>

          {/* Profile Overview */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Profile Overview
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 2, alignItems: 'center' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <GitHubIcon color="primary" sx={{ fontSize: 40 }} />
                  <Box>
                    <Typography variant="h5" fontWeight={600}>
                      {analysisResults.username}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      GitHub User
                    </Typography>
                  </Box>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Threat Level
                  </Typography>
                  <Chip
                    label={analysisResults.threat_level.toUpperCase()}
                    color={getThreatLevelColor(analysisResults.threat_level) as any}
                  />
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Threat Score
                  </Typography>
                  <Typography variant="h4" color={getThreatLevelColor(analysisResults.threat_level)}>
                    {analysisResults.threat_score}/10
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Key Metrics */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Key Metrics
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 3 }}>
                <Box sx={{ textAlign: 'center' }}>
                  <PersonIcon color="primary" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h4" fontWeight={600}>
                    {analysisResults.followers_count}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Followers
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <CodeIcon color="primary" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h4" fontWeight={600}>
                    {analysisResults.public_repos_count}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Public Repos
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <StarIcon color="primary" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h4" fontWeight={600}>
                    {analysisResults.total_stars}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Total Stars
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <ForkIcon color="primary" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h4" fontWeight={600}>
                    {analysisResults.total_forks}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Total Forks
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Repository Analysis */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Repository Analysis
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 3 }}>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Most Used Language
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LanguageIcon color="primary" />
                    <Typography variant="h6">
                      {analysisResults.top_language || 'N/A'}
                    </Typography>
                  </Box>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                    Repository Statistics
                  </Typography>
                  <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: 2 }}>
                    <Box>
                      <Typography variant="h6" color="primary">
                        {analysisResults.repos_with_issues}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Repos with Issues
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="h6" color="primary">
                        {analysisResults.repos_with_pull_requests}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Repos with PRs
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="h6" color="primary">
                        {analysisResults.repos_with_wiki}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Repos with Wiki
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="h6" color="primary">
                        {analysisResults.repos_with_pages}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Repos with Pages
                      </Typography>
                    </Box>
                  </Box>
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Activity Analysis */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Activity Analysis
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 3 }}>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Account Age
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <CalendarIcon color="primary" />
                    <Typography variant="h6">
                      {analysisResults.account_age_days} days
                    </Typography>
                  </Box>
                </Box>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                    Recent Activity
                  </Typography>
                  <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: 2 }}>
                    <Box>
                      <Typography variant="h6" color="primary">
                        {analysisResults.recent_commits}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Recent Commits
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="h6" color="primary">
                        {analysisResults.recent_issues}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Recent Issues
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="h6" color="primary">
                        {analysisResults.recent_pull_requests}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Recent PRs
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="h6" color="primary">
                        {analysisResults.recent_releases}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Recent Releases
                      </Typography>
                    </Box>
                  </Box>
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Threat Indicators */}
          {analysisResults.threat_indicators && analysisResults.threat_indicators.length > 0 && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Threat Indicators
                </Typography>
                <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 2 }}>
                  {analysisResults.threat_indicators.map((indicator, index) => (
                    <Box key={index} sx={{ p: 2, border: 1, borderColor: 'warning.main', borderRadius: 1 }}>
                      <Typography variant="subtitle2" color="warning.main" gutterBottom>
                        {indicator.type}
                      </Typography>
                      <Typography variant="body2">
                        {indicator.description}
                      </Typography>
                      {indicator.severity && (
                        <Chip
                          label={indicator.severity}
                          color="warning"
                          size="small"
                          sx={{ mt: 1 }}
                        />
                      )}
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}

          {/* Recommendations */}
          {analysisResults.recommendations && analysisResults.recommendations.length > 0 && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Recommendations
                </Typography>
                <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 2 }}>
                  {analysisResults.recommendations.map((recommendation, index) => (
                    <Box key={index} sx={{ p: 2, border: 1, borderColor: 'info.main', borderRadius: 1 }}>
                      <Typography variant="subtitle2" color="info.main" gutterBottom>
                        {recommendation.category}
                      </Typography>
                      <Typography variant="body2">
                        {recommendation.description}
                      </Typography>
                      {recommendation.priority && (
                        <Chip
                          label={recommendation.priority}
                          color="info"
                          size="small"
                          sx={{ mt: 1 }}
                        />
                      )}
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}
        </Box>
      )}
    </Box>
  );
}; 