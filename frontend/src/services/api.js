import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 seconds timeout
})

/**
 * Health check endpoint
 * @returns {Promise<Object>} Health status and statistics
 */
export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/api/health')
    return response.data
  } catch (error) {
    console.error('Health check failed:', error)
    throw new Error('Failed to connect to server')
  }
}

/**
 * Submit a query to the backend
 * @param {string} question - The user's question
 * @returns {Promise<Object>} Query response with answer and sources
 */
export const submitQuery = async (question) => {
  try {
    const response = await apiClient.post('/api/query', {
      question: question.trim()
    })
    return response.data
  } catch (error) {
    if (error.response) {
      // Server responded with error
      throw new Error(error.response.data.error || error.response.data.detail || 'Query failed')
    } else if (error.request) {
      // Request made but no response
      throw new Error('No response from server. Please check if the server is running.')
    } else {
      // Something else happened
      throw new Error(error.message || 'An error occurred while processing your query')
    }
  }
}

/**
 * Get available datasets
 * @returns {Promise<Object>} List of available datasets
 */
export const getDatasets = async () => {
  try {
    const response = await apiClient.get('/api/datasets')
    return response.data
  } catch (error) {
    console.error('Failed to fetch datasets:', error)
    throw error
  }
}

/**
 * Get cache statistics
 * @returns {Promise<Object>} Cache statistics
 */
export const getCacheStats = async () => {
  try {
    const response = await apiClient.get('/api/cache/stats')
    return response.data
  } catch (error) {
    console.error('Failed to fetch cache stats:', error)
    throw error
  }
}

/**
 * Clear cache
 * @returns {Promise<Object>} Clear cache response
 */
export const clearCache = async () => {
  try {
    const response = await apiClient.post('/api/cache/clear?confirm=true')
    return response.data
  } catch (error) {
    console.error('Failed to clear cache:', error)
    throw error
  }
}

export default {
  healthCheck,
  submitQuery,
  getDatasets,
  getCacheStats,
  clearCache
}
