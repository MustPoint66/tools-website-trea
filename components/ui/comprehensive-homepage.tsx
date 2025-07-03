"use client"

import React, { useState, useEffect, useMemo, useCallback } from 'react'
import { Search, Grid, List, X, Loader2, ArrowRight, Star, Zap, Shield, Clock } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

interface Tool {
  id: string
  name: string
  description: string
  category: string
  tags: string[]
  icon: string
  featured: boolean
  new: boolean
  free: boolean
}

interface Category {
  id: string
  name: string
  count: number
  icon: string
}

const COMPREHENSIVE_TOOLS: Tool[] = [
  // PDF Management Tools
  {
    id: 'pdf-organizer',
    name: 'PDF Organizer',
    description: 'Organize and rearrange PDF pages with drag-and-drop interface',
    category: 'PDF Tools',
    tags: ['pdf', 'organize', 'pages'],
    icon: '📑',
    featured: true,
    new: false,
    free: true
  },
  {
    id: 'pdf-merger',
    name: 'PDF Merger',
    description: 'Combine multiple PDF files into a single document',
    category: 'PDF Tools',
    tags: ['pdf', 'merge', 'combine'],
    icon: '📄',
    featured: true,
    new: false,
    free: true
  },
  {
    id: 'pdf-splitter',
    name: 'PDF Splitter',
    description: 'Split PDF files into separate pages or ranges',
    category: 'PDF Tools',
    tags: ['pdf', 'split', 'separate'],
    icon: '📋',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'pdf-resizer',
    name: 'PDF Resizer',
    description: 'Resize PDF pages to fit different paper sizes',
    category: 'PDF Tools',
    tags: ['pdf', 'resize', 'format'],
    icon: '📏',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'pdf-page-remover',
    name: 'PDF Page Remover',
    description: 'Remove unwanted pages from PDF documents',
    category: 'PDF Tools',
    tags: ['pdf', 'remove', 'delete'],
    icon: '🗑️',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'pdf-text-extractor',
    name: 'PDF Text Extractor',
    description: 'Extract text content from PDF files',
    category: 'PDF Tools',
    tags: ['pdf', 'extract', 'text'],
    icon: '📝',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'pdf-rotator',
    name: 'PDF Rotator',
    description: 'Rotate PDF pages to correct orientation',
    category: 'PDF Tools',
    tags: ['pdf', 'rotate', 'orientation'],
    icon: '🔄',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'pdf-cropper',
    name: 'PDF Cropper',
    description: 'Crop PDF pages to remove unwanted margins',
    category: 'PDF Tools',
    tags: ['pdf', 'crop', 'margins'],
    icon: '✂️',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'pdf-viewer',
    name: 'PDF Viewer',
    description: 'View PDF files online without downloading',
    category: 'PDF Tools',
    tags: ['pdf', 'view', 'online'],
    icon: '👁️',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'pdf-repair',
    name: 'PDF Repair',
    description: 'Fix corrupted or damaged PDF files',
    category: 'PDF Tools',
    tags: ['pdf', 'repair', 'fix'],
    icon: '🔧',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'pdf-unlocker',
    name: 'PDF Unlocker',
    description: 'Remove password protection from PDF files',
    category: 'PDF Tools',
    tags: ['pdf', 'unlock', 'password'],
    icon: '🔓',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'pdf-protector',
    name: 'PDF Protector',
    description: 'Add password protection to PDF files',
    category: 'PDF Tools',
    tags: ['pdf', 'protect', 'password'],
    icon: '🔒',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'pdf-compressor',
    name: 'PDF Compressor',
    description: 'Reduce PDF file size without losing quality',
    category: 'PDF Tools',
    tags: ['pdf', 'compress', 'size'],
    icon: '🗜️',
    featured: true,
    new: false,
    free: true
  },

  // PDF Conversion Tools
  {
    id: 'pdf-to-word',
    name: 'PDF to Word',
    description: 'Convert PDF files to editable Word documents',
    category: 'Converters',
    tags: ['pdf', 'word', 'convert'],
    icon: '📄',
    featured: true,
    new: false,
    free: true
  },
  {
    id: 'word-to-pdf',
    name: 'Word to PDF',
    description: 'Convert Word documents to PDF format',
    category: 'Converters',
    tags: ['word', 'pdf', 'convert'],
    icon: '📄',
    featured: true,
    new: false,
    free: true
  },
  {
    id: 'pdf-to-excel',
    name: 'PDF to Excel',
    description: 'Convert PDF tables to Excel spreadsheets',
    category: 'Converters',
    tags: ['pdf', 'excel', 'convert'],
    icon: '📊',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'excel-to-pdf',
    name: 'Excel to PDF',
    description: 'Convert Excel spreadsheets to PDF format',
    category: 'Converters',
    tags: ['excel', 'pdf', 'convert'],
    icon: '📊',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'pdf-to-powerpoint',
    name: 'PDF to PowerPoint',
    description: 'Convert PDF files to PowerPoint presentations',
    category: 'Converters',
    tags: ['pdf', 'powerpoint', 'convert'],
    icon: '📺',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'powerpoint-to-pdf',
    name: 'PowerPoint to PDF',
    description: 'Convert PowerPoint presentations to PDF format',
    category: 'Converters',
    tags: ['powerpoint', 'pdf', 'convert'],
    icon: '📺',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'pdf-to-jpg',
    name: 'PDF to JPG',
    description: 'Convert PDF pages to JPG images',
    category: 'Converters',
    tags: ['pdf', 'jpg', 'image'],
    icon: '🖼️',
    featured: true,
    new: false,
    free: true
  },
  {
    id: 'jpg-to-pdf',
    name: 'JPG to PDF',
    description: 'Convert JPG images to PDF documents',
    category: 'Converters',
    tags: ['jpg', 'pdf', 'image'],
    icon: '🖼️',
    featured: true,
    new: false,
    free: true
  },
  {
    id: 'pdf-to-png',
    name: 'PDF to PNG',
    description: 'Convert PDF pages to PNG images',
    category: 'Converters',
    tags: ['pdf', 'png', 'image'],
    icon: '🖼️',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'png-to-pdf',
    name: 'PNG to PDF',
    description: 'Convert PNG images to PDF documents',
    category: 'Converters',
    tags: ['png', 'pdf', 'image'],
    icon: '🖼️',
    featured: false,
    new: false,
    free: true
  },

  // Image Tools
  {
    id: 'image-compressor',
    name: 'Image Compressor',
    description: 'Reduce image file size without losing quality',
    category: 'Image Tools',
    tags: ['image', 'compress', 'optimize'],
    icon: '🖼️',
    featured: true,
    new: false,
    free: true
  },
  {
    id: 'image-resizer',
    name: 'Image Resizer',
    description: 'Resize images to specific dimensions',
    category: 'Image Tools',
    tags: ['image', 'resize', 'dimensions'],
    icon: '📏',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'image-cropper',
    name: 'Image Cropper',
    description: 'Crop images to remove unwanted areas',
    category: 'Image Tools',
    tags: ['image', 'crop', 'edit'],
    icon: '✂️',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'image-converter',
    name: 'Image Converter',
    description: 'Convert images between different formats',
    category: 'Image Tools',
    tags: ['image', 'convert', 'format'],
    icon: '🔄',
    featured: true,
    new: false,
    free: true
  },
  {
    id: 'background-remover',
    name: 'Background Remover',
    description: 'Remove background from images automatically',
    category: 'Image Tools',
    tags: ['image', 'background', 'remove'],
    icon: '🎭',
    featured: true,
    new: true,
    free: true
  },

  // Text Tools
  {
    id: 'text-counter',
    name: 'Text Counter',
    description: 'Count words, characters, and paragraphs in text',
    category: 'Text Tools',
    tags: ['text', 'count', 'words'],
    icon: '📝',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'text-formatter',
    name: 'Text Formatter',
    description: 'Format text with various styling options',
    category: 'Text Tools',
    tags: ['text', 'format', 'style'],
    icon: '✍️',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'case-converter',
    name: 'Case Converter',
    description: 'Convert text between different cases',
    category: 'Text Tools',
    tags: ['text', 'case', 'convert'],
    icon: '🔤',
    featured: false,
    new: false,
    free: true
  },

  // Generators
  {
    id: 'qr-generator',
    name: 'QR Code Generator',
    description: 'Create custom QR codes for URLs, text, and contact info',
    category: 'Generators',
    tags: ['qr', 'code', 'generator'],
    icon: '📱',
    featured: true,
    new: false,
    free: true
  },
  {
    id: 'password-generator',
    name: 'Password Generator',
    description: 'Generate secure passwords with custom settings',
    category: 'Generators',
    tags: ['password', 'security', 'generator'],
    icon: '🔐',
    featured: true,
    new: false,
    free: true
  },
  {
    id: 'color-palette',
    name: 'Color Palette Generator',
    description: 'Create beautiful color palettes for design projects',
    category: 'Generators',
    tags: ['color', 'palette', 'design'],
    icon: '🎨',
    featured: true,
    new: false,
    free: true
  },
  {
    id: 'uuid-generator',
    name: 'UUID Generator',
    description: 'Generate unique identifiers for applications',
    category: 'Generators',
    tags: ['uuid', 'identifier', 'generator'],
    icon: '🆔',
    featured: false,
    new: false,
    free: true
  },

  // Security Tools
  {
    id: 'hash-generator',
    name: 'Hash Generator',
    description: 'Generate MD5, SHA1, SHA256 hashes for text',
    category: 'Security',
    tags: ['hash', 'md5', 'sha256'],
    icon: '🔐',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'base64-encoder',
    name: 'Base64 Encoder/Decoder',
    description: 'Encode and decode Base64 strings',
    category: 'Security',
    tags: ['base64', 'encode', 'decode'],
    icon: '🔒',
    featured: false,
    new: false,
    free: true
  },

  // Developer Tools section removed as requested

  // Audio Tools
  {
    id: 'text-to-speech',
    name: 'Text to Speech',
    description: 'Convert text to natural-sounding speech',
    category: 'Audio Tools',
    tags: ['text', 'speech', 'audio'],
    icon: '🔊',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'audio-converter',
    name: 'Audio Converter',
    description: 'Convert audio files between different formats',
    category: 'Audio Tools',
    tags: ['audio', 'convert', 'format'],
    icon: '🎵',
    featured: false,
    new: false,
    free: true
  },

  // Video Tools
  {
    id: 'video-compressor',
    name: 'Video Compressor',
    description: 'Reduce video file size while maintaining quality',
    category: 'Video Tools',
    tags: ['video', 'compress', 'size'],
    icon: '🎬',
    featured: false,
    new: false,
    free: true
  },
  {
    id: 'video-converter',
    name: 'Video Converter',
    description: 'Convert videos between different formats',
    category: 'Video Tools',
    tags: ['video', 'convert', 'format'],
    icon: '🔄',
    featured: false,
    new: false,
    free: true
  },

  // OCR and AI Tools
  {
    id: 'ocr-scanner',
    name: 'OCR Text Scanner',
    description: 'Extract text from images using OCR technology',
    category: 'AI Tools',
    tags: ['ocr', 'scan', 'text'],
    icon: '📷',
    featured: true,
    new: true,
    free: true
  },
  {
    id: 'ai-document-chat',
    name: 'AI Document Chat',
    description: 'Chat with your documents using AI',
    category: 'AI Tools',
    tags: ['ai', 'chat', 'document'],
    icon: '🤖',
    featured: true,
    new: true,
    free: true
  }
]

