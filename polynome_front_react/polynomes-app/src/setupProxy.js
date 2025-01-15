const { createProxyMiddleware } = require('http-proxy-middleware');

const BASE_URL = 'http://127.0.0.1:8081';
const proxyPaths = ['/racines', '/factoriser', '/newton', '/quadratique', '/plot','/recommend'];

module.exports = function (app) {
  proxyPaths.forEach((path) => {
    app.use(
      path,
      createProxyMiddleware({
        target: BASE_URL,
        changeOrigin: true,
      })
    );
  });
};
