import imageTools from "./image-tools";
import { FileText, Eye, Rotate3D, Scissors, Copy, Shield, Merge, Split, FileImage, Users, Zap, Grid3X3 } from "lucide-react";

// Tool interface - Updated to properly type Lucide icons
interface ToolWithIcon {
  id: string;
  title: string;
  description: string;
  icon: React.ComponentType<React.SVGProps<SVGSVGElement>>;
  href: string;
  category: string;
  name: string;
  premium?: boolean;
  rating?: number;
  tags?: string[];
  users?: string;
  popular?: boolean;
  new?: boolean;
  featured?: boolean;
}

// PDF Management Tools Data
export const pdfTools: ToolWithIcon[] = [
  {
    id: "pdf-organizer",
    name: "PDF Page Organizer",
    title: "PDF Page Organizer",
    href: "/tools/pdf-organizer",
    description: "Reorganize and rearrange PDF pages with intuitive drag-and-drop interface.",
    category: "PDF Management",
    rating: 4.9,
    users: "15K+",
    icon: Grid3X3,
    featured: true,
    tags: ["Organization", "Pages", "Drag-Drop"]
  },
  {
    id: "pdf-merger",
    name: "PDF Merger",
    title: "PDF Merger",
    href: "/tools/pdf-merger",
    description: "Combine multiple PDF files into a single document with custom ordering.",
    category: "PDF Management",
    rating: 4.8,
    users: "25K+",
    icon: Merge,
    featured: true,
    tags: ["Merge", "Combine", "Multiple Files"]
  },
  {
    id: "pdf-splitter",
    name: "PDF Splitter",
    title: "PDF Splitter",
    href: "/tools/pdf-splitter",
    description: "Split PDF documents into separate files by page ranges or individual pages.",
    category: "PDF Management",
    rating: 4.7,
    users: "20K+",
    icon: Split,
    featured: true,
    tags: ["Split", "Separate", "Extract"]
  },
  {
    id: "pdf-resizer",
    name: "PDF Page Resizer",
    title: "PDF Page Resizer",
    href: "/tools/pdf-resizer",
    description: "Resize PDF pages to different dimensions and aspect ratios.",
    category: "PDF Management",
    rating: 4.6,
    users: "12K+",
    icon: FileImage,
    featured: false,
    tags: ["Resize", "Dimensions", "Format"]
  },
  {
    id: "pdf-page-deleter",
    name: "PDF Page Remover",
    title: "PDF Page Remover",
    href: "/tools/pdf-page-deleter",
    description: "Remove unwanted pages from PDF documents quickly and efficiently.",
    category: "PDF Management",
    rating: 4.5,
    users: "10K+",
    icon: Scissors,
    featured: false,
    tags: ["Delete", "Remove", "Pages"]
  },
  {
    id: "pdf-extractor",
    name: "PDF Content Extractor",
    title: "PDF Content Extractor",
    href: "/tools/pdf-extractor",
    description: "Extract text, images, and specific content from PDF documents.",
    category: "PDF Management",
    rating: 4.8,
    users: "18K+",
    icon: Copy,
    featured: true,
    tags: ["Extract", "Text", "Images"]
  },
  {
    id: "pdf-rotator",
    name: "PDF Page Rotator",
    title: "PDF Page Rotator",
    href: "/tools/pdf-rotator",
    description: "Rotate PDF pages to correct orientation or change viewing angle.",
    category: "PDF Management",
    rating: 4.4,
    users: "8K+",
    icon: Rotate3D,
    featured: false,
    tags: ["Rotate", "Orientation", "View"]
  },
  {
    id: "pdf-cropper",
    name: "PDF Page Cropper",
    title: "PDF Page Cropper",
    href: "/tools/pdf-cropper",
    description: "Crop PDF pages to remove unwanted margins and content areas.",
    category: "PDF Management",
    rating: 4.6,
    users: "14K+",
    icon: Scissors,
    featured: false,
    tags: ["Crop", "Margins", "Trim"]
  },
  {
    id: "pdf-viewer",
    name: "Advanced PDF Viewer",
    title: "Advanced PDF Viewer",
    href: "/tools/pdf-viewer",
    description: "Professional PDF viewer with annotation, bookmark, and search capabilities.",
    category: "PDF Management",
    rating: 4.9,
    users: "50K+",
    icon: Eye,
    featured: true,
    tags: ["View", "Annotations", "Search"]
  },
  {
    id: "pdf-repair",
    name: "PDF Repair Tool",
    title: "PDF Repair Tool",
    href: "/tools/pdf-repair",
    description: "Fix corrupted or damaged PDF files and restore readability.",
    category: "PDF Management",
    rating: 4.3,
    users: "6K+",
    icon: Shield,
    featured: false,
    tags: ["Repair", "Fix", "Corrupted"]
  }
];

