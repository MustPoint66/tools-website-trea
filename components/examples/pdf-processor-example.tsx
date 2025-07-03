"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import EnhancedFileUpload from '@/components/ui/enhanced-file-upload';
import { ProcessingOptions } from '@/lib/api';
import { toast } from 'sonner';

interface ProcessingResult {
  downloadUrl?: string;
  taskId?: string;
  [key: string]: unknown;
}

interface PDFProcessorExampleProps {
  className?: string;
}

const PDFProcessorExample: React.FC<PDFProcessorExampleProps> = ({ className }) => {
  const [operation, setOperation] = useState<string>('merge');
  const [options, setOptions] = useState<ProcessingOptions>({});
  const [results, setResults] = useState<ProcessingResult[]>([]);

  const operations = [
    { value: 'merge', label: 'Merge PDFs', description: 'Combine multiple PDF files into one' },
    { value: 'split', label: 'Split PDF', description: 'Split a PDF into multiple files' },
    { value: 'compress', label: 'Compress PDF', description: 'Reduce PDF file size' },
    { value: 'rotate', label: 'Rotate PDF', description: 'Rotate pages in a PDF' },
    { value: 'crop', label: 'Crop PDF', description: 'Crop pages in a PDF' },
    { value: 'add-watermark', label: 'Add Watermark', description: 'Add text or image watermark' },
    { value: 'extract-text', label: 'Extract Text', description: 'Extract text from PDF' },
    { value: 'extract-images', label: 'Extract Images', description: 'Extract images from PDF' },
    { value: 'convert-to-pdf', label: 'Convert to PDF', description: 'Convert documents to PDF' },
    { value: 'ocr', label: 'OCR', description: 'Extract text from scanned documents' }
  ];

  const getAcceptedTypes = (op: string): string[] => {
    switch (op) {
      case 'convert-to-pdf':
        return ['.docx', '.doc', '.txt', '.jpg', '.png'];
      case 'ocr':
        return ['.pdf', '.jpg', '.png', '.gif'];
      default:
        return ['.pdf'];
    }
  };

  const getMaxFiles = (op: string): number => {
    switch (op) {
      case 'merge':
        return 10;
      case 'split':
      case 'compress':
      case 'rotate':
      case 'crop':
      case 'extract-text':
      case 'extract-images':
      case 'ocr':
        return 1;
      case 'convert-to-pdf':
        return 5;
      default:
        return 5;
    }
  };

  const handleOperationChange = (newOperation: string) => {
    setOperation(newOperation);
    setOptions({});
    setResults([]);
  };

  const handleOptionsChange = (key: string, value: unknown) => {
    setOptions(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleProcessingComplete = (completedResults: ProcessingResult[]) => {
    setResults(completedResults);
    toast.success(`Processing completed! ${completedResults.length} file(s) processed.`);
  };

  const renderOperationOptions = () => {
    switch (operation) {
      case 'compress':
        return (
          <div className="space-y-4">
            <div className="space-y-2">
              <Label>Compression Level</Label>
              <Select
                value={String(options.compressionLevel || 'medium')}
                onValueChange={(value) => handleOptionsChange('compressionLevel', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select compression level" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low (better quality, larger size)</SelectItem>
                  <SelectItem value="medium">Medium (balanced)</SelectItem>
                  <SelectItem value="high">High (smaller size, lower quality)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            {options.compressionLevel && (
              <div className="space-y-2">
                <Label>Image Quality ({options.imageQuality || 80}%)</Label>
                <Slider
                  value={[options.imageQuality || 80]}
                  onValueChange={([value]) => handleOptionsChange('imageQuality', value)}
                  min={10}
                  max={100}
                  step={5}
                  className="w-full"
                />
              </div>
            )}
          </div>
        );

      case 'split':
        return (
          <div className="space-y-4">
            <div className="space-y-2">
              <Label>Split Mode</Label>
              <Select
                value={options.splitMode || 'pages'}
                onValueChange={(value) => handleOptionsChange('splitMode', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select split mode" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="pages">Individual pages</SelectItem>
                  <SelectItem value="size">By file size</SelectItem>
                  <SelectItem value="bookmarks">By bookmarks</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        );

      case 'merge':
        return (
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="addBookmarks"
                checked={options.addBookmarks || false}
                onChange={(e) => handleOptionsChange('addBookmarks', e.target.checked)}
                className="rounded"
              />
              <Label htmlFor="addBookmarks">Add bookmarks for each file</Label>
            </div>
          </div>
        );

      case 'ocr':
        return (
          <div className="space-y-4">
            <div className="space-y-2">
              <Label>Language</Label>
              <Select
                value={options.language || 'eng'}
                onValueChange={(value) => handleOptionsChange('language', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select language" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="eng">English</SelectItem>
                  <SelectItem value="spa">Spanish</SelectItem>
                  <SelectItem value="fra">French</SelectItem>
                  <SelectItem value="deu">German</SelectItem>
                  <SelectItem value="chi_sim">Chinese (Simplified)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-2">
              <Label>Output Format</Label>
              <Select
                value={options.outputFormat || 'text'}
                onValueChange={(value) => handleOptionsChange('outputFormat', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select output format" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="text">Plain Text</SelectItem>
                  <SelectItem value="searchable_pdf">Searchable PDF</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  const selectedOperation = operations.find(op => op.value === operation);

  return (
    <div className={`max-w-4xl mx-auto space-y-6 ${className}`}>
      {/* Operation Selection */}
      <Card>
        <CardHeader>
          <CardTitle>PDF Processing Tool</CardTitle>
          <CardDescription>
            Select an operation and upload your files to get started
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Operation Selector */}
          <div className="space-y-2">
            <Label>Operation</Label>
            <Select value={operation} onValueChange={handleOperationChange}>
              <SelectTrigger>
                <SelectValue placeholder="Select an operation" />
              </SelectTrigger>
              <SelectContent>
                {operations.map((op) => (
                  <SelectItem key={op.value} value={op.value}>
                    <div>
                      <div className="font-medium">{op.label}</div>
                      <div className="text-sm text-gray-500">{op.description}</div>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Operation-specific Options */}
          {renderOperationOptions()}
        </CardContent>
      </Card>

      {/* File Upload */}
      <Card>
        <CardHeader>
          <CardTitle>Upload Files</CardTitle>
          <CardDescription>
            {selectedOperation?.description}
            {operation === 'merge' && ' - Upload multiple PDF files to combine them.'}
            {operation === 'split' && ' - Upload a single PDF file to split it.'}
            {operation === 'compress' && ' - Upload a PDF file to reduce its size.'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <EnhancedFileUpload
            operation={operation}
            options={options}
            onComplete={handleProcessingComplete}
            acceptedTypes={getAcceptedTypes(operation)}
            maxFiles={getMaxFiles(operation)}
            maxSize={100} // 100MB
          />
        </CardContent>
      </Card>

      {/* Results */}
      {results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Processing Results</CardTitle>
            <CardDescription>
              Your files have been processed successfully
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {results.map((result, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-950/20 rounded-lg border border-green-200 dark:border-green-800"
                >
                  <div>
                    <p className="font-medium text-green-700 dark:text-green-300">
                      Processing completed successfully
                    </p>
                    <p className="text-sm text-green-600 dark:text-green-400">
                      Task ID: {result.taskId}
                    </p>
                  </div>
                  {result.downloadUrl && (
                    <Button
                      onClick={() => {
                        if (result.downloadUrl) {
                          const link = document.createElement('a');
                          link.href = result.downloadUrl;
                          link.download = `processed_${operation}_${Date.now()}.pdf`;
                          link.click();
                        }
                      }}
                      size="sm"
                      variant="outline"
                    >
                      Download
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Usage Instructions */}
      <Card>
        <CardHeader>
          <CardTitle>How to Use</CardTitle>
        </CardHeader>
        <CardContent>
          <ol className="list-decimal list-inside space-y-2 text-sm text-gray-600 dark:text-gray-400">
            <li>Select the operation you want to perform on your PDF files</li>
            <li>Configure any operation-specific options if available</li>
            <li>Upload your files by dragging and dropping or clicking to select</li>
            <li>Wait for the processing to complete with real-time progress updates</li>
            <li>Download your processed files when ready</li>
          </ol>
          
          <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg border border-blue-200 dark:border-blue-800">
            <p className="text-sm text-blue-700 dark:text-blue-300">
              <strong>Privacy Note:</strong> All processing happens securely on our servers. 
              Files are automatically deleted after processing for your privacy and security.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default PDFProcessorExample;
