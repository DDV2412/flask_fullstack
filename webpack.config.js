const path = require("path");
const TerserPlugin = require("terser-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const conf = (() => {
  const _conf = require("./build-config");
  return require("deepmerge").all([
    {},
    _conf.base || {},
    _conf[process.env.NODE_ENV] || {},
  ]);
})();

conf.distPath = conf.distPath
  ? path.resolve(__dirname, conf.distPath)
  : path.resolve(__dirname, "dist");

const entryPoints = {
  app: "./app/assets/js/webflow.js",
};

const cssRule = {
  test: /\.css$/,
  use: [MiniCssExtractPlugin.loader, "css-loader"],
  include: path.resolve(__dirname, "app/static/styles"),
};

const jsRule = {
  test: /\.js$/,
  exclude: /node_modules/,
  use: ["babel-loader"],
  include: path.resolve(__dirname, "./app/static/js"),
};

const webpackConfig = {
  mode: process.env.NODE_ENV === "production" ? "production" : "development",
  performance: {
    hints: false,
    maxEntrypointSize: 512000,
    maxAssetSize: 512000,
  },
  entry: entryPoints,
  output: {
    path: path.resolve(__dirname, "app/static/dist"),
    filename: "[name].bundle.js",
    publicPath: "/static/dist/",
  },
  module: {
    rules: [jsRule, cssRule],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name].css",
    }),
    citationJs,
  ],
  resolve: {
    extensions: [".js", ".css"],
    modules: ["node_modules"],
  },
  externals: {
    jquery: "jQuery",
  },
};

if (conf.sourcemaps) {
  webpackConfig.devtool = conf.devtool;
}

if (process.env.NODE_ENV === "production" && conf.minify) {
  webpackConfig.optimization = {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          sourceMap: conf.sourcemaps,
        },
        parallel: true,
      }),
    ],
  };
}

module.exports = webpackConfig;
