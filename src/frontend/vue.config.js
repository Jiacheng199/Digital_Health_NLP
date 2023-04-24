const { defineConfig } = require('@vue/cli-service')
// avoid port clash with ontoserver
// can ignore after packing the front-end files
// https://cli.vuejs.org/config/#devserver
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8081
  }
})
