/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  jit: true,
  theme: {
    extend: {
      fontFamily: {
        charts: ['Helvetica', 'Arial', 'sans-serif']
      }
    },
  },
  plugins: [require('tailwind-scrollbar')],
}

