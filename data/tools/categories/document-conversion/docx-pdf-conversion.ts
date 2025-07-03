import { Tool } from '../../../../types/tool';

const documentConversionTools: Tool[] = [
  {
    id: 'docx-to-pdf',
    name: 'DOCX to PDF',
    title: 'Convert DOCX to PDF',
    href: '/tools/docx-to-pdf',
    description: 'Convert Microsoft Word documents (DOCX) to PDF format while maintaining formatting.',
    category: 'PDF Conversion',
    rating: 4.8,
    users: '42K+',
    icon: 'TextFile',
    featured: true,
    tags: ['DOCX', 'PDF', 'Word', 'Convert']
  },
  {
    id: 'pdf-to-docx',
    name: 'PDF to DOCX',
    title: 'Convert PDF to DOCX',
    href: '/tools/pdf-to-docx',
    description: 'Convert PDF files to Microsoft Word documents (DOCX) while preserving layout.',
    category: 'PDF Conversion',
    rating: 4.8,
    users: '39K+',
    icon: 'TextFile',
    featured: true,
    tags: ['PDF', 'DOCX', 'Word', 'Convert']
  }
  // Add other conversions here
];

export default documentConversionTools;

