"use client";

import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Upload, X, FileText, AlertCircle, CheckCircle2, Download, Loader2 } from 'lucide-react';
import { useDropzone } from 'react-dropzone';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { useAppStore } from '@/lib/store';
import { apiService, UploadProgress, ProcessingOptions } from '@/lib/api';

interface ProcessingResult {
  downloadUrl?: string;
  taskId?: string;
  [key: string]: unknown;
}

interface EnhancedFileUploadProps {
  operation: string;
  onComplete?: (results: ProcessingResult[]) => void;
  options?: ProcessingOptions;
  acceptedTypes?: string[];
  maxSize?: number; // in MB
  maxFiles?: number;
  disabled?: boolean;
  className?: string;
}

interface ProcessingFile {
  id: string;
  file: File;
  progress: number;
  status: 'pending' | 'uploading' | 'processing' | 'completed' | 'error';
  error?: string | undefined;
  taskId?: string | undefined;
  downloadUrl?: string | undefined;
  result?: ProcessingResult;
}

const EnhancedFileUpload: React.FC<EnhancedFileUploadProps> = ({
  operation,
  onComplete,
  options = {},
  acceptedTypes = ['.pdf', '.docx', '.txt', '.jpg', '.png'],
  maxSize = 100, // 100MB default
  maxFiles = 5,
  disabled = false,
  className
}) => {
  const [files, setFiles] = useState<ProcessingFile[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const { canMakeRequest, incrementRequestCount } = useAppStore();

  const validateFile = (file: File): string | null => {
    // Rate limiting check
    if (!canMakeRequest()) {
      return 'Rate limit exceeded. Please wait before uploading more files.';
    }

    // File size check
    if (file.size > maxSize * 1024 * 1024) {
      return `File size must be less than ${maxSize}MB`;
    }

    // File type validation using API service
    const validation = apiService.validateFile(file);
    if (!validation.valid) {
      return validation.error || 'Invalid file';
    }

    return null;
  };

  const processFile = async (file: File, fileId: string) => {
    try {
      incrementRequestCount();
      
      const result = await apiService.processFiles(
        operation,
        [file],
        options,
        (progress: UploadProgress) => {
          setFiles(prev => prev.map(f =>
            f.id === fileId
              ? {
                  ...f,
                  progress: progress.progress,
                  status: progress.status,
                  taskId: progress.taskId,
                  error: progress.error ?? undefined
                }
              : f
          ));

          // Show progress toasts
          if (progress.status === 'completed') {
            toast.success(`${file.name} processed successfully!`);
          } else if (progress.status === 'error') {
            toast.error(`Failed to process ${file.name}: ${progress.error}`);
          }
        }
      );

      // Update file with result
      setFiles(prev => prev.map(f =>
        f.id === fileId
          ? {
              ...f,
              result,
              downloadUrl: result.downloadUrl,
              taskId: result.taskId,
              status: 'completed'
            }
          : f
      ));

      return result;

    } catch (error) {
      console.error('Processing error:', error);
      
      setFiles(prev => prev.map(f =>
        f.id === fileId
          ? {
              ...f,
              status: 'error',
              error: error instanceof Error ? error.message : 'Processing failed'
            }
          : f
      ));

      throw error;
    }
  };

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (disabled || isProcessing) return;

    if (files.length + acceptedFiles.length > maxFiles) {
      toast.error(`Maximum ${maxFiles} files allowed`);
      return;
    }

    setIsProcessing(true);

    const newFiles: ProcessingFile[] = [];
    const validFiles: File[] = [];

    // Validate and prepare files
    for (const file of acceptedFiles) {
      const error = validateFile(file);
      const id = `file_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

      if (error) {
        newFiles.push({
          id,
          file,
          progress: 0,
          status: 'error',
          error
        });
        toast.error(`${file.name}: ${error}`);
      } else {
        validFiles.push(file);
        newFiles.push({
          id,
          file,
          progress: 0,
          status: 'pending'
        });
      }
    }

    setFiles(prev => [...prev, ...newFiles]);

    // Process valid files
    const results: ProcessingResult[] = [];
    for (const file of validFiles) {
      const fileData = newFiles.find(f => f.file === file);
      if (fileData) {
        try {
          setFiles(prev => prev.map(f =>
            f.id === fileData.id ? { ...f, status: 'uploading' } : f
          ));

          const result = await processFile(file, fileData.id);
          results.push(result);
        } catch (error) {
          console.error(`Failed to process ${file.name}:`, error);
        }
      }
    }

    setIsProcessing(false);

    // Notify completion
    if (results.length > 0 && onComplete) {
      onComplete(results);
    }

    // Show summary toast
    const successCount = results.length;
    const totalCount = validFiles.length;
    if (successCount === totalCount && totalCount > 0) {
      toast.success(`All ${successCount} files processed successfully!`);
    } else if (successCount > 0) {
      toast.success(`${successCount} of ${totalCount} files processed successfully`);
    }

  }, [disabled, isProcessing, files.length, maxFiles, operation, options, onComplete, processFile, validateFile]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: acceptedTypes.reduce((acc, type) => {
      if (type.startsWith('.')) {
        // Handle file extensions
        const mimeTypes = {
          '.pdf': 'application/pdf',
          '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
          '.doc': 'application/msword',
          '.txt': 'text/plain',
          '.jpg': 'image/jpeg',
          '.jpeg': 'image/jpeg',
          '.png': 'image/png',
          '.gif': 'image/gif'
        };
        const mimeType = mimeTypes[type as keyof typeof mimeTypes];
        if (mimeType) {
          acc[mimeType] = [type];
        }
      }
      return acc;
    }, {} as Record<string, string[]>),
    maxSize: maxSize * 1024 * 1024,
    disabled: disabled || isProcessing
  });
  
  const { style, ...rootProps } = getRootProps();

  const downloadFile = async (file: ProcessingFile) => {
    if (!file.taskId && !file.downloadUrl) return;

    try {
      if (file.downloadUrl) {
        // Direct download URL
        const link = document.createElement('a');
        link.href = file.downloadUrl;
        link.download = file.file.name.replace(/\.[^/.]+$/, '') + '_processed.pdf';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else if (file.taskId) {
        // Download via API
        await apiService.downloadFile(file.taskId, file.file.name);
      }
      
      toast.success(`Downloaded ${file.file.name}`);
    } catch (error) {
      console.error('Download error:', error);
      toast.error('Failed to download file');
    }
  };

  const removeFile = (id: string) => {
    setFiles(prev => prev.filter(f => f.id !== id));
  };

  const clearCompleted = () => {
    setFiles(prev => prev.filter(f => f.status !== 'completed'));
  };

  const retryFile = async (fileId: string) => {
    const file = files.find(f => f.id === fileId);
    if (!file || file.status !== 'error') return;

    setFiles(prev => prev.map(f =>
      f.id === fileId ? { ...f, status: 'pending', error: undefined } : f
    ));

    try {
      await processFile(file.file, fileId);
    } catch (error) {
      console.error('Retry failed:', error);
    }
  };

  const getFileIcon = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'pdf':
        return <FileText className="h-5 w-5 text-red-500" />;
      case 'docx':
      case 'doc':
        return <FileText className="h-5 w-5 text-blue-500" />;
      case 'jpg':
      case 'jpeg':
      case 'png':
      case 'gif':
        return <FileText className="h-5 w-5 text-green-500" />;
      default:
        return <FileText className="h-5 w-5 text-gray-500" />;
    }
  };

  const completedFiles = files.filter(f => f.status === 'completed');
  const processingFiles = files.filter(f => f.status === 'uploading' || f.status === 'processing');

  return (
    <div className={cn("w-full space-y-6", className)}>
      {/* Drop Zone */}
      <motion.div
        whileHover={{ scale: disabled || isProcessing ? 1 : 1.02 }}
        className={cn(
          "relative border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-300",
          isDragActive && !disabled && !isProcessing
            ? "border-blue-500 bg-blue-50 dark:bg-blue-950/20"
            : "border-gray-300 hover:border-gray-400 dark:border-gray-600",
          (disabled || isProcessing) && "opacity-50 cursor-not-allowed",
          "focus-within:ring-2 focus-within:ring-blue-500 focus-within:ring-offset-2"
        )}
        onClick={rootProps.onClick}
        onKeyDown={rootProps.onKeyDown}
        tabIndex={rootProps.tabIndex}
        role={rootProps.role}
        ref={rootProps['ref'] as React.Ref<HTMLDivElement>}
      >
        <input {...getInputProps()} />
        
        <div className="space-y-4">
          <motion.div
            animate={isDragActive ? { scale: 1.1 } : { scale: 1 }}
            className="mx-auto w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center"
          >
            {isProcessing ? (
              <Loader2 className="h-6 w-6 text-blue-500 animate-spin" />
            ) : (
              <Upload className={cn(
                "h-6 w-6",
                isDragActive ? "text-blue-600" : "text-blue-500"
              )} />
            )}
          </motion.div>
          
          <div>
            <p className="text-lg font-medium text-gray-900 dark:text-gray-100">
              {isProcessing
                ? "Processing files..."
                : isDragActive
                ? "Drop files here"
                : `Upload files for ${operation}`}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              {isProcessing
                ? "Please wait while we process your files"
                : "Drag and drop files here, or click to select"}
            </p>
            <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">
              Max {maxFiles} files, {maxSize}MB each. Supported: {acceptedTypes.join(', ')}
            </p>
          </div>
        </div>
      </motion.div>

      {/* Processing Queue */}
      {processingFiles.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100">
              Processing ({processingFiles.length})
            </h4>
          </div>
          
          <div className="space-y-2">
            {processingFiles.map((file) => (
              <motion.div
                key={file.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center space-x-3 p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg border border-blue-200 dark:border-blue-800"
              >
                {getFileIcon(file.file.name)}
                
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                    {file.file.name}
                  </p>
                  
                  {/* Progress Bar */}
                  <div className="mt-2">
                    <div className="flex items-center space-x-2">
                      <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <motion.div
                          className="bg-blue-500 h-2 rounded-full"
                          initial={{ width: 0 }}
                          animate={{ width: `${file.progress}%` }}
                          transition={{ duration: 0.3 }}
                        />
                      </div>
                      <span className="text-xs text-gray-500">
                        {Math.round(file.progress)}%
                      </span>
                    </div>
                    <p className="text-xs text-blue-600 dark:text-blue-400 mt-1">
                      {file.status === 'uploading' ? 'Uploading...' : 'Processing...'}
                    </p>
                  </div>
                </div>
                
                <Loader2 className="h-4 w-4 text-blue-500 animate-spin" />
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* File Results */}
      {files.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100">
              Files ({files.length})
            </h4>
            {completedFiles.length > 0 && (
              <button
                onClick={clearCompleted}
                className="text-xs text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
              >
                Clear completed
              </button>
            )}
          </div>
          
          <div className="space-y-2">
            {files.filter(f => f.status !== 'uploading' && f.status !== 'processing').map((file) => (
              <motion.div
                key={file.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className={cn(
                  "flex items-center space-x-3 p-3 rounded-lg border",
                  file.status === 'completed'
                    ? "bg-green-50 dark:bg-green-950/20 border-green-200 dark:border-green-800"
                    : file.status === 'error'
                    ? "bg-red-50 dark:bg-red-950/20 border-red-200 dark:border-red-800"
                    : "bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700"
                )}
              >
                {getFileIcon(file.file.name)}
                
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                    {file.file.name}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {(file.file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                  
                  {file.status === 'error' && file.error && (
                    <p className="text-xs text-red-500 mt-1">
                      {file.error}
                    </p>
                  )}
                </div>
                
                {/* Action buttons */}
                <div className="flex items-center space-x-2">
                  {file.status === 'completed' && (
                    <>
                      <CheckCircle2 className="h-4 w-4 text-green-500" />
                      <button
                        onClick={() => downloadFile(file)}
                        className="p-1 hover:bg-green-100 dark:hover:bg-green-900 rounded"
                        title="Download processed file"
                      >
                        <Download className="h-4 w-4 text-green-600" />
                      </button>
                    </>
                  )}
                  
                  {file.status === 'error' && (
                    <>
                      <AlertCircle className="h-4 w-4 text-red-500" />
                      <button
                        onClick={() => retryFile(file.id)}
                        className="text-xs text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300"
                      >
                        Retry
                      </button>
                    </>
                  )}
                  
                  <button
                    onClick={() => removeFile(file.id)}
                    className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded"
                  >
                    <X className="h-4 w-4 text-gray-500" />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default EnhancedFileUpload;
