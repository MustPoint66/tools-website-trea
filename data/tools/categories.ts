import { ToolCategory } from '../../types/tool';

// Extended ToolCategory interface with slug property for routing
export interface ToolCategoryWithSlug extends ToolCategory {
  slug: string;
}

// Primary category slug map for consistent routing
export const toolCategories: ToolCategoryWithSlug[] = [
  {
    id: 'pdf-management',
    slug: 'pdf-management',
    name: 'PDF Management',
    description: 'Comprehensive PDF tools for merging, splitting, editing, and managing PDF documents',
    icon: 'FileText',
    toolCount: 25,
    color: 'blue'
  },
  {
    id: 'image-tools',
    slug: 'image-tools',
    name: 'Image Tools',
    description: 'Complete image processing suite for conversion, editing, compression, and enhancement',
    icon: 'Image',
    toolCount: 35,
    color: 'green'
  },
  {
    id: 'text-tools',
    slug: 'text-tools',
    name: 'Text Tools',
    description: 'Text processing utilities for formatting, conversion, analysis, and manipulation',
    icon: 'Type',
    toolCount: 20,
    color: 'purple'
  },
  {
    id: 'calculators',
    slug: 'calculators',
    name: 'Calculators',
    description: 'Mathematical calculators and converters for various calculations and unit conversions',
    icon: 'Calculator',
    toolCount: 15,
    color: 'orange'
  },
  {
    id: 'developer-tools',
    slug: 'developer-tools',
    name: 'Developer Tools',
    description: 'Development utilities including code formatters, generators, validators, and converters',
    icon: 'Code',
    toolCount: 18,
    color: 'indigo'
  }
];

// Category slug lookup map for easy routing
export const categorySlugMap = new Map(
  toolCategories.map(category => [category.slug, category])
);

// Legacy category ID to slug mapping for backward compatibility
export const legacyCategoryMap = new Map([
  ['PDF Management', 'pdf-management'],
  ['PDF Conversion', 'pdf-management'], // Group PDF conversion under PDF management
  ['Edit & Annotate PDF', 'pdf-management'],
  ['Image Tools', 'image-tools'],
  ['AI', 'developer-tools'], // Group AI tools under developer tools
  ['OCR', 'text-tools'], // Group OCR under text tools
  ['Conversion', 'pdf-management'],
  ['Text Tools', 'text-tools'],
  ['Calculators', 'calculators']
]);

// Helper function to get category by slug
export function getCategoryBySlug(slug: string): ToolCategoryWithSlug | undefined {
  return categorySlugMap.get(slug);
}

// Helper function to get slug by legacy category name
export function getSlugByLegacyCategory(categoryName: string): string {
  return legacyCategoryMap.get(categoryName) || 'pdf-management'; // Default fallback
}

export default toolCategories;
