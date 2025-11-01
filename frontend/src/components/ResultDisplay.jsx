import React from 'react'
import AnswerBox from './AnswerBox'
import DataSources from './DataSources'

const ResultDisplay = ({ result }) => {
  return (
    <div className="space-y-6 fade-in">
      <AnswerBox answer={result.answer} />
      
      {result.data_sources && result.data_sources.length > 0 && (
        <DataSources sources={result.data_sources} />
      )}

      {result.query_params && (
        <div className="bg-gray-50 rounded-xl p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <span>🎯</span>
            Query Parameters
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            {result.query_params.states && result.query_params.states.length > 0 && (
              <div>
                <span className="font-semibold text-gray-700">States:</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {result.query_params.states.map((state, idx) => (
                    <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-700 rounded-md text-xs font-medium">
                      {state}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {result.query_params.crops && result.query_params.crops.length > 0 && (
              <div>
                <span className="font-semibold text-gray-700">Crops:</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {result.query_params.crops.map((crop, idx) => (
                    <span key={idx} className="px-2 py-1 bg-green-100 text-green-700 rounded-md text-xs font-medium">
                      {crop}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {result.query_params.years && result.query_params.years.length > 0 && (
              <div>
                <span className="font-semibold text-gray-700">Years:</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {result.query_params.years.map((year, idx) => (
                    <span key={idx} className="px-2 py-1 bg-purple-100 text-purple-700 rounded-md text-xs font-medium">
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
