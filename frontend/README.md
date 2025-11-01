# Project Samarth - Frontend

Modern React frontend for Project Samarth with Tailwind CSS and modular architecture.

## 🚀 Features

- ⚛️ **React 18** - Latest React with hooks
- 🎨 **Tailwind CSS** - Modern utility-first CSS framework
- ⚡ **Vite** - Lightning-fast build tool
- 🏗️ **Modular Architecture** - Clean component structure
- 📱 **Responsive Design** - Works on all devices
- 🎭 **Smooth Animations** - Beautiful transitions and effects

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Header.jsx       # App header
│   │   ├── ServerStats.jsx  # Server statistics
│   │   ├── SampleQuestions.jsx
│   │   ├── QueryForm.jsx    # Query input form
│   │   ├── LoadingSpinner.jsx
│   │   ├── ErrorMessage.jsx
│   │   ├── ResultDisplay.jsx
│   │   ├── AnswerBox.jsx    # Answer display
│   │   └── DataSources.jsx  # Data sources list
│   ├── services/            # API services
│   │   └── api.js           # API client
│   ├── utils/               # Utility functions
│   │   ├── constants.js     # App constants
│   │   └── formatter.js     # Text formatters
│   ├── App.jsx              # Main app component
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## 🛠️ Setup

### Prerequisites

- Node.js 18+ and npm
- Backend server running on http://localhost:8000

### Installation

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev
```

The app will be available at **http://localhost:3000**

## 📦 Available Scripts

```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🎨 Styling with Tailwind

This project uses Tailwind CSS for styling. Key features:

### Custom Colors

```javascript
primary: {
  500: '#667eea',  // Main brand color
  600: '#5568d3',  // Hover state
}
secondary: {
  500: '#764ba2',  // Secondary brand color
}
```

### Custom Components

Reusable component classes in `index.css`:

- `.btn-primary` - Primary button style
- `.card-hover` - Card hover effect
- `.gradient-text` - Gradient text effect
- `.custom-scrollbar` - Styled scrollbar

### Animations

- `fade-in` - Fade in from bottom
- `slide-in-right` - Slide in from right
- `animate-spin` - Loading spinner
- `loading-dots` - Animated dots

## 🔧 Configuration

### Vite Config (`vite.config.js`)

- Port: 3000
- Proxy: API calls to `http://localhost:8000`

### Tailwind Config (`tailwind.config.js`)

- Custom colors
- Custom animations
- Font family

### Environment Variables (`.env`)

```env
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

## 📱 Components

### Header
Displays app title, description, and feature badges.

### ServerStats
Shows live statistics from backend (crop records, rainfall records, status).

### SampleQuestions
Quick-access buttons for sample queries.

### QueryForm
Text area for user input with submit button.

### LoadingSpinner
Animated loading indicator during API calls.

### AnswerBox
Formatted display of AI-generated answers with syntax highlighting.

### DataSources
List of data sources with links.

### ErrorMessage
User-friendly error display.

## 🌐 API Integration

API client in `src/services/api.js`:

```javascript
import { healthCheck, submitQuery, getCacheStats } from './services/api'

// Health check
const health = await healthCheck()

// Submit query
const result = await submitQuery("What is rice production in Punjab?")

// Get cache stats
const stats = await getCacheStats()
```

## 🎯 Text Formatting

The `formatter.js` utility provides:

- Number highlighting with background
- Percentage formatting
- Financial year badges
- State/crop name bolding
- Source tags
- Line break conversion

Example:

```javascript
import { formatAnswer } from './utils/formatter'

const formatted = formatAnswer(rawAnswer)
```

## 🚀 Production Build

```bash
# Build for production
npm run build

# Preview build
npm run preview

# Deploy dist/ folder to hosting service
```

Build output will be in `dist/` folder.

## 📊 Performance

- **Vite** for instant HMR
- **Code splitting** for optimized bundles
- **Lazy loading** for better initial load
- **Optimized images** and assets

## 🎨 Customization

### Change Brand Colors

Edit `tailwind.config.js`:

```javascript
colors: {
  primary: {
    500: '#YOUR_COLOR',
  }
}
```

### Add New Component

1. Create component in `src/components/`
2. Import in parent component
3. Use with props

Example:

```jsx
// src/components/MyComponent.jsx
import React from 'react'

const MyComponent = ({ title }) => {
  return <div className="p-4">{title}</div>
}

export default MyComponent
```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Change port in vite.config.js
server: {
  port: 3001
}
```

### API Connection Failed

- Check backend is running on port 8000
- Verify VITE_API_URL in .env
- Check CORS settings in backend

### Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules
rm package-lock.json
npm install
```

## 📚 Learn More

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)

## 🤝 Contributing

Follow the component structure and use Tailwind CSS for styling. See main CONTRIBUTING.md for guidelines.

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ using React, Vite, and Tailwind CSS**
