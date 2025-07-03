"use client"

import React from "react";
import Link from "next/link";
import { ArrowLeft, Zap, LucideIcon } from "lucide-react";
import { motion } from "framer-motion";

interface ToolTemplateProps {
  title: string;
  description: string;
  icon: LucideIcon;
  children?: React.ReactNode;
}

const ToolTemplate: React.FC<ToolTemplateProps> = ({ title, description, icon: Icon, children }) => {
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
            <div className="flex items-center space-x-2">
              <Zap className="h-8 w-8 text-blue-500" />
              <span className="text-xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
                Tools Mania
              </span>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-500/10 rounded-full mb-6">
            <Icon className="h-8 w-8 text-blue-500" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            {title}
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            {description}
          </p>
        </motion.div>

        {/* Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-12"
        >
          {children || (
            <div className="bg-gray-800/50 border border-gray-700 rounded-2xl p-12 text-center">
              <div className="space-y-4">
                <Icon className="h-16 w-16 text-gray-400 mx-auto" />
                <h3 className="text-2xl font-semibold">Tool Coming Soon</h3>
                <p className="text-gray-400 max-w-md mx-auto">
                  This tool is currently under development. We&apos;re working hard to bring you the best experience.
                </p>
                <Link
                  href="/"
                  className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-medium transition-colors"
                >
                  Explore Other Tools
                </Link>
              </div>
            </div>
          )}
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-green-500/10 rounded-xl mb-4">
              <span className="text-green-500 font-bold">✓</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">Secure & Private</h3>
            <p className="text-gray-400 text-sm">
              Your data is processed securely and never stored on our servers.
            </p>
          </div>
          
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-500/10 rounded-xl mb-4">
              <Zap className="h-6 w-6 text-blue-500" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Lightning Fast</h3>
            <p className="text-gray-400 text-sm">
              Get instant results with our optimized processing engine.
            </p>
          </div>
          
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-purple-500/10 rounded-xl mb-4">
              <span className="text-purple-500 font-bold">∞</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">Unlimited Use</h3>
            <p className="text-gray-400 text-sm">
              Use all our tools as much as you need, completely free.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ToolTemplate;
