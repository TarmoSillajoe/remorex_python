/** @type {import('tailwindcss').Config} */

const colors = require("tailwindcss/colors");
module.exports = {
  content: ["./templates/**/*.{html,js}", "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {},
    colors: {
      transparent: "transparent",
      current: "currentColor",
      black: colors.black,
      blue: colors.blue,
      white: colors.white,
      gray: colors.gray,
      emerald: colors.emerald,
      indigo: colors.indigo,
      yellow: colors.yellow,
      violet: colors.violet,
    },
  },
  plugins: [require("flowbite/plugin")],
  darkMode: "class",
};
