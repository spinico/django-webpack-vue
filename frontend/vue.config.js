const path = require("path");

const production = process.env.NODE_ENV === "production";
const development = !production;
const staticPath = "./static/frontend/";

console.log("Vue [" + (production ? "production" : "development") + "]\n");

const pages = {
  main: {
    entry: "src/pages/Main/main",
    filename: "index.html", 
    chunks: ["vendors", "main"],
    // Template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
    title: "Frontend",
  }
};

module.exports = {
  pages: pages,

  // Produce source map only in development
  productionSourceMap: development,
  filenameHashing: production,

  // The publicPath section defines how Django will locate our bundles. In production,
  // we set the publicPath empty, as this signals to django-webpack-loader to fall back
  // to Django's standard static finder behavior. However, in non-production mode we
  // override this to point to our own webpack development server.
  publicPath: production ? "" : "http://127.0.0.1:8080/",

  // The outputDir defines where the production ready Javascript/CSS will be placed.
  // This most likely should be one of your Django application's static file locations.
  // Specifies where Webpack will build the Vue application (relative to the frontend folder)
  // WARNING: This folder's content will be deleted on a build.
  outputDir: "./build/",

  // Assets path prefix (should match Django static files path)
  assetsDir: staticPath,

  css: {
    // Extract CSS in your components into a standalone CSS files (instead of inlined in JavaScript and injected dynamically).
    // Extracting CSS is disabled by default in development mode since it is incompatible with CSS hot reloading.
    // When building as a library, you can also set this to "false" to avoid your users having to import the CSS themselves.
    //extract: false
    extract: {
      // To format names with a 12-digits hashing value, use: [name].[hash:12].css
      filename: staticPath + "styles/[name].css",
      chunkFilename: staticPath + "styles/[name].css",
    }
  },

  configureWebpack: config => {
    config.devtool = production ? false : "source-map";

    if (production) {
      config.performance = {
        hints: false, // default -> "warning"
        maxAssetSize: 800 * 1024,
        maxEntrypointSize: 800 * 1024
      };

      // To format names with a 12-digits hashing value, use: [name].[hash:12].js
      config.output.filename = staticPath + "[name].js";
      config.output.chunkFilename = staticPath + "[name].js";
    }
  },

  // Optimize our build using the splitChunks plugin, configuring it to extract any vendor
  // javascripts into a single shared bundle. This allows us to keep our individual component
  // javascript files small and allow browsers to cache our common javascript while moving among pages.
  chainWebpack: config => {
    config.optimization.splitChunks({
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: "vendors",
          priority: 1,
          chunks: "all"
        }
      }
    });

    if (production) {
      // To format names with a 12-digits hashing value, use: [name].[hash:12].[ext]

      // vue inspect --rule images
      config.module
        .rule("images")
        .use("url-loader")
        .loader("url-loader")
        .tap(options => {
          options.fallback.options.name = staticPath + "images/[name].[ext]";
          return options;
        });

      // vue inspect --rule svg
      config.module
        .rule("svg")
        .use("file-loader")
        .loader("file-loader")
        .tap(options => {
          options.name = staticPath + "images/[name].[ext]";
          return options;
        });

      // vue inspect --rule media
      config.module
        .rule("media")
        .use("url-loader")
        .loader("url-loader")
        .tap(options => {
          options.fallback.options.name = staticPath + "media/[name].[ext]";
          return options;
        });

      // vue inspect --rule fonts
      config.module
        .rule("fonts")
        .use("url-loader")
        .loader("url-loader")
        .tap(options => {
          options.fallback.options.name = staticPath + "fonts/[name].[ext]";
          return options;
        });

      // Update copy destination for the public folder files
      config.plugin("copy").tap(args => {
        args[0][0].to = path.join(args[0][0].to, staticPath);
        return args;
      });

      // By default, Vue constructs corresponding html files for our bundles, but we have no need for
      // them since we’ll be serving our bundles from Django templates. By deleting the appropriate
      // plugins from our config we can prevent these from being generated (only in production).
      Object.keys(pages).forEach(page => {
        config.plugins.delete(`html-${page}`);
        config.plugins.delete(`preload-${page}`);
        config.plugins.delete(`prefetch-${page}`);
      });
    }

    // Configure a development server for use in non-production modes, allowing to hot
    // reload our Vue components during front-end development.
    config.devServer
      .public("http://127.0.0.1:8080")
      .host("0.0.0.0")
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .headers({ "Access-Control-Allow-Origin": ["*"] })
      // Redirects API requests to the Django development server
      .proxy({
        "^/api": {
          target: "http://127.0.0.1:8000/",
          ws: false
        }
      });
  }
}
