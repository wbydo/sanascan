const webpack = require('webpack');
const CleanWebpackPlugin = require('clean-webpack-plugin');

const main = require('./webpack.main.js');
const renderer = require('./webpack.renderer.js')

main.plugins.push(
  new CleanWebpackPlugin(['dist']),
);

module.exports = [
  main,
  Object.assign(
    renderer,
    {
      target: 'electron-renderer'
    }
  )
];
