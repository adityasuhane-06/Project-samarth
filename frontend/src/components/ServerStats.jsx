import React from 'react'

const ServerStats = ({ health }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 fade-in">
      <div className="bg-white rounded-xl shadow-lg p-6 card-hover">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-500 text-sm font-medium">Crop Records</p>
            <p className="text-3xl font-bold text-primary-600 mt-1">
              {health.crop_records}
            </p>
          </div>
          <div className="text-4xl">🌾</div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6 card-hover">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-500 text-sm font-medium">Rainfall Records</p>
            <p className="text-3xl font-bold text-blue-600 mt-1">
              {health.rainfall_records}
            </p>
          </div>
          <div className="text-4xl">🌧️</div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6 card-hover">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-500 text-sm font-medium">System Status</p>
            <p className="text-2xl font-bold text-green-600 mt-1 capitalize">
              {health.status}
            </p>
          </div>
          <div className="text-4xl">
            {health.mongodb_connected ? '✅' : '⚠️'}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ServerStats
