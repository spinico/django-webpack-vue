const path = require("path");
const webpack = require("webpack"); // To access built-in plugins
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const ForkTsCheckerWebpackPlugin = require("fork-ts-checker-webpack-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const ThemesGeneratorPlugin = require("themes-switch/ThemesGeneratorPlugin");

module.exports = (env, argv) => {
  // Production mode automatically uses ModuleConcatenationPlugin
  const production = argv.mode === "production";
  const development = argv.mode === "development";

  console.log("Webpack [" + (production ? "production" : "development") + "]\n");

  return {
    entry: {
      app: path.resolve(__dirname, "src/app"),
    },
    output: {
      // To include a 12 digits hash value to the file or chuck name: [chunkhash:12]
      filename: "[name].js",
      chunkFilename: "[name].js",
      path: path.resolve(__dirname, "build"),
      // Should match Django's STATIC_URL value
      publicPath: "/static/",
      // Include comments in bundles with information about the contained modules
      pathinfo: false,
    },
    devtool: false,
    plugins: [
      new MiniCssExtractPlugin({
        // To include a 12 digits hash value to the file or chuck name: [chunkhash:12]
        filename: "styles/[name].css",
        chunkFilename: "styles/[name].css",
      }),
      // Run TypeScript type checker on a separate process.
      new ForkTsCheckerWebpackPlugin({
        checkSyntacticErrors: true,
        // Using typescript incremental compilation API is currently only allowed with a single worker.
        workers: 1,
        eslint: true,
      }),
      new ThemesGeneratorPlugin({
        srcDir: "src",
        themesDir: "src/assets/styles/themes",
        outputDir: "../styles/themes",
        defaultStyleName: "default.scss",
        // No random number added to file name of themes.
        useStaticThemeName: true,
        // Specify order of imported files and theme variables.
        // It should be set to true when using sass.
        importAfterVariables: true,
        clearTemp: production,
      }),
      // The ts-loader generates ".js" and ".d.ts" files, these should be ignored
      new webpack.WatchIgnorePlugin([/\.js$/, /\.d\.ts$/]),
      // Inject jQuery implicit globals
      new webpack.ProvidePlugin({
        $: "jquery",
        jQuery: "jquery",
        "window.jQuery": "jquery",
        "window.$": "jquery",
        Popper: ["popper.js", "default"],
        // Extract bootstrap plugins out of the module using the exports-loader module (fixes "Uncaught ReferenceError: '***' is not defined.")
        Alert: "exports-loader?Alert^bootstrap/js/dist/alert",
        Button: "exports-loader?Button^bootstrap/js/dist/button",
        Carousel: "exports-loader?Carousel^bootstrap/js/dist/carousel",
        Collapse: "exports-loader?Collapse^bootstrap/js/dist/collapse",
        Dropdown: "exports-loader?Dropdown^bootstrap/js/dist/dropdown",
        Modal: "exports-loader?Modal^bootstrap/js/dist/modal",
        Popover: "exports-loader?Popover^bootstrap/js/dist/popover",
        Scrollspy: "exports-loader?Scrollspy^bootstrap/js/dist/scrollspy",
        Tab: "exports-loader?Tab^bootstrap/js/dist/tab",
        Toast: "exports-loader?Toast^bootstrap/js/dist/toast",
        Tooltip: "exports-loader?Tooltip^bootstrap/js/dist/tooltip",
        Util: "exports-loader?Util^bootstrap/js/dist/util",
      }),
    ].concat(
      development
        ? [
            // Use custom source map generation (only in development)
            // A full SourceMap is emitted as a separate file.
            new webpack.SourceMapDevToolPlugin({
              filename: "[file].map",
              exclude: ["vendors.js"],
            }),

            // Yields the best quality SourceMaps for development (included in generated bundle)
            // This is equivalent to => devtool: "eval-source-map".
            //new webpack.EvalSourceMapDevToolPlugin({
            //  exclude: /node_modules/, // Do not generate inlined source map for vendors modules
            //}),
          ]
        : [
            // Remove all files inside webpack's "output.path" directory,
            // as well as all unused webpack assets on production build.
            new CleanWebpackPlugin({ root: __dirname, verbose: true }),
            new BundleAnalyzerPlugin({
              analyzerMode: "static",
              reportFilename: "../../report.html",
            }),
          ],
    ),
    optimization: {
      removeAvailableModules: production,
      removeEmptyChunks: production,
      splitChunks: {
        cacheGroups: {
          // Create a "vendors" chunk, which includes all code from node_modules in the whole application.
          // This might result in a large chunk containing all external packages. It is recommended to
          // only include your core frameworks and utilities and dynamically load the rest of the dependencies.
          vendors: {
            test: /[\\/]node_modules[\\/]/,
            chunks: "all",
            name: "vendors",

            // To generate a bundle per package (in the "vendors" subfolder).
            // This requires to update the base template to include each bundles.
            // Note: "cacheGroupKey" == "vendors" (key of the cacheGroup)
            //name(module, chunks, cacheGroupKey) {
            //  // Get the package name. E.g. node_modules/packageName/not/this/part.js or node_modules/packageName
            //  const packageName = module.context.match(/[\\/]node_modules[\\/](.*?)([\\/]|$)/)[1];
            //  // NPM package names are URL-safe, but some servers don't like @ symbols
            //  return `${cacheGroupKey}/${packageName.replace("@", "")}`;
            //},
          },
        },
      },
      // In production, minimize the bundle using the plugin(s) specified in "optimization.minimizer".
      minimize: production,
      minimizer: [
        new TerserPlugin({
          cache: true,
          parallel: true,
          sourceMap: true,
          extractComments: false,
          terserOptions: { output: { comments: false } },
        }),
        new OptimizeCSSAssetsPlugin({
          cssProcessorOptions: { preset: ["default", { discardComments: { removeAll: true } }] },
          canPrint: true,
        }),
      ],

      // Enable/Disable ModuleConcatenationPlugin: Concatenate the scope of all
      // modules into one closure to allow faster execution time in the browser.
      // This is enabled by default in production.
      concatenateModules: production,
    },
    performance: {
      // Production build total size warning when over 400 KB
      maxAssetSize: 1024 * 400,
      maxEntrypointSize: 1024 * 400,
      hints: development ? false : "warning",
    },
    module: {
      // IMPORTANT: when multiple loaders are chained, they are executed in reverse order.
      rules: [
        {
          test: /\.tsx?$/i,
          exclude: /node_modules/,
          use: [
            {
              loader: "ts-loader",
              options: {
                onlyCompileBundledFiles: true,
                transpileOnly: true,
                happyPackMode: true,
                experimentalWatchApi: development,
              },
            },
            {
              loader: "eslint-loader",
              options: {
                //configFile: ".eslintrc.json",
                emitWarning: development,
                failOnWarning: development,
              },
            },
          ],
        },
        {
          test: /\.(sa|sc|c)ss$/i,
          use: [
            // [MiniCssExtractPlugin] should be used only on production builds without style-loader in the loaders chain,
            // especially if you want to have HMR in development. Here is an example to have both HMR in development and
            // styles extracted in a file for production builds
            { loader: MiniCssExtractPlugin.loader, options: { hmr: development } },
            // The importLoaders option configure how many loaders before css-loader should be applied to imported resources.
            { loader: "css-loader", options: { importLoaders: 2 } },
            { loader: "postcss-loader", options: {} },
            { loader: "sass-loader", options: {} },
          ],
        },
        {
          test: /\.(jpe?g|png|gif|svg|webp)$/i,
          use: [
            {
              loader: "url-loader",
              options: {
                // Images larger than 10 KB won’t be inlined
                limit: 10 * 1024,
                // Must preserve original file name as webpack_loader does
                // not keep track of name containing hash value
                name: "[name].[ext]",
                // Relative path for referencing images resources in html template
                outputPath: "images/",
              },
            },
            {
              loader: "image-webpack-loader",
              options: {
                disable: development,
                mozjpeg: { progressive: true, quality: 50 },
                optipng: { enabled: production },
                pngquant: { quality: [0.65, 0.9], speed: 4 },
                gifsicle: { interlaced: false },
                webp: { quality: 75 },
              },
            },
          ],
        },
        {
          test: /\.(eot|ttf|woff|woff2)$/i,
          use: {
            loader: "file-loader",
            options: {
              // To include a 12 digits hash value to the file or chuck name: [md5:hash:hex:12]
              name: "[name].[ext]",
              outputPath: "fonts/",
            },
          },
        },
      ],
    },
    resolve: {
      modules: ["node_modules"],
      alias: {
        ScrollToPlugin: "gsap/src/uncompressed/plugins/ScrollToPlugin",
        // The ScrollMagic alias to prevent warning: "There are multiple modules with names that only differ in casing."
        ScrollMagic: "scrollmagic/scrollmagic/uncompressed/ScrollMagic",
        "ScrollMagic.animation.gsap": "scrollmagic/scrollmagic/uncompressed/plugins/animation.gsap",
        "ScrollMagic.debug.addIndicators": "scrollmagic/scrollmagic/uncompressed/plugins/debug.addIndicators",
      },
      // Attempt to resolve listed extensions in order.
      // This also enables to leave off the extension with "import".
      extensions: [".ts", ".tsx", ".js", ".sass", ".scss"],
    },
    watchOptions: {
      aggregateTimeout: 300,
      poll: 1000,
      ignored: ["node_modules"],
    },
  };
};
