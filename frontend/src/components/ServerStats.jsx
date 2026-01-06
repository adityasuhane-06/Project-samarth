import React from 'react'
import { useTheme } from '../context/ThemeContext'

const ServerStats = ({ health, hasQuery = false }) => {
  const { isDark } = useTheme()
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 slide-in-left">
      <div className={`${isDark ? `glass-dark card-hover-dark border-2 ${hasQuery ? 'border-yellow-600/60' : 'border-silver-500/50'}` : 'glass-light card-hover-light'} rounded-xl p-6 transition-all duration-500`}>
        <div className="flex items-center justify-between">
          <div>
            <p className={`text-sm font-tech font-medium uppercase ${isDark ? 'text-gray-400' : 'text-gray-500'} transition-colors duration-500`}>Crop Records</p>
            <p className={`text-3xl font-display font-bold mt-1 ${isDark ? (hasQuery ? 'text-yellow-400' : 'text-grey-300') : 'text-gradient-from'} transition-colors duration-500`}>
              {health.crop_records}
            </p>
          </div>
          <svg className="w-10 h-10 animate-float" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path className={isDark ? (hasQuery ? 'fill-yellow-400 stroke-yellow-500' : 'fill-grey-300 stroke-silver-400') : 'fill-gradient-from stroke-gradient-via'} strokeWidth="1" d="M12 2l2.4 7.4h7.8l-6.3 4.6 2.4 7.4L12 16.8l-6.3 4.6 2.4-7.4L1.8 9.4h7.8L12 2z"/>
          </svg>
        </div>
      </div>

      <div className={`${isDark ? `glass-dark card-hover-dark border-2 ${hasQuery ? 'border-yellow-600/60' : 'border-silver-500/50'}` : 'glass-light card-hover-light'} rounded-xl p-6 transition-all duration-500`}>
        <div className="flex items-center justify-between">
          <div>
            <p className={`text-sm font-tech font-medium uppercase ${isDark ? 'text-gray-400' : 'text-gray-500'} transition-colors duration-500`}>Rainfall Records</p>
            <p className={`text-3xl font-display font-bold mt-1 ${isDark ? (hasQuery ? 'text-yellow-300' : 'text-grey-200') : 'text-blue-600'} transition-colors duration-500`}>
              {health.rainfall_records}
            </p>
          </div>
          <svg className="w-10 h-10 animate-float" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path className={isDark ? (hasQuery ? 'fill-yellow-300 stroke-yellow-400' : 'fill-grey-200 stroke-silver-400') : 'fill-blue-600 stroke-blue-700'} strokeWidth="0.5" d="M12 3l-2 4h4l-2-4z"/>
            <path className={isDark ? (hasQuery ? 'stroke-yellow-300' : 'stroke-grey-300') : 'stroke-blue-600'} strokeWidth="1.5" strokeLinecap="round" d="M6 12v4M10 14v3M14 14v3M18 12v4M8 18v2M12 19v2M16 18v2"/>
          </svg>
        </div>
      </div>

      <div className={`${isDark ? `glass-dark card-hover-dark border-2 ${hasQuery ? 'border-yellow-600/60' : 'border-silver-500/50'}` : 'glass-light card-hover-light'} rounded-xl p-6 transition-all duration-500`}>
        <div className="flex items-center justify-between">
          <div>
            <p className={`text-sm font-tech font-medium uppercase ${isDark ? 'text-gray-400' : 'text-gray-500'} transition-colors duration-500`}>System Status</p>
            <p className={`text-2xl font-display font-bold mt-1 uppercase ${isDark ? (hasQuery ? 'text-yellow-200' : 'text-grey-100') : 'text-green-600'} transition-colors duration-500`}>
              {health.status}
            </p>
          </div>
          <svg className="w-10 h-10" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            {health.mongodb_connected ? (
              <>
                <circle cx="12" cy="12" r="10" className="fill-green-500/20 stroke-green-500" strokeWidth="1.5"/>
                <path className="stroke-green-500" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4"/>
              </>
            ) : (
              <>
                <path className="fill-yellow-500/20 stroke-yellow-500" strokeWidth="1.5" d="M12 2L2 20h20L12 2z"/>
                <path className="stroke-yellow-500" strokeWidth="2" strokeLinecap="round" d="M12 9v4M12 16h.01"/>
              </>
            )}
          </svg>
        </div>
      </div>
    </div>
  )
}

export default ServerStats
