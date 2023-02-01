const path = require('path');

module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  // chainWebpack: config => {
  //   config.resolve.alias.set(
  //     'vue$',
  //     path.resolve(__dirname, 'node_module/vue/dist/vue.runtime.esm.js')
  //   )
  // }
  // build: {
  //   assetsPublicPath: '/',
  //   assetsSubDirectory: 'static'
  // },
  // resolve: {
  //   alias: {
  //     portfolio: path.resolve(__dirname, 'src/assets/portfolio'),
  //   }
  // }
}
