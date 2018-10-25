const webpack = require('webpack');
const path = require('path');

/*
 * SplitChunksPlugin is enabled by default and replaced
 * deprecated CommonsChunkPlugin. It automatically identifies modules which
 * should be splitted of chunk by heuristics using module duplication count and
 * module category (i. e. node_modules). And splits the chunks…
 *
 * It is safe to remove "splitChunks" from the generated configuration
 * and was added as an educational example.
 *
 * https://webpack.js.org/plugins/split-chunks-plugin/
 *
 */
 const main = {
 	mode: 'development',
   target: 'electron-main',
   entry: path.join(__dirname, 'src','index'),

   output: {
     filename: 'index.js',
     path: path.resolve(__dirname, 'dist')
   },

  node: {
    __dirname: false,
    __filename: false
  },

 	plugins: [],

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

const renderer = {
	mode: 'development',
  target: 'electron-renderer',
  entry: path.join(__dirname, 'src', 'renderer','index'),

  output: {
    filename: 'index.js',
    path: path.resolve(__dirname, 'dist', 'scripts')
  },

	plugins: [],

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
          loaders: ['style-loader', 'css-loader?modules', 'postcss-loader'],
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
	}
};

module.exports = [
  main, renderer
];
