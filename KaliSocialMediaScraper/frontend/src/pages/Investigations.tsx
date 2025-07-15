import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  TextField,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
} from '@mui/material';
import {
  Add as AddIcon,
  Visibility as ViewIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getInvestigations, createInvestigation, deleteInvestigation } from '../services/api';
import toast from 'react-hot-toast';
import type { InvestigationFormData } from '../types';
import { LoadingSpinner } from '../components/LoadingSpinner';

export const Investigations: React.FC = () => {
  const queryClient = useQueryClient();
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);

  // Investigations query
  const { data: investigations, isLoading, error, refetch } = useQuery({
    queryKey: ['investigations'],
    queryFn: () => getInvestigations(),
    retry: 1,
    refetchOnWindowFocus: false,
  });

  // Create investigation mutation
  const createMutation = useMutation({
    mutationFn: createInvestigation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['investigations'] });
      setIsCreateDialogOpen(false);
      toast.success('Investigation created successfully');
    },
    onError: (error) => {
      toast.error('Failed to create investigation');
      console.error('Create investigation error:', error);
    },
  });

  // Delete investigation mutation
  const deleteMutation = useMutation({
    mutationFn: deleteInvestigation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['investigations'] });
      toast.success('Investigation deleted successfully');
    },
    onError: (error) => {
      toast.error('Failed to delete investigation');
      console.error('Delete investigation error:', error);
    },
  });

  const handleCreateInvestigation = (formData: InvestigationFormData) => {
    createMutation.mutate(formData);
  };

  const handleDeleteInvestigation = (id: string) => {
    if (window.confirm('Are you sure you want to delete this investigation?')) {
      deleteMutation.mutate(id);
    }
  };

  const handleRefresh = () => {
    refetch();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'processing':
        return 'warning';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  // Show loading state
  if (isLoading) {
    return <LoadingSpinner message="Loading investigations..." />;
  }

  // Show error state
  if (error) {
    return (
      <Box>
        <Typography variant="h4" component="h1" fontWeight={600} gutterBottom>
          Investigations
        </Typography>
        <Alert 
          severity="error" 
          sx={{ mb: 2 }}
          action={
            <Button color="inherit" size="small" onClick={handleRefresh}>
              Retry
            </Button>
          }
        >
          Failed to load investigations: {error instanceof Error ? error.message : 'Unknown error'}
        </Alert>
        
        {/* Show offline mode content */}
        <Alert severity="info" sx={{ mb: 3 }}>
          Running in offline mode. Some features may be limited.
        </Alert>
        
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              No Investigations Available
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Investigations will appear here once the backend service is available.
            </Typography>
          </CardContent>
        </Card>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" fontWeight={600}>
          Investigations
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={handleRefresh}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setIsCreateDialogOpen(true)}
          >
            New Investigation
          </Button>
        </Box>
      </Box>

      {/* Statistics Cards */}
      <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 3, mb: 3 }}>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Total Investigations
            </Typography>
            <Typography variant="h4">
              {investigations?.length || 0}
            </Typography>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Completed
            </Typography>
            <Typography variant="h4" color="success.main">
              {investigations?.filter((inv: any) => inv.status === 'completed').length || 0}
            </Typography>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Processing
            </Typography>
            <Typography variant="h4" color="warning.main">
              {investigations?.filter((inv: any) => inv.status === 'processing').length || 0}
            </Typography>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Failed
            </Typography>
            <Typography variant="h4" color="error.main">
              {investigations?.filter((inv: any) => inv.status === 'failed').length || 0}
            </Typography>
          </CardContent>
        </Card>
      </Box>

      {/* Investigations Table */}
      <Card>
        <CardContent>
          {investigations && investigations.length > 0 ? (
            <TableContainer component={Paper} variant="outlined">
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Title</TableCell>
                    <TableCell>Target</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Priority</TableCell>
                    <TableCell>Created</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {investigations.map((investigation: any) => (
                    <TableRow key={investigation.id}>
                      <TableCell>
                        <Typography variant="subtitle2" fontWeight={600}>
                          {investigation.title}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          {investigation.description}
                        </Typography>
                      </TableCell>
                      <TableCell>{investigation.target_value}</TableCell>
                      <TableCell>
                        <Chip
                          label={investigation.target_type}
                          size="small"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={investigation.status}
                          color={getStatusColor(investigation.status) as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={investigation.priority || 'medium'}
                          color={getPriorityColor(investigation.priority || 'medium') as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        {new Date(investigation.created_at).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          <IconButton size="small" color="primary">
                            <ViewIcon />
                          </IconButton>
                          <IconButton size="small" color="primary">
                            <EditIcon />
                          </IconButton>
                          <IconButton 
                            size="small" 
                            color="error"
                            onClick={() => handleDeleteInvestigation(investigation.id)}
                          >
                            <DeleteIcon />
                          </IconButton>
                        </Box>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          ) : (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Typography variant="h6" color="textSecondary" gutterBottom>
                No Investigations Found
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Create your first investigation to get started.
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Create Investigation Dialog */}
      <CreateInvestigationDialog
        open={isCreateDialogOpen}
        onClose={() => setIsCreateDialogOpen(false)}
        onSubmit={handleCreateInvestigation}
        isLoading={createMutation.isPending}
      />
    </Box>
  );
};

// Create Investigation Dialog Component
interface CreateInvestigationDialogProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: InvestigationFormData) => void;
  isLoading: boolean;
}

const CreateInvestigationDialog: React.FC<CreateInvestigationDialogProps> = ({
  open,
  onClose,
  onSubmit,
  isLoading,
}) => {
  const [formData, setFormData] = useState<Partial<InvestigationFormData>>({
    target_type: 'domain',
    analysis_depth: 'standard',
    platforms: [],
    include_network_analysis: true,
    include_timeline_analysis: true,
    include_threat_assessment: true,
    analysis_options: {},
    search_timeframe: '30d',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.target_type && formData.target_value) {
      onSubmit(formData as InvestigationFormData);
    }
  };

  const handleReset = () => {
    setFormData({
      target_type: 'domain',
      analysis_depth: 'standard',
      platforms: [],
      include_network_analysis: true,
      include_timeline_analysis: true,
      include_threat_assessment: true,
      analysis_options: {},
      search_timeframe: '30d',
    });
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Create New Investigation</DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Target Value"
              placeholder="Enter domain, username, email, etc."
              value={formData.target_value || ''}
              onChange={(e) => setFormData({ ...formData, target_value: e.target.value })}
              required
              fullWidth
            />
            
            <FormControl fullWidth>
              <InputLabel>Target Type</InputLabel>
              <Select
                value={formData.target_type || 'domain'}
                onChange={(e) => setFormData({ ...formData, target_type: e.target.value as any })}
                label="Target Type"
              >
                <MenuItem value="domain">Domain</MenuItem>
                <MenuItem value="email">Email</MenuItem>
                <MenuItem value="username">Username</MenuItem>
                <MenuItem value="phone">Phone</MenuItem>
                <MenuItem value="ip_address">IP Address</MenuItem>
                <MenuItem value="organization">Organization</MenuItem>
                <MenuItem value="person">Person</MenuItem>
                <MenuItem value="repository">Repository</MenuItem>
                <MenuItem value="github_repository">GitHub Repository</MenuItem>
                <MenuItem value="social_media">Social Media</MenuItem>
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>Analysis Depth</InputLabel>
              <Select
                value={formData.analysis_depth || 'standard'}
                onChange={(e) => setFormData({ ...formData, analysis_depth: e.target.value as any })}
                label="Analysis Depth"
              >
                <MenuItem value="basic">Basic</MenuItem>
                <MenuItem value="standard">Standard</MenuItem>
                <MenuItem value="deep">Deep</MenuItem>
                <MenuItem value="comprehensive">Comprehensive</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleReset} disabled={isLoading}>
            Reset
          </Button>
          <Button onClick={onClose} disabled={isLoading}>
            Cancel
          </Button>
          <Button type="submit" variant="contained" disabled={isLoading}>
            {isLoading ? 'Creating...' : 'Create Investigation'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}; 