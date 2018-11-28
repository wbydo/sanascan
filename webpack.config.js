const webpack = require('webpack');
const CleanWebpackPlugin = require('clean-webpack-plugin');

const main = require('./webpack.main.js');
const renderer = require('./webpack.renderer.js')

module.exports = [
  Object.assign(
    main,
    {
      plugins: [
        new CleanWebpackPlugin(['dist'])
      ]
    }
  ),
  Object.assign(
    renderer,
    {
      target: 'electron-renderer'
    }
  )
];
