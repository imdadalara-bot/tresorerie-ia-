/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}', './index.html'],
  theme: {
    extend: {
      colors: {
        navy: {
          900: '#0F1C30',
          800: '#1A2B48',
          700: '#243D64',
          600: '#2E4F7F',
          500: '#3A6299',
        },
        emerald: {
          400: '#34D399',
          500: '#10B981',
          600: '#059669',
        },
        amber: {
          400: '#FCD34D',
          500: '#F59E0B',
          600: '#D97706',
        },
        surface: '#F0F4FA',
        card: '#FFFFFF',
        danger: '#EF4444',
        'danger-light': '#FEF2F2',
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', "'Segoe UI'", 'Roboto', 'sans-serif'],
      },
      boxShadow: {
        card: '0 1px 4px 0 rgba(26,43,72,0.08), 0 0 0 1px rgba(26,43,72,0.04)',
        float: '0 8px 24px rgba(26,43,72,0.22)',
      },
    },
  },
  plugins: [],
};
