/**
 * Format the answer text with enhanced styling
 * @param {string} answer - Raw answer text from API
 * @returns {string} Formatted HTML string
 */
export const formatAnswer = (answer) => {
  let formatted = answer

  // First, escape any existing HTML
  formatted = formatted.replace(/</g, '&lt;').replace(/>/g, '&gt;')

  // Format ### headings (e.g., "### Maize Production Overview")
  formatted = formatted.replace(
    /###\s+([^\n]+)/g,
    '<h3 class="text-2xl font-bold text-gray-900 mt-6 mb-4 pb-2 border-b-2 border-primary-500">$1</h3>'
  )

  // Format main heading sections (e.g., "**2. Recent Period:**")
  formatted = formatted.replace(
    /\*\*(\d+)\.\s*([^:*]+):\*\*/g,
    '<h3 class="text-xl font-bold text-gray-800 mt-6 mb-3 flex items-center gap-2"><span class="flex-shrink-0 w-6 h-6 flex items-center justify-center bg-primary-500 text-white rounded-full text-sm">$1</span>$2</h3>'
  )

  // Format list items with location, state, and production (e.g., "* Ahmednagar, **Maharashtra**: 296,900.0 units")
  formatted = formatted.replace(
    /\*\s*([^,]+),\s+\*\*([^:*]+)\*\*\s*:\s*([0-9,]+\.?[0-9]*)\s*units/g,
    '<div class="flex items-center gap-3 my-3 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-200 hover:shadow-lg transition-all">' +
    '<div class="flex-1"><span class="text-gray-700 font-medium">$1, </span>' +
    '<span class="font-bold text-lg text-gray-900 bg-yellow-100 px-2 py-0.5 rounded">$2</span></div>' +
    '<div class="text-right"><div class="text-3xl font-extrabold text-yellow-600">$3</div>' +
    '<div class="text-xs text-gray-500 font-medium">units</div></div></div>'
  )

  // Format simple bullet points with bold text (e.g., "* **Total Production:**")
  formatted = formatted.replace(
    /\*\s+\*\*([^:*]+):\*\*/g,
    '<div class="flex items-start gap-2 my-2"><span class="text-primary-500 font-bold">•</span><strong class="font-bold text-gray-800">$1:</strong></div>'
  )

  // Format year badges as bullet points (e.g., "* 2013-14:")
  formatted = formatted.replace(
    /\*\s+(\d{4}-\d{2})\s*:/g,
    '<div class="flex items-center gap-2 my-3 font-semibold text-gray-700"><span class="text-primary-500 text-xl">•</span><span class="inline-block px-3 py-1 text-xs font-bold text-white bg-gradient-to-r from-primary-500 to-purple-600 rounded-full shadow-sm">$1</span></div>'
  )

  // Format simple list items without bold (e.g., "* Amritsar, Punjab : 4,000.0 units")
  formatted = formatted.replace(
    /\*\s+([^:\n]+)\s*:\s*([0-9,]+\.?[0-9]*)\s*units/g,
    '<div class="flex items-center justify-between my-2 pl-6"><span class="text-gray-700">$1</span><span class="font-bold text-yellow-600">$2 units</span></div>'
  )

  // Format numbered list items (e.g., "1. **Bihar**: 5,709.0 units")
  formatted = formatted.replace(
    /(\d+)\.\s+\*\*([^:*]+)\*\*:?\s*:?\*\*\s*([0-9,]+\.?[0-9]*)\s*units/g,
    '<div class="flex items-start gap-3 my-3 p-4 bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow border-l-4 border-yellow-500">' +
    '<span class="flex-shrink-0 w-8 h-8 flex items-center justify-center bg-yellow-500 text-black rounded-full font-bold">$1</span>' +
    '<div class="flex-1"><h4 class="text-xl font-bold text-green-700 mb-1">$2</h4>' +
    '<p class="text-3xl font-extrabold text-yellow-600">$3 <span class="text-sm font-normal text-gray-600">units</span></p></div></div>'
  )

  // Format percentages with highlighting
  formatted = formatted.replace(
    /([0-9]+\.?[0-9]*)%/g,
    '<span class="inline-block px-2 py-1 mx-1 text-sm font-bold text-green-700 bg-green-100 rounded-md">$1%</span>'
  )

  // Format year ranges (e.g., "2014-15", "2023-24")
  formatted = formatted.replace(
    /(\d{4}-\d{2,4})/g,
    '<span class="inline-block px-3 py-1 mx-1 text-xs font-bold text-white bg-gradient-to-r from-primary-500 to-purple-600 rounded-full shadow-sm">$1</span>'
  )

  // Format source badges (with icon emoji)
  formatted = formatted.replace(
    /📊\s*Source:\s*([^\n]+)/g,
    '<div class="inline-flex items-center gap-2 px-3 py-1.5 my-2 text-xs font-semibold text-blue-800 bg-blue-100 border-2 border-blue-300 rounded-lg shadow-sm">' +
    '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"/></svg>' +
    'Source: $1</div>'
  )

  // Format remaining bold text (simple bold)
  formatted = formatted.replace(
    /\*\*([^*]+)\*\*/g,
    '<strong class="font-bold text-gray-800">$1</strong>'
  )

  // Format Product_Code mentions
  formatted = formatted.replace(
    /Product[_ ]Code\s*"?(\d+)"?/gi,
    '<span class="inline-block px-2 py-1 bg-purple-100 text-purple-700 rounded font-mono text-sm font-semibold">Product Code: $1</span>'
  )

  // Highlight state names with background
  const states = [
    'Punjab', 'Haryana', 'Karnataka', 'Maharashtra', 'Tamil Nadu',
    'Uttar Pradesh', 'West Bengal', 'Bihar', 'Rajasthan', 'Gujarat',
    'Madhya Pradesh', 'Andhra Pradesh', 'Kerala', 'Odisha', 'Telangana', 
    'Assam', 'Madhya Pradesh'
  ]
  
  states.forEach(state => {
    const regex = new RegExp(`\\b(${state})\\b(?![^<]*>)`, 'g')
    formatted = formatted.replace(
      regex,
      '<span class="font-bold text-gray-900 bg-yellow-100 px-1.5 py-0.5 rounded">$1</span>'
    )
  })

  // Highlight crop names
  const crops = [
    'maize', 'rice', 'wheat', 'bajra', 'jowar', 'cotton', 'sugarcane', 
    'groundnut', 'soybean', 'pulses', 'Maize', 'Rice', 'Wheat', 'Bajra'
  ]
  
  crops.forEach(crop => {
    const regex = new RegExp(`\\b(${crop})\\b(?![^<]*>)`, 'gi')
    formatted = formatted.replace(
      regex,
      '<span class="font-bold text-green-700">$1</span>'
    )
  })

  // Format "APEDA Production Statistics" and dataset names
  formatted = formatted.replace(
    /`([^`]+)`/g,
    '<code class="px-2 py-1 bg-gray-100 text-gray-800 rounded text-sm font-mono">$1</code>'
  )

  // Convert line breaks (must be done after all other replacements)
  formatted = formatted.replace(/\n\n/g, '<div class="my-4"></div>')
  formatted = formatted.replace(/\n/g, '<br>')

  // Format introductory sentences
  formatted = formatted.replace(
    /^From this limited sample,/,
    '<p class="text-base text-gray-700 mb-4 font-medium">From this limited sample,'
  )

  // Add spacing after sections
  formatted = formatted.replace(
    /(<\/div>)(\*\*)/g,
    '$1<div class="my-6"></div>$2'
  )

  return formatted
}

/**
 * Format large numbers with commas
 * @param {number} num - Number to format
 * @returns {string} Formatted number string
 */
export const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * Format file size
 * @param {number} bytes - Size in bytes
 * @returns {string} Formatted size string
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

/**
 * Truncate text with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export const truncateText = (text, maxLength = 100) => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}
