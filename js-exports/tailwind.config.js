// Reference: https://www.c-sharpcorner.com/article/how-to-use-tailwind-css-in-python-django/

/** @type {import('tailwindcss').Config} */
module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  purge: {
      enabled: false, // true for production build
      content: ['../**/templates/*.html', '../**/templates/**/*.html']
  },
  theme: {
      extend: {},
  },
  variants: {},
  plugins: [require("daisyui")],
}
