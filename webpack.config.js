const path = require("path");

const CopyWebpackPlugin = require("copy-webpack-plugin");
const WriteFilePlugin = require("write-file-webpack-plugin");

const BUILD_DIR = path.resolve(__dirname, "build");

module.exports = {
  entry: path.resolve(__dirname, "site/app.ts"),
  resolve: {
    extensions: [".tsx", ".ts", ".js"]
  },
  output: {
    path: BUILD_DIR,
    filename: "bundle.js"
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        exclude: /node_modules/,
        use: ["babel-loader", "ts-loader"]
      },
      {
        test: /\.scss$/,
        use: ["css-loader", "postcss-loader", "sass-loader"]
      },
      {
        test: /\.(gif|png|jpe?g|svg)$/,
        use: "file-loader"
      }
    ]
  },
  plugins: [new CopyWebpackPlugin(["site/public"]), new WriteFilePlugin()]
};
