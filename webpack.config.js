const path = require('path');
const HtmlWebPackPlugin = require("html-webpack-plugin");

module.exports = {
  entry: './site/app.ts',
	resolve: {
		extensions: ['.tsx', '.ts', '.js']
	},
  output: {
		path: path.resolve(__dirname, "dist"),
    filename: 'bundle.js'
  },
	devServer: {
		contentBase: "./dist"
	},
	module: {
		rules: [
			{
				test: /\.tsx?$/,
				exclude: /node_modules/,
				use: 'ts-loader'
			},
			{
				test: /\.html$/,
				use: [
					{
						loader: "html-loader"
					}
				]
			},
			{
				test: /\.css$/,
				use: ['style-loader', 'css-loader']
			}
		]
	},
	plugins: [
		new HtmlWebPackPlugin({
			template: "./site/index.html",
			filename: "./index.html"
		})
	]
};

