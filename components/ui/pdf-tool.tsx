"use client";

import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { 
  Download, 
  Shield,
  Clock, 
  Zap,
  AlertCircle,
  CheckCircle2,
  Loader2
} from 'lucide-react';
import FileUpload from './file-upload';
import { useToast } from './toast';
import { cn } from '@/lib/utils';

interface PDFToolProps {
  toolId: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  acceptedTypes?: string[];
  maxFileSize?: number;
  processingOptions?: ProcessingOption[];
  onProcess?: (files: File[], options: Record<string, unknown>) => Promise<ProcessedFile[]>;
}

interface ProcessingOption {
  id: string;
  label: string;
  type: 'select' | 'slider' | 'toggle' | 'input';
  defaultValue: unknown;
  options?: { value: string; label: string }[];
  min?: number;
  max?: number;
  step?: number;
}

interface ProcessedFile {
  name: string;
  url: string;
  size: number;
  type: string;
}

const PDFTool: React.FC<PDFToolProps> = ({
  title,
  description,
  icon,
  acceptedTypes = ['.pdf'],
  maxFileSize = 10,
  processingOptions = [],
  onProcess
}) => {
  const [files, setFiles] = useState<File[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processedFiles, setProcessedFiles] = useState<ProcessedFile[]>([]);
  const [options, setOptions] = useState<Record<string, unknown>>({});
  const [processingProgress, setProcessingProgress] = useState(0);
  const { success, error, info } = useToast();

  // Initialize options with default values
  React.useEffect(() => {
    const initialOptions: Record<string, unknown> = {};
    processingOptions.forEach(option => {
      initialOptions[option.id] = option.defaultValue;
    });
    setOptions(initialOptions);
  }, [processingOptions]);

  const handleFileSelect = useCallback((selectedFiles: File[]) => {
    setFiles(selectedFiles);
    setProcessedFiles([]);
    info(`${selectedFiles.length} file(s) selected`, 'Ready to process');
  }, [info]);

  const simulateProcessing = async (): Promise<ProcessedFile[]> => {
    return new Promise((resolve) => {
      let progress = 0;
      const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress >= 100) {
          progress = 100;
          clearInterval(interval);
          setProcessingProgress(100);
          
          // Simulate processed files
          const processed: ProcessedFile[] = files.map((file) => ({
            name: `processed_${file.name}`,
            url: URL.createObjectURL(file), // In real implementation, this would be the processed file
            size: file.size * 0.8, // Simulate compression
            type: file.type
          }));
          
          resolve(processed);
        } else {
          setProcessingProgress(progress);
        }
      }, 200);
    });
  };

  const handleProcess = async () => {
    if (files.length === 0) {
      error('No files selected', 'Please upload files before processing');
      return;
    }

    setIsProcessing(true);
    setProcessingProgress(0);
    
    try {
      let processed: ProcessedFile[];
      
      if (onProcess) {
        processed = await onProcess(files, options);
      } else {
        processed = await simulateProcessing();
      }
      
      setProcessedFiles(processed);
      success(
        'Processing completed!', 
        `Successfully processed ${processed.length} file(s)`
      );
    } catch (err) {
      error(
        'Processing failed', 
        'An error occurred while processing your files. Please try again.'
      );
      console.error('Processing error:', err);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownload = (file: ProcessedFile) => {
    const link = document.createElement('a');
    link.href = file.url;
    link.download = file.name;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    success('Download started', `${file.name} is being downloaded`);
  };

  const handleDownloadAll = () => {
    processedFiles.forEach((file, index) => {
      setTimeout(() => {
        handleDownload(file);
      }, index * 500); // Stagger downloads
    });
  };

  const renderOption = (option: ProcessingOption) => {
    const value = options[option.id];

    switch (option.type) {
      case 'select':
        return (
          <div key={option.id} className="space-y-2">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {option.label}
            </label>
            <select
              value={value as string}
              onChange={(e) => setOptions(prev => ({ ...prev, [option.id]: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              {option.options?.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>
        );

      case 'slider':
        return (
          <div key={option.id} className="space-y-2">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {option.label}: {String(value)}
            </label>
            <input
              type="range"
              min={option.min}
              max={option.max}
              step={option.step}
              value={value as number}
              onChange={(e) => setOptions(prev => ({ ...prev, [option.id]: parseFloat(e.target.value) }))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
            />
          </div>
        );

      case 'toggle':
        return (
          <div key={option.id} className="flex items-center space-x-2">
            <input
              type="checkbox"
              id={option.id}
              checked={value as boolean}
              onChange={(e) => setOptions(prev => ({ ...prev, [option.id]: e.target.checked }))}
              className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
            />
            <label htmlFor={option.id} className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {option.label}
            </label>
          </div>
        );

      case 'input':
        return (
          <div key={option.id} className="space-y-2">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {option.label}
            </label>
            <input
              type="text"
              value={value as string}
              onChange={(e) => setOptions(prev => ({ ...prev, [option.id]: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center space-x-3 mb-4">
          <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
            {icon}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              {title}
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              {description}
            </p>
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
            <Shield className="h-4 w-4 text-green-500" />
            <span>100% Secure Processing</span>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
            <Clock className="h-4 w-4 text-blue-500" />
            <span>Auto-Delete After 1 Hour</span>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
            <Zap className="h-4 w-4 text-yellow-500" />
            <span>Fast Processing</span>
          </div>
        </div>
      </div>

      {/* File Upload */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
          1. Upload Files
        </h2>
        <FileUpload
          onFileSelect={handleFileSelect}
          acceptedTypes={acceptedTypes}
          maxSize={maxFileSize}
          maxFiles={10}
          disabled={isProcessing}
        />
      </div>

      {/* Processing Options */}
      {processingOptions.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            2. Processing Options
          </h2>
          <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {processingOptions.map(renderOption)}
            </div>
          </div>
        </div>
      )}

      {/* Process Button */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
          3. Process Files
        </h2>
        <motion.button
          whileHover={{ scale: files.length > 0 && !isProcessing ? 1.02 : 1 }}
          whileTap={{ scale: files.length > 0 && !isProcessing ? 0.98 : 1 }}
          onClick={handleProcess}
          disabled={files.length === 0 || isProcessing}
          className={cn(
            "w-full py-4 px-6 rounded-lg font-semibold text-white transition-all duration-200",
            files.length > 0 && !isProcessing
              ? "bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-lg"
              : "bg-gray-400 cursor-not-allowed"
          )}
        >
          {isProcessing ? (
            <div className="flex items-center justify-center space-x-2">
              <Loader2 className="h-5 w-5 animate-spin" />
              <span>Processing... {Math.round(processingProgress)}%</span>
            </div>
          ) : (
            <div className="flex items-center justify-center space-x-2">
              <Zap className="h-5 w-5" />
              <span>Process {files.length} File(s)</span>
            </div>
          )}
        </motion.button>

        {/* Progress Bar */}
        {isProcessing && (
          <div className="mt-4">
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <motion.div
                className="bg-gradient-to-r from-blue-600 to-purple-600 h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${processingProgress}%` }}
                transition={{ duration: 0.3 }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Results */}
      {processedFiles.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              4. Download Results
            </h2>
            <button
              onClick={handleDownloadAll}
              className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Download className="h-4 w-4" />
              <span>Download All</span>
            </button>
          </div>

          <div className="space-y-3">
            {processedFiles.map((file, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center justify-between p-4 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  <CheckCircle2 className="h-5 w-5 text-green-500" />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-gray-100">
                      {file.name}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => handleDownload(file)}
                  className="flex items-center space-x-2 px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                >
                  <Download className="h-4 w-4" />
                  <span>Download</span>
                </button>
              </motion.div>
            ))}
          </div>

          {/* Auto-delete notice */}
          <div className="mt-6 p-4 bg-yellow-50 dark:bg-yellow-950 border border-yellow-200 dark:border-yellow-800 rounded-lg">
            <div className="flex items-start space-x-2">
              <AlertCircle className="h-5 w-5 text-yellow-500 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
                  Privacy Notice
                </p>
                <p className="text-sm text-yellow-700 dark:text-yellow-300">
                  All files will be automatically deleted from our servers after 1 hour for your privacy and security.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PDFTool;
