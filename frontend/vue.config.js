module.exports = {
    devServer: {
        watchOptions: {
            ignored: ['node_modules'],
            poll: true
        },
        proxy: 'http://backend:8000',
    },
    publicPath: '/',
}
