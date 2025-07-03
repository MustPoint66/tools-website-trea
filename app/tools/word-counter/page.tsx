"use client"

import React from "react";
import Link from "next/link";
import { FileText, ArrowLeft } from "lucide-react";

const WordCounter = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 text-white">
      {/* Navigation */}
      <nav className="border-b border-gray-800 bg-black/50 backdrop-blur-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <Link href="/" className="flex items-center space-x-2 text-blue-500 hover:text-blue-400 transition-colors">
                <ArrowLeft className="h-5 w-5" />
                <span>Back to Tools</span>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-3xl mx-auto px-4 py-12 text-center">
        {/* Header */}
        <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-500/10 rounded-full mb-6">
          <FileText className="h-8 w-8 text-blue-500" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          Word Counter
        </h1>
        <p className="text-xl text-gray-400 max-w-2xl mx-auto">
          Count the number of words and characters in your text instantly.
        </p>
      </div>
    </div>
  );
};

export default WordCounter;
