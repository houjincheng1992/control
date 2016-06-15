module.exports = {
    entry: './js/index.js',
    output: {
        path: './public/build',
        publicPath: './build',
        filename: 'index.js'
    },
    module: {
        loaders: [
            {
                test: /\.(js)$/,
                loader: 'jsx-loader?harmony'
            }
        ]
    }
}
