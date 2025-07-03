import { Tool } from '../../../../types/tool';

const pdfManagementTools: Tool[] = [
  {
    id: 'pdf-organizer',
    name: 'PDF Page Organizer',
    title: 'PDF Page Organizer',
    href: '/tools/pdf-organizer',
    description: 'Reorganize and rearrange PDF pages with drag-and-drop functionality.',
    category: 'pdf-management',
    rating: 4.9,
    users: '15K+',
    icon: 'Grid3X3',
    featured: true,
    tags: ['Organization', 'Pages', 'Drag-Drop']
  },
  {
    id: 'pdf-merger',
    name: 'PDF Merger',
    title: 'PDF Merger',
    href: '/tools/pdf-merger',
    description: 'Combine multiple PDF files into a single document.',
    category: 'pdf-management',
    rating: 4.8,
    users: '35K+',
    icon: 'FileText',
    featured: true,
    tags: ['Merge', 'Combine', 'Multiple']
  },
  {
    id: 'pdf-splitter',
    name: 'PDF Splitter',
    title: 'PDF Splitter',
    href: '/tools/pdf-splitter',
    description: 'Split PDF files into separate pages or sections.',
    category: 'pdf-management',
    rating: 4.7,
    users: '28K+',
    icon: 'FileText',
    featured: true,
    tags: ['Split', 'Separate', 'Extract']
  },
  {
    id: 'pdf-compressor',
    name: 'PDF Compressor',
    title: 'PDF Compressor',
    href: '/tools/pdf-compressor',
    description: 'Compress PDF files to reduce file size while maintaining quality.',
    category: 'pdf-management',
    rating: 4.8,
    users: '42K+',
    icon: 'Archive',
    featured: true,
    tags: ['Compress', 'Size', 'Optimize']
  },
  {
    id: 'pdf-protector',
    name: 'PDF Protector',
    title: 'PDF Password Protection',
    href: '/tools/pdf-protector',
    description: 'Add password protection and security to PDF files.',
    category: 'pdf-management',
    rating: 4.6,
    users: '22K+',
    icon: 'Shield',
    featured: false,
    tags: ['Protect', 'Password', 'Security']
  },
  {
    id: 'pdf-unlocker',
    name: 'PDF Unlocker',
    title: 'PDF Password Remover',
    href: '/tools/pdf-unlocker',
    description: 'Remove password protection and restrictions from PDF files.',
    category: 'pdf-management',
    rating: 4.5,
    users: '18K+',
    icon: 'Shield',
    featured: false,
    tags: ['Unlock', 'Remove', 'Password']
  },
  {
    id: 'pdf-watermark',
    name: 'PDF Watermark',
    title: 'PDF Watermark Tool',
    href: '/tools/pdf-watermark',
    description: 'Add watermarks to PDF documents for branding or security.',
    category: 'pdf-management',
    rating: 4.4,
    users: '15K+',
    icon: 'Image',
    featured: false,
    tags: ['Watermark', 'Brand', 'Security']
  },
  {
    id: 'pdf-rotator',
    name: 'PDF Page Rotator',
    title: 'PDF Page Rotator',
    href: '/tools/pdf-rotator',
    description: 'Rotate PDF pages to correct orientation.',
    category: 'pdf-management',
    rating: 4.3,
    users: '12K+',
    icon: 'RotateCcw',
    featured: false,
    tags: ['Rotate', 'Orientation', 'Pages']
  },
  {
    id: 'pdf-crop',
    name: 'PDF Page Cropper',
    title: 'PDF Page Cropper',
    href: '/tools/pdf-crop',
    description: 'Crop PDF pages to remove unwanted margins or areas.',
    category: 'pdf-management',
    rating: 4.2,
    users: '10K+',
    icon: 'Crop',
    featured: false,
    tags: ['Crop', 'Margins', 'Trim']
  },
  {
    id: 'pdf-page-remover',
    name: 'PDF Page Remover',
    title: 'PDF Page Remover',
    href: '/tools/pdf-page-remover',
    description: 'Remove unwanted pages from PDF documents.',
    category: 'pdf-management',
    rating: 4.4,
    users: '14K+',
    icon: 'Trash2',
    featured: false,
    tags: ['Remove', 'Delete', 'Pages']
  }
];

export default pdfManagementTools;
