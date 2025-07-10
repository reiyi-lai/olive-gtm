/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'olive': {
          50: '#f7f8f3',
          100: '#edeee3',
          200: '#dde1c8',
          300: '#c5cca4',
          400: '#aab580',
          500: '#8fa05f',
          600: '#778949',
          700: '#5e6b3a',
          800: '#4d5631',
          900: '#41492b',
        }
      }
    },
  },
  plugins: [],
}