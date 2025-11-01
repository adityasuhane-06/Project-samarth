import React from 'react'

const ErrorMessage = ({ message }) => {
  return (
    <div className="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg fade-in">
      <div className="flex items-start gap-3">
        <span className="text-2xl">❌</span>
        <div>
          <h3 className="text-red-800 font-semibold text-lg mb-1">Error</h3>
          <p className="text-red-700">{message}</p>
        </div>
      </div>
    </div>
  )
}

export default ErrorMessage
