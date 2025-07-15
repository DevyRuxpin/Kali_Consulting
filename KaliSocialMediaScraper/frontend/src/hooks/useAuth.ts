import { useState, useEffect, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import { login, register, getCurrentUser, logout, updateProfile, changePassword } from '../services/api';
import { handleApiError } from '../utils/errorHandler';
import type { User } from '../types';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  const queryClient = useQueryClient();

  // Get stored token
  const getStoredToken = (): string | null => {
    return localStorage.getItem('access_token');
  };

  // Set token in storage
  const setStoredToken = (token: string): void => {
    localStorage.setItem('access_token', token);
  };

  // Remove token from storage
  const removeStoredToken = (): void => {
    localStorage.removeItem('access_token');
  };

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: (credentials: LoginCredentials) => login(credentials.username, credentials.password),
    onSuccess: (response) => {
      if (response.status === 'success' && response.data?.access_token) {
        const { access_token, user } = response.data;
        setStoredToken(access_token);
        
        setAuthState({
          user,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        });
        
        toast.success('Login successful');
        queryClient.invalidateQueries({ queryKey: ['user'] });
      } else {
        setAuthState(prev => ({
          ...prev,
          isLoading: false,
          error: 'Login failed',
        }));
        toast.error('Login failed');
      }
    },
    onError: (error) => {
      const errorInfo = handleApiError(error, { component: 'useAuth', action: 'login' });
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: errorInfo.message,
      }));
    },
  });

  // Register mutation
  const registerMutation = useMutation({
    mutationFn: (userData: RegisterData) => register(userData),
    onSuccess: (response) => {
      if (response.status === 'success') {
        toast.success('Registration successful! Please log in.');
      } else {
        toast.error('Registration failed');
      }
    },
    onError: (error) => {
      const errorInfo = handleApiError(error, { component: 'useAuth', action: 'register' });
      toast.error(errorInfo.message);
    },
  });

  // Logout mutation
  const logoutMutation = useMutation({
    mutationFn: logout,
    onSuccess: () => {
      removeStoredToken();
      setAuthState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
      queryClient.clear();
      toast.success('Logged out successfully');
    },
    onError: (error) => {
      const errorInfo = handleApiError(error, { component: 'useAuth', action: 'logout' });
      toast.error(errorInfo.message);
    },
  });

  // Update profile mutation
  const updateProfileMutation = useMutation({
    mutationFn: (userData: Partial<{ full_name: string; email: string }>) => updateProfile(userData),
    onSuccess: (response) => {
      if (response.status === 'success' && response.data?.user) {
        setAuthState(prev => ({
          ...prev,
          user: response.data.user,
        }));
        toast.success('Profile updated successfully');
        queryClient.invalidateQueries({ queryKey: ['user'] });
      }
    },
    onError: (error) => {
      const errorInfo = handleApiError(error, { component: 'useAuth', action: 'updateProfile' });
      toast.error(errorInfo.message);
    },
  });

  // Change password mutation
  const changePasswordMutation = useMutation({
    mutationFn: (passwordData: { old_password: string; new_password: string }) => changePassword(passwordData),
    onSuccess: () => {
      toast.success('Password changed successfully');
    },
    onError: (error) => {
      const errorInfo = handleApiError(error, { component: 'useAuth', action: 'changePassword' });
      toast.error(errorInfo.message);
    },
  });

  // Get current user query
  const { isLoading: isLoadingUser } = useQuery({
    queryKey: ['user'],
    queryFn: getCurrentUser,
    enabled: !!getStoredToken(),
    retry: false,
  });

  // Initialize auth state
  useEffect(() => {
    const token = getStoredToken();
    if (token) {
      // setAuthHeader(token); // This line was removed as per the edit hint
    } else {
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
      }));
    }
  }, []);

  // Manual login function
  const loginUser = useCallback((credentials: LoginCredentials) => {
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));
    loginMutation.mutate(credentials);
  }, [loginMutation]);

  // Manual register function
  const registerUser = useCallback((userData: RegisterData) => {
    registerMutation.mutate(userData);
  }, [registerMutation]);

  // Manual logout function
  const logoutUser = useCallback(() => {
    logoutMutation.mutate();
  }, [logoutMutation]);

  // Manual update profile function
  const updateUserProfile = useCallback((userData: Partial<{ full_name: string; email: string }>) => {
    updateProfileMutation.mutate(userData);
  }, [updateProfileMutation]);

  // Manual change password function
  const changeUserPassword = useCallback((passwordData: { old_password: string; new_password: string }) => {
    changePasswordMutation.mutate(passwordData);
  }, [changePasswordMutation]);

  return {
    // State
    user: authState.user,
    isAuthenticated: authState.isAuthenticated,
    isLoading: authState.isLoading || isLoadingUser,
    error: authState.error,
    
    // Actions
    login: loginUser,
    register: registerUser,
    logout: logoutUser,
    updateProfile: updateUserProfile,
    changePassword: changeUserPassword,
    
    // Mutation states
    isLoggingIn: loginMutation.isPending,
    isRegistering: registerMutation.isPending,
    isLoggingOut: logoutMutation.isPending,
    isUpdatingProfile: updateProfileMutation.isPending,
    isChangingPassword: changePasswordMutation.isPending,
  };
}; 