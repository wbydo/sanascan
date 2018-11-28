const webpack = require('webpack');
const main = require('./webpack.main.js');
const renderer = require('./webpack.renderer.js')

module.exports = Object.assign(
  renderer,
  {target: 'electron-renderer'}
);
