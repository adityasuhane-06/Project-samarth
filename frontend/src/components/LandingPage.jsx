import React, { useState, useEffect } from 'react'
import { useTheme } from '../context/ThemeContext'

const LandingPage = ({ onEnter }) => {
  const { isDark } = useTheme()
  const [animateOut, setAnimateOut] = useState(false)
  const [textVisible, setTextVisible] = useState(false)

  useEffect(() => {
    setTextVisible(true)
  }, [])

  const handleEnter = () => {
    setAnimateOut(true)
    setTimeout(() => {
      onEnter()
    }, 800)
  }

  return (
    <div className={`fixed inset-0 z-50 flex flex-col items-center justify-center transition-all duration-1000 ${animateOut ? 'opacity-0 scale-105 filter blur-lg' : 'opacity-100'}`}>
      
      <div className="relative z-10 text-center space-y-12 p-8 max-w-5xl w-full">
        {/* Main Title with Reveal Effect */}
        <div className="overflow-hidden relative">
          <h1 
            className={`text-6xl md:text-8xl lg:text-9xl font-display font-bold tracking-tighter transition-transform duration-1000 ease-out transform
              ${textVisible ? 'translate-y-0 opacity-100' : 'translate-y-full opacity-0'}
              ${isDark ? 'text-transparent bg-clip-text bg-gradient-to-b from-white via-silver-200 to-gray-500' : 'text-gray-900'}
            `}
          >
            PROJECT
          </h1>
          <h1 
            className={`text-6xl md:text-8xl lg:text-9xl font-display font-bold tracking-tighter transition-transform duration-1000 delay-100 ease-out transform
              ${textVisible ? 'translate-y-0 opacity-100' : 'translate-y-full opacity-0'}
              ${isDark ? 'text-transparent bg-clip-text bg-gradient-to-b from-silver-100 via-silver-400 to-gray-600' : 'text-gray-800'}
            `}
          >
            SAMARTH
          </h1>
        </div>
        
        {/* Animated Line */}
        <div className={`h-px w-0 mx-auto transition-all duration-1000 delay-500 ease-in-out ${textVisible ? 'w-32 md:w-64' : 'w-0'} ${isDark ? 'bg-yellow-500' : 'bg-yellow-600'}`}></div>
        
        {/* Subtitle with gold accent */}
        <div className={`overflow-hidden transition-all duration-1000 delay-700 ${textVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          <p className={`text-lg md:text-2xl font-tech tracking-[0.3em] uppercase ${isDark ? 'text-yellow-500' : 'text-yellow-600'}`}>
            Advanced Agricultural Intelligence
          </p>
        </div>

        {/* Minimalistic Button */}
        <div className={`transition-all duration-1000 delay-1000 ${textVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          <button
            onClick={handleEnter}
            className={`group relative px-16 py-5 bg-transparent overflow-hidden transition-all duration-500
              ${isDark ? 'text-silver-300 hover:text-black' : 'text-gray-600 hover:text-white'}
            `}
          >
            {/* Button Borders - Minimalistic Corners */}
            <span className={`absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 transition-all duration-300 ${isDark ? 'border-silver-500 group-hover:border-yellow-500' : 'border-gray-400 group-hover:border-yellow-600'}`}></span>
            <span className={`absolute top-0 right-0 w-4 h-4 border-t-2 border-r-2 transition-all duration-300 ${isDark ? 'border-silver-500 group-hover:border-yellow-500' : 'border-gray-400 group-hover:border-yellow-600'}`}></span>
            <span className={`absolute bottom-0 left-0 w-4 h-4 border-b-2 border-l-2 transition-all duration-300 ${isDark ? 'border-silver-500 group-hover:border-yellow-500' : 'border-gray-400 group-hover:border-yellow-600'}`}></span>
            <span className={`absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 transition-all duration-300 ${isDark ? 'border-silver-500 group-hover:border-yellow-500' : 'border-gray-400 group-hover:border-yellow-600'}`}></span>
            
            {/* Fill Effect */}
            <span className={`absolute inset-0 w-full h-full transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left ease-out ${isDark ? 'bg-yellow-500' : 'bg-yellow-600'}`}></span>
            
            {/* Text */}
            <span className="relative flex items-center gap-4 font-tech text-xl font-bold tracking-widest uppercase">
              Initialize System
              <svg className="w-5 h-5 transition-transform duration-500 group-hover:translate-x-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </span>
          </button>
        </div>
      </div>
      
      {/* Footer minimal info */}
      <div className={`absolute bottom-8 left-0 w-full text-center transition-opacity duration-700 delay-1000 ${textVisible ? 'opacity-40' : 'opacity-0'}`}>
        <p className={`text-xs font-mono ${isDark ? 'text-silver-500' : 'text-gray-400'}`}>
          SYSTEM V3.0 // READY FOR INPUT
        </p>
      </div>
    </div>
  )
}

export default LandingPage
