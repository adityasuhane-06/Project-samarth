import React from 'react'
import { formatAnswer } from '../utils/formatter'

const AnswerBox = ({ answer }) => {
  return (
    <div className="bg-gradient-to-br from-primary-50 via-white to-secondary-50 
                    border-l-4 border-primary-500 p-8 rounded-xl shadow-lg slide-in-right">
      <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-3">
        <span className="text-3xl">💡</span>
        Answer
      </h3>
      <div 
        className="text-gray-700 leading-relaxed text-lg custom-scrollbar max-h-[600px] overflow-y-auto pr-2"
        dangerouslySetInnerHTML={{ __html: formatAnswer(answer) }}
      />
    </div>
  )
}

export default AnswerBox
