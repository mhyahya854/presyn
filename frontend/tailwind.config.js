/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        presyn: {
          bg: "#090d16",
          surface: "#111726",
          elevated: "#172033",
          border: "#1e293b",
          borderSubtle: "#172030",
          primary: "#2563eb",
          primaryHover: "#1d4ed8",
          text: "#f8fafc",
          textMuted: "#94a3b8",
          textDim: "#64748b",
          success: "#10b981",
          warning: "#f59e0b",
          danger: "#ef4444",
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "-apple-system",
          "BlinkMacSystemFont",
          '"Segoe UI"',
          "Roboto",
          '"Helvetica Neue"',
          "Arial",
          "sans-serif",
        ],
      },
      borderRadius: {
        DEFAULT: "0.25rem",
        md: "0.375rem",
        lg: "0.5rem",
      },
    },
  },
  plugins: [],
};
