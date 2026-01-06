import React from 'react'
import { formatAnswer } from '../utils/formatter'
import { useTheme } from '../context/ThemeContext'

const AnswerBox = ({ answer }) => {
  const { isDark } = useTheme()
  
  return (
    <div className={`p-8 rounded-xl shadow-lg slide-in-right relative overflow-hidden
                    ${isDark 
                      ? 'glass-dark border-l-4 border-silver-400 border-2 border-silver-500/50' 
                      : 'bg-gradient-to-br from-gradient-from/10 via-white to-gradient-via/10 border-l-4 border-gradient-from'
                    }`}>
      {isDark && (
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0 bg-gradient-to-br from-grey-500/20 via-transparent to-grey-300/20"></div>
        </div>
      )}
      <h3 className={`text-2xl font-display font-bold mb-6 flex items-center gap-3 relative z-10 ${isDark ? 'text-grey-200' : 'text-gray-800'}`}>
        <svg className="w-8 h-8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2a7 7 0 00-7 7c0 2.38 1.19 4.47 3 5.74V17a2 2 0 002 2h4a2 2 0 002-2v-2.26c1.81-1.27 3-3.36 3-5.74a7 7 0 00-7-7z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M9 21h6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          <path d="M12 6v3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
        </svg>
        ANSWER
      </h3>
      <div 
        className={`leading-relaxed text-lg custom-scrollbar max-h-[600px] overflow-y-auto pr-2 relative z-10 font-sans
                   ${isDark ? 'text-gray-300' : 'text-gray-700'}`}
        dangerouslySetInnerHTML={{ __html: formatAnswer(answer) }}
      />
    </div>
  )
}

export default AnswerBox
