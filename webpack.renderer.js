const webpack = require('webpack');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  mode: 'development',
  entry: path.join(__dirname, 'src', 'renderer','index'),

  output: {
    filename: 'index.js',
    path: path.resolve(__dirname, 'dist', 'renderer')
  },

  plugins: [
    new HtmlWebpackPlugin({
      template: "./src/renderer/index.html",
      filename: "index.html"
    })
  ],

  module: {
    rules: [{
      test: /\.tsx?$/,
      use: 'ts-loader'
    }, {
      test: /\.tsx?$/,
      enforce: 'pre',
      loader: 'tslint-loader',
      options: {
        configFile: './tslint.json',
        typeCheck: true,
      },
    }, {
      test: /\.css$/,
      use: [
        'style-loader',
        {
          loader: 'css-loader',
          options: {
            modules: true,
            localIdentName: '[name]-[local]-[hash:base64:5]'
          },
        },
        'postcss-loader'
      ]
    }, {
      test: /\.html$/,
      use: 'html-loader'
    }],
  },

  resolve: {
    extensions: [
      '.ts',
      '.tsx',
      '.js',
    ]
  },

  optimization: {
    splitChunks: {
      cacheGroups: {
        vendors: {
          priority: -10,
          test: /[\\/]node_modules[\\/]/
        }
      },

      chunks: 'async',
      minChunks: 1,
      minSize: 30000,
      name: false
    }
  },
};
