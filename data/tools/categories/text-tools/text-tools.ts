import { Tool } from '../../../../types/tool';

const textTools: Tool[] = [
  {
    id: 'word-counter',
    name: 'Word Counter',
    title: 'Word Counter & Text Analytics',
    href: '/tools/word-counter',
    description: 'Count words, characters, paragraphs, and analyze text statistics.',
    category: 'text-tools',
    rating: 4.8,
    users: '45K+',
    icon: 'Hash',
    featured: true,
    tags: ['Word Count', 'Text', 'Analytics', 'Statistics']
  },
  {
    id: 'text-formatter',
    name: 'Text Formatter',
    title: 'Text Formatter & Case Converter',
    href: '/tools/text-formatter',
    description: 'Format text with various case conversions and styling options.',
    category: 'text-tools',
    rating: 4.7,
    users: '38K+',
    icon: 'Type',
    featured: true,
    tags: ['Format', 'Case', 'Convert', 'Text']
  },
  {
    id: 'text-diff',
    name: 'Text Diff Checker',
    title: 'Text Difference Checker',
    href: '/tools/text-diff',
    description: 'Compare two texts and highlight differences side by side.',
    category: 'text-tools',
    rating: 4.6,
    users: '22K+',
    icon: 'GitCompare',
    featured: false,
    tags: ['Compare', 'Diff', 'Text', 'Changes']
  },
  {
    id: 'text-encoder',
    name: 'Text Encoder/Decoder',
    title: 'Text Encoder & Decoder',
    href: '/tools/text-encoder',
    description: 'Encode and decode text using various encoding methods (Base64, URL, HTML).',
    category: 'text-tools',
    rating: 4.5,
    users: '32K+',
    icon: 'Code',
    featured: false,
    tags: ['Encode', 'Decode', 'Base64', 'URL']
  },
  {
    id: 'markdown-editor',
    name: 'Markdown Editor',
    title: 'Online Markdown Editor',
    href: '/tools/markdown-editor',
    description: 'Write and preview Markdown with live rendering and export options.',
    category: 'text-tools',
    rating: 4.8,
    users: '55K+',
    icon: 'FileEdit',
    featured: true,
    popular: true,
    tags: ['Markdown', 'Editor', 'Preview', 'Export']
  },
  {
    id: 'text-replacer',
    name: 'Text Replace Tool',
    title: 'Find & Replace Text Tool',
    href: '/tools/text-replacer',
    description: 'Find and replace text with support for regex patterns and bulk operations.',
    category: 'text-tools',
    rating: 4.6,
    users: '28K+',
    icon: 'Search',
    featured: false,
    tags: ['Replace', 'Find', 'Regex', 'Bulk']
  },
  {
    id: 'text-splitter',
    name: 'Text Splitter',
    title: 'Text Splitter & Line Tool',
    href: '/tools/text-splitter',
    description: 'Split text by various delimiters and organize into lines or columns.',
    category: 'text-tools',
    rating: 4.4,
    users: '18K+',
    icon: 'Split',
    featured: false,
    tags: ['Split', 'Lines', 'Delimiter', 'Organize']
  },
  {
    id: 'text-cleaner',
    name: 'Text Cleaner',
    title: 'Text Cleaner & Formatter',
    href: '/tools/text-cleaner',
    description: 'Clean text by removing extra spaces, line breaks, and unwanted characters.',
    category: 'text-tools',
    rating: 4.5,
    users: '25K+',
    icon: 'Eraser',
    featured: false,
    tags: ['Clean', 'Format', 'Remove', 'Spaces']
  }
];

export default textTools;
