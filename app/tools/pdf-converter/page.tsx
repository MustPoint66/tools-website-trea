"use client";

import React, { useState, useRef, useCallback } from 'react';
import { motion } from 'framer-motion';
import { 
  FileText, 
  Upload, 
  Download, 
  X, 
  CheckCircle, 
  AlertCircle,
  ArrowLeft,
  Zap
} from 'lucide-react';
import Link from 'next/link';

interface FileState {
  file: File;
  id: string;
  status: 'uploading' | 'processing' | 'complete' | 'error';
  progress: number;
}

const PDFConverter = () => {
  const [files, setFiles] = useState<FileState[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFiles = useCallback((newFiles: File[]) => {
    const validFiles = newFiles.filter(file => 
      file.type.includes('word') || 
      file.type.includes('excel') || 
      file.type.includes('powerpoint') ||
      file.type === 'text/plain' ||
      file.name.endsWith('.docx') ||
      file.name.endsWith('.xlsx') ||
      file.name.endsWith('.pptx') ||
      file.name.endsWith('.txt')
    );

    const fileStates: FileState[] = validFiles.map(file => ({
      file,
      id: Math.random().toString(36).substr(2, 9),
      status: 'uploading',
      progress: 0
    }));

    setFiles(prev => [...prev, ...fileStates]);

    // Simulate file processing
    fileStates.forEach(fileState => {
      simulateProcessing(fileState.id);
    });
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    handleFiles(droppedFiles);
  }, [handleFiles]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      handleFiles(selectedFiles);
    }
  }, [handleFiles]);

  const simulateProcessing = (fileId: string) => {
    const updateProgress = (progress: number, status: FileState['status']) => {
      setFiles(prev => prev.map(f => 
        f.id === fileId ? { ...f, progress, status } : f
      ));
    };

    // Simulate upload progress
    let progress = 0;
    const uploadInterval = setInterval(() => {
      progress += Math.random() * 20;
      if (progress >= 100) {
        clearInterval(uploadInterval);
        updateProgress(100, 'processing');
        
        // Simulate processing
        setTimeout(() => {
          updateProgress(100, 'complete');
        }, 2000);
      } else {
        updateProgress(progress, 'uploading');
      }
    }, 200);
  };

  const removeFile = (fileId: string) => {
    setFiles(prev => prev.filter(f => f.id !== fileId));
  };

  const downloadFile = (fileId: string) => {
    // In a real app, this would download the converted file
    const fileState = files.find(f => f.id === fileId);
    if (fileState) {
      // Create a dummy PDF blob for demo
      const blob = new Blob(['%PDF-1.4 Demo converted file'], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${fileState.file.name.split('.')[0]}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  const getStatusIcon = (status: FileState['status']) => {
    switch (status) {
      case 'uploading':
      case 'processing':
        return <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500" />;
      case 'complete':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'error':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
    }
  };

  const getStatusText = (status: FileState['status']) => {
    switch (status) {
      case 'uploading':
        return 'Uploading...';
      case 'processing':
        return 'Converting to PDF...';
      case 'complete':
        return 'Ready to download';
      case 'error':
        return 'Conversion failed';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 text-white">
      {/* Navigation */}
      <nav className="border-b border-gray-800 bg-black/50 backdrop-blur-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <Link href="/" className="flex items-center space-x-2 text-blue-500 hover:text-blue-400 transition-colors">
                <ArrowLeft className="h-5 w-5" />
                <span>Back to Tools</span>
              </Link>
            </div>
            <div className="flex items-center space-x-2">
              <Zap className="h-8 w-8 text-blue-500" />
              <span className="text-xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
                Tools Mania
              </span>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-500/10 rounded-full mb-6">
            <FileText className="h-8 w-8 text-blue-500" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            PDF Converter
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Convert your documents to PDF format quickly and securely. Support for Word, Excel, PowerPoint, and text files.
          </p>
        </motion.div>

        {/* Upload Area */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <div
            className={`relative border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 ${
              isDragOver 
                ? 'border-blue-500 bg-blue-500/5' 
                : 'border-gray-600 hover:border-gray-500'
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept=".doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt"
              onChange={handleFileSelect}
              className="hidden"
            />
            
            <div className="space-y-4">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-gray-800 rounded-full">
                <Upload className="h-10 w-10 text-gray-400" />
              </div>
              
              <div>
                <h3 className="text-2xl font-semibold mb-2">Drop your files here</h3>
                <p className="text-gray-400 mb-6">
                  or click to browse from your computer
                </p>
                
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => fileInputRef.current?.click()}
                  className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-xl font-medium transition-colors"
                >
                  <Upload className="h-5 w-5" />
                  Choose Files
                </motion.button>
              </div>
              
              <p className="text-sm text-gray-500">
                Supports: DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT
              </p>
            </div>
          </div>
        </motion.div>

        {/* File List */}
        {files.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="space-y-4"
          >
            <h3 className="text-xl font-semibold mb-4">Converting Files</h3>
            
            {files.map((fileState) => (
              <div
                key={fileState.id}
                className="bg-gray-800/50 border border-gray-700 rounded-xl p-6"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <FileText className="h-6 w-6 text-blue-500" />
                    <div>
                      <p className="font-medium">{fileState.file.name}</p>
                      <p className="text-sm text-gray-400">
                        {(fileState.file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    {getStatusIcon(fileState.status)}
                    <span className="text-sm text-gray-400">
                      {getStatusText(fileState.status)}
                    </span>
                    
                    {fileState.status === 'complete' ? (
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => downloadFile(fileState.id)}
                        className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                      >
                        <Download className="h-4 w-4" />
                        Download PDF
                      </motion.button>
                    ) : (
                      <button
                        onClick={() => removeFile(fileState.id)}
                        className="p-2 text-gray-400 hover:text-red-400 transition-colors"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                </div>
                
                {(fileState.status === 'uploading' || fileState.status === 'processing') && (
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${fileState.progress}%` }}
                    />
                  </div>
                )}
              </div>
            ))}
          </motion.div>
        )}

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-green-500/10 rounded-xl mb-4">
              <CheckCircle className="h-6 w-6 text-green-500" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Secure & Private</h3>
            <p className="text-gray-400 text-sm">
              Your files are processed securely and deleted after conversion.
            </p>
          </div>
          
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-500/10 rounded-xl mb-4">
              <Zap className="h-6 w-6 text-blue-500" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Fast Conversion</h3>
            <p className="text-gray-400 text-sm">
              Convert multiple files simultaneously with high-speed processing.
            </p>
          </div>
          
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-purple-500/10 rounded-xl mb-4">
              <FileText className="h-6 w-6 text-purple-500" />
            </div>
            <h3 className="text-lg font-semibold mb-2">High Quality</h3>
            <p className="text-gray-400 text-sm">
              Maintain original formatting and quality in your PDF output.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default PDFConverter;
