import { Tool } from '../../../../types/tool';

const developerTools: Tool[] = [
  {
    id: 'json-formatter',
    name: 'JSON Formatter',
    title: 'JSON Formatter & Validator',
    href: '/tools/json-formatter',
    description: 'Format, validate, and beautify JSON data with syntax highlighting.',
    category: 'developer-tools',
    rating: 4.8,
    users: '75K+',
    icon: 'Code',
    featured: true,
    tags: ['JSON', 'Format', 'Validate', 'Beautify']
  },
  {
    id: 'regex-tester',
    name: 'Regex Tester',
    title: 'Regular Expression Tester',
    href: '/tools/regex-tester',
    description: 'Test and validate regular expressions with real-time matching.',
    category: 'developer-tools',
    rating: 4.7,
    users: '55K+',
    icon: 'Search',
    featured: true,
    tags: ['Regex', 'Test', 'Pattern', 'Match']
  },
  {
    id: 'url-encoder-decoder',
    name: 'URL Encoder/Decoder',
    title: 'URL Encoder & Decoder',
    href: '/tools/url-encoder-decoder',
    description: 'Encode and decode URLs for safe transmission and processing.',
    category: 'developer-tools',
    rating: 4.6,
    users: '40K+',
    icon: 'Link',
    featured: false,
    tags: ['URL', 'Encode', 'Decode', 'Web']
  },
  {
    id: 'base64-encoder',
    name: 'Base64 Encoder/Decoder',
    title: 'Base64 Encoder & Decoder',
    href: '/tools/base64-encoder',
    description: 'Encode and decode text or files to/from Base64 format.',
    category: 'developer-tools',
    rating: 4.7,
    users: '65K+',
    icon: 'Code',
    featured: true,
    tags: ['Base64', 'Encode', 'Decode', 'Text']
  },
  {
    id: 'hash-generator',
    name: 'Hash Generator',
    title: 'MD5, SHA1, SHA256 Hash Generator',
    href: '/tools/hash-generator',
    description: 'Generate cryptographic hashes for text and files using various algorithms.',
    category: 'developer-tools',
    rating: 4.8,
    users: '45K+',
    icon: 'Hash',
    featured: true,
    tags: ['Hash', 'MD5', 'SHA1', 'SHA256']
  },
  {
    id: 'color-picker',
    name: 'Color Picker',
    title: 'Color Picker & Palette Tool',
    href: '/tools/color-picker',
    description: 'Pick colors and generate palettes with hex, RGB, and HSL values.',
    category: 'developer-tools',
    rating: 4.6,
    users: '85K+',
    icon: 'Palette',
    featured: true,
    tags: ['Color', 'Picker', 'Palette', 'Hex']
  },
  {
    id: 'password-generator',
    name: 'Password Generator',
    title: 'Secure Password Generator',
    href: '/tools/password-generator',
    description: 'Generate secure, random passwords with customizable options.',
    category: 'developer-tools',
    rating: 4.9,
    users: '95K+',
    icon: 'Key',
    featured: true,
    popular: true,
    tags: ['Password', 'Generate', 'Secure', 'Random']
  },
  {
    id: 'lorem-ipsum',
    name: 'Lorem Ipsum Generator',
    title: 'Lorem Ipsum Text Generator',
    href: '/tools/lorem-ipsum',
    description: 'Generate placeholder text for design and development projects.',
    category: 'developer-tools',
    rating: 4.5,
    users: '35K+',
    icon: 'Type',
    featured: false,
    tags: ['Lorem', 'Ipsum', 'Placeholder', 'Text']
  },
  {
    id: 'qr-code-generator',
    name: 'QR Code Generator',
    title: 'QR Code Generator & Scanner',
    href: '/tools/qr-code-generator',
    description: 'Generate QR codes for text, URLs, and other data.',
    category: 'developer-tools',
    rating: 4.8,
    users: '120K+',
    icon: 'QrCode',
    featured: true,
    popular: true,
    tags: ['QR Code', 'Generate', 'Scan', 'URL']
  },
  {
    id: 'sql-formatter',
    name: 'SQL Formatter',
    title: 'SQL Query Formatter',
    href: '/tools/sql-formatter',
    description: 'Format and beautify SQL queries with proper indentation.',
    category: 'developer-tools',
    rating: 4.6,
    users: '30K+',
    icon: 'Database',
    featured: false,
    tags: ['SQL', 'Format', 'Query', 'Database']
  }
];

export default developerTools;
