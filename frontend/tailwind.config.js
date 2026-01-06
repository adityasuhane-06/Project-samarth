/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Duotone dark theme colors
        dark: {
          bg: '#000000',
          surface: '#0a0a0a',
          elevated: '#141414',
          border: '#1f1f1f',
        },
        light: {
          bg: '#f8f9fa',
          surface: '#ffffff',
          elevated: '#f1f3f5',
          border: '#e0e0e0',
        },
        // Grey accent colors for duotone
        grey: {
          50: '#fafafa',
          100: '#f5f5f5',
          200: '#e5e5e5',
          300: '#d4d4d4',
          400: '#a3a3a3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',
        },
        // Silver accent colors for borders
        silver: {
          50: '#f8f9fa',
          100: '#f1f3f5',
          200: '#e9ecef',
          300: '#dee2e6',
          400: '#ced4da',
          500: '#adb5bd',
          600: '#8c95a1',
          700: '#6c757d',
          800: '#495057',
          900: '#343a40',
        },
        // Modern gradient colors
        gradient: {
          from: '#737373',
          via: '#a3a3a3',
          to: '#d4d4d4',
        }
      },
      fontFamily: {
        // Robotic/Tech fonts
        display: ['Orbitron', 'sans-serif'],
        tech: ['Rajdhani', 'sans-serif'],
        mono: ['Space Mono', 'Courier New', 'monospace'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'spin-slow': 'spin 3s linear infinite',
        'gradient-shift': 'gradientShift 8s ease infinite',
        'float': 'float 3s ease-in-out infinite',
      },
      keyframes: {
        gradientShift: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
      backgroundSize: {
        '200': '200% 200%',
      },
    },
  },
  plugins: [],
}
