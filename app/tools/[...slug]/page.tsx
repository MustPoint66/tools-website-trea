"use client"

import React from "react";
import ToolTemplate from "@/components/ui/tool-template";
import { 
  FileText, 
  Image, 
  Type, 
  Calculator, 
  Code, 
  Settings,
  Zap,
  Shield,
  Sparkles,
  LucideIcon,
  Archive,
  Maximize,
  User,
  Smartphone,
  RefreshCw,
  Paintbrush,
  Palette,
  Layers,
  Eye,
  Crop,
  Circle,
  Grid,
  Plus,
  Languages,
  Grid3X3,
  Square,
  Layout,
  Play,
  FlipHorizontal,
  Info,
  Download,
  Contrast
} from "lucide-react";

// Tool data mapping
interface ToolInfo {
  title: string;
  description: string;
  icon: LucideIcon;
}

const toolData: Record<string, ToolInfo> = {
  // PDF Management Tools
  "pdf-organizer": {
    title: "PDF Organizer",
    description: "Organize and rearrange PDF pages with drag-and-drop functionality.",
    icon: Settings
  },
  "pdf-merger": {
    title: "PDF Merger",
    description: "Merge multiple PDF files into a single document.",
    icon: FileText
  },
  "pdf-splitter": {
    title: "PDF Splitter",
    description: "Split PDF files into separate pages or sections.",
    icon: FileText
  },
  "pdf-page-resizer": {
    title: "PDF Page Resizer",
    description: "Resize PDF pages to different dimensions and paper sizes.",
    icon: Settings
  },
  "pdf-page-deleter": {
    title: "PDF Page Deleter",
    description: "Remove unwanted pages from PDF documents.",
    icon: FileText
  },
  "pdf-content-extractor": {
    title: "PDF Content Extractor",
    description: "Extract text, images, and other content from PDF files.",
    icon: FileText
  },
  "pdf-page-rotator": {
    title: "PDF Page Rotator",
    description: "Rotate PDF pages to correct orientation.",
    icon: Settings
  },
  "pdf-page-cropper": {
    title: "PDF Page Cropper",
    description: "Crop PDF pages to remove unwanted margins or areas.",
    icon: Settings
  },
  "pdf-viewer": {
    title: "PDF Viewer",
    description: "View PDF documents online without downloading.",
    icon: FileText
  },
  "pdf-repair": {
    title: "PDF Repair",
    description: "Repair corrupted or damaged PDF files.",
    icon: Settings
  },
  "pdf-unlocker": {
    title: "PDF Unlocker",
    description: "Remove password protection and restrictions from PDF files.",
    icon: Shield
  },
  "pdf-protector": {
    title: "PDF Protector",
    description: "Add password protection and security to PDF files.",
    icon: Shield
  },
  "pdf-form-flattener": {
    title: "PDF Form Flattener",
    description: "Flatten PDF forms to make them non-editable.",
    icon: Settings
  },
  "pdf-page-numbering": {
    title: "PDF Page Numbering",
    description: "Add page numbers to PDF documents.",
    icon: Settings
  },
  "pdf-headers-footers": {
    title: "PDF Headers & Footers",
    description: "Add headers and footers to PDF pages.",
    icon: Settings
  },
  "pdf-metadata-editor": {
    title: "PDF Metadata Editor",
    description: "Edit PDF metadata including title, author, and keywords.",
    icon: Settings
  },
  "pdf-compressor": {
    title: "PDF Compressor",
    description: "Compress PDF files to reduce file size while maintaining quality.",
    icon: Zap
  },
  "pdf-editor": {
    title: "PDF Editor",
    description: "Edit PDF documents with advanced editing tools.",
    icon: Settings
  },
  "pdf-add-text": {
    title: "PDF Add Text",
    description: "Add text annotations and comments to PDF documents.",
    icon: Type
  },
  "pdf-add-image": {
    title: "PDF Add Image",
    description: "Insert images and graphics into PDF documents.",
    icon: Image
  },
  "pdf-watermark": {
    title: "PDF Watermark",
    description: "Add watermarks to PDF documents for branding or security.",
    icon: Shield
  },
  "pdf-edit-text": {
    title: "PDF Edit Text",
    description: "Edit existing text content in PDF documents.",
    icon: Type
  },
  "pdf-whiteout": {
    title: "PDF Whiteout",
    description: "Remove or cover unwanted text and content in PDFs.",
    icon: Settings
  },
  "pdf-annotate": {
    title: "PDF Annotate",
    description: "Add annotations, comments, and markup to PDF documents.",
    icon: Settings
  },
  "pdf-highlight": {
    title: "PDF Highlight",
    description: "Highlight important text and sections in PDF documents.",
    icon: Palette
  },
  "pdf-sign": {
    title: "PDF Sign",
    description: "Add digital signatures to PDF documents.",
    icon: Shield
  },
  "pdf-filler": {
    title: "PDF Form Filler",
    description: "Fill out PDF forms and documents electronically.",
    icon: Settings
  },
  
  // PDF Conversion Tools
  "pdf-to-docx": {
    title: "PDF to DOCX",
    description: "Convert PDF files to Microsoft Word DOCX format.",
    icon: FileText
  },
  "pdf-to-excel": {
    title: "PDF to Excel",
    description: "Convert PDF files to Microsoft Excel format.",
    icon: FileText
  },
  "excel-to-pdf": {
    title: "Excel to PDF",
    description: "Convert Microsoft Excel files to PDF format.",
    icon: FileText
  },
  "pdf-to-powerpoint": {
    title: "PDF to PowerPoint",
    description: "Convert PDF files to Microsoft PowerPoint format.",
    icon: FileText
  },
  "powerpoint-to-pdf": {
    title: "PowerPoint to PDF",
    description: "Convert Microsoft PowerPoint files to PDF format.",
    icon: FileText
  },
  "pdf-to-jpg": {
    title: "PDF to JPG",
    description: "Convert PDF pages to JPG image format.",
    icon: Image
  },
  "jpg-to-pdf": {
    title: "JPG to PDF",
    description: "Convert JPG images to PDF format.",
    icon: FileText
  },
  "pdf-to-png": {
    title: "PDF to PNG",
    description: "Convert PDF pages to PNG image format.",
    icon: Image
  },
  "png-to-pdf": {
    title: "PNG to PDF",
    description: "Convert PNG images to PDF format.",
    icon: FileText
  },
  "pdf-to-text": {
    title: "PDF to Text",
    description: "Extract plain text from PDF documents.",
    icon: Type
  },
  "text-to-pdf": {
    title: "Text to PDF",
    description: "Convert plain text files to PDF format.",
    icon: FileText
  },
  "pdf-to-html": {
    title: "PDF to HTML",
    description: "Convert PDF documents to HTML web format.",
    icon: Code
  },
  "html-to-pdf": {
    title: "HTML to PDF",
    description: "Convert HTML web pages to PDF format.",
    icon: FileText
  },
  
  // OCR and AI Tools
  "ocr-text-scanner": {
    title: "OCR Text Scanner",
    description: "Extract text from images and scanned documents using OCR.",
    icon: Type
  },
  "universal-file-converter": {
    title: "Universal File Converter",
    description: "Convert between 100+ file formats including documents, images, and more.",
    icon: Settings
  },
  "ai-document-chat": {
    title: "AI Document Chat",
    description: "Chat with your documents using AI to extract insights and answers.",
    icon: Sparkles
  },
  
// Bi-directional Document Conversions
"docx-to-pdf": {
  title: "DOCX to PDF Converter",
  description: "Convert Microsoft Word documents to PDF format while maintaining formatting.",
  icon: FileText
},
"xlsx-to-pdf": {
  title: "Excel to PDF Converter",
  description: "Convert Microsoft Excel spreadsheets to PDF format.",
  icon: FileText
},
"pdf-to-xlsx": {
  title: "PDF to Excel Converter",
  description: "Convert PDF files to Microsoft Excel spreadsheets with table recognition.",
  icon: FileText
},
"pptx-to-pdf": {
  title: "PowerPoint to PDF Converter",
  description: "Convert Microsoft PowerPoint presentations to PDF format.",
  icon: FileText
},
"pdf-to-pptx": {
  title: "PDF to PowerPoint Converter",
  description: "Convert PDF files to Microsoft PowerPoint presentations.",
  icon: FileText
},
"txt-to-pdf": {
  title: "Text to PDF Converter",
  description: "Convert plain text files to PDF format with formatting options.",
  icon: FileText
},
"pdf-to-txt": {
  title: "PDF to Text Converter",
  description: "Extract text content from PDF files and save as plain text.",
  icon: FileText
},

// Additional Format Conversions
"jpg-to-heic": {
  title: "JPG to HEIC Converter",
  description: "Convert JPG images to HEIC format for efficient storage.",
  icon: RefreshCw
},
"png-to-heic": {
  title: "PNG to HEIC Converter",
  description: "Convert PNG images to HEIC format.",
  icon: RefreshCw
},
"svg-to-jpg": {
  title: "SVG to JPG Converter",
  description: "Convert SVG vector graphics to JPG format.",
  icon: RefreshCw
},
"jpg-to-eps": {
  title: "JPG to EPS Converter",
  description: "Convert JPG images to EPS vector format.",
  icon: RefreshCw
},
"avif-to-jpg": {
  title: "AVIF to JPG Converter",
  description: "Convert AVIF images to JPG format.",
  icon: RefreshCw
},
"avif-to-png": {
  title: "AVIF to PNG Converter",
  description: "Convert AVIF images to PNG format.",
  icon: RefreshCw
},
"avif-to-webp": {
  title: "AVIF to WEBP Converter",
  description: "Convert AVIF images to WEBP format.",
  icon: RefreshCw
},

// Legacy Document Tools
  "text-formatter": {
    title: "Text Formatter",
    description: "Format and style your text with various formatting options.",
    icon: Settings
  },
  "document-merger": {
    title: "Document Merger",
    description: "Merge multiple documents into a single file.",
    icon: FileText
  },
  "document-viewer": {
    title: "Document Viewer",
    description: "View documents online without downloading.",
    icon: FileText
  },
  "pdf-to-word": {
    title: "PDF to Word",
    description: "Convert PDF documents to Word format.",
    icon: FileText
  },
  "word-to-pdf": {
    title: "Word to PDF",
    description: "Convert Word documents to PDF format.",
    icon: FileText
  },
  "ppt-to-pdf": {
    title: "PowerPoint to PDF",
    description: "Convert PowerPoint presentations to PDF format.",
    icon: FileText
  },
  "pdf-unlock": {
    title: "PDF Unlock",
    description: "Remove password protection from PDF files.",
    icon: Shield
  },
  "pdf-rotate": {
    title: "PDF Rotate",
    description: "Rotate PDF pages to the correct orientation.",
    icon: Settings
  },
  
// Image Tools

"image-to-text": {
  title: "Image To Text",
  description: "Extract text from images using OCR technology.",
  icon: FileText
},
"compress-image": {
  title: "Compress Image Size",
  description: "Compress your image to reduce file size.",
  icon: Archive
},
"resize-image": {
  title: "Resize Image Dimensions",
  description: "Resize your image dimensions.",
  icon: Maximize
},
"profile-photo-maker": {
  title: "Profile Photo Maker",
  description: "Create round profile photo from image.",
  icon: User
},
"heic-to-jpg": {
  title: "HEIC to JPG",
  description: "Convert an iPhone HEIC image to JPG.",
  icon: Smartphone
},
"blur-background": {
  title: "Blur Background Tools",
  description: "Image background blur effect.",
  icon: Zap
},
"webp-to-jpg": {
  title: "WebP to JPG",
  description: "Convert a WebP image to JPG format.",
  icon: RefreshCw
},
"cleanup-picture": {
  title: "Cleanup Picture",
  description: "Cleanup picture and remove unwanted elements.",
  icon: Paintbrush
},
"combine-images": {
  title: "Combine Images",
  description: "Combine Images Online into one.",
  icon: Layers
},
"transparent-background": {
  title: "Make Background Transparent",
  description: "Make background transparent.",
  icon: Eye
},
"png-to-jpg": {
  title: "PNG to JPG",
  description: "Convert a PNG Image to JPG Online.",
  icon: RefreshCw
},
"webp-to-png": {
  title: "WEBP to PNG",
  description: "Convert a WEBP Image to PNG Online.",
  icon: RefreshCw
},
"crop-image": {
  title: "Crop Image",
  description: "Crop your image to desired dimensions.",
  icon: Crop
},
"jpg-to-png": {
  title: "JPG to PNG",
  description: "Convert a JPG Image to PNG Online.",
  icon: RefreshCw
},
"png-to-webp": {
  title: "PNG to WEBP",
  description: "Convert a PNG Image to WEBP Online.",
  icon: RefreshCw
},
"jpg-to-webp": {
  title: "JPG to WEBP",
  description: "Convert a JPG Image to WEBP Online.",
  icon: RefreshCw
},
"make-round-image": {
  title: "Make Round Image",
  description: "Make round image with circular crop.",
  icon: Circle
},
"png-to-svg": {
  title: "PNG to SVG",
  description: "Convert a PNG Image to SVG Online.",
  icon: RefreshCw
},
"add-text-to-image": {
  title: "Add Text to an Image",
  description: "Easily Add Text To an Image Online.",
  icon: Type
},
"jpg-to-svg": {
  title: "JPG to SVG",
  description: "Convert a JPG Image to SVG Online.",
  icon: RefreshCw
},
"black-white": {
  title: "Black & White",
  description: "Make your photo black & white.",
  icon: Contrast
},
"heic-to-png": {
  title: "HEIC to PNG",
  description: "Convert an iPhone HEIC image to PNG.",
  icon: Smartphone
},
"image-splitter": {
  title: "Image Splitter",
  description: "Cut image into pieces.",
  icon: Grid
},
"add-images": {
  title: "Add Images",
  description: "Add images to an existing image.",
  icon: Plus
},
"translate-image": {
  title: "Translate Image",
  description: "Translate text in your image.",
  icon: Languages
},
"pixelate-image": {
  title: "Pixelate Image",
  description: "Pixelate your photo with custom intensity.",
  icon: Grid3X3
},
"add-border": {
  title: "Add Border to Image",
  description: "Add a border to your image.",
  icon: Square
},
"collage-maker": {
  title: "Collage Maker",
  description: "Create Photo Collages Online.",
  icon: Layout
},
"svg-to-png": {
  title: "SVG to PNG",
  description: "Convert a SVG image to PNG free.",
  icon: RefreshCw
},
"gif-to-mp4": {
  title: "GIF to MP4",
  description: "Convert animated GIF to MP4 Online.",
  icon: Play
},
"jpg-to-gif": {
  title: "JPG to GIF",
  description: "Convert a JPG Image to GIF Online.",
  icon: RefreshCw
},
"flip-image": {
  title: "Flip Image",
  description: "Flip Image horizontally or vertically.",
  icon: FlipHorizontal
},
"tiff-to-jpg": {
  title: "TIFF to JPG",
  description: "Convert a TIFF Image to JPG Online.",
  icon: RefreshCw
},
"webp-to-gif": {
  title: "WEBP to GIF",
  description: "Convert a WEBP Image to GIF Online.",
  icon: RefreshCw
},
"view-metadata": {
  title: "View Metadata",
  description: "View metadata for your image.",
  icon: Info
},
"png-to-eps": {
  title: "PNG to EPS",
  description: "Convert a PNG Image to EPS Online.",
  icon: RefreshCw
},
"png-to-gif": {
  title: "PNG to GIF",
  description: "Convert a PNG Image to GIF Online.",
  icon: RefreshCw
},
"jpg-to-tiff": {
  title: "JPG to TIFF",
  description: "Convert a JPG Image to TIFF Online.",
  icon: RefreshCw
},
"eps-to-png": {
  title: "EPS to PNG",
  description: "Convert an EPS image to PNG.",
  icon: RefreshCw
},
"psd-to-jpg": {
  title: "PSD to JPG",
  description: "Convert a PSD Image to JPG Online.",
  icon: RefreshCw
},
"psd-to-png": {
  title: "PSD to PNG",
  description: "Convert a PSD Image to PNG Online.",
  icon: RefreshCw
},
"gif-to-jpg": {
  title: "GIF to JPG",
  description: "Convert a GIF Image to JPG Online.",
  icon: RefreshCw
},
"psd-to-ai": {
  title: "PSD to AI",
  description: "Convert a PSD Image to AI Online.",
  icon: RefreshCw
},
"tiff-to-png": {
  title: "TIFF to PNG",
  description: "Convert a TIFF Image to PNG Online.",
  icon: RefreshCw
},
"gif-to-png": {
  title: "GIF to PNG",
  description: "Convert a GIF Image to PNG Online.",
  icon: RefreshCw
},
"font-awesome-to-png": {
  title: "Font Awesome to PNG",
  description: "Convert Font Awesome icons to PNG.",
  icon: Download
},
"png-to-tiff": {
  title: "PNG to TIFF",
  description: "Convert a PNG Image to TIFF Online.",
  icon: RefreshCw
},
"eps-to-jpg": {
  title: "EPS to JPG",
  description: "Convert a EPS Image to JPG Online.",
  icon: RefreshCw
},
"eps-to-svg": {
  title: "EPS to SVG",
  description: "Convert a EPS Image to SVG Online.",
  icon: RefreshCw
},
"tiff-to-text": {
  title: "TIFF To Text",
  description: "Extract text from TIFF images using OCR.",
  icon: FileText
},
"jpg-to-avif": {
  title: "JPG to AVIF",
  description: "Convert a JPG Image to AVIF Online.",
  icon: RefreshCw
},
"gif-to-apng": {
  title: "GIF to APNG",
  description: "Convert animated GIF Image to APNG Online.",
  icon: RefreshCw
},
"psd-to-svg": {
  title: "PSD to SVG",
  description: "Convert a PSD Image to SVG Online.",
  icon: RefreshCw
},
"png-to-avif": {
  title: "PNG to AVIF",
  description: "Convert a PNG Image to AVIF Online.",
  icon: RefreshCw
},
"tiff-to-svg": {
  title: "TIFF to SVG",
  description: "Convert a TIFF Image to SVG Online.",
  icon: RefreshCw
},
"webp-to-avif": {
  title: "WEBP to AVIF",
  description: "Convert a WEBP Image to AVIF Online.",
  icon: RefreshCw
},
"gif-to-avif": {
  title: "GIF to AVIF",
  description: "Convert a GIF Image to AVIF Online.",
  icon: RefreshCw
},
"heic-to-avif": {
  title: "HEIC to AVIF",
  description: "Convert a HEIC Image to AVIF Online.",
  icon: RefreshCw
},
"webp-video-to-jpg": {
  title: "WebP Video Frame Extractor",
  description: "Upload a WebP Video and download all frames as JPG.",
  icon: Play
},
  "image-resizer": {
    title: "Image Resizer",
    description: "Resize images to custom dimensions quickly.",
    icon: Image
  },
  "image-converter": {
    title: "Image Converter",
    description: "Convert images between different formats.",
    icon: Settings
  },
  "image-compressor": {
    title: "Image Compressor",
    description: "Compress images to reduce file size.",
    icon: Zap
  },
  "image-cropper": {
    title: "Image Cropper",
    description: "Crop images to specific dimensions.",
    icon: Image
  },
  "watermark": {
    title: "Watermark Tool",
    description: "Add watermarks to your images.",
    icon: Shield
  },
  
  // Text Tools
  "case-converter": {
    title: "Case Converter",
    description: "Convert text between different case formats.",
    icon: Type
  },
  "text-encoder": {
    title: "Text Encoder",
    description: "Encode and decode text in various formats.",
    icon: Shield
  },
  "lorem-generator": {
    title: "Lorem Generator",
    description: "Generate placeholder text for your projects.",
    icon: Sparkles
  },
  "text-diff": {
    title: "Text Diff",
    description: "Compare two texts and highlight differences.",
    icon: Settings
  },
  "regex-tester": {
    title: "Regex Tester",
    description: "Test and validate regular expressions.",
    icon: Code
  },
  "text-counter": {
    title: "Text Counter",
    description: "Count characters, words, and lines in text.",
    icon: Calculator
  },
  
  // Developer Tools section removed as requested

  
  // Calculators
  "calculator": {
    title: "Basic Calculator",
    description: "Perform basic mathematical calculations.",
    icon: Calculator
  },
  "percentage-calc": {
    title: "Percentage Calculator",
    description: "Calculate percentages and percentage changes.",
    icon: Calculator
  },
  "unit-converter": {
    title: "Unit Converter",
    description: "Convert between different units of measurement.",
    icon: Settings
  },
  "date-calculator": {
    title: "Date Calculator",
    description: "Calculate differences between dates.",
    icon: Calculator
  },
  "bmi-calculator": {
    title: "BMI Calculator",
    description: "Calculate your Body Mass Index.",
    icon: Calculator
  },
  "loan-calculator": {
    title: "Loan Calculator",
    description: "Calculate loan payments and interest.",
    icon: Calculator
  },
  
  // Color Tools section removed as requested
};

interface ToolPageProps {
  params: {
    slug: string[];
  };
}

const ToolPage: React.FC<ToolPageProps> = ({ params }) => {
  const toolSlug = params.slug.join("/");
  const tool = toolData[toolSlug];

  if (!tool) {
    return (
      <ToolTemplate
        title="Tool Not Found"
        description="The tool you're looking for doesn't exist or has been moved."
        icon={FileText}
      />
    );
  }

  return (
    <ToolTemplate
      title={tool.title}
      description={tool.description}
      icon={tool.icon}
    />
  );
};

export default ToolPage;
