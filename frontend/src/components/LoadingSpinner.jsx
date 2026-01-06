import React from 'react'
import { useTheme } from '../context/ThemeContext'

const LoadingSpinner = () => {
  const { isDark } = useTheme()
  
  return (
    <div className="text-center py-12 fade-in">
      <div className="inline-block">
        <div className={`w-16 h-16 border-4 rounded-full animate-spin mx-auto mb-4 ${isDark ? 'border-dark-border border-t-grey-400' : 'border-light-border border-t-gradient-from'}`}></div>
        <p className={`font-tech font-medium ${isDark ? 'text-grey-300' : 'text-gradient-from'}`}>
          ANALYZING QUERY AND PROCESSING DATA
          <span className="loading-dots">
            <span>.</span>
            <span>.</span>
            <span>.</span>
          </span>
        </p>
        <p className={`text-sm mt-2 font-mono ${isDark ? 'text-gray-500' : 'text-gray-500'}`}>
          This may take a few seconds...
        </p>
      </div>
    </div>
  )
}

export default LoadingSpinner
