/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#10b981", // vert Tailwind par défaut
        dark: "#1f2937",
        light: "#f9fafb",
      },
    },
  },
  plugins: [],
}
