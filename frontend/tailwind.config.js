/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // Важно, чтобы tailwind видел все файлы React
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
