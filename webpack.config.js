const path = require('path');
const HtmlWebPackPlugin = require('html-webpack-plugin');
const HtmlWebpackInlineSVGPlugin = require('webpack-html-plugin-svg-inline');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = env => {
  process.env.values_path = env ? env.values_path : '';

  return {
    entry: './site/app.ts',
    resolve: {
      extensions: ['.tsx', '.ts', '.js']
    },
    resolveLoader: {
      modules: ['node_modules', path.resolve(__dirname, 'site/loaders')]
    },
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: 'bundle.js'
    },
    devServer: {
      contentBase: './dist'
    },
    module: {
      rules: [
        {
          test: /\.ts$/,
          exclude: /node_modules/,
          use: ['babel-loader', 'ts-loader']
        },
        {
          test: /\.html$/,
          use: [
            {
              loader: 'html-loader'
            }
          ]
        },
        {
          test: /\.scss$/,
          use: ExtractTextPlugin.extract({
            fallback: "style-loader",
            use: [
              'css-loader',
              'postcss-loader',
              'sass-loader'
            ],
          })
        },
        {
          test: /\.(gif|png|jpe?g|svg)$/,
          use: 'file-loader'
        }
      ]
    },
    plugins: [
      new HtmlWebPackPlugin({
        template: './site/index.html',
        filename: './index.html'
      }),
      new HtmlWebpackInlineSVGPlugin(),
      new ExtractTextPlugin('[name]-[hash].css')
    ]
  };
};
