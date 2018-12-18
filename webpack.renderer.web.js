const webpack = require('webpack');
const main = require('./webpack.main.js');
const renderer = require('./webpack.renderer.js')
const path = require('path');

const config = Object.assign(
  renderer,
  {
    target: 'web'
  }
);

config.output = {
  filename: 'index.js',
  path: path.resolve(__dirname, 'dist_web')
};

module.exports = config
