import React from 'react'

const LoadingSpinner = () => {
  return (
    <div className="text-center py-12 fade-in">
      <div className="inline-block">
        <div className="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin mx-auto mb-4"></div>
        <p className="text-primary-700 font-medium">
          Analyzing your question and querying datasets
          <span className="loading-dots">
            <span>.</span>
            <span>.</span>
            <span>.</span>
          </span>
        </p>
        <p className="text-gray-500 text-sm mt-2">
          This may take a few seconds...
        </p>
      </div>
    </div>
  )
}

export default LoadingSpinner
