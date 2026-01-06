import React from 'react'
import AnswerBox from './AnswerBox'
import DataSources from './DataSources'
import { useTheme } from '../context/ThemeContext'

const ResultDisplay = ({ result }) => {
  const { isDark } = useTheme()
  
  return (
    <div className="space-y-6 fade-in">
      <AnswerBox answer={result.answer} />
      
      {result.data_sources && result.data_sources.length > 0 && (
        <DataSources sources={result.data_sources} />
      )}

      {result.query_params && (
        <div className={`rounded-xl p-6 border-2 ${isDark ? 'glass-dark border-silver-500/50' : 'bg-gray-50 border-gray-200'}`}>
          <h3 className={`text-lg font-tech font-semibold mb-3 flex items-center gap-2 ${isDark ? 'text-gray-200' : 'text-gray-800'}`}>
            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="1.5"/>
              <circle cx="12" cy="12" r="5" stroke="currentColor" strokeWidth="1.5"/>
              <circle cx="12" cy="12" r="2" fill="currentColor"/>
            </svg>
            QUERY PARAMETERS
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            {result.query_params.states && result.query_params.states.length > 0 && (
              <div>
                <span className={`font-semibold font-tech ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>States:</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {result.query_params.states.map((state, idx) => (
                    <span key={idx} className={`px-2 py-1 rounded-md text-xs font-tech ${isDark ? 'bg-grey-400/20 text-grey-200 border border-silver-400/50' : 'bg-blue-100 text-blue-700'}`}>
                      {state}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {result.query_params.crops && result.query_params.crops.length > 0 && (
              <div>
                <span className={`font-semibold font-tech ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>Crops:</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {result.query_params.crops.map((crop, idx) => (
                    <span key={idx} className={`px-2 py-1 rounded-md text-xs font-tech ${isDark ? 'bg-grey-500/20 text-grey-300 border border-silver-500/50' : 'bg-green-100 text-green-700'}`}>
                      {crop}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {result.query_params.years && result.query_params.years.length > 0 && (
              <div>
                <span className={`font-semibold font-tech ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>Years:</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {result.query_params.years.map((year, idx) => (
                    <span key={idx} className={`px-2 py-1 rounded-md text-xs font-tech ${isDark ? 'bg-grey-300/20 text-grey-100 border border-silver-300/50' : 'bg-purple-100 text-purple-700'}`}>
                      {year}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default ResultDisplay
