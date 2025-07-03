"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Search, 
  Grid3X3, 
  Menu, 
  X, 
  FileText, 
  Download,
  Merge,
  Split,
  Edit3,
  Zap,
  ArrowRight,
  Sparkles,
  FileImage,
  Scissors,
  RotateCcw,
  Lock,
  Unlock,
  Settings
} from "lucide-react";
import { cn } from "@/lib/utils";

// Modern Button Component
const Button = React.forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: "default" | "outline" | "ghost" | "secondary";
    size?: "default" | "sm" | "lg" | "icon";
  }
>(({ className, variant = "default", size = "default", ...props }, ref) => {
  const baseClasses = "inline-flex items-center justify-center rounded-xl font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 active:scale-[0.98]";
  
  const variants = {
    default: "bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 shadow-lg hover:shadow-xl",
    outline: "border-2 border-gray-200 bg-white text-gray-900 hover:bg-gray-50 hover:border-gray-300",
    ghost: "text-gray-600 hover:text-gray-900 hover:bg-gray-100",
    secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200",
  };

  const sizes = {
    default: "h-12 px-6 py-3 text-sm",
    sm: "h-9 px-4 py-2 text-xs",
    lg: "h-14 px-8 py-4 text-base",
    icon: "h-10 w-10",
  };

  return (
    <button
      className={cn(baseClasses, variants[variant], sizes[size], className)}
      ref={ref}
      {...props}
    />
  );
});
Button.displayName = "Button";

// Modern Card Component
const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-2xl border border-gray-200 bg-white/80 backdrop-blur-sm shadow-sm hover:shadow-md transition-all duration-200",
      className
    )}
    {...props}
  />
));
Card.displayName = "Card";

// Tool interface
interface Tool {
  id: string;
  name: string;
  description: string;
  icon: React.ComponentType<React.SVGProps<SVGSVGElement>>;
  href: string;
  category: string;
  featured?: boolean;
  new?: boolean;
  popular?: boolean;
  free?: boolean;
}

// Tools data with modern categories
const toolsData: Tool[] = [
  // PDF Management Tools
  {
    id: "pdf-merge",
    name: "Merge PDF",
    description: "Combine multiple PDF files into one document",
    icon: Merge,
    href: "/tools/merge-pdf",
    category: "PDF Tools",
    featured: true,
    popular: true,
    free: true
  },
  {
    id: "pdf-split", 
    name: "Split PDF",
    description: "Separate PDF pages into individual files",
    icon: Split,
    href: "/tools/split-pdf",
    category: "PDF Tools",
    featured: true,
    free: true
  },
  {
    id: "pdf-compress",
    name: "Compress PDF",
    description: "Reduce PDF file size without losing quality",
    icon: Download,
    href: "/tools/compress-pdf",
    category: "PDF Tools",
    featured: true,
    popular: true,
    free: true
  },
  {
    id: "pdf-protect",
    name: "Protect PDF",
    description: "Add password protection to your PDF files",
    icon: Lock,
    href: "/tools/protect-pdf",
    category: "PDF Tools",
    free: true
  },
  {
    id: "pdf-unlock",
    name: "Unlock PDF",
    description: "Remove password protection from PDF files",
    icon: Unlock,
    href: "/tools/unlock-pdf",
    category: "PDF Tools",
    free: true
  },
  {
    id: "pdf-edit",
    name: "Edit PDF",
    description: "Add text, images, and annotations to PDFs",
    icon: Edit3,
    href: "/tools/edit-pdf",
    category: "PDF Tools",
    featured: true,
    free: true
  },
  {
    id: "pdf-sign",
    name: "Sign PDF",
    description: "Add electronic signatures to PDF documents",
    icon: Edit3,
    href: "/tools/sign-pdf",
    category: "PDF Tools",
    popular: true,
    free: true
  },
  {
    id: "pdf-rotate",
    name: "Rotate PDF",
    description: "Rotate PDF pages to the correct orientation",
    icon: RotateCcw,
    href: "/tools/rotate-pdf",
    category: "PDF Tools",
    free: true
  },
  
  // Conversion Tools
  {
    id: "word-to-pdf",
    name: "Word to PDF",
    description: "Convert Word documents to PDF format",
    icon: FileText,
    href: "/tools/word-to-pdf",
    category: "Convert",
    featured: true,
    popular: true,
    free: true
  },
  {
    id: "excel-to-pdf",
    name: "Excel to PDF", 
    description: "Convert Excel spreadsheets to PDF",
    icon: FileText,
    href: "/tools/excel-to-pdf",
    category: "Convert",
    featured: true,
    free: true
  },
  {
    id: "ppt-to-pdf",
    name: "PowerPoint to PDF",
    description: "Convert presentations to PDF format", 
    icon: FileText,
    href: "/tools/ppt-to-pdf",
    category: "Convert",
    free: true
  },
  {
    id: "jpg-to-pdf",
    name: "JPG to PDF",
    description: "Convert images to PDF documents",
    icon: FileImage,
    href: "/tools/jpg-to-pdf",
    category: "Convert",
    popular: true,
    free: true
  },
  
  // Image Tools
  {
    id: "image-resize",
    name: "Resize Image",
    description: "Change image dimensions and size",
    icon: FileImage,
    href: "/tools/resize-image",
    category: "Image Tools",
    free: true
  },
  {
    id: "image-compress",
    name: "Compress Image",
    description: "Reduce image file size while maintaining quality",
    icon: Zap,
    href: "/tools/compress-image", 
    category: "Image Tools",
    popular: true,
    free: true
  },
  {
    id: "image-crop",
    name: "Crop Image",
    description: "Crop and trim images to focus on specific areas",
    icon: Scissors,
    href: "/tools/crop-image",
    category: "Image Tools",
    free: true
  },
  
  // Text Tools
  {
    id: "word-counter",
    name: "Word Counter",
    description: "Count words, characters, and paragraphs",
    icon: FileText,
    href: "/tools/word-counter",
    category: "Text Tools",
    free: true
  },
  {
    id: "case-converter",
    name: "Case Converter",
    description: "Convert text between different cases",
    icon: Settings,
    href: "/tools/case-converter",
    category: "Text Tools",
    free: true
  }
];

