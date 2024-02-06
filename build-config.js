module.exports = {
  development: {
    distPath: "./app/static",

    // Minify assets.
    minify: false,

    // Generate sourcemaps.
    sourcemaps: false,

    // https://webpack.js.org/configuration/devtool/#development
    devtool: "eval-source-map",

    // Use this option with caution because it will remove entire output directory.
    // Will affect only and `build` command
    cleanDist: true,
    fastDev: false,
  },
  production: {
    // Build path can be both relative or absolute.
    // Current dist path is `./assets/vendor` which will be used by templates from `html\` directory. Set distPath: './assets/vendor' to generate assets in dist folder.
    distPath: "./app/static",

    // Minify assets.
    // Note: Webpack will minify js sources in production mode regardless to this option
    minify: true,

    // Generate sourcemaps.

    sourcemaps: false,
    // https://webpack.js.org/configuration/devtool/#production
    devtool: "#source-map",

    // Use this option with caution because it will remove entire output directory.
    // Will affect only `build:prod` command
    cleanDist: true,
    fastDev: false,
  },
};
