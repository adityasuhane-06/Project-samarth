import React from 'react'
import { useTheme } from '../context/ThemeContext'

const Header = ({ hasQuery = false }) => {
  const { isDark, toggleTheme } = useTheme()

  return (
    <div className={`${isDark ? 'glass-dark' : 'glass-light'} rounded-2xl p-8 mb-6 fade-in relative overflow-hidden ${isDark ? `border-2 ${hasQuery ? 'border-yellow-600/60' : 'border-silver-400/50'}` : ''} transition-all duration-500`}>
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <svg className="w-12 h-12 animate-float" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path className={isDark ? 'stroke-grey-200' : 'stroke-gradient-from'} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" d="M12 2L3 7v5c0 6.075 4.095 11.763 10 13 5.905-1.237 10-6.925 10-13V7l-9-5z"/>
              <path className={isDark ? 'stroke-silver-300' : 'stroke-gradient-via'} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" d="M12 7v10"/>
              <path className={isDark ? 'stroke-silver-300' : 'stroke-gradient-via'} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" d="M8 12h8"/>
              <circle className={isDark ? 'stroke-silver-400' : 'stroke-gradient-from'} strokeWidth="1.5" cx="12" cy="12" r="2"/>
            </svg>
            <h1 className={`text-4xl font-display font-bold transition-all duration-500 ${hasQuery ? 'text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-yellow-500 to-yellow-600' : 'gradient-text'}`}>
              PROJECT SAMARTH
            </h1>
          </div>
          
          {/* Theme toggle button */}
          <button
            onClick={toggleTheme}
            className={`p-3 rounded-lg transition-all duration-300 ${
              isDark 
                ? 'bg-dark-elevated neon-border hover:bg-neon-cyan/10' 
                : 'bg-white border-2 border-gradient-from hover:bg-gradient-from/10'
            }`}
            aria-label="Toggle theme"
          >
            {isDark ? (
              <svg className="w-6 h-6 text-neon-cyan" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            ) : (
              <svg className="w-6 h-6 text-gradient-from" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            )}
          </button>
        </div>
        
        <p className={`font-tech text-lg leading-relaxed mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
          Intelligent Q&A System for Indian Agricultural Data
        </p>
        <p className={`font-mono text-sm ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
          Powered by Google Gemini AI & data.gov.in datasets from Ministry of Agriculture and IMD
        </p>

        <div className="mt-6 flex flex-wrap gap-2">
          <span className={`inline-flex items-center px-3 py-1 rounded-lg text-xs font-tech font-semibold ${
            isDark 
              ? 'bg-grey-400/10 text-grey-300 border-2 border-silver-400/40' 
              : 'bg-gradient-from/10 text-gradient-from border border-gradient-from/30'
          }`}>
            <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="2" fill="currentColor"/>
              <path d="M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M2 12h3M19 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            AI Agent
          </span>
          <span className={`inline-flex items-center px-3 py-1 rounded-lg text-xs font-tech font-semibold ${
            isDark 
              ? 'bg-grey-500/10 text-grey-400 border-2 border-silver-500/40' 
              : 'bg-green-500/10 text-green-600 border border-green-500/30'
          }`}>
            <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M13 2L3 14h8l-2 8 10-12h-8l2-8z" fill="currentColor" stroke="currentColor" strokeWidth="0.5" strokeLinejoin="round"/>
            </svg>
            MongoDB Caching
          </span>
          <span className={`inline-flex items-center px-3 py-1 rounded-lg text-xs font-tech font-semibold ${
            isDark 
              ? 'bg-grey-600/10 text-grey-200 border-2 border-silver-600/40' 
              : 'bg-blue-500/10 text-blue-600 border border-blue-500/30'
          }`}>
            <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="3" y="3" width="7" height="7" rx="1" fill="currentColor"/>
              <rect x="14" y="3" width="7" height="7" rx="1" fill="currentColor"/>
              <rect x="14" y="14" width="7" height="7" rx="1" fill="currentColor"/>
              <rect x="3" y="14" width="7" height="7" rx="1" fill="currentColor"/>
            </svg>
            5+ Data Sources
          </span>
          <span className={`inline-flex items-center px-3 py-1 rounded-lg text-xs font-tech font-semibold ${
            isDark 
              ? 'bg-grey-300/10 text-grey-100 border-2 border-silver-300/40' 
              : 'bg-purple-500/10 text-purple-600 border border-purple-500/30'
          }`}>
            <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M2 7l10 5 10-5-10-5L2 7z" fill="currentColor"/>
              <path d="M2 12l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M2 17l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            135x Faster
          </span>
        </div>
      </div>
    </div>
  )
}

export default Header
