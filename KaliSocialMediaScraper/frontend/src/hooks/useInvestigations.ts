import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import { 
  getInvestigations, 
  createInvestigation, 
  getInvestigation, 
  deleteInvestigation 
} from '../services/api';
import type { InvestigationFormData } from '../types';

export const useInvestigations = (filters?: {
  status?: string;
  targetType?: string;
  skip?: number;
  limit?: number;
}) => {

  // Fetch investigations
  const {
    data: investigations,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ['investigations', filters],
    queryFn: () => getInvestigations(
      filters?.skip || 0,
      filters?.limit || 100,
      filters?.status,
      filters?.targetType
    ),
  });

  // Create investigation mutation
  const createMutation = useMutation({
    mutationFn: (data: InvestigationFormData) => createInvestigation(data),
    onSuccess: () => {
      useQueryClient().invalidateQueries({ queryKey: ['investigations'] });
      toast.success('Investigation created successfully');
    },
    onError: (error) => {
      toast.error('Failed to create investigation');
      console.error('Create investigation error:', error);
    },
  });

  // Delete investigation mutation
  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteInvestigation(id),
    onSuccess: () => {
      useQueryClient().invalidateQueries({ queryKey: ['investigations'] });
      toast.success('Investigation deleted successfully');
    },
    onError: (error) => {
      toast.error('Failed to delete investigation');
      console.error('Delete investigation error:', error);
    },
  });

  return {
    investigations,
    isLoading,
    error,
    refetch,
    createInvestigation: createMutation.mutate,
    deleteInvestigation: deleteMutation.mutate,
    isCreating: createMutation.isPending,
    isDeleting: deleteMutation.isPending,
  };
};

export const useInvestigation = (id: string) => {
  const {
    data: investigation,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ['investigation', id],
    queryFn: () => getInvestigation(id),
    enabled: !!id,
  });

  return {
    investigation,
    isLoading,
    error,
    refetch,
  };
}; 