import { toast } from 'react-hot-toast';

export interface ApiError {
  status: number;
  message: string;
  details?: any;
  timestamp: string;
}

export interface ErrorContext {
  component?: string;
  action?: string;
  userId?: string;
  timestamp: string;
}

export class ErrorHandler {
  private static instance: ErrorHandler;
  private errorLog: ApiError[] = [];
  private maxLogSize = 100;

  private constructor() {}

  static getInstance(): ErrorHandler {
    if (!ErrorHandler.instance) {
      ErrorHandler.instance = new ErrorHandler();
    }
    return ErrorHandler.instance;
  }

  /**
   * Handle API errors with appropriate user feedback
   */
  handleApiError(error: any, context?: Partial<ErrorContext>): ApiError {
    const errorInfo: ApiError = {
      status: this.getErrorStatus(error),
      message: this.getErrorMessage(error),
      details: this.getErrorDetails(error),
      timestamp: new Date().toISOString()
    };

    // Log the error
    this.logError(errorInfo, context);

    // Show appropriate user feedback
    this.showUserFeedback(errorInfo);

    return errorInfo;
  }

  /**
   * Handle network errors
   */
  handleNetworkError(error: any, context?: Partial<ErrorContext>): ApiError {
    const networkError: ApiError = {
      status: 0,
      message: 'Network connection error. Please check your internet connection.',
      details: error,
      timestamp: new Date().toISOString()
    };

    this.logError(networkError, context);
    this.showUserFeedback(networkError);

    return networkError;
  }

  /**
   * Handle validation errors
   */
  handleValidationError(errors: any, context?: Partial<ErrorContext>): ApiError {
    const validationError: ApiError = {
      status: 400,
      message: 'Validation failed. Please check your input.',
      details: errors,
      timestamp: new Date().toISOString()
    };

    this.logError(validationError, context);
    this.showUserFeedback(validationError);

    return validationError;
  }

  /**
   * Handle authentication errors
   */
  handleAuthError(error: any, context?: Partial<ErrorContext>): ApiError {
    const authError: ApiError = {
      status: 401,
      message: 'Authentication required. Please log in again.',
      details: error,
      timestamp: new Date().toISOString()
    };

    this.logError(authError, context);
    this.showUserFeedback(authError);

    return authError;
  }

  /**
   * Handle permission errors
   */
  handlePermissionError(error: any, context?: Partial<ErrorContext>): ApiError {
    const permissionError: ApiError = {
      status: 403,
      message: 'You do not have permission to perform this action.',
      details: error,
      timestamp: new Date().toISOString()
    };

    this.logError(permissionError, context);
    this.showUserFeedback(permissionError);

    return permissionError;
  }

  /**
   * Handle rate limiting errors
   */
  handleRateLimitError(error: any, context?: Partial<ErrorContext>): ApiError {
    const rateLimitError: ApiError = {
      status: 429,
      message: 'Rate limit exceeded. Please try again later.',
      details: error,
      timestamp: new Date().toISOString()
    };

    this.logError(rateLimitError, context);
    this.showUserFeedback(rateLimitError);

    return rateLimitError;
  }

  /**
   * Handle server errors
   */
  handleServerError(error: any, context?: Partial<ErrorContext>): ApiError {
    const serverError: ApiError = {
      status: 500,
      message: 'Server error occurred. Please try again later.',
      details: error,
      timestamp: new Date().toISOString()
    };

    this.logError(serverError, context);
    this.showUserFeedback(serverError);

    return serverError;
  }

  /**
   * Get error status code
   */
  private getErrorStatus(error: any): number {
    if (error?.response?.status) {
      return error.response.status;
    }
    if (error?.status) {
      return error.status;
    }
    return 500;
  }

  /**
   * Get user-friendly error message
   */
  private getErrorMessage(error: any): string {
    // Check for axios error response
    if (error?.response?.data?.detail) {
      return error.response.data.detail;
    }
    if (error?.response?.data?.message) {
      return error.response.data.message;
    }
    if (error?.message) {
      return error.message;
    }
    return 'An unexpected error occurred.';
  }

  /**
   * Get error details for debugging
   */
  private getErrorDetails(error: any): any {
    return {
      originalError: error,
      response: error?.response?.data,
      status: error?.response?.status,
      headers: error?.response?.headers
    };
  }

  /**
   * Log error for debugging
   */
  private logError(error: ApiError, context?: Partial<ErrorContext>): void {
    const logEntry = {
      ...error,
      context: {
        ...context,
        timestamp: new Date().toISOString()
      }
    };

    // Add to error log
    this.errorLog.push(logEntry);
    if (this.errorLog.length > this.maxLogSize) {
      this.errorLog.shift();
    }

    // Log to console in development
    if (import.meta.env.DEV) {
      console.error('API Error:', logEntry);
    }

    // TODO: Send to error tracking service in production
    // this.sendToErrorTracking(logEntry);
  }

  /**
   * Show appropriate user feedback based on error type
   */
  private showUserFeedback(error: ApiError): void {
    const { status, message } = error;

    switch (status) {
      case 400:
        toast.error(`Invalid request: ${message}`);
        break;
      case 401:
        toast.error('Please log in to continue');
        // TODO: Redirect to login
        break;
      case 403:
        toast.error('You do not have permission for this action');
        break;
      case 404:
        toast.error('Resource not found');
        break;
      case 429:
        toast.error('Too many requests. Please wait a moment.');
        break;
      case 500:
        toast.error('Server error. Please try again later.');
        break;
      default:
        toast.error(message);
    }
  }

  /**
   * Get error log for debugging
   */
  getErrorLog(): ApiError[] {
    return [...this.errorLog];
  }

  /**
   * Clear error log
   */
  clearErrorLog(): void {
    this.errorLog = [];
  }

  /**
   * Check if error is retryable
   */
  isRetryableError(error: ApiError): boolean {
    const retryableStatuses = [408, 429, 500, 502, 503, 504];
    return retryableStatuses.includes(error.status);
  }

  /**
   * Get retry delay for rate limit errors
   */
  getRetryDelay(error: ApiError): number {
    if (error.status === 429) {
      // Parse Retry-After header if available
      const retryAfter = error.details?.headers?.['retry-after'];
      if (retryAfter) {
        return parseInt(retryAfter) * 1000;
      }
      return 5000; // Default 5 seconds
    }
    return 1000; // Default 1 second
  }
}

// Export singleton instance
export const errorHandler = ErrorHandler.getInstance();

// Export convenience functions
export const handleApiError = (error: any, context?: Partial<ErrorContext>) => 
  errorHandler.handleApiError(error, context);

export const handleNetworkError = (error: any, context?: Partial<ErrorContext>) => 
  errorHandler.handleNetworkError(error, context);

export const handleValidationError = (errors: any, context?: Partial<ErrorContext>) => 
  errorHandler.handleValidationError(errors, context);

export const handleAuthError = (error: any, context?: Partial<ErrorContext>) => 
  errorHandler.handleAuthError(error, context);

export const handlePermissionError = (error: any, context?: Partial<ErrorContext>) => 
  errorHandler.handlePermissionError(error, context);

export const handleRateLimitError = (error: any, context?: Partial<ErrorContext>) => 
  errorHandler.handleRateLimitError(error, context);

export const handleServerError = (error: any, context?: Partial<ErrorContext>) => 
  errorHandler.handleServerError(error, context); 