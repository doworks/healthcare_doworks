const path = require('path');
const { defineConfig } = require('@vue/cli-service');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = defineConfig({
  lintOnSave: false,
  publicPath: "/vuejs/template/",
  css: {
    extract: false,
  },
  chainWebpack: (config) => {
    config.resolve.alias
      .set('swiper$', 'swiper/js/swiper.js')
      .end();
    
    config.plugin('define').tap((args) => {
      const defineArgs = args[0];
      defineArgs['__VUE_PROD_HYDRATION_MISMATCH_DETAILS__'] = true;
      return args;
    });
  },

  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.ico$/,
          loader: 'file-loader',
          options: {
            name: '[name].[ext]'
          }
        },
       
      ]
    },
    plugins: [
      new CopyWebpackPlugin({
        patterns: [
          {
            from: path.resolve(__dirname, 'src/assets/css'),
            to: path.resolve(__dirname, 'dist/css'),
          },
          {
            from: path.resolve(__dirname, 'src/assets/admin/css'),
            to: path.resolve(__dirname, 'dist/admin/css'),
          },
          {
            from: path.resolve(__dirname, 'src/assets/pharmacy/css'),
            to: path.resolve(__dirname, 'dist/pharmacy/css'),
          },
        ],
      }),
    ],
  },
});
