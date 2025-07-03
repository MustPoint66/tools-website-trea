import { Tool } from '../../types/tool';

// Import all categorized tools
import comprehensiveConversionTools from './comprehensive-conversion-tools';
import pdfManagementTools from './categories/pdf-management/pdf-management-tools';
import aiTools from './categories/ai-tools/ai-tools';
import imageEditingTools from './categories/image-editing/image-editing-tools';
import textTools from './categories/text-tools/text-tools';
import calculatorTools from './categories/calculators/calculator-tools';
import developerTools from './categories/developer-tools/developer-tools';

// Original tools (for backward compatibility)
import pdfTools from './pdf-tools';
import conversionTools from './conversion-tools';
import otherTools from './other-tools';
import imageTools from './image-tools';

// Combine all tools with proper organization
export const allToolsOrganized: Tool[] = [
  ...comprehensiveConversionTools,
  ...pdfManagementTools,
  ...aiTools,
  ...imageEditingTools,
  ...textTools,
  ...calculatorTools,
  ...developerTools,
  // Legacy tools (remove duplicates by checking if ID already exists)
  ...pdfTools.filter(tool => 
    !comprehensiveConversionTools.some(ct => ct.id === tool.id) &&
    !pdfManagementTools.some(pmt => pmt.id === tool.id)
  ),
  ...conversionTools.filter(tool => 
    !comprehensiveConversionTools.some(ct => ct.id === tool.id)
  ),
  ...otherTools.filter(tool => 
    !aiTools.some(at => at.id === tool.id) &&
    !textTools.some(tt => tt.id === tool.id)
  ),
  ...imageTools.filter(tool => 
    !comprehensiveConversionTools.some(ct => ct.id === tool.id) &&
    !imageEditingTools.some(iet => iet.id === tool.id) &&
    !aiTools.some(at => at.id === tool.id)
  )
];

// Export categorized collections
export const toolsByCategory = {
  'pdf-management': [...comprehensiveConversionTools.filter(t => t.category === 'pdf-management'), ...pdfManagementTools],
  'image-tools': [...comprehensiveConversionTools.filter(t => t.category === 'image-tools'), ...imageEditingTools],
  'text-tools': textTools,
  'calculators': calculatorTools,
  'developer-tools': [...aiTools, ...developerTools]
};

// Legacy collections for backward compatibility
export const legacyToolsByCategory = {
  conversion: comprehensiveConversionTools,
  pdfManagement: pdfManagementTools,
  ai: aiTools,
  imageEditing: imageEditingTools
};

// Import the new category system
import { toolCategories } from './categories';

// Export updated category information using the new slug-based system
export const categories = toolCategories.map(category => ({
  id: category.id,
  slug: category.slug,
  name: category.name,
  description: category.description,
  toolCount: allToolsOrganized.filter(t => t.category === category.slug).length,
  icon: category.icon,
  color: category.color
}));

// Legacy category mapping for backward compatibility
export const legacyCategories = [
  {
    id: 'pdf-conversion',
    name: 'PDF Conversion',
    description: 'Convert PDF files to and from various formats',
    toolCount: comprehensiveConversionTools.filter(t => t.category === 'pdf-management').length,
    icon: 'RefreshCw',
    color: 'blue'
  },
  {
    id: 'image-conversion',
    name: 'Image Conversion',
    description: 'Convert images between different formats',
    toolCount: comprehensiveConversionTools.filter(t => t.category === 'image-tools').length,
    icon: 'Image',
    color: 'green'
  }
];

export default allToolsOrganized;
