import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env['BACKEND_URL'] || 'http://localhost:8000';

// File size limits (in bytes)
const MAX_FILE_SIZE = 100 * 1024 * 1024; // 100MB
const ALLOWED_FILE_TYPES = [
  'application/pdf',
  'image/jpeg',
  'image/png',
  'image/gif',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'text/plain'
];

function validateFile(file: File): { valid: boolean; error?: string } {
  if (file.size > MAX_FILE_SIZE) {
    return { valid: false, error: 'File size exceeds 100MB limit' };
  }
  
  if (!ALLOWED_FILE_TYPES.includes(file.type)) {
    return { valid: false, error: 'Unsupported file type' };
  }
  
  return { valid: true };
}

export async function POST(
  request: NextRequest,
  { params }: { params: { operation: string } }
): Promise<NextResponse> {
  try {
    const { operation } = params;
    
    // Get form data
    const formData = await request.formData();
    const files = formData.getAll('files') as File[];
    const optionsStr = formData.get('options') as string | null;
    const options: Record<string, unknown> = optionsStr ? JSON.parse(optionsStr) : {};
    
    // Validate files
    for (const file of files) {
      const validation = validateFile(file);
      if (!validation.valid) {
        return NextResponse.json(
          { error: validation.error, code: 'VALIDATION_ERROR' },
          { status: 400 }
        );
      }
    }
    
    // Create FormData for backend
    const backendFormData = new FormData();
    
    // Add files to form data
    for (const file of files) {
      backendFormData.append('files', file);
    }
    
    // Add options
    if (Object.keys(options).length > 0) {
      backendFormData.append('options', JSON.stringify(options));
    }
    
    // Generate a unique task ID for progress tracking
    const taskId = `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    backendFormData.append('task_id', taskId);
    
    // Make request to backend
    const backendResponse = await fetch(`${BACKEND_URL}/api/pdf/${operation}`, {
      method: 'POST',
      body: backendFormData,
      headers: {
        // Don't set Content-Type, let fetch set it with boundary
      },
    });
    
    if (!backendResponse.ok) {
      const errorData: { error?: string; [key: string]: unknown } = await backendResponse.json().catch(() => ({ error: 'Unknown error' }));
      return NextResponse.json(
        { 
          error: (errorData.error as string) || 'Backend processing failed',
          code: 'BACKEND_ERROR',
          details: errorData
        },
        { status: backendResponse.status }
      );
    }
    
    // Check if response is a file download
    const contentType = backendResponse.headers.get('content-type');
    if (contentType && (contentType.includes('application/pdf') || contentType.includes('application/zip'))) {
      // Return file response
      const buffer = await backendResponse.arrayBuffer();
      const headers = new Headers();
      headers.set('Content-Type', contentType);
      headers.set('Content-Disposition', backendResponse.headers.get('content-disposition') || 'attachment');
      
      return new NextResponse(buffer, {
        status: 200,
        headers,
      });
    }
    
    // Return JSON response with task ID for progress tracking
    const data: Record<string, unknown> = await backendResponse.json();
    return NextResponse.json({
      ...data,
      taskId,
      message: 'Processing started successfully'
    });
    
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        code: 'INTERNAL_ERROR',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

// Handle progress tracking
export async function GET(
  request: NextRequest,
  { }: { params: { operation: string } }
): Promise<NextResponse> {
  try {
    const { searchParams } = new URL(request.url);
    const taskId = searchParams.get('taskId');
    const action = searchParams.get('action');
    
    if (action === 'progress' && taskId) {
      // Get progress from backend
      const progressResponse = await fetch(`${BACKEND_URL}/api/pdf/progress/${taskId}`);
      
      if (!progressResponse.ok) {
        return NextResponse.json(
          { error: 'Failed to get progress' },
          { status: progressResponse.status }
        );
      }
      
      const progressData: Record<string, unknown> = await progressResponse.json();
      return NextResponse.json(progressData);
    }
    
    if (action === 'download' && taskId) {
      // Download completed file
      const downloadResponse = await fetch(`${BACKEND_URL}/api/pdf/download/${taskId}`);
      
      if (!downloadResponse.ok) {
        return NextResponse.json(
          { error: 'File not found or processing not complete' },
          { status: downloadResponse.status }
        );
      }
      
      const buffer = await downloadResponse.arrayBuffer();
      const contentType = downloadResponse.headers.get('content-type') || 'application/octet-stream';
      const contentDisposition = downloadResponse.headers.get('content-disposition') || 'attachment';
      
      const headers = new Headers();
      headers.set('Content-Type', contentType);
      headers.set('Content-Disposition', contentDisposition);
      
      return new NextResponse(buffer, {
        status: 200,
        headers,
      });
    }
    
    return NextResponse.json(
      { error: 'Invalid action or missing parameters' },
      { status: 400 }
    );
    
  } catch (error) {
    console.error('Progress API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
