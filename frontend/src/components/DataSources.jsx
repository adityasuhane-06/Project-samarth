import React from 'react'

const DataSources = ({ sources }) => {
  return (
    <div className="space-y-3">
      <h3 className="text-xl font-semibold text-gray-800 flex items-center gap-2">
        <span>📚</span>
        Data Sources
      </h3>
      <div className="space-y-3">
        {sources.map((source, idx) => (
          <div
            key={idx}
            className="bg-gradient-to-r from-white to-blue-50 border-2 border-blue-200 
                     p-6 rounded-xl transition-all duration-300 hover:shadow-xl 
                     hover:-translate-y-1 hover:border-primary-400"
          >
            <h4 className="font-bold text-primary-700 text-lg mb-2">
              {source.dataset}
            </h4>
            <p className="text-gray-600 mb-2 text-sm">
              <span className="font-semibold">Source:</span> {source.source}
            </p>
            <a
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-700 text-sm font-medium 
                       break-all inline-flex items-center gap-1 hover:underline"
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