// PDF Conversion Tools Data
export const conversionTools: ToolWithIcon[] = [
  {
    id: "docx-pdf-converter",
    name: "DOCX ↔ PDF Converter",
    title: "Convert DOCX to PDF",
    href: "/tools/docx-pdf-converter",
    description: "Convert between Microsoft Word documents and PDF files with full formatting preservation.",
    category: "PDF Conversion",
    rating: 4.8,
    users: "42K+",
    icon: FileText,
    featured: true,
    tags: ["DOCX", "PDF", "Word", "Convert"]
  },
  {
    id: "excel-pdf-converter",
    name: "Excel ↔ PDF Converter",
    title: "Convert Excel to PDF",
    href: "/tools/excel-pdf-converter",
    description: "Convert between Excel spreadsheets and PDF files with table formatting intact.",
    category: "PDF Conversion",
    rating: 4.7,
    users: "35K+",
    icon: FileText,
    featured: true,
    tags: ["Excel", "Spreadsheet", "PDF", "Convert"]
  },
  {
    id: "ppt-pdf-converter",
    name: "PowerPoint ↔ PDF Converter",
    title: "Convert PowerPoint to PDF",
    href: "/tools/ppt-pdf-converter",
    description: "Convert between PowerPoint presentations and PDF files with slide layouts preserved.",
    category: "PDF Conversion",
    rating: 4.6,
    users: "28K+",
    icon: FileText,
    featured: true,
    tags: ["PowerPoint", "Presentation", "PDF", "Convert"]
  },
  {
    id: "jpg-pdf-converter",
    name: "JPG ↔ PDF Converter",
    title: "Convert JPG to PDF",
    href: "/tools/jpg-pdf-converter",
    description: "Convert between JPG images and PDF files with quality optimization.",
    category: "PDF Conversion",
    rating: 4.9,
    users: "85K+",
    icon: FileImage,
    featured: true,
    tags: ["JPG", "Image", "PDF", "Convert"]
  },
  {
    id: "png-pdf-converter",
    name: "PNG ↔ PDF Converter",
    title: "Convert PNG to PDF",
    href: "/tools/png-pdf-converter",
    description: "Convert between PNG images and PDF files with transparency support.",
    category: "PDF Conversion",
    rating: 4.8,
    users: "72K+",
    icon: FileImage,
    featured: true,
    tags: ["PNG", "Image", "PDF", "Convert"]
  }
];

// Other Tools
export const otherTools: ToolWithIcon[] = [
  {
    id: "ocr-scanner",
    name: "OCR Text Scanner",
    title: "OCR Text Scanner",
    href: "/tools/ocr-scanner",
    description: "Extract text from images and scanned documents with high accuracy.",
    category: "OCR",
    rating: 4.7,
    users: "30K+",
    icon: FileText,
    featured: true,
    tags: ["OCR", "Text", "Extract"]
  },
  {
    id: "file-converter",
    name: "Universal File Converter",
    title: "Universal File Converter",
    href: "/tools/file-converter",
    description: "Convert between 100+ file formats including documents, images, and videos.",
    category: "Conversion",
    rating: 4.6,
    users: "45K+",
    icon: Zap,
    featured: true,
    tags: ["Convert", "Formats", "Universal"]
  },
  {
    id: "ai-chat",
    name: "AI Document Chat",
    title: "AI Document Chat",
    href: "/tools/ai-chat",
    description: "Chat with your documents using advanced AI to get instant answers.",
    category: "AI",
    rating: 4.9,
    users: "22K+",
    icon: Users,
    featured: true,
    tags: ["AI", "Chat", "Analysis"],
    premium: true
  }
];

// Transform image tools to match the expected interface
const transformedImageTools: ToolWithIcon[] = imageTools.map(tool => ({
  ...tool,
  icon: FileImage, // Default icon for image tools
}));

// Combine all tools
export const allTools: ToolWithIcon[] = [...pdfTools, ...conversionTools, ...otherTools, ...transformedImageTools];

export default allTools;
