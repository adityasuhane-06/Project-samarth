import React from 'react'
import { useTheme } from '../context/ThemeContext'

const ErrorMessage = ({ message }) => {
  const { isDark } = useTheme()
  
  return (
    <div className={`border-l-4 p-6 rounded-lg fade-in ${isDark ? 'bg-red-900/20 border-red-500' : 'bg-red-50 border-red-500'}`}>
      <div className="flex items-start gap-3">
        <svg className="w-6 h-6 mt-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="12" cy="12" r="10" className="fill-red-500/20 stroke-red-500" strokeWidth="1.5"/>
          <path d="M8 8l8 8M16 8l-8 8" className="stroke-red-500" strokeWidth="2" strokeLinecap="round"/>
        </svg>
        <div>
          <h3 className={`font-tech font-semibold text-lg mb-1 uppercase ${isDark ? 'text-red-400' : 'text-red-800'}`}>Error</h3>
          <p className={`font-sans ${isDark ? 'text-red-300' : 'text-red-700'}`}>{message}</p>
        </div>
      </div>
    </div>
  )
}

export default ErrorMessage