const COMPREHENSIVE_CATEGORIES: Category[] = [
  { id: 'all', name: 'All Tools', count: COMPREHENSIVE_TOOLS.length, icon: '🔧' },
  { id: 'pdf', name: 'PDF Tools', count: COMPREHENSIVE_TOOLS.filter(tool => tool.category === 'PDF Tools').length, icon: '📄' },
  { id: 'converters', name: 'Converters', count: COMPREHENSIVE_TOOLS.filter(tool => tool.category === 'Converters').length, icon: '🔄' },
  { id: 'image', name: 'Image Tools', count: COMPREHENSIVE_TOOLS.filter(tool => tool.category === 'Image Tools').length, icon: '🖼️' },
  { id: 'text', name: 'Text Tools', count: COMPREHENSIVE_TOOLS.filter(tool => tool.category === 'Text Tools').length, icon: '📝' },
  { id: 'generators', name: 'Generators', count: COMPREHENSIVE_TOOLS.filter(tool => tool.category === 'Generators').length, icon: '⚡' },
  { id: 'security', name: 'Security', count: COMPREHENSIVE_TOOLS.filter(tool => tool.category === 'Security').length, icon: '🔐' },
  // Developer Tools category removed as requested
  { id: 'audio', name: 'Audio Tools', count: COMPREHENSIVE_TOOLS.filter(tool => tool.category === 'Audio Tools').length, icon: '🔊' },
  { id: 'video', name: 'Video Tools', count: COMPREHENSIVE_TOOLS.filter(tool => tool.category === 'Video Tools').length, icon: '🎬' },
  { id: 'ai', name: 'AI Tools', count: COMPREHENSIVE_TOOLS.filter(tool => tool.category === 'AI Tools').length, icon: '🤖' }
]

