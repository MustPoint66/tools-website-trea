import { Tool } from '../../../../types/tool';

const imageConversionTools: Tool[] = [
  {
    id: 'png-to-jpg',
    name: 'PNG to JPG',
    title: 'Convert PNG to JPG',
    href: '/tools/png-to-jpg',
    description: 'Convert PNG images to JPG format with high quality.',
    category: 'Image Tools',
    rating: 4.9,
    users: '40K+',
    icon: 'Image',
    featured: true,
    tags: ['PNG', 'JPG', 'Convert']
  },
  {
    id: 'jpg-to-png',
    name: 'JPG to PNG',
    title: 'Convert JPG to PNG',
    href: '/tools/jpg-to-png',
    description: 'Convert JPG images to PNG format with transparency support.',
    category: 'Image Tools',
    rating: 4.8,
    users: '38K+',
    icon: 'Image',
    featured: true,
    tags: ['JPG', 'PNG', 'Convert']
  }
  // Add other conversions here
];

export default imageConversionTools;

