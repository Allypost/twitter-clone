module.exports = {
  outputDir: "./dist",

  // relative to outputDir
  assetsDir: "static",

  devServer: {
    writeToDisk: true, // https://webpack.js.org/configuration/dev-server/#devserverwritetodisk-
  },

  css: {
    requireModuleExtension: false,
    loaderOptions: {
      css: {
        modules: {
          localIdentName: `${
            "production" !== process.env.NODE_ENV
            ? "[path][name]__[local]--"
            : ""
          }[emoji]-[sha256:hash:base64:8]`,
        },
        localsConvention: "camelCaseOnly",
      },
    },
  },
};