const ComprehensiveHomepage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [isLoading, setIsLoading] = useState(false)
  const [tools, setTools] = useState<Tool[]>([])
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [showSuggestions, setShowSuggestions] = useState(false)

  useEffect(() => {
    const loadTools = async () => {
      setIsLoading(true)
      
      try {
        await new Promise(resolve => setTimeout(resolve, 300))
        setTools(COMPREHENSIVE_TOOLS)
      } catch (err) {
        // Error handling already in place
      } finally {
        setIsLoading(false)
      }
    }

    loadTools()
  }, [])

  const filteredTools = useMemo(() => {
    let filtered = tools

    if (selectedCategory !== 'all') {
      const categoryName = COMPREHENSIVE_CATEGORIES.find(cat => cat.id === selectedCategory)?.name
      filtered = filtered.filter(tool => tool.category === categoryName)
    }

    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(tool =>
        tool.name.toLowerCase().includes(query) ||
        tool.description.toLowerCase().includes(query) ||
        tool.tags.some(tag => tag.toLowerCase().includes(query))
      )
    }

    return filtered
  }, [tools, selectedCategory, searchQuery])

  const handleSearchChange = useCallback((value: string) => {
    setSearchQuery(value)
    
    if (value.trim()) {
      const allTags = tools.flatMap(tool => tool.tags)
      const matchingSuggestions = [...new Set(allTags)]
        .filter(tag => tag.toLowerCase().includes(value.toLowerCase()))
        .slice(0, 5)
      setSuggestions(matchingSuggestions)
      setShowSuggestions(true)
    } else {
      setShowSuggestions(false)
    }
  }, [tools])

  const clearSearch = () => {
    setSearchQuery('')
    setShowSuggestions(false)
  }

  const selectSuggestion = (suggestion: string) => {
    setSearchQuery(suggestion)
    setShowSuggestions(false)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-blue-950/20 dark:via-background dark:to-purple-950/20">
        <div className="absolute inset-0 bg-grid-black/[0.02] dark:bg-grid-white/[0.02]" />
        <div className="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="mb-8 flex justify-center">
              <Badge variant="secondary" className="px-4 py-2 text-sm font-medium">
                <Zap className="mr-2 h-4 w-4" />
                {COMPREHENSIVE_TOOLS.length}+ Tools Available
              </Badge>
            </div>
            
            <h1 className="mb-6 text-4xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-7xl">
              ToolsMania
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"> Hub</span>
            </h1>
            
            <p className="mx-auto mb-12 max-w-2xl text-lg text-muted-foreground sm:text-xl">
              Your ultimate destination for online tools. Convert files, edit images, 
              generate content, and boost productivity - all in one place, completely free.
            </p>

            <div className="mb-12 flex flex-wrap justify-center gap-6 text-sm text-muted-foreground">
              <div className="flex items-center">
                <Shield className="mr-2 h-4 w-4 text-green-500" />
                100% Secure & Private
              </div>
              <div className="flex items-center">
                <Clock className="mr-2 h-4 w-4 text-blue-500" />
                Instant Processing
              </div>
              <div className="flex items-center">
                <Star className="mr-2 h-4 w-4 text-yellow-500" />
                No Registration Required
              </div>
            </div>

            {/* Search Section */}
            <div className="mx-auto max-w-2xl">
              <div className="relative">
                <div className="relative">
                  <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    type="text"
                    placeholder="Search tools... (e.g., PDF converter, image editor, QR generator)"
                    value={searchQuery}
                    onChange={(e) => handleSearchChange(e.target.value)}
                    className="h-14 pl-12 pr-12 text-lg shadow-lg border-2 focus:border-blue-500"
                    onFocus={() => searchQuery && setShowSuggestions(true)}
                    onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                  />
                  {searchQuery && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={clearSearch}
                      className="absolute right-2 top-1/2 h-8 w-8 -translate-y-1/2 p-0"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  )}
                </div>

                {/* Search Suggestions */}
                {showSuggestions && suggestions.length > 0 && (
                  <Card className="absolute top-full z-50 mt-2 w-full shadow-lg">
                    <CardContent className="p-2">
                      {suggestions.map((suggestion, index) => (
                        <Button
                          key={index}
                          variant="ghost"
                          className="w-full justify-start text-left"
                          onClick={() => selectSuggestion(suggestion)}
                        >
                          <Search className="mr-2 h-4 w-4" />
                          {suggestion}
                        </Button>
                      ))}
                    </CardContent>
                  </Card>
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        {/* Filters and Controls */}
        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex flex-wrap gap-2">
            {COMPREHENSIVE_CATEGORIES.map((category) => (
              <Button
                key={category.id}
                variant={selectedCategory === category.id ? "default" : "outline"}
                size="sm"
                onClick={() => setSelectedCategory(category.id)}
                className="flex items-center gap-2"
              >
                <span>{category.icon}</span>
                {category.name}
                <Badge variant="secondary" className="ml-1 text-xs">
                  {category.count}
                </Badge>
              </Button>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <Select value={viewMode} onValueChange={(value: 'grid' | 'list') => setViewMode(value)}>
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="grid">
                  <div className="flex items-center gap-2">
                    <Grid className="h-4 w-4" />
                    Grid
                  </div>
                </SelectItem>
                <SelectItem value="list">
                  <div className="flex items-center gap-2">
                    <List className="h-4 w-4" />
                    List
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Results Count */}
        <div className="mb-6 flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            {isLoading ? (
              <span className="flex items-center gap-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                Loading tools...
              </span>
            ) : (
              `Showing ${filteredTools.length} of ${tools.length} tools`
            )}
          </p>
        </div>

        {/* Tools Grid/List */}
        {isLoading ? (
          <div className={`grid gap-6 ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1'}`}>
            {Array.from({ length: 9 }).map((_, index) => (
              <Card key={index}>
                <CardHeader>
                  <div className="flex items-start gap-3">
                    <Skeleton className="h-12 w-12 rounded-lg" />
                    <div className="flex-1 space-y-2">
                      <Skeleton className="h-5 w-3/4" />
                      <Skeleton className="h-4 w-full" />
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex gap-2">
                      <Skeleton className="h-6 w-16" />
                      <Skeleton className="h-6 w-12" />
                    </div>
                    <Skeleton className="h-9 w-full" />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : filteredTools.length === 0 ? (
          /* Empty State */
          <Card className="py-16 text-center">
            <CardContent>
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-muted">
                <Search className="h-8 w-8 text-muted-foreground" />
              </div>
              <h3 className="mb-2 text-lg font-semibold">No tools found</h3>
              <p className="mb-6 text-muted-foreground">
                {searchQuery
                  ? `No tools match "${searchQuery}". Try adjusting your search or browse categories.`
                  : 'No tools available in this category.'}
              </p>
              <div className="flex justify-center gap-3">
                {searchQuery && (
                  <Button variant="outline" onClick={clearSearch}>
                    Clear Search
                  </Button>
                )}
                <Button onClick={() => setSelectedCategory('all')}>
                  Browse All Tools
                </Button>
              </div>
            </CardContent>
          </Card>
        ) : (
          <div className={`grid gap-6 ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1'}`}>
            {filteredTools.map((tool) => (
              <Card
                key={tool.id}
                className="group cursor-pointer transition-all duration-200 hover:shadow-lg hover:-translate-y-1"
              >
                <CardHeader>
                  <div className="flex items-start gap-3">
                    <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 text-2xl">
                      {tool.icon}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2">
                        <CardTitle className="text-lg group-hover:text-blue-600 transition-colors">
                          {tool.name}
                        </CardTitle>
                        <div className="flex gap-1">
                          {tool.featured && (
                            <Badge variant="default" className="text-xs">
                              Featured
                            </Badge>
                          )}
                          {tool.new && (
                            <Badge variant="secondary" className="text-xs">
                              New
                            </Badge>
                          )}
                        </div>
                      </div>
                      <CardDescription className="mt-1 line-clamp-2">
                        {tool.description}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex flex-wrap gap-1">
                      {tool.tags.slice(0, 3).map((tag) => (
                        <Badge key={tag} variant="outline" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                      {tool.tags.length > 3 && (
                        <Badge variant="outline" className="text-xs">
                          +{tool.tags.length - 3}
                        </Badge>
                      )}
                    </div>
                    <Button className="w-full group-hover:bg-blue-600 transition-colors">
                      Use Tool
                      <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}

export default ComprehensiveHomepage
