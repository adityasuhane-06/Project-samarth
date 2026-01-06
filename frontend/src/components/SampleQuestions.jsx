import React from 'react'
import { useTheme } from '../context/ThemeContext'

const SampleQuestions = ({ questions, onSelectQuestion }) => {
  const { isDark } = useTheme()
  
  return (
    <div className="space-y-3">
      <h3 className={`text-xl font-tech font-semibold flex items-center gap-2 ${isDark ? 'text-gray-200' : 'text-gray-800'}`}>
        <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="1.5"/>
          <circle cx="12" cy="12" r="1.5" fill="currentColor"/>
          <path stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" d="M12 6v3M12 15v3"/>
        </svg>
        SAMPLE QUERIES
      </h3>
      <div className="flex flex-wrap gap-3">
        {questions.map((q, idx) => (
          <button
            key={idx}
            onClick={() => onSelectQuestion(q)}
            className={`px-4 py-2 rounded-lg text-sm font-tech transition-all duration-300 
                     hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0
                     ${isDark
                       ? 'bg-dark-elevated border-2 border-silver-400/40 text-grey-300 hover:bg-grey-400/20 hover:border-silver-300'
                       : 'bg-gradient-from/10 border-2 border-gradient-from/30 text-gradient-from hover:bg-gradient-from hover:text-white hover:border-gradient-from'
                     }`}
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  )
}

export default SampleQuestions
