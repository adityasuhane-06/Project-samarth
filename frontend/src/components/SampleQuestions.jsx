import React from 'react'

const SampleQuestions = ({ questions, onSelectQuestion }) => {
  return (
    <div className="space-y-3">
      <h3 className="text-xl font-semibold text-gray-800 flex items-center gap-2">
        <span>💡</span>
        Sample Questions:
      </h3>
      <div className="flex flex-wrap gap-3">
        {questions.map((q, idx) => (
          <button
            key={idx}
            onClick={() => onSelectQuestion(q)}
            className="px-4 py-2 bg-primary-50 text-primary-700 border-2 border-primary-200 
                     rounded-lg text-sm font-medium transition-all duration-300 
                     hover:bg-primary-500 hover:text-white hover:border-primary-500 
                     hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  )
}

export default SampleQuestions
