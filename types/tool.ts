import { ReactNode } from "react";

// Base tool interface
export interface Tool {
  id: string;
  name: string;
  title: string;
  href: string;
  description: string;
  category: ToolCategories;
  rating: number;
  users: string;
  icon: string | ReactNode;
  featured: boolean;
  tags: string[];
  premium?: boolean;
  new?: boolean;
  popular?: boolean;
  fileTypes?: string[];
  maxFileSize?: string;
  processingTime?: string;
}

// Tool category interface
export interface ToolCategory {
  id: string;
  name: string;
  description: string;
  icon: string | ReactNode;
  toolCount: number;
  tools?: Tool[];
  color?: string;
}

// Filter and search options
export interface FilterOptions {
  searchQuery: string;
  selectedCategory: string;
  showFeaturedOnly?: boolean;
  showPremiumOnly?: boolean;
  showNewOnly?: boolean;
  sortBy?: 'name' | 'rating' | 'users' | 'recent';
  sortOrder?: 'asc' | 'desc';
}

// View mode options
export interface ViewModeOptions {
  mode: "grid" | "list";
  itemsPerPage?: number;
  showFilters?: boolean;
}

// Tool categories enum - Updated to use slug-based categories
export type ToolCategories = 
  | "All"
  | "pdf-management"
  | "image-tools"
  | "text-tools"
  | "calculators"
  | "developer-tools"
  // Legacy categories for backward compatibility
  | "PDF Management" 
  | "Edit & Annotate PDF"
  | "PDF Conversion"
  | "OCR"
  | "Conversion"
  | "AI"
  | "Image Tools"
  | "Text Tools"
  | "Calculators";

// File processing interfaces
export interface ProcessingFile {
  id: string;
  file: File;
  status: 'pending' | 'uploading' | 'processing' | 'completed' | 'error';
  progress: number;
  taskId?: string;
  downloadUrl?: string;
  error?: string | undefined;
  result?: any;
}

// Tool configuration
export interface ToolConfig {
  allowedFileTypes: string[];
  maxFileSize: number;
  maxFiles: number;
  requiresAuth?: boolean;
  isPremium?: boolean;
}

// API response types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// Tool usage statistics
export interface ToolStats {
  totalUsers: number;
  totalProcessed: number;
  averageRating: number;
  lastUpdated: Date;
}
