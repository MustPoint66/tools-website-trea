import { getSlugByLegacyCategory } from './categories';
import type { ToolCategories } from '../../types/tool';

/**
 * Migration utility for converting legacy category names to new slug-based categories
 */

// Function to migrate category from legacy name to slug
export function migrateCategoryToSlug(legacyCategory: string): string {
  return getSlugByLegacyCategory(legacyCategory);
}

// Function to check if a category is a new slug-based category
export function isSlugBasedCategory(category: ToolCategories): boolean {
  const slugCategories = ['pdf-management', 'image-tools', 'text-tools', 'calculators', 'developer-tools'];
  return slugCategories.includes(category as string);
}

// Function to get all valid category slugs
export function getAllValidSlugs(): string[] {
  return ['pdf-management', 'image-tools', 'text-tools', 'calculators', 'developer-tools'];
}

// Function to validate category slug
export function isValidCategorySlug(slug: string): boolean {
  return getAllValidSlugs().includes(slug);
}

// Batch migration function for tools array
export function migrateToolsCategories<T extends { category: ToolCategories }>(tools: T[]): T[] {
  return tools.map(tool => ({
    ...tool,
    category: (isSlugBasedCategory(tool.category) 
      ? tool.category 
      : migrateCategoryToSlug(tool.category)) as ToolCategories
  }));
}

export default {
  migrateCategoryToSlug,
  isSlugBasedCategory,
  getAllValidSlugs,
  isValidCategorySlug,
  migrateToolsCategories
};
