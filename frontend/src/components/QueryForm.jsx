import React from 'react'

const QueryForm = ({ question, setQuestion, onSubmit, loading }) => {
  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <div>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about agricultural data... e.g., 'What is the rice production in Punjab for 2023?'"
          className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl 
                   focus:border-primary-500 focus:ring-4 focus:ring-primary-100 
                   outline-none transition-all duration-300 resize-none 
                   text-gray-700 placeholder-gray-400 custom-scrollbar"
          rows="4"
        />
      </div>
      
      <button
        type="submit"
        disabled={loading}
        className="w-full btn-primary flex items-center justify-center gap-2"
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
            <span>🔍</span>
            Get Answer
          </>
        )}
      </button>
    </form>
  )
}

export default QueryForm
