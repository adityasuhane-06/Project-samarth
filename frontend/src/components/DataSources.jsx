import React from 'react'
import { useTheme } from '../context/ThemeContext'

const DataSources = ({ sources }) => {
  const { isDark } = useTheme()
  
  return (
    <div className="space-y-3">
      <h3 className={`text-xl font-tech font-semibold flex items-center gap-2 ${isDark ? 'text-gray-200' : 'text-gray-800'}`}>
        <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <circle cx="7" cy="6" r="1" fill="currentColor"/>
          <circle cx="7" cy="12" r="1" fill="currentColor"/>
          <circle cx="7" cy="18" r="1" fill="currentColor"/>
        </svg>
        DATA SOURCES
      </h3>
      <div className="space-y-3">
        {sources.map((source, idx) => (
          <div
            key={idx}
            className={`p-6 rounded-xl transition-all duration-300 hover:shadow-xl hover:-translate-y-1
                     ${isDark
                       ? 'glass-dark border-2 border-silver-500/50 hover:border-silver-400 card-hover-dark'
                       : 'bg-gradient-to-r from-white to-blue-50 border-2 border-blue-200 hover:border-gradient-from card-hover-light'
                     }`}
          >
            <h4 className={`font-display font-bold text-lg mb-2 ${isDark ? 'text-grey-200' : 'text-gradient-from'}`}>
              {source.dataset}
            </h4>
            <p className={`mb-2 text-sm font-sans ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
              <span className="font-semibold">Source:</span> {source.source}
            </p>
            <a
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className={`text-sm font-mono break-all inline-flex items-center gap-1 hover:underline
                       ${isDark ? 'text-grey-300 hover:text-grey-200' : 'text-gradient-from hover:text-gradient-via'}`}
            >
              {source.url}
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
          </div>
        ))}
      </div>
    </div>
  )
}

export default DataSources
