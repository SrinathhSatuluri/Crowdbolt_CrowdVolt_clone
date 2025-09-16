/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        'orbitron': ['var(--font-orbitron)', 'monospace'],
        'bungee': ['var(--font-bungee)', 'cursive'],
        'lora': ['var(--font-lora)', 'serif'],
        'playfair': ['var(--font-playfair)', 'serif'],
        'cinzel': ['var(--font-cinzel)', 'serif'],
        'bebas': ['var(--font-bebas)', 'sans-serif'],
      },
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
      },
    },
  },
  plugins: [],
}