/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        olive: {
          50: '#f7f8f3',
          100: '#eef1e7',
          200: '#dde3cf',
          300: '#c6d0b0',
          400: '#aab88d',
          500: '#8fa070',
          600: '#728257',
          700: '#5a6646',
          800: '#49533a',
          900: '#3e4632',
        }
      }
    },
  },
  plugins: [],
}
