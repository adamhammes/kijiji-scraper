const path = require("path");

const ExtractTextPlugin = require("extract-text-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const WriteFilePlugin = require("write-file-webpack-plugin");

const BUILD_DIR = path.resolve(__dirname, "build");

module.exports = {
  entry: path.resolve(__dirname, "site/app.ts"),
  devtool: "source-map",
  resolve: {
    extensions: [".tsx", ".ts", ".js", ".scss"]
  },
  output: {
    path: BUILD_DIR,
    filename: "bundle.js",
    publicPath: "/"
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
        use: ExtractTextPlugin.extract({
          use: ["css-loader", "postcss-loader", "sass-loader"]
        })
      },
      {
        test: /\.(gif|png|jpe?g|svg)$/,
        use: "file-loader"
      }
    ]
  },
  plugins: [
    new CopyWebpackPlugin([
      {
        from: "site/public",
        to: BUILD_DIR,
        toType: "dir"
      }
    ]),
    new WriteFilePlugin(),
    new ExtractTextPlugin("styles.css")
  ]
};
