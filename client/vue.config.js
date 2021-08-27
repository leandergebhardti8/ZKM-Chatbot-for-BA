const webpack = require("webpack");

const PUBLIC_PATH_AMAZON =
"https://zkm-chatbot.s3.eu-central-1.amazonaws.com/chatbot/";
const PUBLIC_PATH = "https://chatbot8.zkm.de/chatbot"
const ASSETS_PATH = process.env.NODE_ENV === "production" ? PUBLIC_PATH : "/";

module.exports = {
  publicPath: ASSETS_PATH,
  filenameHashing: false,
  productionSourceMap: false,
  integrity: false,
  css: {
    extract: false
  },
  transpileDependencies: ["ansi-regex", "dom7", "ssr-window", "swiper", "he"],
  configureWebpack: {
    resolve: {
      extensions: [".js"],
      alias: {
        jquery: "jquery/dist/jquery.min.js"
      }
    },
    plugins: [
      new webpack.ProvidePlugin({
        $: "jquery",
        jQuery: "jquery",
        Popper: ["popper.js", "default"],
        Util: "exports-loader?Util!bootstrap/js/dist/util"
      })
    ],
    optimization: {
      splitChunks: false
    }
  },
  chainWebpack: config => {
    config.module
      .rule("images")
      .test(/\.(png|jpe?g|gif|webp)(\?.*)?$/)
      .use("url-loader")
      .loader("url-loader")
      .tap(options => {
        // modify the options...
        options.limit = 8192;
        return options;
      });

    config.module.rule("svg").uses.clear();
    config.module
      .rule("svg")
      .use("svg-url-loader")
      .loader("svg-url-loader")
      .options({
        encoding: "base64",
        limit: 4096,
        fallback: {
          loader: "file-loader",
          options: {
            name: "img/[name].[hash:8].[ext]"
          }
        }
      });

    config.module
      .rule("fonts")
      .test(/\.(woff|woff2?|eot|ttf|otf)(\?.*)?$/)
      .use("url-loader")
      .loader("url-loader")
      .options({
        options: {
          outputPath: "fonts/",
          name: "fonts/[name].[hash:7].[ext]"
        }
      });
  }
};
