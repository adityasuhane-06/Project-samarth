import React from 'react'

const Header = () => {
  return (
    <div className="bg-white rounded-2xl shadow-2xl p-8 mb-6 fade-in">
      <div className="flex items-center gap-3 mb-4">
        <span className="text-5xl">🌾</span>
        <h1 className="text-4xl font-bold gradient-text">
          Project Samarth
        </h1>
      </div>
      
      <p className="text-gray-600 text-lg leading-relaxed">
        Intelligent Q&A System for Indian Agricultural Data
        <br />
        <span className="text-sm text-gray-500">
          Powered by Google Gemini AI & data.gov.in datasets from Ministry of Agriculture and IMD
        </span>
      </p>

      <div className="mt-6 flex flex-wrap gap-2">
        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-primary-100 text-primary-700">
          🤖 Two-Model AI
        </span>
        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-700">
          ⚡ MongoDB Caching
        </span>
        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">
          📊 5 Data Sources
        </span>
        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-purple-100 text-purple-700">
          🚀 135x Faster
        </span>
      </div>
    </div>
  )
}

export default Header
