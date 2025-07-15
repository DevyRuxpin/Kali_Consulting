// Email Validation
export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Domain Validation
export const validateDomain = (domain: string): boolean => {
  const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/;
  return domainRegex.test(domain);
};

// URL Validation
export const validateUrl = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

// IP Address Validation
export const validateIpAddress = (ip: string): boolean => {
  const ipv4Regex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  const ipv6Regex = /^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$/;
  
  return ipv4Regex.test(ip) || ipv6Regex.test(ip);
};

// Username Validation
export const validateUsername = (username: string): boolean => {
  const usernameRegex = /^[a-zA-Z0-9_-]{3,20}$/;
  return usernameRegex.test(username);
};

// Password Validation
export const validatePassword = (password: string): {
  isValid: boolean;
  errors: string[];
} => {
  const errors: string[] = [];
  
  if (password.length < 8) {
    errors.push('Password must be at least 8 characters long');
  }
  
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter');
  }
  
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter');
  }
  
  if (!/\d/.test(password)) {
    errors.push('Password must contain at least one number');
  }
  
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    errors.push('Password must contain at least one special character');
  }
  
  return {
    isValid: errors.length === 0,
    errors,
  };
};

// Phone Number Validation
export const validatePhoneNumber = (phone: string): boolean => {
  const phoneRegex = /^\+?[\d\s\-\(\)]{10,}$/;
  return phoneRegex.test(phone);
};

// Credit Card Validation (Luhn Algorithm)
export const validateCreditCard = (cardNumber: string): boolean => {
  const cleanNumber = cardNumber.replace(/\D/g, '');
  
  if (cleanNumber.length < 13 || cleanNumber.length > 19) {
    return false;
  }
  
  let sum = 0;
  let isEven = false;
  
  for (let i = cleanNumber.length - 1; i >= 0; i--) {
    let digit = parseInt(cleanNumber[i]);
    
    if (isEven) {
      digit *= 2;
      if (digit > 9) {
        digit -= 9;
      }
    }
    
    sum += digit;
    isEven = !isEven;
  }
  
  return sum % 10 === 0;
};

// File Validation
export const validateFile = (
  file: File,
  options: {
    maxSize?: number; // in bytes
    allowedTypes?: string[];
    maxFiles?: number;
  } = {}
): {
  isValid: boolean;
  errors: string[];
} => {
  const errors: string[] = [];
  const { maxSize = 10 * 1024 * 1024, allowedTypes = [] } = options;
  
  if (file.size > maxSize) {
    errors.push(`File size must be less than ${formatFileSize(maxSize)}`);
  }
  
  if (allowedTypes.length > 0 && !allowedTypes.includes(file.type)) {
    errors.push(`File type must be one of: ${allowedTypes.join(', ')}`);
  }
  
  return {
    isValid: errors.length === 0,
    errors,
  };
};

// Date Validation
export const validateDate = (date: string): boolean => {
  const dateObj = new Date(date);
  return dateObj instanceof Date && !isNaN(dateObj.getTime());
};

export const validateDateRange = (
  startDate: string,
  endDate: string
): {
  isValid: boolean;
  errors: string[];
} => {
  const errors: string[] = [];
  
  if (!validateDate(startDate)) {
    errors.push('Invalid start date');
  }
  
  if (!validateDate(endDate)) {
    errors.push('Invalid end date');
  }
  
  if (validateDate(startDate) && validateDate(endDate)) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    
    if (start >= end) {
      errors.push('Start date must be before end date');
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors,
  };
};

// Form Validation
export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  custom?: (value: any) => boolean | string;
}

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

export const validateField = (
  value: any,
  rules: ValidationRule
): ValidationResult => {
  const errors: string[] = [];
  
  // Required validation
  if (rules.required && (!value || value.toString().trim() === '')) {
    errors.push('This field is required');
  }
  
  if (value && value.toString().trim() !== '') {
    const stringValue = value.toString();
    
    // Min length validation
    if (rules.minLength && stringValue.length < rules.minLength) {
      errors.push(`Minimum length is ${rules.minLength} characters`);
    }
    
    // Max length validation
    if (rules.maxLength && stringValue.length > rules.maxLength) {
      errors.push(`Maximum length is ${rules.maxLength} characters`);
    }
    
    // Pattern validation
    if (rules.pattern && !rules.pattern.test(stringValue)) {
      errors.push('Invalid format');
    }
    
    // Custom validation
    if (rules.custom) {
      const customResult = rules.custom(value);
      if (typeof customResult === 'string') {
        errors.push(customResult);
      } else if (!customResult) {
        errors.push('Invalid value');
      }
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors,
  };
};

// Form Validation
export const validateForm = (
  data: Record<string, any>,
  schema: Record<string, ValidationRule>
): {
  isValid: boolean;
  errors: Record<string, string[]>;
} => {
  const errors: Record<string, string[]> = {};
  let isValid = true;
  
  for (const [field, rules] of Object.entries(schema)) {
    const fieldErrors = validateField(data[field], rules);
    if (!fieldErrors.isValid) {
      errors[field] = fieldErrors.errors;
      isValid = false;
    }
  }
  
  return { isValid, errors };
};

// Investigation Form Validation
export const validateInvestigationForm = (data: any): ValidationResult => {
  const errors: string[] = [];
  
  if (!data.title || data.title.trim() === '') {
    errors.push('Title is required');
  }
  
  if (!data.target_value || data.target_value.trim() === '') {
    errors.push('Target value is required');
  }
  
  if (!data.target_type) {
    errors.push('Target type is required');
  }
  
  if (data.target_type === 'domain' && !validateDomain(data.target_value)) {
    errors.push('Invalid domain format');
  }
  
  if (data.target_type === 'github' && !validateUsername(data.target_value)) {
    errors.push('Invalid GitHub username format');
  }
  
  return {
    isValid: errors.length === 0,
    errors,
  };
};

// Social Media Form Validation
export const validateSocialMediaForm = (data: any): ValidationResult => {
  const errors: string[] = [];
  
  if (!data.username || data.username.trim() === '') {
    errors.push('Username is required');
  }
  
  if (!data.platforms || data.platforms.length === 0) {
    errors.push('At least one platform must be selected');
  }
  
  if (data.max_posts && (data.max_posts < 1 || data.max_posts > 1000)) {
    errors.push('Max posts must be between 1 and 1000');
  }
  
  return {
    isValid: errors.length === 0,
    errors,
  };
};

// Utility function for file size formatting
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
}; 