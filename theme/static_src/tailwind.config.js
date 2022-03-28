/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
  content: [
    /**
     * HTML. Paths to Django template files that will contain Tailwind CSS classes.
     */

    /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
    "../templates/base.html",
    "../templates/**/*.html",
    "../templates/**/**/*.html",

    /*
     * Main templates directory of the project (BASE_DIR/templates).
     * Adjust the following line to match your project structure.
     */
    "../../templates/**/*.html",

    /*
     * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
     * Adjust the following line to match your project structure.
     */
    "../../**/templates/**/*.html",

    /**
     * Python: If you use Tailwind CSS classes in Python, uncomment the following line
     * and make sure the pattern below matches your project structure.
     */
    '../../**/*.py'
  ],
  theme: {
    extend: {
      colors: {
        primary: "#18345e" /* navyblue */,
        tertinary: "#22c1dc" /* lightblue */,
        secondary: "#f0ab20" /* yellow */,
        red: "#c01f48" /* for errors */,
        other: "#007bd6" /* blue */,
        lightGrey: "#e5e5e4" /* for background */,
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms")
  ]

};
