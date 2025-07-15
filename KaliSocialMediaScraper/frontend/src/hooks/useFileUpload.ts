import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import { uploadFile, downloadFile } from '../services/api';
import { handleApiError } from '../utils/errorHandler';

export interface FileUploadOptions {
  maxSize?: number; // in bytes
  allowedTypes?: string[];
  multiple?: boolean;
}

export interface FileUploadResult {
  success: boolean;
  fileId?: string;
  url?: string;
  error?: string;
}

export interface FileDownloadOptions {
  filename?: string;
  showProgress?: boolean;
}

export const useFileUpload = (options: FileUploadOptions = {}) => {
  const {
    maxSize = 10 * 1024 * 1024, // 10MB default
    allowedTypes = ['image/*', 'application/pdf', 'text/csv', 'application/json'],
    multiple = false,
  } = options;

  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);

  // File validation
  const validateFile = useCallback((file: File): string | null => {
    // Check file size
    if (file.size > maxSize) {
      return `File size exceeds ${Math.round(maxSize / 1024 / 1024)}MB limit`;
    }

    // Check file type
    const isValidType = allowedTypes.some(type => {
      if (type.endsWith('/*')) {
        return file.type.startsWith(type.replace('/*', ''));
      }
      return file.type === type;
    });

    if (!isValidType) {
      return `File type ${file.type} is not allowed`;
    }

    return null;
  }, [maxSize, allowedTypes]);

  // Upload mutation
  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const error = validateFile(file);
      if (error) {
        throw new Error(error);
      }

      setIsUploading(true);
      setUploadProgress(0);

      try {
        const response = await uploadFile(file, '/uploads/');
        
        // Simulate progress (in real implementation, you'd track actual progress)
        const progressInterval = setInterval(() => {
          setUploadProgress(prev => {
            if (prev >= 90) {
              clearInterval(progressInterval);
              return 100;
            }
            return prev + 10;
          });
        }, 100);

        return response;
      } finally {
        setIsUploading(false);
        setUploadProgress(0);
      }
    },
    onSuccess: (response) => {
      if (response.status === 'success') {
        toast.success('File uploaded successfully');
      } else {
        toast.error('Upload failed');
      }
    },
    onError: (error) => {
      const errorInfo = handleApiError(error, { component: 'useFileUpload', action: 'upload' });
      toast.error(errorInfo.message);
    },
  });

  // Download mutation
  const downloadMutation = useMutation({
    mutationFn: async ({ endpoint, filename }: { endpoint: string; filename?: string }) => {
      await downloadFile(endpoint, filename);
    },
    onSuccess: () => {
      toast.success('File downloaded successfully');
    },
    onError: (error) => {
      const errorInfo = handleApiError(error, { component: 'useFileUpload', action: 'download' });
      toast.error(errorInfo.message);
    },
  });

  // Upload file
  const uploadFileHandler = useCallback(async (file: File): Promise<FileUploadResult> => {
    try {
      const result = await uploadMutation.mutateAsync(file);
      return {
        success: true,
        fileId: result.data?.file_id,
        url: result.data?.url,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Upload failed',
      };
    }
  }, [uploadMutation]);

  // Upload multiple files
  const uploadMultipleFiles = useCallback(async (files: File[]): Promise<FileUploadResult[]> => {
    const results: FileUploadResult[] = [];
    
    for (const file of files) {
      const result = await uploadFileHandler(file);
      results.push(result);
    }
    
    return results;
  }, [uploadFileHandler]);

  // Download file
  const downloadFileHandler = useCallback(async (endpoint: string, filename?: string) => {
    try {
      await downloadMutation.mutateAsync({ endpoint, filename });
    } catch (error) {
      console.error('Download failed:', error);
    }
  }, [downloadMutation]);

  // Create file input element
  const createFileInput = useCallback(() => {
    const input = document.createElement('input');
    input.type = 'file';
    input.multiple = multiple;
    input.accept = allowedTypes.join(',');
    return input;
  }, [multiple, allowedTypes]);

  // Trigger file selection
  const selectFiles = useCallback((): Promise<File[]> => {
    return new Promise((resolve) => {
      const input = createFileInput();
      
      input.onchange = (event) => {
        const target = event.target as HTMLInputElement;
        const files = Array.from(target.files || []);
        resolve(files);
      };
      
      input.click();
    });
  }, [createFileInput]);

  // Drag and drop handlers
  const handleDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.stopPropagation();
  }, []);

  const handleDrop = useCallback(async (event: React.DragEvent): Promise<FileUploadResult[]> => {
    event.preventDefault();
    event.stopPropagation();
    
    const files = Array.from(event.dataTransfer.files);
    return await uploadMultipleFiles(files);
  }, [uploadMultipleFiles]);

  return {
    // State
    uploadProgress,
    isUploading,
    isDownloading: downloadMutation.isPending,
    
    // Actions
    uploadFile: uploadFileHandler,
    uploadMultipleFiles,
    downloadFile: downloadFileHandler,
    selectFiles,
    
    // Drag and drop
    handleDragOver,
    handleDrop,
    
    // Validation
    validateFile,
    
    // Utilities
    createFileInput,
  };
}; 