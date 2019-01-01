const webpack = require('webpack');
const path = require('path');
const HardSourceWebpackPlugin = require('hard-source-webpack-plugin');

module.exports = {
  mode: 'development',
  target: 'electron-main',
  entry: path.join(__dirname, 'src','main'),

  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  },

  node: {
    __dirname: false,
    __filename: false
  },

  plugins: [
    // new HardSourceWebpackPlugin({
    //   cacheDirectory: path.resolve(__dirname, '.cache', 'main')
    // }),
  ],

  module: {
    rules: [{
      test: /\.ts?$/,
      use: 'ts-loader'
    }, {
      test: /\.ts?$/,
      enforce: 'pre',
      loader: 'tslint-loader',
      options: {
        configFile: './tslint.json',
        typeCheck: true,
      },
    }],
  },

  resolve: {
    extensions: [
      '.ts',
      '.js',
      '.json',
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
  }
};