const categories = [
  { id: "all", name: "All Tools", icon: Grid3X3 },
  { id: "PDF Tools", name: "PDF", icon: FileText },
  { id: "Convert", name: "Convert", icon: RotateCcw },
  { id: "Image Tools", name: "Images", icon: FileImage },
  { id: "Text Tools", name: "Text", icon: Settings }
];

const ModernHomepage = (): JSX.Element => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Filter tools based on search and category
  const filteredTools = toolsData.filter(tool => {
    const matchesSearch = tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         tool.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === "all" || tool.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const featuredTools = toolsData.filter(tool => tool.featured);

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <Zap className="h-4 w-4 text-white" />
              </div>
              <span className="text-xl font-semibold text-gray-900">
                ToolsMania
              </span>
            </div>
            
            <div className="hidden md:flex items-center space-x-6">
              <a href="#tools" className="text-gray-600 hover:text-gray-900 transition-colors font-medium">Tools</a>
              <a href="#about" className="text-gray-600 hover:text-gray-900 transition-colors font-medium">About</a>
              <a href="#pricing" className="text-gray-600 hover:text-gray-900 transition-colors font-medium">Pricing</a>
              <Button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors">Get Started</Button>
            </div>

            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden border-t border-gray-100 bg-white"
            >
              <div className="px-4 py-4 space-y-3">
                <a href="#tools" className="block text-gray-600 font-medium">Tools</a>
                <a href="#about" className="block text-gray-600 font-medium">About</a>
                <a href="#pricing" className="block text-gray-600 font-medium">Pricing</a>
                <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium">Get Started</Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>

      {/* Hero Section */}
      <section className="relative py-16 lg:py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <div className="inline-flex items-center px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-sm font-medium mb-6">
                <Sparkles className="w-4 h-4 mr-2" />
                Free online tools
              </div>
              
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
                Make files work
                <span className="block text-blue-600">
                  for you
                </span>
              </h1>
              
              <p className="text-lg text-gray-600 mb-10 max-w-2xl mx-auto">
                Transform, convert, and edit your documents instantly. Free, secure, and easy to use.
              </p>
            </motion.div>

            {/* Search Section */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="max-w-xl mx-auto mb-12"
            >
              <div className="relative mb-6">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search tools..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full h-12 pl-12 pr-4 text-base rounded-lg border border-gray-300 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                />
              </div>

              {/* Category Pills */}
              <div className="flex flex-wrap gap-2 justify-center">
                {categories.map((category) => (
                  <button
                    key={category.id}
                    onClick={() => setSelectedCategory(category.id)}
                    className={cn(
                      "inline-flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all",
                      selectedCategory === category.id
                        ? "bg-blue-600 text-white"
                        : "bg-white text-gray-700 hover:bg-gray-50 border border-gray-200"
                    )}
                  >
                    <category.icon className="w-4 h-4 mr-2" />
                    {category.name}
                  </button>
                ))}
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Featured Tools */}
      <section className="py-20 bg-white/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              Most Popular Tools
            </h2>
            <p className="text-xl text-gray-600">
              Get started with our most frequently used tools
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredTools.map((tool, index) => (
              <motion.div
                key={tool.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <Card className="group p-5 hover:shadow-lg transition-all duration-200 cursor-pointer border border-gray-200 hover:border-blue-300">
                  <div className="flex items-start space-x-3">
                    <div className="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center group-hover:bg-blue-100 transition-all">
                      <tool.icon className="w-5 h-5 text-blue-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-1">
                        <h3 className="text-base font-medium text-gray-900 truncate">
                          {tool.name}
                        </h3>
                        {tool.popular && (
                          <span className="text-xs font-medium text-orange-600 bg-orange-50 px-2 py-1 rounded-md">
                            Popular
                          </span>
                        )}
                      </div>
                      <p className="text-gray-600 text-sm line-clamp-2 mb-3">
                        {tool.description}
                      </p>
                      <div className="flex items-center justify-between">
                        {tool.free && (
                          <span className="text-xs font-medium text-green-600">
                            Free
                          </span>
                        )}
                        <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-blue-600 group-hover:translate-x-0.5 transition-all ml-auto" />
                      </div>
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* All Tools Section */}
      <section id="tools" className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              All Tools
            </h2>
            <p className="text-xl text-gray-600">
              {filteredTools.length} tools found
              {selectedCategory !== "all" && ` in ${categories.find(c => c.id === selectedCategory)?.name}`}
            </p>
          </div>

          {filteredTools.length === 0 ? (
            <div className="text-center py-16">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Search className="h-8 w-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No tools found</h3>
              <p className="text-gray-600 mb-4">
                Try adjusting your search or selecting a different category.
              </p>
              <Button onClick={() => { setSearchQuery(""); setSelectedCategory("all"); }}>
                Clear filters
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filteredTools.map((tool, index) => (
                <motion.div
                  key={tool.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.05 }}
                >
                  <Card className="group p-5 hover:shadow-lg transition-all duration-200 cursor-pointer border border-gray-200 hover:border-blue-300">
                    <div className="flex items-start space-x-3">
                      <div className="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center group-hover:bg-blue-100 transition-all">
                        <tool.icon className="w-5 h-5 text-blue-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2 mb-1">
                          <h3 className="text-base font-medium text-gray-900 truncate">
                            {tool.name}
                          </h3>
                          {tool.new && (
                            <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded-md">
                              New
                            </span>
                          )}
                          {tool.popular && (
                            <span className="text-xs font-medium text-orange-600 bg-orange-50 px-2 py-1 rounded-md">
                              Popular
                            </span>
                          )}
                        </div>
                        <p className="text-gray-600 text-sm line-clamp-2 mb-3">
                          {tool.description}
                        </p>
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-gray-500">
                            {tool.category}
                          </span>
                          <div className="flex items-center space-x-2">
                            {tool.free && (
                              <span className="text-xs font-medium text-green-600">
                                Free
                              </span>
                            )}
                            <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-blue-600 group-hover:translate-x-0.5 transition-all" />
                          </div>
                        </div>
                      </div>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Ready to boost your productivity?
          </h2>
          <p className="text-xl text-indigo-100 mb-8">
            Join thousands of users who trust our tools for their daily work.
          </p>
          <Button size="lg" variant="secondary" className="bg-white text-indigo-600 hover:bg-gray-50">
            Get Started Now
            <ArrowRight className="w-5 h-5 ml-2" />
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center">
                  <Zap className="h-4 w-4 text-white" />
                </div>
                <span className="text-xl font-bold">ToolsMania</span>
              </div>
              <p className="text-gray-400">
                Your ultimate destination for powerful online tools.
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Tools</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">PDF Tools</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Convert Files</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Image Tools</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Text Tools</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Status</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
            <p>&copy; 2024 ToolsMania. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ModernHomepage;
