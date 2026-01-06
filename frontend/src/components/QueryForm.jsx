import React from 'react'
import { useTheme } from '../context/ThemeContext'

const QueryForm = ({ question, setQuestion, onSubmit, loading }) => {
  const { isDark } = useTheme()
  const hasQuery = question.trim().length > 0
  
  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <div>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about agricultural data... e.g., 'What is the rice production in Punjab for 2023?'"
          className={`w-full px-4 py-3 rounded-xl font-sans
                   outline-none transition-all duration-500 resize-none custom-scrollbar
                   ${isDark 
                     ? `bg-dark-elevated border-2 ${hasQuery ? 'border-yellow-600/70' : 'border-silver-500/50'} text-gray-200 placeholder-gray-500 ${hasQuery ? 'focus:border-yellow-500 focus:ring-4 focus:ring-yellow-500/20' : 'focus:border-silver-400 focus:ring-4 focus:ring-silver-400/20'}` 
                     : 'bg-white border-2 border-light-border text-gray-700 placeholder-gray-400 focus:border-gradient-from focus:ring-4 focus:ring-gradient-from/20'
                   }`}
          rows="4"
        />
      </div>
      
      <button
        type="submit"
        disabled={loading}
        className={`w-full ${isDark ? (hasQuery ? 'bg-gradient-to-r from-yellow-600 to-yellow-500 text-black' : 'btn-primary-dark') : 'btn-primary-light'} px-6 py-3 rounded-lg font-tech font-bold transition-all duration-500 flex items-center justify-center gap-2 uppercase tracking-wider disabled:opacity-50 disabled:cursor-not-allowed`}
      >
        {loading ? (
          <>
            <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Processing...
          </>
        ) : (
          <>
            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="10" cy="10" r="7" stroke="currentColor" strokeWidth="2"/>
              <path d="M15 15l6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            Get Answer
          </>
        )}
      </button>
    </form>
  )
}

export default QueryForm
