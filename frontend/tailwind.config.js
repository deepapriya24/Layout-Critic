/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0A0A0F",
        panel: "#12121A",
        accent: "#E87A2D",
      },
      fontFamily: {
        mono: ["JetBrains Mono", "monospace"],
        sans: ["Inter", "sans-serif"],
      },
      boxShadow: {
        glow: "0 0 20px rgba(232, 122, 45, 0.5)",
        glowSm: "0 0 10px rgba(232, 122, 45, 0.35)",
      },
      keyframes: {
        scan: {
          "0%": { top: "0%" },
          "100%": { top: "100%" },
        },
        pulseBorder: {
          "0%, 100%": { opacity: "0.6" },
          "50%": { opacity: "1" },
        },
        slideIn: {
          "0%": { opacity: "0", transform: "translateX(20px)" },
          "100%": { opacity: "1", transform: "translateX(0)" },
        },
      },
      animation: {
        scan: "scan 1.6s linear infinite",
        pulseBorder: "pulseBorder 1.8s ease-in-out infinite",
        slideIn: "slideIn 0.4s ease-out forwards",
      },
    },
  },
  plugins: [],
};
