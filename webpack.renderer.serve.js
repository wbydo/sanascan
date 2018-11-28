const webpack = require('webpack');
const main = require('./webpack.main.js');
const renderer = require('./webpack.renderer.js')

module.exports = Object.assign(
  renderer,
  {
    devServer: {
      inline: true,
      contentBase: 'dist'
    },
    devtool: "cheap-module-source-map",
  }
);
