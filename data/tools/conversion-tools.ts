import { Tool } from '../../types/tool';

const conversionTools: Tool[] = [
  {
    id: 'docx-pdf-converter',
    name: 'DOCX to PDF Converter',
    title: 'DOCX to PDF Converter',
    href: '/tools/docx-pdf-converter',
    description: 'Convert Microsoft Word documents to PDF files with full formatting preservation.',
    category: 'pdf-management',
    rating: 4.8,
    users: '42K+',
    icon: 'FileText',
    featured: true,
    tags: ['DOCX', 'PDF', 'Word', 'Convert']
  },
  // Add other conversion tools here
];

export default conversionTools;
