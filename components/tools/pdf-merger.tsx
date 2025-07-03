"use client";

import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Upload, 
  FileText, 
  X, 
  Download, 
  AlertCircle, 
  CheckCircle,
  ArrowUp,
  ArrowDown,
  Merge
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { cn } from '@/lib/utils';
import { ProcessingFile, ApiResponse } from '@/types/tool';

interface PDFMergerProps {
  className?: string;
}

export const PDFMerger: React.FC<PDFMergerProps> = ({ className }) => {
  const [files, setFiles] = useState<ProcessingFile[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map((file, index) => ({
      id: `${Date.now()}-${index}`,
      file,
      status: 'pending' as const,
      progress: 0,
    }));
    
    setFiles(prev => [...prev, ...newFiles]);
    setError(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: true,
    maxSize: 50 * 1024 * 1024, // 50MB
  });

  const removeFile = (id: string) => {
    setFiles(prev => prev.filter(f => f.id !== id));
  };

  const moveFile = (id: string, direction: 'up' | 'down') => {
    setFiles(prev => {
      const currentIndex = prev.findIndex(f => f.id === id);
      if (currentIndex === -1) return prev;
      
      const newIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1;
      if (newIndex < 0 || newIndex >= prev.length) return prev;
      
      const newFiles = [...prev];
      if (newFiles[currentIndex] && newFiles[newIndex]) {
        [newFiles[currentIndex], newFiles[newIndex]] = [newFiles[newIndex], newFiles[currentIndex]];
      }
      return newFiles;
    });
  };

  const mergePDFs = async () => {
    if (files.length < 2) {
      setError('Please select at least 2 PDF files to merge.');
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const formData = new FormData();
      files.forEach((fileData, index) => {
        formData.append(`pdf_${index}`, fileData.file);
      });

      const response = await fetch('/api/pdf/merge', {
        method: 'POST',
        body: formData,
      });

      const result: ApiResponse = await response.json();

      if (!result.success) {
        throw new Error(result.error || 'Failed to merge PDFs');
      }

      setDownloadUrl(result.data.downloadUrl);
      setFiles(prev => prev.map(f => ({ ...f, status: 'completed', progress: 100 })));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while merging PDFs');
      setFiles(prev => prev.map(f => ({ ...f, status: 'error' })));
    } finally {
      setIsProcessing(false);
    }
  };

  const resetTool = () => {
    setFiles([]);
    setDownloadUrl(null);
    setError(null);
    setIsProcessing(false);
  };

  return (
    <div className={cn("max-w-4xl mx-auto p-6 space-y-6", className)}>
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-2">PDF Merger</h1>
        <p className="text-muted-foreground">
          Combine multiple PDF files into a single document. Drag and drop to reorder pages.
        </p>
      </div>

      {/* Upload Area */}
      {!downloadUrl && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5" />
              Upload PDF Files
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div
              {...getRootProps()}
              className={cn(
                "border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors",
                isDragActive ? "border-primary bg-primary/5" : "border-muted-foreground/25",
                "hover:border-primary hover:bg-primary/5"
              )}
            >
              <input {...getInputProps()} />
              <Upload className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
              <p className="text-lg font-medium mb-2">
                {isDragActive ? "Drop PDF files here" : "Drag & drop PDF files here"}
              </p>
              <p className="text-sm text-muted-foreground mb-4">
                or click to select files (max 50MB per file)
              </p>
              <Button variant="outline">
                Choose Files
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* File List */}
      {files.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Selected Files ({files.length})
              </span>
              <Button
                variant="outline"
                size="sm"
                onClick={resetTool}
                disabled={isProcessing}
              >
                Clear All
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <AnimatePresence>
                {files.map((fileData, index) => (
                  <motion.div
                    key={fileData.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="flex items-center gap-3 p-3 border rounded-lg"
                  >
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <FileText className="h-4 w-4 text-red-500" />
                        <span className="font-medium truncate">{fileData.file.name}</span>
                        <Badge variant="outline" className="text-xs">
                          {(fileData.file.size / (1024 * 1024)).toFixed(1)} MB
                        </Badge>
                        {fileData.status === 'completed' && (
                          <CheckCircle className="h-4 w-4 text-green-500" />
                        )}
                        {fileData.status === 'error' && (
                          <AlertCircle className="h-4 w-4 text-red-500" />
                        )}
                      </div>
                      
                      {fileData.status === 'processing' && (
                        <Progress value={fileData.progress} className="mt-2" />
                      )}
                    </div>

                    <div className="flex items-center gap-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => moveFile(fileData.id, 'up')}
                        disabled={index === 0 || isProcessing}
                      >
                        <ArrowUp className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => moveFile(fileData.id, 'down')}
                        disabled={index === files.length - 1 || isProcessing}
                      >
                        <ArrowDown className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeFile(fileData.id)}
                        disabled={isProcessing}
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>

            {files.length >= 2 && !downloadUrl && (
              <div className="mt-6 text-center">
                <Button
                  onClick={mergePDFs}
                  disabled={isProcessing}
                  size="lg"
                  className="w-full sm:w-auto"
                >
                  {isProcessing ? (
                    <>
                      <div className="animate-spin h-4 w-4 mr-2 border-2 border-white border-t-transparent rounded-full" />
                      Merging PDFs...
                    </>
                  ) : (
                    <>
                      <Merge className="h-4 w-4 mr-2" />
                      Merge PDFs
                    </>
                  )}
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Download Section */}
      {downloadUrl && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-green-600">
                <CheckCircle className="h-5 w-5" />
                PDF Merged Successfully!
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-muted-foreground">
                Your PDF files have been successfully merged into a single document.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-3">
                <Button asChild className="flex-1">
                  <a href={downloadUrl} download>
                    <Download className="h-4 w-4 mr-2" />
                    Download Merged PDF
                  </a>
                </Button>
                <Button variant="outline" onClick={resetTool}>
                  Merge Another Set
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Info Section */}
      <Card>
        <CardContent className="pt-6">
          <h3 className="font-semibold mb-3">How to use PDF Merger:</h3>
          <ol className="list-decimal list-inside space-y-2 text-sm text-muted-foreground">
            <li>Upload multiple PDF files by dragging and dropping or clicking to select</li>
            <li>Reorder files using the up/down arrows to set the merge order</li>
            <li>Click &quot;Merge PDFs&quot; to combine all files into one document</li>
            <li>Download your merged PDF file</li>
          </ol>
          
          <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg">
            <p className="text-xs text-blue-600 dark:text-blue-400">
              🔒 <strong>Privacy:</strong> All files are processed securely and automatically deleted after download.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
