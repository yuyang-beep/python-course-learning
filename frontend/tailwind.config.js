/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'human-black': '#0f0f0f',
        'human-dark': '#1a1a1a',
        'human-gray': '#333333',
        'human-text': '#e0e0e0',
        'human-blue': '#00d4ff',
        'human-green': '#00ff88',
        'human-red': '#ff4444',
      },
      fontFamily: {
        mono: ['Courier New', 'monospace'],
      },
    },
  },
  plugins: [],
}
